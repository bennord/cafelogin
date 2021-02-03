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
        help=f"Args that start with '--' (eg. --driver-version) can also be set in a config file ({', '.join(DEFAULT_CONFIG_FILES)} or specified via -c). "
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
        "--driver-version",
        default=actions.DEFAULT_DRIVER_VERSION,
        help="Specify the webdriver version to use.",
    )

    args, unused_args = parser.parse_known_args()
    with actions.create_webdriver_context(driver_version=args.driver_version) as driver:
        actions.ensure_portal_connection(driver=driver)