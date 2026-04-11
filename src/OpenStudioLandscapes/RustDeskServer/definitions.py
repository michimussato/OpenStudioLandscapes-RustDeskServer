from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.RustDeskServer.assets

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.RustDeskServer.assets],
)


defs = Definitions(
    assets=[
        *assets_base,
    ],
)
