import json
from abc import abstractmethod

from looqbox.config.logger import PythonPackageLogger
from looqbox.flows.steps.step import Step
from looqbox.global_calling import GlobalCalling
from looqbox.objects.message.message import Message
from looqbox.objects.message.message_keys import MessageKeys


class ScriptExecution(Step):
    def __init__(self, message: Message):
        super().__init__(message)
        self.script_info = message.get(MessageKeys.SCRIPT_INFO)
        self.logger = PythonPackageLogger().get_logger()
        self.response_parameters = message.get(MessageKeys.RESPONSE_PARAMETERS)
        self.json_raw_parameters = self._get_json_response_parameter_content()

    def _get_json_response_parameter_content(self):
        try:
            with open(self.script_info.response_parameters_path, "r") as response_file:
                response_file_dict = json.load(response_file)
                response_file.close()
        except Exception as e:
                self.logger.error(f"Error when reading response parameters: {e}.")
        return response_file_dict

    def execute(self):
        response = self._load_and_exec_module()
        self.message.offer((
            MessageKeys.RESPONSE, response
        ))

    @abstractmethod
    def _load_and_exec_module(self):
        ...

    @staticmethod
    def _remove_query_from_global_list() -> None:
        try:
            GlobalCalling.looq.clear_session_query_list()
        except KeyError as error:
            print(KeyError(f"Could not find session id in queries list: {error}"))
