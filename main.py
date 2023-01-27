import os

from thumbor.context import Context
from thumbor.server import get_config, configure_log, get_importer

# use_environment to enable gathering of settings through env
config = get_config(config_path=".", use_environment=False)
configure_log(config, "DEBUG")
importer = get_importer(config)
context = Context(server=None, config=config, importer=importer)

# read config
uk_config = [
    {
        "rotate": (50,),
        "flip_horizontally": ()
    },
    {
        "rotate": (50,)
    },
    {
        "flip_vertically": (),
    },
    {
        "flip_horizontally": (),
    }
]


def get_filename(filename: str, filters_: dict, args: tuple):
    filename += f"_{','.join(filters_.keys())}"

    if args:
        filename += f"_{','.join([str(arg) for arg in args])}"

    filename += ".jpg"

    return filename


def process_transformations():
    # calling engine, although we'd need to call filters directly ideally (as custom logic is implemented there)
    for filename in os.listdir("./test_images"):
        for filters in uk_config:
            with open(f"./test_images/{filename}", "rb") as image:
                context.modules.engine.load(image.read(), None)

                # apply transformations
                for filter_, args in filters.items():
                    getattr(context.modules.engine, filter_)(*args)

                with open(f"./produced_images/{get_filename(filename, filters, args)}", "wb") as new_image:
                    new_image.write(context.modules.engine.read())


process_transformations()
