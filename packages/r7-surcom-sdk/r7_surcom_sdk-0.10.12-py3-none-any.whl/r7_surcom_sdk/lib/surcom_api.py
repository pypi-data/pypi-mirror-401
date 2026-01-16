
import logging
import sys
import zipfile
import time
from typing import Tuple
from importlib.metadata import version

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from r7_surcom_sdk.lib import SurcomSDKException, constants, sdk_helpers, sdk_config
from r7_surcom_sdk.lib.sdk_terminal_fonts import colors, formats, fmt

LOG = logging.getLogger(constants.LOGGER_NAME)

# TODO: add mockserver tests for this file


class SurcomAPI():

    def __init__(
        self,
        base_url: str,
        api_key: str,
        user_agent_str: str = None
    ):
        """
        The main class for the Surface Command API

        :param base_url: the base URL of the Surface Command API
        :type base_url: str
        :param api_key: the API key to use for authentication. If using the legacy format, this should be in the format:
            '__legacy__<tenant_id>/<username>:<password>'
        :type api_key: str, optional
        :param user_agent_str: an optional user agent string to append to the default user agent
            (r7-surcom-sdk/<version>). This is useful for debugging and logging purposes.
            This should be a string that describes the client using the SDK, e.g. 'import-data command'
        :type user_agent_str: str, optional
        """

        # TODO: validate the url
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.session()

        user_agent = f"{constants.FULL_PROGRAM_NAME}/{version(constants.PACKAGE_NAME)}"

        if user_agent_str:
            user_agent = f"{user_agent}/{user_agent_str}"

        self.session.headers.update({
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip"
        })

        if api_key.startswith(constants.LEGACY_PREFIX):

            if ":" not in api_key or "/" not in api_key:
                raise SurcomSDKException(
                    "If using the legacy format to authenticate, make sure the api_key is in the format: "
                    "'__legacy__<tenant_id>/<username>:<password>'"
                )

            username, pw = api_key.replace(constants.LEGACY_PREFIX, "").split(":")
            self.session.auth = HTTPBasicAuth(username=username, password=pw)
            self.using_api_key = False

        else:
            self.session.headers.update({"X-API-Key": api_key})
            self.using_api_key = True

    def _request(
            self,
            method: str,
            url: str,
            params: dict = None,
            data: dict = None,
            json: dict = None,
            headers: dict = None,
            # TODO: make this a config
            timeout: float = constants.REQUESTS_TIMEOUT_SECONDS,
            return_response_object: bool = False
    ) -> dict:
        """
        The main method that sends all requests to Surface Command

        :param method: the request method. One of GET, POST, PUT or DELETE
        :type method: str
        :param url: the URL of the API in Surface Command to send the request to
        :type url: str
        :param params: dict of parameters to send in the query string for the Request
        :type params: dict, optional
        :param data: dict, bytes, or file-like object to send in the body of the Request
        :type data: dict, optional
        :param json: a JSON serializable Python object to send in the body of the Request
        :type json: dict, optional
        :param headers: dictionary of extra HTTP Headers to send with the Request. Headers set in the
            __init__ method are sent with every request
        :type headers: dict, optional
        :param timeout: How many seconds to wait for the server to send data before giving up,
            defaults to constants.REQUESTS_TIMEOUT_SECONDS
        :type timeout: float, optional
        :param return_response_object: if set to True returns the requests.response object, defaults to False
        :type return_response_object: bool, optional
        :return: The body of the response as a dict or the full requests.Response object if `return_response_object`
            is set to True
        :rtype: dict
        """
        # TODO: what about cert files
        rtn_value = None

        if method not in constants.REQUEST_SUPPORTED_METHODS:
            raise SurcomSDKException(f"'{method}' is not one of '{','.join(constants.REQUEST_SUPPORTED_METHODS)}'")

        url = f"{self.base_url}/{url}"

        LOG.debug("Making '%s' request to URL: '%s'", method, url)

        if params:
            LOG.debug("With params: %s", str(params))

        r = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout
        )

        try:
            trace_id = r.headers.get(constants.HEADER_NOETIC_TRACE_ID)

            if trace_id:
                LOG.debug(f"{fmt(constants.HEADER_NOETIC_TRACE_ID, c=colors.RED)}: {trace_id}")

            r.raise_for_status()

            if return_response_object:
                return r

        except HTTPError as err:

            LOG.debug(f"Error Response: {str(err)}")

            err_detail = r.text

            try:
                err_detail = r.json()

                # Sometimes an error message is a just a plain str
                # (yeah, even after we call .json())
                if isinstance(err_detail, str):
                    raise SurcomSDKException(err_detail)

                # Sometimes errors are in "message"
                err_detail = err_detail.get("message", err_detail)

                # Sometimes errors are then nested in "detail"
                if isinstance(err_detail, dict):
                    err_detail.get("detail", err_detail)

            except requests.exceptions.JSONDecodeError:
                LOG.debug("We could not decode the JSON error message")

            if self.using_api_key and r.status_code == 403:
                err_msg = f"This API Key does not have the correct permissions.\nERROR: {err_detail}\n{str(err)}"
                raise SurcomSDKException(err_msg)

            if err_detail:
                sdk_helpers.print_log_msg(err_detail, log_level=logging.ERROR)

                # No need to show the Python traceback if we get a valid
                # error message from the server
                sys.tracebacklimit = 0

            if trace_id:
                sdk_helpers.print_log_msg(f"X-Noetic-Trace-Id: {trace_id}", log_level=logging.ERROR)

            raise err

        try:
            rtn_value = r.json()
        except requests.exceptions.JSONDecodeError:
            LOG.debug(f"We failed to get json from the response: {str(r)}")
            rtn_value = r.text

        return rtn_value

    @staticmethod
    def _filter_type_attributes(
        type_content: dict,
        attributes_to_remove: list = constants.TYPE_ATTRIBUTES_TO_REMOVE
    ) -> dict:
        """
        Remove attributes from a type content dict

        :param type_content: the content of the type to filter
        :type type_content: dict
        :param attributes_to_remove: list of attributes to remove from the type content
        :type attributes_to_remove: list
        :return: the filtered type content
        :rtype: dict
        """
        for attr in attributes_to_remove:
            if attr in type_content:
                LOG.debug(f"Removing attribute '{attr}' from type")
                type_content.pop(attr)

        return type_content

    # --- IMPORT METHODS --- #

    def import_batch_create(
        self,
        import_id: str,
        execution_id: str = None
    ) -> str:
        """
        Create a batch for an import in Surface Command

        :param import_id: the id of the import
        :type import_id: str
        :param execution_id: an optional execution_id to give the workflow that
            invokes the batch, defaults to None
        :type execution_id: str, optional
        :return: the id of the created batch
        :rtype: str
        """
        params = None

        if execution_id:
            params = {"execution_id": execution_id}

        r = self._request(
            method="POST",
            url=f"graph-api/batch/{import_id}",
            params=params
        )

        batch_id = r.get("items", [])[0].get("content", {}).get("id")

        return batch_id

    def import_batch_add_data(
        self,
        import_id: str,
        batch_id: str,
        data: dict
    ) -> str:

        params = {
            "import_id": import_id,
            "batch_id": batch_id
        }

        r = self._request(
            method="POST",
            url="graph-api/objects",
            params=params,
            json=data
        )

        return r

    def import_batch_finalize(
        self,
        import_id: str,
        batch_id: str
    ):
        """
        Finalize an import batch in Surface Command

        :param import_id: the id of the import
        :type import_id: str
        :param batch_id: the id of the batch to finalize
        :type batch_id: str
        """
        r = self._request(
            method="POST",
            url=f"graph-api/batch/{import_id}/{batch_id}"
        )

        return r

    # --- TYPE METHODS --- #

    def types_get(
        self,
        type_name: str,
        params: dict = None
    ) -> dict:
        """
        Get a type in Surface Command

        :param type_name: the name of the type to get (this is the type_id)
        :type type_name: str
        """

        try:
            r = self._request(
                method="GET",
                url=f"schema-api/types/{type_name}",
                params=params
            )
        except SurcomSDKException as err:
            if "not found" in str(err):
                return None

            raise err

        return r

    def types_create(
        self,
        content: dict
    ):
        """
        Create a type in Surface Command

        :param content: the content of the type to create
        :type content: dict
        """
        type_name = content.get(constants.X_SAMOS_TYPE_NAME)
        type_to_upload = {type_name: content}

        if not type_name:
            raise SurcomSDKException(
                f"Type name is required. Nothing found for key '{constants.X_SAMOS_TYPE_NAME}'",
            )

        r = self._request(
            method="POST",
            url="schema-api/types",
            json=type_to_upload
        )

        return r

    def types_get_core_and_unified_types(
        self
    ) -> Tuple[dict, dict]:
        """
        Get all Core and Unified (abstract) types in Surface Command
        from Noetic Builtins

        Also get the core.named-object type

        :return: a tuple with two dicts, the first with the Core types,
            the second with the Unified types
        :rtype: Tuple[dict, dict]
        """

        noetic_builtin_types = {}
        core_types = {}

        result = self.run_cypher_query(
            cypher="""
                MATCH (i:`sys.apps.integration`) --> (t:`sys.type`)
                WHERE i.id = "noetic.builtins.app"
                    AND NOT t.`x-samos-type-name` CONTAINS "sys."
                    AND t.`x-samos-abstract` = true
                return t
            """
        )

        items = result.get("items", [])

        if not items:
            raise SurcomSDKException("No items found when querying for noetic builtin types")

        for i in items:
            type_content = i.get("content", {})
            type_name = type_content.get("x-samos-type-name", "")

            if type_content.get("deprecated", False):
                LOG.debug(f"Ignoring deprecated type '{type_name}'")
                continue

            LOG.debug(f"Found noetic builtin type: '{type_name}'")

            type_content = self._filter_type_attributes(type_content)

            if type_name.startswith("core."):
                core_types[type_name] = type_content

            else:
                noetic_builtin_types[type_name] = type_content

        # NOTE: core.named-object is not part of Noetic Builtins, so we have to query it separately
        core_named_object_type = self.run_cypher_query(
            cypher="""
            MATCH (t:`sys.type`)
            WHERE t.`x-samos-type-name` = "core.named-object"
            RETURN t
            """
        )

        items = core_named_object_type.get("items", [])

        if not items:
            raise SurcomSDKException("No items found when querying for core.named-object type")

        for i in items:
            type_content = i.get("content", {})
            type_name = type_content.get("x-samos-type-name", "")

            LOG.debug(f"Found core type: '{type_name}'")

            type_content = self._filter_type_attributes(type_content)

            core_types[type_name] = type_content

        return core_types, noetic_builtin_types

    def types_get_source_types(
        self
    ) -> dict:
        """
        First get a list of all installed Connectors in Surface Command,
        then for each Connector get all Source types it provides

        :return: a dict with all Source types in Surface Command
        :rtype: dict
        """
        source_types = {}

        installed_apps = self.app_get_installed()

        for app_id in installed_apps.keys():

            LOG.debug(f"Getting source types for Connector '{app_id}'")

            if app_id.startswith("noetic") or app_id.startswith("rapid7"):
                LOG.debug(f"Skipping Connector '{app_id}' as it is a system Connector")
                continue

            result = self.run_cypher_query(
                cypher=f"""
                    MATCH (i:`sys.apps.integration`) --> (t:`sys.type`)
                    WHERE i.id = "{app_id}"
                    return t
                """
            )

            items = result.get("items", [])

            if not items:
                LOG.debug(f"No source types found for Connector '{app_id}'")
                continue

            for i in items:
                type_content = i.get("content", {})
                type_name = type_content.get("x-samos-type-name", "")

                if type_content.get("deprecated", False):
                    LOG.debug(f"Ignoring deprecated type '{type_name}'")
                    continue

                LOG.debug(f"Found source type: '{type_name}'")

                type_content = self._filter_type_attributes(type_content)

                source_types[type_name] = type_content

        return source_types

    # --- APP METHODS --- #

    def app_status(
        self,
        connector_id: str
    ) -> dict:
        """
        Get the status of an app (Connector) in Surface Command

        :param connector_id: the id of the app to get the status of
        :type connector_id: str
        :return: the status of the app
        :rtype: dict
        """

        if not connector_id:
            raise SurcomSDKException(
                "'connector_id' is required to get the status of an Connector"
            )

        r = self._request(
            method="GET",
            url="apps-api/apps/info/status",
            params={"integration_ids": connector_id}
        )

        err_msg = f"Failed to get the status for Connector '{connector_id}'. Response: {str(r)}"

        if not isinstance(r, list):
            LOG.debug("The response is not a list, we cannot get the status")
            raise SurcomSDKException(err_msg)

        if len(r) >= 1:

            statuses = r[0].get("statuses", [])

            if statuses and isinstance(statuses, list) and len(statuses) == 1:
                return statuses[0]

        raise SurcomSDKException(err_msg)

    def app_get_installed(
        self
    ) -> dict:
        """
        Get all installed Connectors in Surface Command

        :return: the list of installed Connectors
        :rtype: dict
        """

        r = self._request(
            method="GET",
            url="apps-api/apps"
        )

        return r

    def app_install_from_zip(
        self,
        connector_id: str = "",
        connector_version: str = "",
        path_connector_zip: str = "",
        load_sample_data: bool = False
    ) -> dict:
        """
        Install a Connector in Surface Command

        :param connector_id: the ID of the Connector to try install from S3
        :type connector_id: str
        :param connector_version: the version of the Connector to try install from S3
        :type connector_version: str
        :param path_connector_zip: the path to the Connector zip file to install
        :type path_connector_zip: str
        :param load_sample_data: if True, set the `load_sample_data` parameter. Defaults to False
        :type load_sample_data: bool
        :return: the response from a POST to the apps-api/apps endpoint
        :rtype: dict
        """

        # NOTE: we only support async installs
        params = {
            "async_install": True
        }

        if load_sample_data:
            LOG.debug("Setting the `load_sample_data` parameter")
            params["load_sample_data"] = True

        # If a connector_id is provided, we add the `integration_id` and `version` parameters
        if connector_id:

            # If a connector_id is provided, other parameters cannot be set
            if path_connector_zip or load_sample_data:
                raise SurcomSDKException("If you specify a connector_id you "
                                         f"cannot set the `{constants.ARG_SAMPLE_DATA}` or `{constants.ARG_ZIP}` flags")

            LOG.debug(f"The connector_id '{connector_id}' was specified. Adding the 'integration_id' parameter")
            params["integration_id"] = connector_id

            if connector_version:
                LOG.debug(f"'v{connector_version}' was specified. Adding the 'version' parameter")
                params["version"] = connector_version

            r = self._request(
                method="POST",
                url="apps-api/apps",
                params=params,
                timeout=sdk_config.get_config(
                    option=constants.CONFIG_NAME_TIMEOUT_INSTALL_CONNECTOR,
                    option_type="int",
                    default=600
                )
            )

        # Else if its a zip, read the contents and set the `body`
        elif path_connector_zip:

            if not zipfile.is_zipfile(path_connector_zip):
                raise SurcomSDKException(f"'{path_connector_zip}' is not a valid zip file")

            headers = {
                "Content-Type": "application/octet-stream"
            }

            LOG.debug(f"Attempting to install the Connector from '{path_connector_zip}'")

            with open(path_connector_zip, "rb") as fp:

                r = self._request(
                    method="POST",
                    url="apps-api/apps",
                    headers=headers,
                    params=params,
                    data=fp,
                    timeout=sdk_config.get_config(
                        option=constants.CONFIG_NAME_TIMEOUT_INSTALL_CONNECTOR,
                        option_type="int",
                        default=600
                    )
                )

        else:
            raise SurcomSDKException("You must provide either a path to a connector zip or a valid connector id")

        return r

    # --- WORKFLOW METHODS --- #

    def print_workflow_logs(
        self,
        execution_id: str,
        only_user_msgs: bool = False
    ) -> bool:
        """
        Print the logs for the workflow with the given Execution ID

        If there is an error or an exception log we return False, True otherwise

        :param execution_id: Execution ID of the Workflow
        :type execution_id: str
        :param only_user_msgs: If True, only gets the User logs, defaults to False
        :type only_user_msgs: bool, optional
        :return: False if there is an error or exception log, True otherwise
        :rtype: bool
        """
        # TODO: add test

        size = 100
        offset = 0
        more_logs = True
        response = None
        all_logs = []
        no_error = True

        while more_logs:

            # Wait a while (logs may arrive after the workflow stops!)
            time.sleep(2.0)

            response = self._request(
                method="GET",
                url=f"workflow-api/executions/{execution_id}"
            )

            # If the workflow is still running, do not flip more_logs
            if response not in constants.WF_RUNNING_STATES:
                more_logs = False

            # If the workflow is in a failed state, print the error message and return
            if response == "error":
                response = self._request(
                    method="GET",
                    url=f"workflow-api/executions/{execution_id}/incidents",
                )
                error = response.get("error_message", {}).get("message", "Unknown error")
                err_msg = f"{fmt('WORKFLOW FAILED:', c=colors.RED, f=formats.BOLD)}"
                sdk_helpers.print_log_msg(f"{err_msg}\n{error}")
                return False

            params = {
                "only_user_msgs": only_user_msgs,
                "size": size,
                "offset": offset
            }

            response = self._request(
                method="GET",
                url=f"workflow-api/executions/{execution_id}/logs",
                params=params
            )

            logs = []

            if not response:
                LOG.debug("No logs found in the response.")

            elif isinstance(response, list):
                for item in response:
                    logs.append({
                        "@timestamp": item["content"].get("@timestamp"),
                        "levelname": item["content"].get("levelname"),
                        "workflow": item["content"].get("samos", {}).get("workflow_id"),
                        "function": item["content"].get("samos", {}).get("function"),
                        "message": item["content"].get("message"),
                        "exception": item["content"].get("exception")
                    })

            else:
                LOG.debug("Logs did not return in structured form.")

            if logs:

                for log in logs:
                    log_msg = f"[{log['@timestamp']}] {log['message']}"

                    if log.get("exception"):
                        log_msg = f"{log_msg}\n{fmt('ERROR', c=colors.RED, f=formats.BOLD)}: {log['exception']}"
                        no_error = False

                    sdk_helpers.print_log_msg(log_msg)

            all_logs.extend(logs)
            offset = offset + len(response)

        return no_error

    # --- GRAPH METHODS --- #

    def run_cypher_query(
        self,
        cypher: str,
        length: int = 500,
    ) -> dict:
        """
        Run a cypher query in Surface Command

        :param cypher: the cypher query to run
        :type cypher: str
        :param length: the maximum number of results to return, defaults to 500
        :type length: int, optional
        :return: the results of the cypher query
        :rtype: dict
        """

        # Remove extra whitespace and new lines
        sanitized_cypher = ' '.join(cypher.split())

        LOG.debug(f"Running cypher query: '{sanitized_cypher}'")

        params = {
            "length": length,
            "depth": 0,
        }

        data = {
            "cypher": sanitized_cypher,
        }

        r = self._request(
            method="POST",
            url="graph-api/objects/cypher",
            json=data,
            params=params
        )

        return r

    # --- DATA METHODS --- #

    def get_correlation_keys(
        self
    ) -> list:
        """
        Get all correlation keys in Surface Command

        :return: list of correlation keys
        :rtype: list
        """

        result = self.run_cypher_query(
            cypher="MATCH (k:`sys.correlation-key`) RETURN k"
        )

        items = result.get("items", [])

        if not items:
            raise SurcomSDKException("No items found when querying for correlation keys")

        correlation_keys = []

        for i in items:
            key_content = i.get("content", {})
            key_name = key_content.get("name", "")

            LOG.debug(f"Found correlation key: '{key_name}'")
            correlation_keys.append(key_content)

        return correlation_keys
