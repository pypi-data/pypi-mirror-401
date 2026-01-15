from looqbox_commons.src.main.logger.logger_interface import LoggerInterface
from looqbox_commons.src.main.logger.logger import RootLogger
from looqbox.global_calling import GlobalCalling

class PythonPackageLogger(LoggerInterface):
    should_use_log_file = False if GlobalCalling.looq.test_mode else True
    logger = RootLogger().get_new_logger("python_package", use_file_handler=should_use_log_file)

    def get_logger(self):
        return self.logger


class ResponseLogger(LoggerInterface):
    should_use_log_file = False if GlobalCalling.looq.test_mode else True
    logger = RootLogger().get_new_logger("response", use_file_handler=should_use_log_file)
    
    def _get_logger(self):
        return self.logger

    @property
    def __call__(self):
        return self._get_logger()
