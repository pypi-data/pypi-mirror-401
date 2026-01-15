from looqbox.flows.base_flow import BaseFlow
from looqbox.flows.steps.define_global_variables_step import DefineGlobalVariablesStep
from looqbox.flows.steps.execute_form_script import ExecuteFormScriptStep
from looqbox.flows.steps.load_response_form_parameters_step import LoadResponseFormParametersStep
from looqbox.flows.steps.remove_query_from_global_list_step import RemoveQueryFromGlobalListStep
from looqbox.flows.steps.response_writer_step import ResponseWriterStep
from looqbox.flows.steps.set_natural_language_parameter_step import SetNaturalLanguageParameterStep


class ScriptResponseFormFlow(BaseFlow):

    def define_steps(self):
        self.steps = [
            LoadResponseFormParametersStep,
            DefineGlobalVariablesStep,
            SetNaturalLanguageParameterStep,
            ExecuteFormScriptStep,
            RemoveQueryFromGlobalListStep,
            ResponseWriterStep
        ]
