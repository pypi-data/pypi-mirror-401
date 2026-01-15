from dataclasses import asdict

from looqbox.flows.steps.step import Step
from looqbox.global_calling import GlobalCalling
from looqbox.objects.container.response_vars import FeatureFlags
from looqbox.objects.message.message import Message
from looqbox.objects.message.message_keys import MessageKeys

global_variables = GlobalCalling().looq


class DefineGlobalVariablesStep(Step):
    def __init__(self, message: Message):
        super().__init__(message)
        self.script_info = message.get(MessageKeys.SCRIPT_INFO)
        self.response_parameters = message.get(MessageKeys.RESPONSE_PARAMETERS)

    def execute(self):
        self.set_response_vars_to_global_variables()
        self.set_question_params_to_global_variables()

    def set_response_vars_to_global_variables(self):
        response_vars = asdict(self.script_info.response_vars)
        for key, value in response_vars.items():
            setattr(global_variables, key, getattr(self.script_info.response_vars,key))
        setattr(global_variables, "version", self.script_info.version)
        if global_variables.feature_flags is None:
            global_variables.feature_flags = FeatureFlags({"file_sync": 15})

    def set_question_params_to_global_variables(self):
        question = str(self.response_parameters.question)
        company_id = self.response_parameters.company_id
        self.set_global_variable("question", question)
        self.set_global_variable("company_id", company_id)

    @staticmethod
    def set_global_variable(key: str, value: any):
        setattr(global_variables, key, value)


