from typing import Optional

from pydantic.dataclasses import dataclass

from looqbox.config.pydantic_configuration import PydanticConfiguration


@dataclass(config=PydanticConfiguration.Config)
class QueryServiceConfiguration:
    """
    This class hold configuration for the query feature of the Looqbox's response package. The main properties os this
    class are:
    - search_job_id_interval_time (float): interval time in seconds between checks for status job (BigQuery only)
    - file_watcher_interval_time (float): interval time in seconds between checks for existence of
                                          result file (JDBC only)
    - query_host (str): base host for QueryExecutor service (JDBC only)
    - query_host_port (int): port for QueryExecutor service (JDBC only)
    - query_endpoint (str): endpoint used to send a query request to Query Executor service (JDBC only)
    - request_timeout (float): time limit, in seconds, to perform an HTTP request
    - export_batch_size_limit (int): Number of rows to be exported to file per step
    """

    search_job_id_interval_time: Optional[float] = 0.0005
    file_watcher_interval_time:Optional[float] = 0.0005
    query_host: Optional[str] = "http://localhost"
    query_host_port:Optional[int] = 8080
    query_endpoint:Optional[str]  = "query"
    request_timeout:Optional[float] = 2.5
    export_batch_size_limit:Optional[int]  = 100
