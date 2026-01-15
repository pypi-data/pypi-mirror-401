from abc import abstractmethod

from looqbox.config.logger import PythonPackageLogger
from looqbox.flows.steps.step import Step
from looqbox.objects.message.message import Message
from looqbox.objects.message.message_keys import MessageKeys


# noinspection PyArgumentList
class AbstractResponseParametersLoader(Step):

    def __init__(self, message: Message):
        super().__init__(message)
        self.script_info = message.get(MessageKeys.SCRIPT_INFO)
        self.logger = PythonPackageLogger().get_logger()

    def execute(self):
        self.message.offer(
            (MessageKeys.RESPONSE_PARAMETERS, self._load_response_parameters())
        )

    @abstractmethod
    def _load_response_parameters(self):
        ...
