import sys
import argparse
import logging
import logging.config
import json
import time
from commands.base import *
from commands.neutron import *

from prettytable import PrettyTable
import utils
import json

logger = logging.getLogger(__name__)


def json_body(string):
    """Validate the given string is in json format."""

    try:
        json.loads(string)
    except:
        msg = "{} is not a perfect json in string format".format(string)
        raise argparse.ArgumentTypeError(msg)
    return string


def getcommands():
    """Return the list of command names."""

    return [cmd.name for cmd in BaseCommand.__subclasses__()]


def process_args(argv):
    """Command line arguments definition and parsing routine."""

    parser = argparse.ArgumentParser("Neutron Resource Cleanup script")
    parser.add_argument("-T", "--tenant-id", help="Tenant ID", required=True)
    parser.add_argument("--command", choices=getcommands(),
                        help="command name", required=True)
    parser.add_argument("--args", type=json_body, required=False,
                        help="args for commands in json in string format."
                        " Example Format: '{\"name\":\"net1\"}' ",)
    options = parser.parse_args()
    return options


def run(options):
    """Executes the given command."""

    for cmd in BaseCommand.__subclasses__():
        if cmd.name == options.command:
            cmd(options)


def main(argv):
    """Main routine."""

    options = process_args(argv)
    logging.basicConfig(level=logging.INFO)
    logger.info('Neutron script starts with the arguments %s' % options)
    options.creds = utils.get_credentials()
    run(options)


if __name__ == "__main__":
    main(sys.argv)
