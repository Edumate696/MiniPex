import argparse
import pathlib
import sys

import minipex
from minipex.debug import Logger

Logger.setLevel(Logger.NOTSET)


def parse_args() -> argparse.Namespace:
    def CustomFileType(string):
        # the special argument "-" means sys.std{in,out}
        if string == '-':
            return None
        f = argparse.FileType()(string)
        if pathlib.Path(f.name).suffix != '.mpx':
            raise argparse.ArgumentTypeError('Can only support .mpx files')
        return f

    parser = argparse.ArgumentParser(usage='%(prog)s [options] ... [file | -] [args] ...')
    parser.add_argument('-v', '--version', action='version', version=get_version_text())
    parser.add_argument('file', nargs='?', type=CustomFileType, default='-',
                        help='program read from script file (default: interactive shell)')
    parser.add_argument('args', default=[], nargs='*', help='arguments passed to program')
    return parser.parse_args()


def get_version_text() -> str:
    return f'Mini-Pex v{minipex.__version__}'


def run() -> None:
    options = parse_args()
    if options.file:
        Logger.debug(f'Executing {options.file} with args {",".join(options.args)}')
    else:
        Logger.debug(f'Starting Shell Mode')
        shell()


def shell():
    print(get_version_text())
    print('Type \'exit()\' and press enter to end session.')
    while True:
        src = input('>>> ')
        if src:
            try:
                out = eval(src)
                if out is not None:
                    print(repr(out))
            except Exception as e:
                print(e, file=sys.stderr)
