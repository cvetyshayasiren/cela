from parsing.rule_parse import RuleParse
from parsing.figure_parse import FigureParse
import argparse
import curses

from main.ca_params import Caparams, StuckBehaviour
from cellular_automaton.figure import Figure
from cellular_automaton.rule import Rule
from randomisation.randoms import random_symbols, random_rule, random_prepared_rule
from randomisation.random_seed import RandomSeed

def arg_parser() -> argparse.Namespace:
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
        "-s", "--symbols", type=str, dest = "symbols",
        help="symbols used to render cells (e.g. ' .oO'), default: random"
    )
    parser.add_argument(
        "-S", "--seed", type=int, default=None, dest = "seed",
        help="random seed for reproducibility, default: random"
    )
    parser.add_argument(
        "-b", "--blank", action="store_true", dest = "blank",
        help="clear the field before starting"
    )
    parser.add_argument(
        "-p", "--pause", action="store_true", dest = "pause",
        help="start paused"
    )

    # rule parse
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-r", "--rule", type=str, dest = "rule",
        help="rule in B/S/ notation (e.g. B2/S0345/10), default: random"
    )
    group.add_argument(
        "--gol", action="store_true",
        help="start with Game of Life rule (B3/S23)"
    )
    group.add_argument(
        "--gof", action="store_true",
        help="start with Game of Fly rule (B2/S0345/10)"
    )



    parser.add_argument(
        "-B", "--behaviour",
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

    parser.add_argument(
        "-c", "--contain", type=str, dest="contain", nargs="*",
        help="cells to set: 'x:y[:a]', space-separated. "
         "x/y/a are numbers or expressions with w, h, a "
         "(e.g. '3:2:4 w/2:h/3 5:w/2'). Default: random"
    )

    args = parser.parse_args()
    return args

def args_to_params(stdscr, args: argparse.Namespace) -> Caparams:
    height, width = stdscr.getmaxyx()
    if args.fullscreen is None: height-=1
    if args.width: width = args.width
    if args.height: height = args.height
        
    if args.gol: rule: Rule = RuleParse.from_string(Rule.game_of_life)
    elif args.gof: rule: Rule = RuleParse.from_string(Rule.game_of_fly)
    else:
        rule: Rule = (parse_or_raise("Rule", RuleParse.from_string, args.rule) 
              if args.rule is not None else random_prepared_rule())
        
    
    figure = Figure(width = width, height = height)
    if args.blank is None: figure.fill_full_random()
    if(args.contain): parse_or_raise("contain", FigureParse.contain_cells, figure, rule.aging, args.contain)
    
    return Caparams(
        stdscr = stdscr,
        figure = figure,
        rule = rule,
        delay = args.delay,
        stuck_behaviour=args.behaviour,
        symbols = random_symbols() if args.symbols is None else args.symbols,
        seed = RandomSeed.seed if args.seed is None else args.seed
    )

def parse_or_raise(label: str, fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"invalid {label}: {e}")
