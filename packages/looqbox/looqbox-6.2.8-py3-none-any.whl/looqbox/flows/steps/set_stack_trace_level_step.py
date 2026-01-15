import os
import sys
from looqbox.configuration.popo.flow_settings import FlowSettings
from looqbox.flows.steps.step import Step
from looqbox.global_calling import GlobalCalling
from looqbox.utils.utils import load_json_from_path
from looqbox.config.object_mapper import ObjectMapper

global_variables = GlobalCalling.looq


class SetStackTraceLevelStep(Step):
    def execute(self):
        self._get_flow_settings()
        self._set_stacktrace_level()

    def _get_flow_settings(self):
        self._flow_settings = GlobalCalling.looq.feature_flags.response_packages_configuration.flow_settings

    def _get_stacktrace_level(self):
        try:
            self._get_flow_settings()
            return self._flow_settings.stacktrace_level
        except:
            flow_settings_path = os.path.join(
                os.path.dirname(__file__),
                "..", "..",
                "resources", "flow_setting.json")
            return load_json_from_path(flow_settings_path).get("stackTraceLevel", 0)

    def _set_stacktrace_level(self):

        if not global_variables.test_mode:
            sys.tracebacklimit = self._get_stacktrace_level()
        else:
            sys.tracebacklimit = None