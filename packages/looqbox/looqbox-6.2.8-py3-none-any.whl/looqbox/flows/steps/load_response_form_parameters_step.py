import json

from looqbox.config.logger import PythonPackageLogger
from looqbox.config.object_mapper import ObjectMapper
from looqbox.flows.steps.abstract_response_parameters_loader import AbstractResponseParametersLoader
from looqbox.flows.steps.step import Step
from looqbox.objects.message.message import Message
from looqbox.objects.message.message_keys import MessageKeys
from looqbox.objects.response_parameters.response_parameters import ResponseParameters
from looqbox.objects.response_parameters.response_user import ResponseUser


# noinspection PyArgumentList
class LoadResponseFormParametersStep(AbstractResponseParametersLoader):

    def _load_response_parameters(self):
        with open(self.script_info.response_parameters_path, "r") as response_file:
            try:
                response_file_dict = json.load(response_file)
                self.response_parameters =  ResponseParameters(
                    question="",
                    user=ResponseUser(id=1, login="", group_id=1),
                    company_id=1
                )
                self.response_parameters.form_parameters = response_file_dict
            except Exception as e:
                self.logger.error(f"Error when mapping response parameters: {e}. \nUsing mocked version.")
                self.response_parameters = ResponseParameters(
                    question="mocked question",
                    user=ResponseUser(id=1, login="mocked login", group_id=1),
                    company_id=1
                )
            response_file.close()
        self.response_parameters.response_vars = self.script_info.response_vars
        return self.response_parameters
