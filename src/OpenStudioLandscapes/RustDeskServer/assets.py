import copy
import enum
import pathlib
from typing import Dict, Generator, List, Union

import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    AssetsDefinition,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
from OpenStudioLandscapes.engine.common_assets.compose_scope import (
    get_compose_scope_group__cmd,
)
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
from OpenStudioLandscapes.engine.common_assets.feature import get_feature__CONFIG
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out_v2
from OpenStudioLandscapes.engine.common_assets.group_in import (
    get_feature_in,
    get_feature_in_parent,
)
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.config.models import ConfigEngine
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker.compose_dicts import *

# from OpenStudioLandscapes.RustDeskServer import dist
from OpenStudioLandscapes.RustDeskServer.config.models import CONFIG_STR, Config
from OpenStudioLandscapes.RustDeskServer.constants import *

# https://github.com/yaml/pyyaml/issues/722#issuecomment-1969292770
yaml.SafeDumper.add_multi_representer(
    data_type=enum.Enum,
    representer=yaml.representer.SafeRepresenter.represent_str,
)


compose_scope_group__cmd: AssetsDefinition = get_compose_scope_group__cmd(
    ASSET_HEADER=ASSET_HEADER,
)

CONFIG: AssetsDefinition = get_feature__CONFIG(
    ASSET_HEADER=ASSET_HEADER,
    CONFIG_STR=CONFIG_STR,
    search_model_of_type=Config,
)

feature_in: AssetsDefinition = get_feature_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_BASE=ASSET_HEADER_BASE,
    ASSET_HEADER_FEATURE_IN={},
)

group_out: AssetsDefinition = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph: AssetsDefinition = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose: AssetsDefinition = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out_v2: AssetsDefinition = get_feature_out_v2(
    ASSET_HEADER=ASSET_HEADER,
)


# Produces
# - feature_in_parent
# - CONFIG_PARENT
# if ConfigParent is or type FeatureBaseModel
feature_in_parent: Union[AssetsDefinition, None] = get_feature_in_parent(
    ASSET_HEADER=ASSET_HEADER,
    config_parent=ConfigParent,
)


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def compose_networks(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[
    Output[Dict[str, Dict[str, Dict[str, str]]]] | AssetMaterialization, None, None
]:

    env: Dict = CONFIG.env

    compose_network_mode = DockerComposePolicies.NETWORK_MODE.BRIDGE

    docker_dict = get_network_dicts(
        context=context,
        compose_network_mode=compose_network_mode,
        env=env,
    )

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
    },
)
def compose_rustdeskserver(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
    compose_networks: Dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """ """

    env: Dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    network_dict = {}
    ports_dict_hbbs = {}
    ports_dict_hbbr = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict_hbbs = {
            "ports": [
                f"{CONFIG.rustdeskserver_HBBS_WEB_CONSOLE_PORT_HOST}:{CONFIG.rustdeskserver_HBBS_WEB_CONSOLE_PORT_CONTAINER}",
                f"{CONFIG.rustdeskserver_HBBS_NAT_TYPE_TEST_PORT_HOST}:{CONFIG.rustdeskserver_HBBS_NAT_TYPE_TEST_PORT_CONTAINER}",
                f"{CONFIG.rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_HOST}:{CONFIG.rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_CONTAINER}",
                f"{CONFIG.rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_HOST}:{CONFIG.rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_CONTAINER}",
                f"{CONFIG.rustdeskserver_HBBS_WEB_CLIENTS_SUPPORT_PORT_HOST}:{CONFIG.rustdeskserver_HBBS_WEB_CLIENTS_SUPPORT_PORT_CONTAINER}",
            ]
        }
        ports_dict_hbbr = {
            "ports": [
                f"{CONFIG.rustdeskserver_HBBR_RELAY_SERVICES_PORT_HOST}:{CONFIG.rustdeskserver_HBBR_RELAY_SERVICES_PORT_CONTAINER}",
                f"{CONFIG.rustdeskserver_HBBR_WEB_CLIENTS_SUPPORT_PORT_CONTAINER}:{CONFIG.rustdeskserver_HBBR_WEB_CLIENTS_SUPPORT_PORT_HOST}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks["network_mode"]}

    data_store = CONFIG.rustdeskserver_data_store_expanded
    data_store.mkdir(parents=True, exist_ok=True)

    volumes_dict = {
        "volumes": [
            f"{data_store.as_posix()}:/root:rw",
        ],
    }

    # For portability, convert absolute volume paths to relative paths

    _volume_relative = []

    for v in volumes_dict["volumes"]:

        host, container = v.split(":", maxsplit=1)

        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=CONFIG.docker_compose_expanded,
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    volumes_dict = {
        "volumes": [
            *_volume_relative,
        ],
    }

    service_name_hbbs = "hbbs"
    container_name_hbbs, host_name_hbbs = get_docker_compose_names(
        context=context,
        service_name=service_name_hbbs,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=config_engine.openstudiolandscapes__domain_lan,
    )
    # container_name_hbbs = "--".join(
    #     [service_name_hbbs, env.get("LANDSCAPE", "default")]
    # )
    # host_name_hbbs = ".".join(
    #     [
    #         service_name_hbbs,
    #         env["OPENSTUDIOLANDSCAPES__DOMAIN_LAN"],
    #     ]
    # )

    service_name_hbbr = "hbbr"
    container_name_hbbr, host_name_hbbr = get_docker_compose_names(
        context=context,
        service_name=service_name_hbbr,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=config_engine.openstudiolandscapes__domain_lan,
    )
    # container_name_hbbr = "--".join(
    #     [service_name_hbbr, env.get("LANDSCAPE", "default")]
    # )
    # host_name_hbbr = ".".join(
    #     [
    #         service_name_hbbr,
    #         env["OPENSTUDIOLANDSCAPES__DOMAIN_LAN"],
    #     ]
    # )

    command_hbbs = ["hbbs", "-r", host_name_hbbr]
    command_hbbr = ["hbbr"]

    # https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker/
    docker_dict = {
        "services": {
            # hbbs
            service_name_hbbs: {
                "container_name": container_name_hbbs,
                "hostname": host_name_hbbs,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                # "mac_address": ":".join(re.findall(r"..", env["HOST_ID"])),
                "restart": DockerComposePolicies.RESTART_POLICY.UNLESS_STOPPED.value,
                "image": CONFIG.rustdeskserver_docker_image,
                **copy.deepcopy(volumes_dict),
                **copy.deepcopy(network_dict),
                **copy.deepcopy(ports_dict_hbbs),
                "environment": {
                    "ALWAYS_USE_RELAY": CONFIG.rustdeskserver_HBBS_ALWAYS_USE_RELAY,
                },
                # "healthcheck": {
                # },
                "command": command_hbbs,
                "depends_on": [
                    "hbbr",
                ],
            },
            # hbbr
            service_name_hbbr: {
                "container_name": container_name_hbbr,
                "hostname": host_name_hbbr,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                # "mac_address": ":".join(re.findall(r"..", env["HOST_ID"])),
                "restart": DockerComposePolicies.RESTART_POLICY.UNLESS_STOPPED.value,
                "image": CONFIG.rustdeskserver_docker_image,
                **copy.deepcopy(volumes_dict),
                **copy.deepcopy(network_dict),
                **copy.deepcopy(ports_dict_hbbr),
                # "environment": {
                # },
                # "healthcheck": {
                # },
                "command": command_hbbr,
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_rustdeskserver": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_rustdeskserver"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[List[Dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )
