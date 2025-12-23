import pathlib

from dagster import get_dagster_logger
from pydantic import (
    Field, PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.str_gen import get_config_str
from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.RustDeskServer import dist

config_default = pathlib.Path(__file__).parent.joinpath("config_default.yml")


# class UseRelay(enum.StrEnum):
#     YES = "Y"
#     NO = "N"


class Config(FeatureBaseModel):
    feature_name: str = dist.name

    rustdeskserver_docker_image: str = Field(
        default="docker.io/rustdesk/rustdesk-server:latest",
    )

    rustdeskserver_HBBS_ALWAYS_USE_RELAY: str = Field(
        default="Y",
        description="Number of workers to simulate in parallel.",
        # examples=[i.name for i in UseRelay],
    )

    rustdeskserver_HBBS_WEB_CONSOLE_PORT_HOST: PositiveInt = Field(
        default=21114,
    )

    rustdeskserver_HBBS_WEB_CONSOLE_PORT_CONTAINER: str = Field(
        default="21114/tcp",
    )

    rustdeskserver_HBBS_NAT_TYPE_TEST_PORT_HOST: PositiveInt = Field(
        default=21115,
    )

    rustdeskserver_HBBS_NAT_TYPE_TEST_PORT_CONTAINER: str = Field(
        default="21115/tcp",
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_HOST: PositiveInt = Field(
        default=21116,
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_TCP_PORT_CONTAINER: str = Field(
        default="21116/tcp",
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_HOST: PositiveInt = Field(
        default=21116,
    )

    rustdeskserver_HBBS_ID_REGISTRATION_HEARTBEAT_UDP_PORT_CONTAINER: str = Field(
        default="21116/udp",
    )

    rustdeskserver_HBBS_WEB_CLIENTS_SUPPORT_PORT_HOST: PositiveInt = Field(
        default=21118,
    )

    rustdeskserver_HBBS_WEB_CLIENTS_SUPPORT_PORT_CONTAINER: str = Field(
        default="21118/tcp",
    )

    rustdeskserver_HBBR_RELAY_SERVICES_PORT_HOST: PositiveInt = Field(
        default=21117,
    )

    rustdeskserver_HBBR_RELAY_SERVICES_PORT_CONTAINER: int = Field(
        default="21117/tcp",
    )

    rustdeskserver_HBBR_WEB_CLIENTS_SUPPORT_PORT_CONTAINER: PositiveInt = Field(
        default=21119,
    )

    rustdeskserver_HBBR_WEB_CLIENTS_SUPPORT_PORT_HOST: str = Field(
        default="21119/tcp",
    )

    rustdeskserver_data_store: pathlib.Path = Field(
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/data"),
    )

    # EXPANDABLE PATHS
    @property
    def rustdeskserver_data_store_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")
        LOGGER.debug(f"Expanding {self.rustdeskserver_data_store}...")
        ret = pathlib.Path(
            self.rustdeskserver_data_store.expanduser()
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


CONFIG_STR = get_config_str(
    Config=Config,
)

