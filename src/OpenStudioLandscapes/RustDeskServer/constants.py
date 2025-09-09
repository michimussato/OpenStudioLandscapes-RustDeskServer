__all__ = [
    "DOCKER_USE_CACHE",
    "ASSET_HEADER",
    "FEATURE_CONFIGS",
]

import pathlib
from typing import Any, Generator

from dagster import (
    AssetExecutionContext,
    AssetMaterialization,
    AssetOut,
    MetadataValue,
    Output,
    get_dagster_logger,
    multi_asset,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL
from OpenStudioLandscapes.engine.enums import OpenStudioLandscapesConfig

DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False


GROUP = "RustDeskServer"
KEY = [GROUP]
FEATURE = f"OpenStudioLandscapes-{GROUP}".replace("_", "-")

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
}

# @formatter:off
FEATURE_CONFIGS = {
    OpenStudioLandscapesConfig.DEFAULT: {
        "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
        "HBBS_ALWAYS_USE_RELAY": ["Y", "N"][0],
        # hbbs
        "HBBS_WEB_CONSOLE_PORT_HOST": "21114",  # Only in Pro version
        "HBBS_WEB_CONSOLE_PORT_CONTAINER": "21114/tcp",  # Only in Pro version
        "HBBS_NAT_TYPE_TEST_PORT_HOST": "21115",
        "HBBS_NAT_TYPE_TEST_PORT_CONTAINER": "21115/tcp",
        "HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_HOST": "21116",
        "HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_CONTAINER": "21116/tcp",
        "HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_HOST": "21116",
        "HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_CONTAINER": "21116/udp",
        "HBBS_WEB_CLIENTS_SUPPORT_PORT_HOST": "21118",  # Can be disabled if web clients are not needed
        "HBBS_WEB_CLIENTS_SUPPORT_PORT_CONTAINER": "21118/tcp",  # Can be disabled if web clients are not needed
        # hbbr
        "HBBR_RELAY_SERVICES_PORT_HOST": "21117",
        "HBBR_RELAY_SERVICES_PORT_CONTAINER": "21117/tcp",
        "HBBR_WEB_CLIENTS_SUPPORT_PORT_CONTAINER": "21119",  # Can be disabled if web clients are not needed
        "HBBR_WEB_CLIENTS_SUPPORT_PORT_HOST": "21119/tcp",  # Can be disabled if web clients are not needed
        "DATA_STORE": pathlib.Path(
            "{DOT_LANDSCAPES}",
            "{LANDSCAPE}",
            f"{GROUP}__{'__'.join(KEY)}",
            "data",
        )
        .expanduser()
        .as_posix(),
    }
}
# @formatter:on


# Todo:
#  - [ ] move to common_assets
@multi_asset(
    name=f"constants_{ASSET_HEADER['group_name']}",
    outs={
        "NAME": AssetOut(
            **ASSET_HEADER,
            dagster_type=str,
            description="",
        ),
        "FEATURE_CONFIGS": AssetOut(
            **ASSET_HEADER,
            dagster_type=dict,
            description="",
        ),
        "DOCKER_COMPOSE": AssetOut(
            **ASSET_HEADER,
            dagster_type=pathlib.Path,
            description="",
        ),
    },
)
def constants_multi_asset(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[OpenStudioLandscapesConfig, dict[str | Any, bool | str | Any]]]
    | AssetMaterialization
    | Output[Any]
    | Output[pathlib.Path]
    | Any,
    None,
    None,
]:
    """ """

    yield Output(
        output_name="FEATURE_CONFIGS",
        value=FEATURE_CONFIGS,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("FEATURE_CONFIGS"),
        metadata={
            "__".join(
                context.asset_key_for_output("FEATURE_CONFIGS").path
            ): MetadataValue.json(FEATURE_CONFIGS),
        },
    )

    yield Output(
        output_name="NAME",
        value=__name__,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("NAME"),
        metadata={
            "__".join(context.asset_key_for_output("NAME").path): MetadataValue.path(
                __name__
            ),
        },
    )

    docker_compose = pathlib.Path(
        "{DOT_LANDSCAPES}",
        "{LANDSCAPE}",
        f"{ASSET_HEADER['group_name']}__{'_'.join(ASSET_HEADER['key_prefix'])}",
        "__".join(context.asset_key_for_output("DOCKER_COMPOSE").path),
        "docker_compose",
        "docker-compose.yml",
    )

    yield Output(
        output_name="DOCKER_COMPOSE",
        value=docker_compose,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output("DOCKER_COMPOSE"),
        metadata={
            "__".join(
                context.asset_key_for_output("DOCKER_COMPOSE").path
            ): MetadataValue.path(docker_compose),
        },
    )
