# Author: Cameron F. Abrams, <cfa22@drexel.edu>
import argparse as ap
from importlib.metadata import version

from .properties import get_database

banner = """
                                  █████ ████                    
                                 ░░███ ░░███                    
  █████   ██████   ████████    ███████  ░███   ██████  ████████ 
 ███░░   ░░░░░███ ░░███░░███  ███░░███  ░███  ███░░███░░███░░███
░░█████   ███████  ░███ ░███ ░███ ░███  ░███ ░███████  ░███ ░░░ 
 ░░░░███ ███░░███  ░███ ░███ ░███ ░███  ░███ ░███░░░   ░███     
 ██████ ░░████████ ████ █████░░████████ █████░░██████  █████    
░░░░░░   ░░░░░░░░ ░░░░ ░░░░░  ░░░░░░░░ ░░░░░  ░░░░░░  ░░░░░     
                                                                                 
       ████████  ████████   ██████  ████████   █████            
      ░░███░░███░░███░░███ ███░░███░░███░░███ ███░░             
       ░███ ░███ ░███ ░░░ ░███ ░███ ░███ ░███░░█████            
       ░███ ░███ ░███     ░███ ░███ ░███ ░███ ░░░░███           
       ░███████  █████    ░░██████  ░███████  ██████            
       ░███░░░  ░░░░░      ░░░░░░   ░███░░░  ░░░░░░             
       ░███                         ░███                        
       █████                        █████                       
      ░░░░░                        ░░░░░              
        (c) 2026, Cameron F. Abrams <cfa22@drexel.edu> 
"""

def cli():
    P = get_database()
    subcommands = {
        'showprops': dict(
            func = P.show_properties,
            help = 'show available properties',
            ),
        'find' : dict(
            func = P.find_compound,
            help = 'find compound by name',
            ),
        'show': dict(
            func = P.show_compound_properties,
            help = 'show properties for a compound',
        )
    }
    parser = ap.ArgumentParser(
        prog='sandlerprops',
        description="Sandlerprops: A Python interface to the properties database provided with Chemical, Biochemical, and Engineering Thermodynamics (5th edition) by Stan Sandler",
        epilog='(c) 2026 Cameron F. Abrams <cfa22@drexel.edu>'
    )
    parser.add_argument(
        '-b',
        '--banner',
        default=False,
        action=ap.BooleanOptionalAction,
        help='toggle banner message'
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'sandlerprops version {version("sandlerprops")}',
        help='show program version and exit'
    )
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="command",
        metavar="<command>",
        required=True,
    )
    command_parsers={}
    for k, specs in subcommands.items():
        command_parsers[k] = subparsers.add_parser(
            k,
            help=specs['help'],
            add_help=False,
            formatter_class=ap.RawDescriptionHelpFormatter
        )
        command_parsers[k].set_defaults(func=specs['func'])
        command_parsers[k].add_argument(
            '--help',
            action='help',
            help=specs['help']
        )

    command_parsers['find'].add_argument(
        'compound_name',
        type=str,
        help='name of compound to find'
    )
    command_parsers['show'].add_argument(
        'compound_name',
        type=str,
        help='name of compound whose properties to show'
    )

    args = parser.parse_args()
    if args.banner:
        print(banner)
    if hasattr(args, 'func'):
        args.func(args)
    else:
        my_list = ', '.join(list(subcommands.keys()))
        print(f'No subcommand found. Expected one of {my_list}')
    if args.banner:
        print('Thanks for using sandlerprops!')