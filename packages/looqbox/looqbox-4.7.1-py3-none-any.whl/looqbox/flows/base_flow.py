import json
import uuid
import os.path

from abc import abstractmethod
from typing import Any, Callable, Dict, List

from multimethod import multimethod

from looqbox.global_calling import GlobalCalling
from looqbox.utils.utils import _format_quotes, load_json_from_relative_path


class BaseFlow:
    def __init__(self, script_info: str):
        script_data = json.loads(script_info)
        self.input_json_file = script_data.get("responseParameters", {})
        self.script_file = script_data.get("vars", {}).get("response_path", "")
        self.output_json_file = script_data.get("resultPath", "")
        self.upload_file = script_data.get("UploadFile", "")
        self.vars = script_data.get("vars", {})
        self.data: Dict[str, Any] | str = {}
        self.global_variables = GlobalCalling().looq
        GlobalCalling().looq.session_id = uuid.uuid4()
        GlobalCalling().looq.query_list[GlobalCalling().looq.session_id] = []

    def read_response_parameters(self) -> None:
        raw_file = open(self.input_json_file, 'r', encoding='utf-8').read()
        self.data = _format_quotes(raw_file)
        self.data = json.loads(self.data)

    def response_enricher(self) -> None:
        self.data.update(self.vars)

    def define_global_variables(self) -> None:
        for key, value in self.vars.items():
            setattr(self.global_variables, key, value)
        self._update_response_packages_config()
        response_question = self.data.get("question", {})
        self.global_variables.question = self.get_question(response_question)

    def _update_response_packages_config(self) -> None:
        default_package_configuration = {
            "database_configuration": {
              "search_job_id_interval_time": 0.0005,
              "file_watcher_interval_time": 0.0005,
              "query_host": "http://localhost",
              "query_host_port": 8080,
              "query_endpoint": "query",
              "request_timeout": 2.5,
              "export_batch_size_limit": 100
            },
            "use_query_caller_as_default": False,
            "flow_settings": {
                "stacktrace_level": 0
            }
        }
        if self.global_variables.feature_flags is None:
            self.global_variables.feature_flags = {"response_package_configuration": default_package_configuration}
        else:
            complete_config = self._update_default_configuration_values(default_package_configuration)
            self.global_variables.feature_flags["response_package_configuration"] = complete_config
            del  self.global_variables.feature_flags["responsePackagesConfiguration"]

    def _update_default_configuration_values(self, default_package_configuration) -> dict:
        for configuration in default_package_configuration:
            if isinstance(default_package_configuration[configuration], dict):
                default_package_configuration[configuration] = self._iterate_over_config(configuration, default_package_configuration)

            elif self._is_config_set_in_feature_flags(configuration):
                self._replace_default_with_defined_value(configuration, default_package_configuration)

        return default_package_configuration

    def _iterate_over_config(self, configuration, default_package_configuration):
        return self._update_config_key_value(configuration, default_package_configuration[configuration])

    def _replace_default_with_defined_value(self, configuration, default_package_configuration) -> Any:
        default_package_configuration[configuration] = (self.global_variables.feature_flags
        .get("responsePackagesConfiguration")[configuration])

    def _is_config_set_in_feature_flags(self, configuration: str) -> bool:
        return configuration in self.global_variables.feature_flags.get("responsePackagesConfiguration")

    def _update_config_key_value(self, current_key: any, default_value: any):
        for configuration in default_value:
            if configuration in self.global_variables.feature_flags.get("responsePackagesConfiguration").get(current_key, []):
                default_value[configuration] = (self.global_variables.feature_flags
                                                        .get("responsePackagesConfiguration")[current_key][configuration])
        return default_value

    @multimethod
    def get_question(self, question: dict) -> dict:
        return question.get("clean", "")

    @multimethod
    def get_question(self, question: str) -> str:
        return question

    def response_writer(self) -> None:
        with open(self.output_json_file, 'w') as file:
            if isinstance(self.data, dict):
                self.data = json.dumps(self.data, ensure_ascii=False)
            file.write(self.data)
            file.close()

    def _set_stack_trace_level(self) -> None:

        import sys
        flow_settings_path = os.path.join(os.path.dirname(__file__), "..", "..",
                                          "configuration", "flow_settings.json")

        if self.global_variables.test_mode:
            flow_setting = load_json_from_relative_path(flow_settings_path)
            sys.tracebacklimit = flow_setting.stackTraceLevel
        else:
            sys.tracebacklimit = None

    @staticmethod
    def _remove_query_from_global_list() -> None:
        try:
            del GlobalCalling.looq.query_list[GlobalCalling.looq.session_id]
        except KeyError as error:
            print(KeyError("Could not find session id in queries list"))

    @staticmethod
    def run_steps(steps: List[Callable]) -> None:
        [step() for step in steps]

    @abstractmethod
    def run(self) -> None:
        ...
