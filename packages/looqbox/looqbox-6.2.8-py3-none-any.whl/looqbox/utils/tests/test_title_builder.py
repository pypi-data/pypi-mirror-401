import os
import unittest

from looqbox import load_json_from_path
from looqbox.integration.integration_links import map_to_response_parameters
from looqbox.objects.response_parameters.response_parameters import ResponseParameters
from looqbox.utils.title_builder import TitleBuilder


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.response_parameter_simple:ResponseParameters = map_to_response_parameters(
            load_json_from_path(os.path.join(os.path.dirname(__file__), "resources", "response_parameter_simple.json"))
        )

        self.response_parameter_two_filters:ResponseParameters = map_to_response_parameters(
            load_json_from_path(os.path.join(os.path.dirname(__file__), "resources", "response_parameter_with_two_filters.json"))
        )

        self.response_parameter_composed_entity_name:ResponseParameters = map_to_response_parameters(
            load_json_from_path(os.path.join(os.path.dirname(__file__), "resources", "response_parameter_with_compose_entity_name.json"))
        )

        self.response_parameter_as_json = load_json_from_path(os.path.join(os.path.dirname(__file__), "resources", "response_parameter_simple.json"))

    def test_convert_json_to_response_parameter(self):
        title_builder = TitleBuilder(self.response_parameter_as_json, root_title="Venda")

        self.assertTrue(isinstance(title_builder.response_parameter, ResponseParameters))
        self.assertEqual(title_builder.response_parameter, self.response_parameter_simple)

    def test_built_title_with_temporal_filter(self):
        title_builder = TitleBuilder(self.response_parameter_composed_entity_name)
        self.assertTrue("de 01/12/2024 a 31/12/2024 (mês: 12/2024)", title_builder.build_non_temporal_entity_filter_line())

    def test_build_title_with_composed_entity(self):

        expected_title = '''Venda por usuario
 de 01/12/2024 a 31/12/2024 (mês: 12/2024)
Passado: Passador de Fio Dental BITUFO com 30 Unidades
Ambiente: viavarejo-prod
Categoria De Consulta: response element'''
        title_candidate = TitleBuilder(self.response_parameter_composed_entity_name, root_title="Venda").build()

        self.assertEqual(expected_title, title_candidate)

    def test_build_title_with_two_filters(self):
            expected_title = '''Venda por cidade
 dia 10/12/2024 (ter sem: 50/2024)
Estado : SP, RJ'''
            title_candidate = TitleBuilder(self.response_parameter_two_filters, root_title="Venda").build()

            self.assertEqual(expected_title, title_candidate)

    def test_build_title_with_simple_entity(self):
            expected_title = '''Venda por plu
 dia 05/12/2024 (qui sem: 49/2024)
Estado: SP
Loja: Ponto Certo
Categoria: CARNES'''
            title_candidate = TitleBuilder(self.response_parameter_simple, root_title="Venda").build()

            self.assertEqual(expected_title, title_candidate)
