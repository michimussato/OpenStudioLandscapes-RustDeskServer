from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Template.assets
import OpenStudioLandscapes.Template.constants

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Template.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Template.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)
