
from r7_surcom_sdk.cmds.model.download import DownloadCommand
from r7_surcom_sdk.lib import constants
from r7_surcom_sdk.lib.sdk_cmd import SurcomSDKMainCommand


class ModelCmd(SurcomSDKMainCommand):

    """
    [help]
    Interact with the {PRODUCT_NAME} Data Model.
    ---

    [description]
    Use these commands to download and manage the Data Model
    ---

    [usage]
    $ {PROGRAM_NAME} {COMMAND} download
    ---
    """
    def __init__(self, parent_parser):

        cmd_docstr = self.__doc__.format(
            PLATFORM_NAME=constants.PLATFORM_NAME,
            PRODUCT_NAME=constants.PRODUCT_NAME,
            PROGRAM_NAME=constants.PROGRAM_NAME,
            COMMAND=constants.CMD_MODEL
        )

        super().__init__(
            parent=parent_parser,
            cmd_name=constants.CMD_MODEL,
            cmd_docstr=cmd_docstr
        )

        # Add sub commands
        self.cmd_download = DownloadCommand(self.cmd_parser)

    def run(self, args):

        if args.model == constants.CMD_DOWNLOAD:
            self.cmd_download.run(args)

        else:
            self.main_parser.print_help()
