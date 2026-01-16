

import os
import logging
import shutil

from r7_surcom_sdk.lib import SurcomSDKException, constants, sdk_helpers, sdk_config
from r7_surcom_sdk.lib.surcom_api import SurcomAPI
from r7_surcom_sdk.lib.sdk_argparse import Args
from r7_surcom_sdk.lib.sdk_cmd import SurcomSDKSubCommand
from r7_surcom_sdk.lib.sdk_terminal_fonts import colors, formats

LOG = logging.getLogger(constants.LOGGER_NAME)


class DownloadCommand(SurcomSDKSubCommand):
    """
    [help]
    Download the {PRODUCT_NAME} Data Model.
    ---

    [description]
    Downloads the Data Model used by our Agent Skill
    ---

    [usage]
    $ {PROGRAM_NAME} {COMMAND} {SUB_CMD} <path_to_type_definition.yaml>
    ---
    """
    def __init__(self, types_parser):

        self.cmd_name = constants.CMD_MODEL
        self.sub_cmd_name = constants.CMD_DOWNLOAD

        cmd_docstr = self.__doc__.format(
            PROGRAM_NAME=constants.PROGRAM_NAME,
            PRODUCT_NAME=constants.PRODUCT_NAME,
            COMMAND=self.cmd_name,
            SUB_CMD=self.sub_cmd_name
        )

        super().__init__(
            parent=types_parser,
            cmd_name=self.sub_cmd_name,
            cmd_docstr=cmd_docstr
        )

        self.cmd_parser.add_argument(
            "--all",
            help="Download all types (core and unified).",
            action="store_true"
        )

        self.cmd_parser.add_argument(
            "--unified-types",
            help="If provided, download the Core and Unified types that are provided by Surface Command.",
            action="store_true"
        )

        self.cmd_parser.add_argument(
            "--source-types",
            help="If provided, download the Source types that are provided by any installed Connectors.",
            action="store_true"
        )

        self.cmd_parser.add_argument(
            "--clean",
            help="If provided, remove the existing Data Model before downloading.",
            action="store_true"
        )

        self.cmd_parser.add_argument(*Args.yes.flag, **Args.yes.kwargs)

    def _write_types(
        self,
        path_data_model: str,
        type_kind: str,
        types_dict: dict,
    ):
        path_types_folder = os.path.join(path_data_model, type_kind)

        for t_name, t_content in types_dict.items():

            path_type = os.path.join(path_types_folder, f"{t_name}.yaml")
            sdk_helpers.write_file(path_type, t_content, as_yaml=True)

        sdk_helpers.print_log_msg(
            f"Wrote {len(types_dict)} '{type_kind}' to '{path_types_folder}'.",
            log_level=logging.INFO
        )

    def run(self, args):
        SurcomSDKException.command_ran = f"{self.cmd_name} {self.sub_cmd_name}"

        sdk_helpers.print_log_msg(
            f"Starting the '{self.cmd_name} {self.sub_cmd_name}' command",
            divider=True
        )

        if not (args.all or args.source_types or args.unified_types):
            raise SurcomSDKException(
                "You must specify at least one of '--all', '--unified-types' or '--source-types' "
                "to download the Data Model."
            )

        path_ws = sdk_config.get_config(constants.CONFIG_NAME_PATH_CONNECTOR_WS)

        # Find the GH folder from the connector workspace. If we can't find it we error
        path_github_folder = sdk_helpers.find_folder(path_ws, constants.DIR_NAME_GH_FOLDER)

        connection = sdk_config.get_default_connection(prompt=True, default_to_yes=args.yes)

        surcom_client = SurcomAPI(
            base_url=connection.url,
            api_key=connection.api_key,
            user_agent_str=f"'{self.cmd_name} {self.sub_cmd_name}' command"
        )

        # Check if the model already exists, if so, we remove it and write a new one
        path_sc_data_model = os.path.join(path_github_folder, constants.DIR_NAME_SC_DATA_MODEL)

        if os.path.exists(path_sc_data_model):
            sdk_helpers.print_log_msg(
                f"An existing Data Model was already found at '{path_sc_data_model}'",
                log_color=colors.WARNING
            )

            if args.clean:
                sdk_helpers.print_log_msg(
                    f"The '--clean' flag was provided. Removing the existing Data Model at '{path_sc_data_model}'...",
                    log_color=colors.WARNING,
                    log_format=formats.ITALIC
                )
                shutil.rmtree(path_sc_data_model)

        if args.all or args.unified_types:

            sdk_helpers.print_log_msg("Downloading Core and Unified types...", log_level=logging.INFO)

            # Get the Core and Unified types
            core_types, noetic_builtin_types = surcom_client.types_get_core_and_unified_types()

            sdk_helpers.print_log_msg("Downloading Correlation Keys...", log_level=logging.INFO)

            # Get the Correlation Keys
            correlation_keys = surcom_client.get_correlation_keys()

            sdk_helpers.print_log_msg("Writing Core and Unified types...", log_level=logging.INFO)

            # Write the Core types
            self._write_types(
                path_data_model=path_sc_data_model,
                type_kind="core-types",
                types_dict=core_types
            )

            # Write the Unified types
            self._write_types(
                path_data_model=path_sc_data_model,
                type_kind="unified-types",
                types_dict=noetic_builtin_types
            )

            # Write the Correlation Keys
            path_correlation_keys = os.path.join(path_sc_data_model, "data", "sys.correlation-key.json")

            sdk_helpers.print_log_msg("Writing Correlation Keys...", log_level=logging.INFO)

            sdk_helpers.write_file(
                path_correlation_keys,
                correlation_keys,
                as_json=True
            )

        if args.all or args.source_types:

            sdk_helpers.print_log_msg("Downloading Source types...", log_level=logging.INFO)

            source_types = surcom_client.types_get_source_types()

            sdk_helpers.print_log_msg("Writing Source types...", log_level=logging.INFO)

            # Write the Source types
            self._write_types(
                path_data_model=path_sc_data_model,
                type_kind="source-types",
                types_dict=source_types
            )

        sdk_helpers.print_log_msg(
            f"The {constants.PRODUCT_NAME} Data Model is now available in '{path_sc_data_model}'.",
            log_level=logging.INFO,
            log_color=colors.OKGREEN
        )

        sdk_helpers.print_log_msg(f"Finished running the '{self.cmd_name} {self.sub_cmd_name}' command.", divider=True)
