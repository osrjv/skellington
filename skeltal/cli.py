import argparse
import logging
from skeltal.bot import Bot

LOGGER = logging.getLogger(__name__)

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


def run():
    parser = argparse.ArgumentParser("skeltal")
    _ = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d » %(levelname)s » %(message)s",
        datefmt="%H:%M:%S",
    )

    bot = Bot("localhost", 25565)

    try:
        print(LOGO, flush=True)
        bot.run_forever()
    except KeyboardInterrupt:
        logging.warning("User interrupt")
        bot.shutdown()
    except Exception as exc:
        print(exc)
        bot.shutdown()
