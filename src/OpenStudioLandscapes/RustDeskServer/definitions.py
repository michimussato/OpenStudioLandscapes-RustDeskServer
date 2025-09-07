from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.RustDeskServer.assets
import OpenStudioLandscapes.RustDeskServer.constants

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.RustDeskServer.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.RustDeskServer.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)
