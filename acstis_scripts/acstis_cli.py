import argparse
import logging

import colorlog
from nyawc.Options import Options

from acstis.Driver import Driver
from acstis.helpers.PackageHelper import PackageHelper


def require_arguments():
    """Get the arguments from CLI input.

    Returns:
        :class:`argparse.Namespace`: A namespace with all the parsed CLI arguments.

    """

    parser = argparse.ArgumentParser(
        prog=PackageHelper.get_alias(),
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=220, width=220)
    )

    optional = parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")

    required.add_argument("-d", "--domain", help="the domain to scan (e.g. finnwea.com)", required=True)

    optional.add_argument("-c", "--crawl", help="use the crawler to scan all the entire domain", action="store_true")
    optional.add_argument("-vp", "--verify-payload",
                          help="use a javascript engine to verify if the payload was executed "
                               "(otherwise false positives may occur)",
                          action="store_true")
    optional.add_argument("-av", "--angular-version",
                          help="manually pass the angular version (e.g. 1.4.2) if the automatic check doesn't work",
                          type=str, default=None)
    optional.add_argument("-vrl", "--vulnerable-requests-log",
                          help="log all vulnerable requests to this file (e.g. /var/logs/acstis.log or urls.log)",
                          type=str, default=None)
    optional.add_argument("-siv", "--stop-if-vulnerable",
                          help="(crawler option) stop scanning if a vulnerability was found", action="store_true")
    optional.add_argument("-pmm", "--protocol-must-match",
                          help="(crawler option) only scan pages with the same protocol as the startpoint (e.g. only "
                               "https)",
                          action="store_true")
    optional.add_argument("-sos", "--scan-other-subdomains",
                          help="(crawler option) also scan pages that have another subdomain than the startpoint",
                          action="store_true")
    optional.add_argument("-soh", "--scan-other-hostnames",
                          help="(crawler option) also scan pages that have another hostname than the startpoint",
                          action="store_true")
    optional.add_argument("-sot", "--scan-other-tlds",
                          help="(crawler option) also scan pages that have another tld than the startpoint",
                          action="store_true")
    optional.add_argument("-md", "--max-depth", help="(crawler option) the maximum search depth (default is unlimited)",
                          type=int)
    optional.add_argument("-mt", "--max-threads",
                          help="(crawler option) the maximum amount of simultaneous threads to use (default is 20)",
                          type=int, default=20)
    optional.add_argument("-iic", "--ignore-invalid-certificates",
                          help="(crawler option) ignore invalid ssl certificates", action="store_true")
    optional.add_argument("-tc", "--trusted-certificates",
                          help="(crawler option) trust this CA_BUNDLE file (.pem) or directory with certificates",
                          type=str, default=None)

    parser._action_groups.append(optional)
    return parser.parse_args()


def setup_logger():
    """Setup ColorLog to enable colored logging output."""

    # Colored logging
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "white",
            "SUCCESS": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white"
        }
    ))

    logger = colorlog.getLogger()
    logger.addHandler(handler)

    # Also show INFO logs
    logger.setLevel(logging.INFO)

    # Add SUCCESS logging
    logging.SUCCESS = 25
    logging.addLevelName(
        logging.SUCCESS,
        "SUCCESS"
    )

    # Disable Selenium logging
    selenium_logger = logging.getLogger("selenium.webdriver.remote.remote_connection")
    selenium_logger.setLevel(logging.WARNING)

    setattr(
        logger,
        "success",
        lambda message, *args: logger._log(logging.SUCCESS, message, args)
    )


def print_banner():
    """Print a useless ASCII art banner to make things look a bit nicer."""

    print("""
  /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$
 /$$__  $$ /$$__  $$ /$$__  $$|__  $$__/|_  $$_/ /$$__  $$
| $$  \ $$| $$  \__/| $$  \__/   | $$     | $$  | $$  \__/
| $$$$$$$$| $$      |  $$$$$$    | $$     | $$  |  $$$$$$
| $$__  $$| $$       \____  $$   | $$     | $$   \____  $$
| $$  | $$| $$    $$ /$$  \ $$   | $$     | $$   /$$  \ $$
| $$  | $$|  $$$$$$/|  $$$$$$/   | $$    /$$$$$$|  $$$$$$/
|__/  |__/ \______/  \______/    |__/   |______/ \______/

Version """ + PackageHelper.get_version() + """ - Copyright 2017 Tijme Gommers <tijme@finnwea.com>
    """)


def main():
    """Start the scanner."""

    print_banner()
    setup_logger()

    args = require_arguments()

    options = Options()

    options.scope.protocol_must_match = args.protocol_must_match
    options.scope.subdomain_must_match = not args.scan_other_subdomains
    options.scope.hostname_must_match = not args.scan_other_hostnames
    options.scope.tld_must_match = not args.scan_other_tlds
    options.scope.max_depth = args.max_depth if args.crawl else 0
    options.performance.max_threads = args.max_threads
    options.misc.verify_ssl_certificates = not args.ignore_invalid_certificates
    options.misc.trusted_certificates = args.trusted_certificates

    driver = Driver(args, options)
    driver.start()


if __name__ == "__main__":
    main()
