from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.RustDeskServer.assets

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.RustDeskServer.assets],
)


defs = Definitions(
    assets=[
        *assets,
    ],
)
