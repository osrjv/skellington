import argparse
import logging
import re
from skeltal.bot import Bot

LOGO = """
   .x+=:.         ..                       ..      s                      ..
  z`    ^%  < .z@8"`                 x .d88"      :8                x .d88"
     .   <k  !@88E                    5888R      .88                 5888R
   .@8Ned8"  '888E   u         .u     '888R     :888ooo       u      '888R
 .@^%8888"    888E u@8NL    ud8888.    888R   -*8888888    us888u.    888R
x88:  `)8b.   888E`"88*"  :888'8888.   888R     8888    .@88 "8888"   888R
8888N=*8888   888E .dN.   d888 '88%"   888R     8888    9888  9888    888R
 %8"    R88   888E~8888   8888.+"      888R     8888    9888  9888    888R
  @8Wou 9%    888E '888&  8888L        888R    .8888Lu= 9888  9888    888R
.888888P`     888E  9888. '8888c. .+  .888B .  ^%888*   9888  9888   .888B .
`   ^"F     '"888*" 4888"  "88888%    ^*888%     'Y"    "888*""888"  ^*888%
               ""    ""      "YP'       "%               ^Y"   ^Y'     "%
"""

LOGGER = logging.getLogger(__name__)
LEVELS = [logging.INFO, logging.DEBUG, logging.TRACE]
ADDRESS = "localhost:25565"


def address_type(value):
    pattern = re.compile(
        r"""
        (\[[:a-fA-F0-9]+\]|      # IPv6
        (?:\d{1,3}\.){3}\d{1,3}| # IPv4
        [-a-zA-Z0-9.]+)          # Hostname
        (?::(\d+))?              # Port
        """,
        re.X,
    )
    try:
        addr, port = pattern.match(value).group(1, 2)
        return (addr, int(port))
    except Exception as exc:
        raise argparse.ArgumentTypeError(
            "Address should be valid hostname:port pair"
        ) from exc


def run():
    parser = argparse.ArgumentParser("skeltal")
    parser.add_argument("address", nargs="?", type=address_type, default=ADDRESS)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    level = LEVELS[min(args.verbose, len(LEVELS) - 1)]
    logging.basicConfig(
        level=level,
        format="%(asctime)s.%(msecs)03d » %(levelname)s » %(message)s",
        datefmt="%H:%M:%S",
    )

    bot = Bot(address=args.address[0], port=args.address[1])

    try:
        print(LOGO, flush=True)
        bot.run_forever()
    except KeyboardInterrupt:
        logging.warning("User interrupt")
    finally:
        bot.shutdown()
