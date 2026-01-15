import importlib.util

from looqbox.flows.steps.script_execution_step import ScriptExecution
from looqbox.integration.integration_links import _response_json
from looqbox.objects.message.message import Message


class ExecuteScriptStep(ScriptExecution):
    def __init__(self, message: Message):
        super().__init__(message)

    def _load_and_exec_module(self):
        spec = importlib.util.spec_from_file_location(
            "executed_script",
            self.script_info.response_vars.response_path
        )
        script_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script_module)  # This publishes to the interface
        try:
            response = _response_json(self.response_parameters, script_module.looq_response, raw_json_content=self.json_raw_parameters)
            return response
        except Exception as error:
            self._remove_query_from_global_list()
            raise Exception from error
