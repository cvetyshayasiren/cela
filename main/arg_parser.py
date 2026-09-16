import argparse
import curses

from main.ca_params import Caparams, StuckBehaviour
from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from randomisation.randoms import random_symbols
from randomisation.random_seed import RandomSeed

def arg_parser(stdscr: curses.window):
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
        "-d", "--delay", type=float, dest="delay", default=0.1,
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
    parser.add_argument(
        "-S", "--seed", type=int, default=None, dest = "seed",
        help="random seed for reproducibility, default: random"
    )

    parser.add_argument(
        "-b", "--behaviour",
        type=lambda v: StuckBehaviour[v.upper()],
        choices=list(StuckBehaviour),
        default=StuckBehaviour.CONTINUE,
        dest = "behaviour",
        metavar="{pause,continue,stop}",
        help="action when two consecutive frames are identical "
            "(deeper cycles are not detected): "
            "pause, continue (restart with random field), or stop. "
            "Default: continue"
    )

    args = parser.parse_args()
    complete_args = complete_namespace(stdscr=stdscr, args=args)
    return complete_args


def complete_namespace(stdscr, args: argparse.Namespace) -> argparse.Namespace:
    RandomSeed.init(seed = args.seed)
    h, w = stdscr.getmaxyx()
    if args.width is None:
        args.width = w
    if args.height is None:
        args.height = h if args.fullscreen else h - 1
    if args.rule is None:
        args.rule = Rule.game_of_fly
    else:
        try:
            args.rule = Rule.from_string(args.rule).to_string()
        except ValueError as e:
            raise argparse.ArgumentTypeError(f"invalid rule {args.rule!r}: {e}")
    if args.symbols is None:
        args.symbols = random_symbols()
    if args.seed is None:
        args.seed = RandomSeed.seed

    return args

def args_to_params(stdscr, args: argparse.Namespace) -> Caparams:
    figure = Figure(width = args.width, height = args.height)
    figure.fill_full_random()
    return Caparams(
        stdscr = stdscr,
        figure = figure,
        rule = Rule.from_string(args.rule),
        delay = args.delay,
        stuck_behaviour=args.behaviour,
        symbols = args.symbols,
        seed = args.seed
    )
