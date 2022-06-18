import traceback
import os
import datetime
import source.constants as constants

DUMP_DIR = "errors"

if not os.path.isdir(DUMP_DIR):
    os.makedirs(DUMP_DIR)


def dump_error() -> str:
    path = os.path.join(DUMP_DIR, datetime.datetime.now().replace(microsecond=0).isoformat().replace(":", "-") + ".txt")
    with open(path, 'w') as f:
        f.write("Reverse Proxy v{} Dump File:\n\n".format(constants.VERSION))
        f.write(traceback.format_exc())

    print("Created dump file at {}".format(path))
    traceback.print_exc()

    return path
