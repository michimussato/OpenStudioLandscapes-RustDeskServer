import pathlib
from typing import List

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
    computed_field,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.RustDeskServer import constants, dist

# class UseRelay(enum.StrEnum):
#     YES = "Y"
#     NO = "N"


class Config(FeatureBaseModel):
    feature_name: str = dist.name

    group_name: str = constants.ASSET_HEADER["group_name"]

    key_prefixes: List[str] = constants.ASSET_HEADER["key_prefix"]

    rustdeskserver_docker_image: str = Field(
        default="docker.io/rustdesk/rustdesk-server:latest",
    )

    rustdeskserver_HBBS_ALWAYS_USE_RELAY: str = Field(
        default="Y",
        examples=["Y", "N"],
    )

    rustdeskserver_HBBS_WEB_CONSOLE_PORT_HOST: PositiveInt = Field(
        default=21114,
        description="Only in Pro version.",
    )

    rustdeskserver_HBBS_WEB_CONSOLE_PORT_CONTAINER: PositiveInt = Field(
        default=21114,
        description="Only in Pro version.",
    )

    rustdeskserver_HBBS_NAT_TYPE_TEST_PORT_HOST: PositiveInt = Field(
        default=21115,
    )

    rustdeskserver_HBBS_NAT_TYPE_TEST_PORT_CONTAINER: PositiveInt = Field(
        default=21115,
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_HOST: PositiveInt = Field(
        default=21116,
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_CONTAINER: PositiveInt = (
        Field(
            default=21116,
        )
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_HOST: PositiveInt = Field(
        default=21116,
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_CONTAINER: PositiveInt = (
        Field(
            default=21116,
        )
    )

    rustdeskserver_HBBS_WEB_CLIENTS_SUPPORT_PORT_HOST: PositiveInt = Field(
        default=21118,
        description="Can be disabled if web clients are not needed.",
    )

    rustdeskserver_HBBS_WEB_CLIENTS_SUPPORT_PORT_CONTAINER: PositiveInt = Field(
        default=21118,
        description="Can be disabled if web clients are not needed.",
    )

    rustdeskserver_HBBR_RELAY_SERVICES_PORT_HOST: PositiveInt = Field(
        default=21117,
    )

    rustdeskserver_HBBR_RELAY_SERVICES_PORT_CONTAINER: PositiveInt = Field(
        default=21117,
    )

    rustdeskserver_HBBR_WEB_CLIENTS_SUPPORT_PORT_CONTAINER: PositiveInt = Field(
        default=21119,
        description="Can be disabled if web clients are not needed.",
    )

    rustdeskserver_HBBR_WEB_CLIENTS_SUPPORT_PORT_HOST: PositiveInt = Field(
        default=21119,
        description="Can be disabled if web clients are not needed.",
    )

    rustdeskserver_data_store: pathlib.Path = Field(
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data"),
    )

    # EXPANDABLE PATHS
    @computed_field
    @property
    def rustdeskserver_data_store_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")
        LOGGER.debug(f"Expanding {self.rustdeskserver_data_store}...")
        ret = pathlib.Path(
            self.rustdeskserver_data_store.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


CONFIG_STR = Config.get_docs()
