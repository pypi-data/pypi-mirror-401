import importlib.util

from looqbox.flows.steps.script_execution_step import ScriptExecution
from looqbox.integration.integration_links import _response_json_form
from looqbox.objects.message.message import Message


class ExecuteFormScriptStep(ScriptExecution):
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
            if not self.script_info.upload_file:
                # TODO Fix the session_data arg
                # Given that the current FES version does not send the previous json (the one created with the
                # Language-Service) this values is set as a empty dict temporary
                return _response_json_form(self.response_parameters.form_parameters, dict(), script_module.looq_response)
            return _response_json_form(self.script_info.upload_file,self.response_parameters, script_module.looq_response)

        except Exception as error:
            self._remove_query_from_global_list()
            raise Exception from error
