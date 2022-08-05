import cafelogin
import sys
import requests
import configargparse
import cafelogin.actions as actions

DEFAULT_CONFIG_FILES = ["cafelogin.config", "~/cafelogin.config"]


def add_help_argument(parser: configargparse.ArgumentParser):
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message.",
    )


def add_config_argument(parser: configargparse.ArgumentParser):
    parser.add_argument(
        "-c",
        "--config-file",
        is_config_file=True,
        help=f"Args that start with '--' (eg. --firefox-driver-version) can also be set in a config file ({', '.join(DEFAULT_CONFIG_FILES)} or specified via -c). "
        + "Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (details here https://goo.gl/R74nmi). "
        + "Arg precedence: commandline > config-file > defaults.",
    )


def run():
    parser = configargparse.ArgParser(
        default_config_files=DEFAULT_CONFIG_FILES,
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
        add_config_file_help=False,
    )
    add_help_argument(parser)
    add_config_argument(parser)
    parser.add_argument(
        "--version",
        action="version",
        version=cafelogin.__version__,
    )
    parser.add_argument(
        "--browser",
        default=actions.DEFAULT_TARGET_BROWSER,
        choices=["chrome", "firefox"],
        help="Target browser to use.",
    )
    parser.add_argument(
        "--chrome-driver-version",
        default=actions.DEFAULT_CHROME_DRIVER_VERSION,
        help="Specify the chrome webdriver version to use.",
    )
    parser.add_argument(
        "--firefox-driver-version",
        default=actions.DEFAULT_FIREFOX_DRIVER_VERSION,
        help="Specify the firefox webdriver version to use.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Continue watching for changes in portal connectivity.",
    )
    parser.add_argument(
        "--watch-interval",
        type=int,
        default=20,
        help="The frequency with which to watch for portal changes.",
    )

    args, unused_args = parser.parse_known_args()

    try:
        with actions.create_webdriver_context(
            target_browser=args.browser,
            chrome_driver_version=args.chrome_driver_version,
            firefox_driver_version=args.firefox_driver_version,
        ) as driver:
            if args.watch:
                actions.watch_portal_connection(
                    driver=driver, watch_interval=args.watch_interval
                )
            else:
                actions.ensure_portal_connection(driver=driver)
    except requests.exceptions.ConnectionError as error:
        sys.exit(error)
    except KeyboardInterrupt:
        pass
