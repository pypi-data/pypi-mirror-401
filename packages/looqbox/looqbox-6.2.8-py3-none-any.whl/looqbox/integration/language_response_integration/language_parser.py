from datetime import datetime

from multimethod import multimethod

from looqbox.config.logger import PythonPackageLogger
from looqbox.global_calling import GlobalCalling
from looqbox.objects.nodes.node import Node
from looqbox.objects.nodes.node_type import NodeType
from looqbox.objects.response_parameters.condition.comparative.comparison_node import ComparisonNode
from looqbox.objects.response_parameters.condition.comparative.temporal_statements_to_compare_node import \
    TemporalStatementsToCompareNode
from looqbox.objects.response_parameters.condition.condition import Condition
from looqbox.objects.response_parameters.group_by.group_by import GroupBy
from looqbox.objects.response_parameters.keyword.keyword import Keyword
from looqbox.utils.dot_notation import Functional
from looqbox.utils.utils import as_dict_ignore_nones


class LanguageParser:
    """
    Interface to parse and to retrieve parameteres from Looqbox's NPl object

    This class aim to serve as a middle-ground for the user and the NLP objects, hence providing methods and tools
    to search and to get entities, partitions and keywords (to name a few) from a more complex object.

    Attributes:
    language_content (dict): Looqbox's Language (NLP) object.

    Examples:
    >>> language_content = LanguageParser(par)
    >>> entity = language_content.get_entity_filter("$date",
    ...                                             entity_default=[["2023-01-01", 2023-12-31]])
    """

    def __init__(self):

        self.response_filters = GlobalCalling.looq.response_filters or dict()
        self.response_keywords = GlobalCalling.looq.response_keywords or dict()
        self.response_groupings = GlobalCalling.looq.response_partitions or dict()
        self.response_parameters = GlobalCalling.looq.response_parameters or dict()
        self.syntax_tree = GlobalCalling.looq.syntax_tree or None
        self.logger = PythonPackageLogger().get_logger()

    def get_entity_filter(self, entity_name: str, default_value: any = None) -> Condition:

        """
        Method to get an entity value from Looqbox's NPL object.
        
        Args:
        entity_name (str): The entity name, usually beginning with the "$" symbol
        default_value (dict|list[list[any]], optional): The value that will be used if the NPL does not contain
         the entity searched for, usually, this value will be a list or a None value, .e.g [[1, 2]].
        
        Returns: 
        Entity: This method returns the asked entity properties and its values in form of an Entity class instance
        
        Example:
        to get a state from the NLP parser:
       >>> asked_state = LanguageParser.get_entity_filter("$state", entity_default_value = [["NY", "CA"]])
        """
        return self.response_filters.get(entity_name, default_value)

    def get_partitions_filter(self, partition_name, default_value=None) -> GroupBy:

        """
        Method to get a partiton value from Looqbox's NPL object.

        Args:
        partition_name (str): The partition name, usually beginning with the "$" symbol
        partition_default_value (dict|list[str], optional): The value that will be used if the NPL does not contain the
         partition searched for, usually, this value will be a list or a None value, .e.g ["by day"].

        Returns:
        Grouping: This method returns the asked partition properties and its values in form of a Grouping class instance

        Example:
        to get a state from the NLP parser:
        >>> date_aggregation = LanguageParser.get_partitions_filter("date", entity_default_value = ["by week"])
        """

        return self.response_groupings.get(partition_name, default_value)

    @multimethod
    def get_asked_keywords(self, keyword: str, default_value=None) -> Keyword:

        """
        Method to get a keyword value from Looqbox's NPL object.

        Args:
        keyword (str or int): The keyword name or id
        keyword_default_value (dict|list[str], optional): The value that will be used if the NPL does not contain the
         keyword searched for, usually, this value will be a list or a None value, .e.g ["campanha"].

        Returns:
        Keyword: This method returns the asked keyword properties and its values in form of a Keyword class instance

        Example:
        to get a state from the NLP parser:
        >>> keyword_asked = LanguageParser.get_asked_keywords("loja", keyword_default_value = ["estabelecimento"])
        """

        return self.response_keywords.get(keyword, default_value)

    @multimethod
    def get_asked_keywords(self, keyword: int, default_value=None) -> Keyword:
        return (
                Functional(self.response_keywords)
                .map(lambda keyword_name, value: value)
                .first(lambda keyword_obj: keyword_obj.metadata.entity.id == keyword)
                or default_value
        )

    def get_comparative_nodes(self, only_value=False, as_token=False, as_dict=True):
        if not self.syntax_tree:
            self.logger.error("No syntax tree found")
            return None
        nodes = self.syntax_tree.recursively_get_self_and_children_nodes()
        comparative_nodes = Functional(nodes).filter_not_none_to_list(lambda it: isinstance(it, ComparisonNode))
        if not comparative_nodes:
            # THIS DOES NOT SUPPORT MULTIPLE COMPARISONS
            def filter_query_comparison_nodes(node_list: list[Node]) -> list[Node]:

                # Filter to find only QueryComparisonNodes
                query_comparison_nodes = [n for n in node_list if n.node_type == NodeType.QUERY_COMPARISON]

                query_arguments_to_map_nodes = []

                # For each QueryComparisonNode, obtain descendants that are of type QUERY_ARGUMENTS_TO_MAP
                for qc_node in query_comparison_nodes:
                    if hasattr(qc_node, "content") and qc_node.content:
                        for child in qc_node.content:
                            if isinstance(child, Node):
                                query_arguments_to_map_nodes.extend(
                                    [descendant for descendant in child.recursively_get_self_and_children_nodes()
                                     if descendant.node_type == NodeType.QUERY_ARGUMENTS_TO_MAP]
                                )

                return query_arguments_to_map_nodes

            segments_to_compare = (
                Functional(filter_query_comparison_nodes(nodes))
                .map_to_list(lambda it: it.text)
            )

            statements_to_compare = (
                Functional(self.response_parameters.conditions)
                .filter_to_list(lambda it: it.text in segments_to_compare)
            )

            comparative_entities = Functional(statements_to_compare).map_to_list(lambda it: it.parameter_name)
            if self._has_date_and_datetime(comparative_entities):
                # If both $date and $datetime are present, change $datetime to $date
                datetime_node = Functional(statements_to_compare).first(lambda it: it.parameter_name == "$datetime")
                datetime_node.parameter_name = "$date"

            if self._is_comparative(segments_to_compare, statements_to_compare):
                return None

            comparative_node = TemporalStatementsToCompareNode()
            comparative_node.text = " vs ".join(segments_to_compare)
            comparative_node.content = statements_to_compare
            comparative_nodes = [comparative_node]

        def extract_start_date(temporal_relation):
            dates = (
                Functional(temporal_relation.relations)
                .flat_map(lambda lst: lst)
                .filter(lambda rel_value: rel_value._operator in ('GREATER_THAN_EQUAL', 'GREATER_THAN'))
                .map(lambda rel_value: datetime.strptime(rel_value.value.date, "%Y-%m-%d"))
                .to_list()
            )
            if dates:
                return min(dates)
            else:
                return datetime.max

        # Sort the content for each TemporalStatementsToCompareNode
        for node in comparative_nodes:
            if not isinstance(node, TemporalStatementsToCompareNode):
                continue
            node.content = (
                Functional(node.content)
                .sort_by(extract_start_date)
                .to_list()
            )

        tokens = Functional(comparative_nodes).map_not_none_to_list(lambda it: it.to_token())
        if not comparative_nodes:
            return None
        if only_value:
            return Functional(comparative_nodes).map_not_none_to_list(lambda it: it.values)
        if as_token:
            return tokens
        if as_dict:
            return (
                Functional(tokens)
                .map_not_none(lambda it: as_dict_ignore_nones(it)).to_list()
            )
        return comparative_nodes

    def _has_date_and_datetime(self, comparative_entities):
        return "$date" in comparative_entities and "$datetime" in comparative_entities

    @staticmethod
    def _is_comparative(segments_to_compare, statements_to_compare):
        is_empty = not segments_to_compare and not statements_to_compare
        has_same_length = len(segments_to_compare) == len(statements_to_compare)
        is_greater_than_one = len(segments_to_compare) > 1
        return is_empty or not has_same_length or not is_greater_than_one
