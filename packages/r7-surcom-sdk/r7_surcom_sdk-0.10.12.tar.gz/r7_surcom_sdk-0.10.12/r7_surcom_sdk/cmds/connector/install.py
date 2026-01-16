
import logging
import zipfile
import datetime

from r7_surcom_sdk.lib import (SurcomSDKException, constants, sdk_config,
                               sdk_helpers)
from r7_surcom_sdk.lib.sdk_argparse import Args
from r7_surcom_sdk.lib.sdk_cmd import SurcomSDKSubCommand
from r7_surcom_sdk.lib.surcom_api import SurcomAPI
from r7_surcom_sdk.lib.sdk_terminal_fonts import colors, formats

LOG = logging.getLogger(constants.LOGGER_NAME)


class InstallCommand(SurcomSDKSubCommand):
    """
    [help]
    Install a connector into {PRODUCT_NAME}.
    ---

    [description]
    Install a Surcom Connector into {PRODUCT_NAME} either from a packaged ZIP file or from the Connector Store.

If the ZIP file has not been signed, the version must be suffixed with '{CUSTOM_CONNECTOR_SUFFIX}' to indicate it is a
Custom Connector, else we raise an error.

If installing from the Connector Store, specify the `--connector-id` parameter and optionally the `--connector-version`
parameter. If no version is specified, the latest version is installed. We support connector_ids with dots
or underscores.

    ---

    [usage]
    $ {PROGRAM_NAME} {COMMAND} {SUB_CMD} --connector-id 'cyber.fix.app'
    $ {PROGRAM_NAME} {COMMAND} {SUB_CMD} --connector-id 'cyber_fix_app' --connector-version '2.1.1569'
    $ {PROGRAM_NAME} {COMMAND} {SUB_CMD} --zip '/path/to/connector.zip' --sample-data --yes
    ---
    """
    def __init__(self, connectors_parser):

        self.cmd_name = constants.CMD_CONNECTORS
        self.sub_cmd_name = constants.CMD_INSTALL

        cmd_docstr = self.__doc__.format(
            PROGRAM_NAME=constants.PROGRAM_NAME,
            PLATFORM_NAME=constants.PLATFORM_NAME,
            PRODUCT_NAME=constants.PRODUCT_NAME,
            CUSTOM_CONNECTOR_SUFFIX=constants.CUSTOM_CONNECTOR_SUFFIX,
            COMMAND=self.cmd_name,
            SUB_CMD=self.sub_cmd_name
        )

        super().__init__(
            parent=connectors_parser,
            cmd_name=self.sub_cmd_name,
            cmd_docstr=cmd_docstr)

        self.cmd_parser.add_argument(*Args.path_connector.flag, **Args.path_connector.kwargs)
        self.cmd_parser.add_argument(*Args.connector_id.flag, **Args.connector_id.kwargs)
        self.cmd_parser.add_argument(*Args.connector_version.flag, **Args.connector_version.kwargs)
        self.cmd_parser.add_argument(*Args.path_connector_zip.flag, **Args.path_connector_zip.kwargs)
        self.cmd_parser.add_argument(*Args.sample_data.flag, **Args.sample_data.kwargs)
        self.cmd_parser.add_argument(*Args.yes.flag, **Args.yes.kwargs)

    @staticmethod
    def _print_success_log(
        connector_id: str,
        connector_version: str,
        connection_name: str
    ):
        if connector_version == "latest":
            msg = f"Successfully installed the latest version of '{connector_id}'"
        else:
            msg = f"Successfully installed '{connector_id}' with the version 'v{connector_version}'"

        msg = f"{msg} in {connection_name}"
        sdk_helpers.print_log_msg(msg, log_color=colors.OKGREEN, log_format=formats.BOLD)

    def run(self, args, cmd_package=None, cmd_sign=None):
        SurcomSDKException.command_ran = f"{self.cmd_name} {self.sub_cmd_name}"

        sdk_helpers.print_log_msg(
            f"Starting the '{self.cmd_name} {self.sub_cmd_name}' command",
            divider=True
        )

        # TODO: support installing Connector depends-on
        # Check if they are installed, if not install them first
        # Make sure we respect the order

        connection = sdk_config.get_default_connection()

        surcom_client = SurcomAPI(
            base_url=connection.url,
            api_key=connection.api_key,
            user_agent_str=f"'{self.cmd_name} {self.sub_cmd_name}' command"
        )

        if args.path_connector_zip:
            sdk_helpers.print_log_msg(
                f"Installing the connector ZIP '{args.path_connector_zip}' into '{connection.name}'"
            )

            if not zipfile.is_zipfile(args.path_connector_zip):
                raise SurcomSDKException(
                    message=f"'{args.path_connector_zip}' is not a valid zip file",
                    solution="Please run `surcom connector package` again to create a valid connector zip file",
                )

            if not sdk_helpers.is_signed_zip(path_zip_file=args.path_connector_zip):
                sdk_helpers.print_log_msg(
                    "This zip file is not signed. We are assuming it is a Custom Connector",
                    log_level=logging.WARNING,
                    log_format=formats.BOLD
                )

                if not sdk_helpers.is_zip_using_custom_version(path_zip_file=args.path_connector_zip):
                    raise SurcomSDKException(
                        message=f"The zip is not signed and its version is not suffixed with "
                                f"'{constants.CUSTOM_CONNECTOR_SUFFIX}'",
                        solution="To install this in Surface Command you need to ensure its packaged with the "
                                 "--orchestrator flag. Run `surcom connector package --orchestrator` and try again "
                                 f"with the '{constants.CUSTOM_CONNECTOR_SUFFIX}' zip that is generated"
                    )

        elif args.connector_id:

            msg = "Using the Connector Store to install"

            if "_" in args.connector_id:
                args.connector_id = args.connector_id.replace("_", ".")
                LOG.debug("Replacing underscores with dots in the connector_id. New id is: '%s'", args.connector_id)

            if args.connector_version:
                msg = f"{msg} 'v{args.connector_version}'"

            else:
                msg = f"{msg} the latest version"

            msg = f"{msg} of the Connector '{args.connector_id}'"

            sdk_helpers.print_log_msg(msg)

        else:
            sdk_helpers.print_log_msg(
                f"Attempting to install the connector from '{args.path_connector}' into '{connection.name}'"
            )

            # NOTE: a Connector that we install from src will have the version '1.0.<tx>+dev'
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            args.build_number = f"{ts}{constants.DEV_CONNECTOR_SUFFIX}"

            LOG.debug("Setting the build_number to: %s", args.build_number)

            path_unsigned_connector = cmd_package.run(args=args)

            # NOTE: we have to set this to the output of cmd_package before running cmd_sign
            args.path_connector_zip = path_unsigned_connector
            args.path_p12_file = None
            path_signed_connector = cmd_sign.run(args=args)

            # NOTE: now we have signed the connector we reset the `path_connector_zip` argument and continue to install
            args.path_connector_zip = path_signed_connector

        sdk_helpers.prompt_to_confirm(
            prompt=f"Are you sure you want to use the '{connection.name}' configuration to install this connector?",
            default_to_yes=args.yes
        )

        r = surcom_client.app_install_from_zip(
            connector_id=args.connector_id,
            connector_version=args.connector_version,
            path_connector_zip=args.path_connector_zip,
            load_sample_data=args.sample_data
        )

        # NOTE: we get the id and version from the CLI args
        # if not set we read them from the provided zip
        connector_id = args.connector_id
        connector_version = args.connector_version

        if args.path_connector_zip:

            if not connector_id:
                connector_id = sdk_helpers.read_from_manifest(args.path_connector_zip, "id")

            if not connector_version:
                connector_version = sdk_helpers.read_from_manifest(args.path_connector_zip, "version")

        if not connector_version:
            connector_version = "latest"

        msg = "Connector installation is running asynchronously"
        msg = f"{msg}. The Execution ID is: '{r.get('execution_id')}'"
        msg = f"{msg}. Attempting to monitor workflow logs..."
        sdk_helpers.print_log_msg(msg, log_color=colors.OKBLUE, log_format=formats.BOLD)
        wf_passed = surcom_client.print_workflow_logs(execution_id=r.get("execution_id"), only_user_msgs=True)

        if wf_passed:
            self._print_success_log(
                connector_id=connector_id,
                connector_version=connector_version,
                connection_name=connection.name
            )

        sdk_helpers.print_log_msg(f"Finished running the '{self.sub_cmd_name}' command", divider=True)
