from looqbox.flows.steps.step import Step
from looqbox.global_calling import GlobalCalling


class RemoveQueryFromGlobalListStep(Step):
    def execute(self):
        try:
            GlobalCalling.looq.clear_session_query_list()
        except KeyError as error:
            print(KeyError(f"Could not find session id in queries list: {error}"))
