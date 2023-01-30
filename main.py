import asyncio
import os

from thumbor.context import Context
from thumbor.filters import FiltersFactory
from thumbor.server import get_config, configure_log, get_importer

uk_config = [
    {
        "brightness": 90
    },
    {
        "rotate": 90,
    },
    {
        "blur": 10,
    },
]

# use_environment=True to enable gathering of settings through env
config = get_config(config_path=".", use_environment=False)

configure_log(config, "DEBUG")

importer = get_importer(config)

context = Context(server=None, config=config, importer=importer)

available_filters = FiltersFactory(context.modules.filters).filter_classes_map


def get_filename(filename: str, filters_: dict, value: int):
    new_filename = ','.join(filters_.keys())

    if value:
        new_filename += f"_{value}"

    new_filename += filename

    return new_filename


async def process_transformations():
    for filename in os.listdir("./test_images"):
        for filters in uk_config:
            with open(f"./test_images/{filename}", "rb") as image:
                context.modules.engine.load(image.read(), None)

                # apply transformations
                for filter_, value in filters.items():
                    parameters = f"{filter_}({value})" if value else f"{filter_}()"

                    Filter = available_filters.get(filter_)(params=parameters, context=context)

                    await getattr(Filter, filter_)(value) if value else getattr(Filter, filter_)()

                with open(f"./produced_images/{get_filename(filename, filters, value)}", "wb") as new_image:
                    new_image.write(context.modules.engine.read())


asyncio.run(process_transformations())
