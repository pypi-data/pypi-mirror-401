import importlib.metadata
import os
import signal
import sys
from argparse import ArgumentParser

from silx import config

try:
    from ewoksorange.canvas.main import main as ewoksorange_main
    from ewoksorange.gui.canvas.main import arg_parser
except ImportError as e:
    error_msg = f"ERROR: {e.msg}.\n"
    error_msg += "To use `darfix` command, please use the full installation of darfix:\npip install darfix[full]\n"
    sys.stdout.write(error_msg)
    exit()

__CTRL_C_PRESSED_ONCE = False


def __handle_ctrl_c(*args):
    global __CTRL_C_PRESSED_ONCE
    if not __CTRL_C_PRESSED_ONCE:
        __CTRL_C_PRESSED_ONCE = True
        sys.stdout.write("\nPress CTRL+C again to force kill app.\n")
    else:
        # harakiri
        sys.stdout.write("\nApp killed by user.\n")
        os.kill(os.getpid(), signal.SIGKILL)


def main(argv=None):

    config._MPL_TIGHT_LAYOUT = True

    parser = ArgumentParser(parents=[arg_parser()], add_help=False)

    parser.add_argument(
        "--version",
        action="store_true",
        help="Display version",
    )

    parser.add_argument(
        "--use-opengl-plot",
        action="store_true",
        help="Use opengl as default backend for all plots. Faster but some limitations : https://www.silx.org/doc/silx/2.2.1/troubleshooting.html",
    )

    if argv is None:
        argv = sys.argv
    options, _ = parser.parse_known_args(argv[1:])

    if options.use_opengl_plot:
        config.DEFAULT_PLOT_BACKEND = "gl"
        argv.pop(argv.index("--use-opengl-plot"))

    if options.version:
        print(f"Darfix version: {importlib.metadata.version('darfix')}")
        return

    signal.signal(signal.SIGINT, __handle_ctrl_c)

    ewoksorange_main()


if __name__ == "__main__":
    sys.exit(main())
