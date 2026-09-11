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
    parser.add_argument(
        "-d", "--delay", type=float, dest="height", default=0.1,
        help="delay between frames in seconds, default 0.1"
    )
    parser.add_argument(
        "-f", "--fullscreen", dest="fullscreen", action="store_true",
        help="field fills the screen; ignored for dimensions set via -W/-H"
    )
    parser.add_argument(
        "-r", "--rule", type=str, dest = "rule",
        help="rule in B/S/ notation (e.g. B2/S0345/10), default: random"
    )
    parser.add_argument(
        "-s", "--symbols", type=str, dest = "symbols",
        help="symbols used to render cells (e.g. ' .oO'), default: random"
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
