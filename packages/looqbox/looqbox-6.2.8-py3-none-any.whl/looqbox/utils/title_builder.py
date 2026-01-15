import re

from multimethod import multimethod

from looqbox import title_with_date
from looqbox.integration.integration_links import map_to_response_parameters
from looqbox.objects.response_parameters.condition.set_relation import SetRelation
from looqbox.objects.response_parameters.condition.temporal_relation import TemporalRelation
from looqbox.objects.response_parameters.response_parameters import ResponseParameters

__all__ = ["TitleBuilder"]

class TitleBuilder:
    response_parameter: ResponseParameters = None
    root_title: str = ""
    group_aggregation:str = None
    temporal_filter: str = None
    non_temporal_filter: str = None

    @multimethod
    def __init__(self, response_parameters: ResponseParameters, root_title: str=""):
        '''
        Class used to create titles based on values passed by the response parameter

        Args:
            response_parameters(ResponseParameters): response parameter retrieved from language service
            root_title response_parameters(str, optional): text that will be placed in the beginning of title string
        '''

        self.response_parameter = response_parameters
        self.root_title = root_title

    @multimethod
    def __init__(self, response_parameters: dict, root_title: str=""):
        '''
        Args:
            response_parameters(str): response parameter retrieved from language service
            root_title response_parameters(str, optional): text that will be placed in the beginning of title string
        '''
        self.response_parameter = map_to_response_parameters(response_parameters)
        self.root_title = root_title

    def build(self) -> str:
        '''
        Returns:
        str: string based on filters passed from ResponseParameter
        '''
        title_from_non_temporal_entity = self.non_temporal_filter if self.non_temporal_filter is not None else self.build_non_temporal_entity_filter_line()
        title_from_temporal_entity = self.temporal_filter if self.temporal_filter is not None else self.build_temporal_entity_filter_line()
        title_from_group = self.group_aggregation if self.group_aggregation is not None else self.build_group_line()
        return f"{self.root_title} {title_from_group}{title_from_temporal_entity}\n{title_from_non_temporal_entity}"

    def build_group_line(self) -> str:
        groups = [self.response_parameter.group_by.get(item) for item in self.response_parameter.group_by]
        return " ".join(group.text for group in groups)

    def build_temporal_entity_filter_line(self) -> str:
        dates = [date_entity for date_entity in self.response_parameter.conditions if date_entity is not None and isinstance(date_entity, TemporalRelation)]
        if len(dates) == 0:
            return ""
        date_as_str = []
        for date in dates:
            date_as_str.extend(date.date_str_by_granularity)
        return "\n" + title_with_date(header="", date_int=date_as_str[0])

    def build_non_temporal_entity_filter_line(self) -> str:
        entities = [non_temporal_entity for non_temporal_entity in self.response_parameter.conditions if non_temporal_entity is not None and isinstance(non_temporal_entity, SetRelation)]
        if len(entities) == 0:
            return ""
        return "\n".join(f"{self._remove_diamond_from_entity(entity.text.title())}: {", ".join(str(value.name) for value in entity.relations[0].values)}" for entity in entities)

    def _remove_diamond_from_entity(self, entity_text:str):
        diamond_pattern = r'\[[^\]]*\]'
        text_without_diamond = re.sub(diamond_pattern, "", entity_text)
        return self._get_phrase_with_unique_words_from_title(text_without_diamond)

    @staticmethod
    def _get_phrase_with_unique_words_from_title(text_without_diamond):
        return ' '.join(dict.fromkeys(text_without_diamond.strip().split(" ")))

    def set_group(self, group_value:str):
        self.group_aggregation = group_value

    def set_temporal_filter(self, temporal_filter:str):
        self.temporal_filter = temporal_filter

    def set_non_temporal_filter(self, non_temporal_filter:str):
        self.non_temporal_filter = non_temporal_filter
