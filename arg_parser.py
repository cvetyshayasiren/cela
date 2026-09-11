import argparse

def arg_parser(stdscr):
    parser = argparse.ArgumentParser(
        description="Cellular automaton in the terminal"
    )
    parser.add_argument(
        "-W", "--width", type=int, dest="width",
        help="field width (cells horizontally), default: fit to screen"
    )
    parser.add_argument(
        "-H", "--height", type=int, dest="height",
        help="field height (cells vertically), default: fit to screen (status bar excluded)"
    )

    args = parser.parse_args()
    complete_args = complete_namespace(stdscr=stdscr, args=args)
    return complete_args



def complete_namespace(stdscr, args: argparse.Namespace):
    h, w = stdscr.getmaxyx()
    if args.width is None:
        args.width = w
    if args.height is None:
        args.height = h

    return args
