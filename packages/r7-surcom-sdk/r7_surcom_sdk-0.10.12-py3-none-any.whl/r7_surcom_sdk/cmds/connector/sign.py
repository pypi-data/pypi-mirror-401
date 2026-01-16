
import logging
import zipfile
import os
import tempfile
import shutil

from r7_surcom_sdk.lib import SurcomSDKException, constants, sdk_config, sdk_helpers
from r7_surcom_sdk.lib.sdk_argparse import Args
from r7_surcom_sdk.lib.sdk_cmd import SurcomSDKSubCommand
from r7_surcom_sdk.lib.sdk_terminal_fonts import colors, formats, fmt

LOG = logging.getLogger(constants.LOGGER_NAME)


class SignCommand(SurcomSDKSubCommand):
    """
    [help]
    Sign a connector using jarsigner.
    ---

    [description]
    This command uses a Docker image to sign the provided connector ZIP file using the provided .p12 certificate
with jarsigner so that you can install and run it in {PRODUCT_NAME}.

You must set the `{CONFIG_NAME_P12_STORE_PASS}` option in the [{CONFIG_SEC_MAIN}] section of your {CONFIG_FILE_NAME}
file. This can be a 1Password Secret Reference.

You can optionally set the `{CONFIG_NAME_PATH_P12_FILE}` option to avoid providing the `--path-p12-file` argument.
    ---

    [usage]
    $ {PROGRAM_NAME} {COMMAND} {SUB_CMD} /path/to/connector.zip
    $ {PROGRAM_NAME} {COMMAND} {SUB_CMD} /path/to/connector.zip --path-p12-file /path/to/cert.p12
    ---
    """
    def __init__(self, connectors_parser):

        self.cmd_name = constants.CMD_CONNECTORS
        self.sub_cmd_name = constants.CMD_SIGN

        cmd_docstr = self.__doc__.format(
            PROGRAM_NAME=constants.PROGRAM_NAME,
            PLATFORM_NAME=constants.PLATFORM_NAME,
            PRODUCT_NAME=constants.PRODUCT_NAME,
            CONFIG_FILE_NAME=constants.CONFIG_FILE_NAME,
            CONFIG_SEC_MAIN=constants.CONFIG_SEC_MAIN,
            CONFIG_NAME_P12_STORE_PASS=constants.CONFIG_NAME_P12_STORE_PASS,
            CONFIG_NAME_PATH_P12_FILE=constants.CONFIG_NAME_PATH_P12_FILE,
            COMMAND=self.cmd_name,
            SUB_CMD=self.sub_cmd_name
        )

        super().__init__(
            parent=connectors_parser,
            cmd_name=self.sub_cmd_name,
            cmd_docstr=cmd_docstr)

        self.cmd_parser.add_argument(Args.pos_path_connector_zip.flag, **Args.pos_path_connector_zip.kwargs)
        self.cmd_parser.add_argument(*Args.path_p12_file.flag, **Args.path_p12_file.kwargs)

    def _sign_with_docker(
        self,
        args,
        path_unsigned_zip: str,
        path_signed_zip_file: str,
        path_p12_file: str,
        jarsigner_store_pass: str,
        sensitive_patterns: list = None
    ):

        with tempfile.TemporaryDirectory() as tmpdir:

            # Copy .p12 to temp directory
            temp_p12 = os.path.join(tmpdir, "cert.p12")
            shutil.copy(path_p12_file, temp_p12)

            # Copy ZIP to temp directory
            temp_zip = os.path.join(tmpdir, os.path.basename(path_unsigned_zip))
            shutil.copy(path_unsigned_zip, temp_zip)

            signed_name = os.path.basename(path_signed_zip_file)

            cli_args = [
                "docker", "run", "--rm", "-v", f"{tmpdir}:/workspace", "-w", "/workspace",
                constants.JDK_IMAGE,
                "jarsigner",
                "-storepass", jarsigner_store_pass,
                "-keystore", "cert.p12",
                "-storetype", "PKCS12",
                "-digestalg", "SHA-256",
                "-signedjar", signed_name,
                os.path.basename(temp_zip),
                "noetic"
            ]

            result = sdk_helpers.run_subprocess(cli_args, regex_patterns_to_mask=sensitive_patterns)

            if args.verbose:

                if hasattr(result, 'stderr') and result.stderr:
                    LOG.debug(result.stderr.decode().strip())

                if hasattr(result, 'stdout') and result.stdout:
                    LOG.debug(result.stdout.decode().strip())

            # Copy signed file back to original location
            shutil.copy(
                os.path.join(tmpdir, signed_name),
                path_signed_zip_file
            )

    def _is_zero_value_cert(self, path_p12_file: str) -> bool:
        """
        Check if the provided .p12 file is a zero-value certificate

        :param path_p12_file: path to the .p12 file
        :type path_p12_file: str
        :return: True if it is a zero-value cert, False otherwise
        :rtype: bool
        """
        return os.path.basename(path_p12_file).startswith("zero-value")

    def run(self, args) -> str:
        SurcomSDKException.command_ran = f"{self.cmd_name} {self.sub_cmd_name}"

        sdk_helpers.print_log_msg(
            f"Starting the '{self.cmd_name} {self.sub_cmd_name}' command",
            divider=True
        )

        if not zipfile.is_zipfile(args.path_connector_zip):
            raise SurcomSDKException(
                message=f"'{args.path_connector_zip}' is not a valid zip file",
                solution="Please run `surcom connector package` again to create a valid connector zip file",
            )

        # NOTE: If the user did not provide a path for the .p12 file, we set it to an empty string
        # so that sdk_config.get_config() can handle it appropriately.
        if args.path_p12_file is None:
            args.path_p12_file = ""

        path_p12_file = sdk_config.get_config(
            option=constants.CONFIG_NAME_PATH_P12_FILE,
            option_type="str",
            default=args.path_p12_file
        )

        if not os.path.isfile(path_p12_file):
            raise SurcomSDKException(
                message=f"The .p12 file at '{path_p12_file}' does not exist",
                solution="Please provide a valid path to a .p12 file using the '--path-p12-file' argument "
                         "or set the 'path_p12_file' option in the [surcom-sdk] section in the surcom_config file."
            )

        zip_file_name = os.path.basename(args.path_connector_zip)

        # NOTE: we append signed to the filename
        path_signed_zip_file = os.path.join(
            os.path.dirname(args.path_connector_zip),
            zip_file_name.replace(".zip", "-signed.zip")
        )

        sdk_helpers.print_log_msg(
            f"Preparing to sign the connector ZIP '{args.path_connector_zip}' "
            f"using the .p12 file at '{path_p12_file}'"
        )

        # Else it is signed, so we raise an error if the user tries to install a custom connector
        if sdk_helpers.is_zip_using_custom_version(path_zip_file=args.path_connector_zip):
            raise SurcomSDKException(
                message="You are attempting to sign a zip that is a Custom Connector. "
                        "Custom Connectors cannot be signed.",
                solution="Repackage this connector without using the `--orchestrator` flag and try again."
            )

        # NOTE: If this is a zero-value cert, we do not need a password
        if not self._is_zero_value_cert(path_p12_file):

            store_pass = sdk_config.get_config(
                option=constants.CONFIG_NAME_P12_STORE_PASS,
                default=""
            )

            if not store_pass:

                prompt = "Enter the password for the P12 file"
                prompt = f"\n{fmt(prompt, f=formats.BOLD)}"

                store_pass = sdk_helpers.get_cli_input(
                    prompt=prompt,
                    is_password=True
                )

            sensitive_patterns = [store_pass]

        else:
            store_pass = ""  # nosec
            sensitive_patterns = []

        sdk_helpers.print_log_msg(
            f"Signing the connector ZIP with jarsigner using the Docker image '{constants.JDK_IMAGE}'. This may take a "
            "few moments...",
            log_color=colors.OKBLUE,
            log_format=formats.BOLD
        )

        self._sign_with_docker(
            args=args,
            path_unsigned_zip=args.path_connector_zip,
            path_signed_zip_file=path_signed_zip_file,
            path_p12_file=path_p12_file,
            jarsigner_store_pass=store_pass,
            sensitive_patterns=sensitive_patterns
        )

        sdk_helpers.print_log_msg(
            f"Signed connector ZIP created at '{path_signed_zip_file}'",
            log_color=colors.OKGREEN,
            log_format=formats.BOLD
        )

        sdk_helpers.print_log_msg(f"Finished running the '{self.sub_cmd_name}' command", divider=True)

        return path_signed_zip_file
