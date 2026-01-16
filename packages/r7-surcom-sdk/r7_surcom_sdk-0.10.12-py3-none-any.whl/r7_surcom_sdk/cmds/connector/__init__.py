
from r7_surcom_sdk.cmds.connector.codegen import CodegenCommand
from r7_surcom_sdk.cmds.connector.init import InitCommand
from r7_surcom_sdk.cmds.connector.package import PackageCommand
from r7_surcom_sdk.cmds.connector.validate import ValidateCommand
from r7_surcom_sdk.cmds.connector.invoke import InvokeCommand
from r7_surcom_sdk.cmds.connector.install import InstallCommand
from r7_surcom_sdk.cmds.connector.sign import SignCommand
from r7_surcom_sdk.lib import constants
from r7_surcom_sdk.lib.sdk_cmd import SurcomSDKMainCommand


class ConnectorsCmd(SurcomSDKMainCommand):

    """
    [help]
    Develop connectors for {PRODUCT_NAME}.
    ---

    [description]
    Use these commands to create, manage, and deploy connectors for the
{PRODUCT_NAME}.

Your connector development workspace is set by the `path_connector_ws`
option in the {CONFIG_FILE_NAME} file.
    ---

    [usage]
    $ {PROGRAM_NAME} {COMMAND} init
    $ {PROGRAM_NAME} {COMMAND} codegen
    $ {PROGRAM_NAME} {COMMAND} invoke
    $ {PROGRAM_NAME} {COMMAND} package
    ---
    """
    def __init__(self, parent_parser):

        cmd_docstr = self.__doc__.format(
            PRODUCT_NAME=constants.PRODUCT_NAME,
            PROGRAM_NAME=constants.PROGRAM_NAME,
            CONFIG_FILE_NAME=constants.CONFIG_FILE_NAME,
            COMMAND=constants.CMD_CONNECTORS
        )

        super().__init__(
            parent=parent_parser,
            cmd_name=constants.CMD_CONNECTORS,
            cmd_docstr=cmd_docstr
        )

        # Add sub commands
        self.cmd_init = InitCommand(self.cmd_parser)
        self.cmd_codegen = CodegenCommand(self.cmd_parser)
        self.cmd_invoke = InvokeCommand(self.cmd_parser)
        self.cmd_validate = ValidateCommand(self.cmd_parser)
        self.cmd_package = PackageCommand(self.cmd_parser)
        self.cmd_sign = SignCommand(self.cmd_parser)
        self.cmd_install = InstallCommand(self.cmd_parser)

    def run(self, args):

        if args.connector == constants.CMD_INIT:
            self.cmd_init.run(args)

        elif args.connector == constants.CMD_CODEGEN:
            self.cmd_codegen.run(args)

        elif args.connector == constants.CMD_PACKAGE:
            self.cmd_package.run(
                args,
                cmd_validate=self.cmd_validate,
            )

        elif args.connector == constants.CMD_INVOKE:
            self.cmd_invoke.run(
                args,
                cmd_package=self.cmd_package,
            )

        elif args.connector == constants.CMD_VALIDATE:
            self.cmd_validate.run(args)

        elif args.connector == constants.CMD_INSTALL:
            self.cmd_install.run(
                args,
                cmd_package=self.cmd_package,
                cmd_sign=self.cmd_sign,
            )

        elif args.connector == constants.CMD_SIGN:
            self.cmd_sign.run(args)

        else:
            self.main_parser.print_help()
