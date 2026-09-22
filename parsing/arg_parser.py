from debug import printl
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

    #figure
    parser.add_argument(
        "-W", "--width", type=int, dest="width",
        help="field width (cells horizontally), default: fit to screen"
    )
    parser.add_argument(
        "-H", "--height", type=int, dest="height",
        help="field height (cells vertically), default: fit to screen (status bar excluded)"
    )
    parser.add_argument(
        "-F", "--fullscreen", dest="fullscreen", action="store_true",
        help="field fills the screen; ignored for dimensions set via -W/-H"
    )
    parser.add_argument(
        "-b", "--blank", action="store_true", dest = "blank",
        help="clear the field before starting"
    )
    parser.add_argument(
        "-f", "--fill", type=float, default=None, dest = "fill", metavar="FRACTION",
        help="randomly fill the field with 1s at given fraction (0.0..1.0), default: random"
    )
    parser.add_argument(
        "-c", "--contain", type=FigureParse.validate_contains, dest="contain", nargs="*",
        help="cells to set: 'x:y[:a]', space-separated. "
         "x/y/a are numbers or expressions with w, h, a "
         "(e.g. '3:2:4 w/2:h/3 5:w/2'). Default: random"
    )
    parser.add_argument(
        "-R", "--rect", type=lambda s: parse_or_raise("rect", FigureParse.rect_parse, s), dest = "rect",
        metavar="W:H",
        help="add a rectangle of size W:H in the center of the field "
             "(e.g. '5:3'). Default: none"
    )


    #rule
    group_rule = parser.add_mutually_exclusive_group()
    group_rule.add_argument(
        "-r", "--rule", type=RuleParse.from_string, dest = "rule",
        help="rule in B/S/ notation (e.g. B2/S0345/10), default: random"
    )
    group_rule.add_argument(
        "-gol", action="store_true", dest = "gol",
        help="start with Game of Life rule (B3/S23)"
    )
    group_rule.add_argument(
        "-gof", action="store_true", dest = "gof",
        help="start with Game of Fly rule (B2/S0345/10)"
    )

    #player
    parser.add_argument(
        "-p", "--pause", action="store_true", dest = "pause",
        help="start paused"
    )
    parser.add_argument(
        "-d", "--delay", type=float, dest="delay", default=0.1,
        help="delay between frames in seconds, default 0.1"
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

    #other
    parser.add_argument(
        "-S", "--seed", type=int, default=None, dest = "seed",
        help="random seed for reproducibility, default: random"
    )
    parser.add_argument(
        "-s", "--symbols", type=str, dest = "symbols",
        help="symbols used to render cells (e.g. ' .oO'), default: random"
    )


    ##RANDOM
    #figure
    
    
    #rule
    group_rule.add_argument(
        "-rr", action="store_true", dest="rr",
        help= "absolute random rule"
    )
    group_rule.add_argument(
        "-rra", action="store_true", dest="rra",
        help= "random rule with age"
    )
    group_rule.add_argument(
        "-rrs", action="store_true", dest="rrs",
        help= "random rule without age (simple)"
    )
    

    args = parser.parse_args()
    return args

def args_to_params(stdscr, args: argparse.Namespace) -> Caparams:

    #rule
    rule: Rule = random_prepared_rule()
    if args.gol: rule = RuleParse.from_string(Rule.game_of_life)
    if args.gof: rule = RuleParse.from_string(Rule.game_of_fly)
    if args.rr: rule = random_rule()
    if args.rra: rule = random_rule(aging_only=True)
    if args.rrs: rule = random_rule(aging_only=False)
    if args.rule: rule = args.rule
    
    #figure
    height, width = stdscr.getmaxyx()
    if args.fullscreen is None: height-=1
    if args.width: width = args.width
    if args.height: height = args.height
    figure = Figure(width = width, height = height)
    if args.fill: figure.fill_random(fraction=args.fill)
    if args.blank: figure.blank_field()
    if args.contain: FigureParse.contain_cells(figure=figure, max_age=rule.aging, cells=args.contain)
    if args.rect: FigureParse.contain_rect(figure=figure, rect = args.rect)

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
    
