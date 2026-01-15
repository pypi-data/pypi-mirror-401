import numpy as np
import pandas as pd

from looqbox.database.connections.connection_big_query import BigQueryConnection
import unittest
from os.path import dirname, join
import json
from pandas import Float64Dtype, Int64Dtype, StringDtype, read_csv

class TestBigQueryConnection(unittest.TestCase):

    def setUp(self):
        self.connection = BigQueryConnection("MockedName")
        data = {
            'numeric_col': ['1.1', '2.2', '3.3'],
            'integer_col': ['1', '2', '3'],
            'record_col': [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}],
            'timestamp_col': ['2024-08-29 12:34:56', '2024-08-30 12:34:56', '2024-08-31 12:34:56']
        }
        self.data_frame = pd.DataFrame(data)

    # def test_table_name_matcher_simple_query(self):
    #     query = """
    #     SELECT
    #        *
    #     FROM
    #         `google_billing.gcp_billing` AS t1
    #     WHERE
    #         1=1
    #         AND (
    #             t1.Date >= '2024-03-01'
    #             AND t1.Date < '2024-04-01'
    #         )
    #     ORDER BY
    #         1 DESC
    #          """
    #
    #     self.connection.set_query_script(query)
    #     self.connection._get_table_name_from_query()
    #     self.assertEqual("google_billing.gcp_billing",
    #                      self.connection._get_table_name_from_query())
    #
    # def test_table_name_matcher_join_query(self):
    #     query = """
    #     SELECT
    #         *
    #     FROM
    #         `varejo_alimentar.FATO_VENDA_PRODUTO` AS t4
    #     LEFT JOIN
    #         `varejo_alimentar.DIM_LOJA` AS t1
    #         ON t4.ID_LOJA = t1.ID_LOJA
    #     WHERE
    #         1=1
    #         AND (
    #             t4.DATE >= '2024-03-11'
    #             AND t4.DATE < '2024-03-12'
    #         )
    #     GROUP BY
    #     ESTADO
    #     ORDER BY
    #         2 DESC,
    #         3 DESC,
    #         4 DESC
    #     LIMIT 1001
    #          """
    #
    #     self.connection.set_query_script(query)
    #     self.connection._get_table_name_from_query()
    #     self.assertEqual("varejo_alimentar.FATO_VENDA_PRODUTO",
    #                      self.connection._get_table_name_from_query())
    #
    # def test_table_name_matcher_join_with_subquery(self):
    #     query = """
    #     SELECT
    #         *
    #     FROM
    #     (
    #         WITH
    #           receita_companhia_por_dia AS (
    #           SELECT
    #             *
    #           FROM
    #             `looqlake-prod.hortifruti_prod.fato_receita_item` fri
    #           GROUP BY
    #             1,
    #             2 ),
    #           fri AS (
    #           SELECT
    #             *
    #           FROM
    #             `looqlake-prod.hortifruti_prod.fato_receita_item` AS t1
    #           LEFT JOIN
    #             `looqlake-prod.hortifruti_prod.dim_produto_hierarq` AS t2
    #           ON
    #             t1.SK_PRODUTO = t2.SK_PRODUTO
    #           GROUP BY
    #             1,
    #             2,
    #             3,
    #             4,
    #             5),
    #           ric AS (
    #           SELECT
    #             *
    #           FROM
    #             fri
    #           INNER JOIN (
    #             SELECT
    #               *
    #             FROM
    #               `looqlake-prod.hortifruti_prod.fato_receita_cupom` ) frc
    #           ON
    #             fri.SK_CUPOM = frc.SK_CUPOM
    #           LEFT JOIN
    #             `looqlake-prod.hortifruti_prod.dim_tpo_receita` tr
    #           ON
    #             tr.SK_TPO_RECEITA = frc.SK_TPO_RECEITA
    #           INNER JOIN (
    #             *
    #             FROM
    #               `looqlake-prod.hortifruti_prod.dim_canal_venda_hierarq` ) cvh
    #           ON
    #             frc.SK_CANAL_VENDA = cvh.SK_CANAL_VENDA_MARCACAO_HIERQ
    #           GROUP BY
    #             1,
    #             2,
    #             3,
    #             4,
    #             5,
    #             6,
    #             7,
    #             8,
    #             9,
    #             10 )
    #         SELECT
    #           *
    #         FROM
    #           ric
    #         JOIN
    #           receita_companhia_por_dia rcd
    #         ON
    #           ric.SK_TEMPO = rcd.SK_TEMPO
    #           AND ric.SK_LOJA = rcd.SK_LOJA
    #         FULL JOIN (
    #           *
    #           FROM
    #             `looqlake-prod.hortifruti_prod.fato_orcamento_canal_venda_digital_categoria_loja_dia`
    #           GROUP BY
    #             1,
    #             2,
    #             3,
    #             4 ) focv
    #         ON
    #           ric.SK_LOJA = focv.SK_LOJA
    #           AND CAST(FORMAT_DATE('%Y%m%d', ric.SK_TEMPO) AS INT64) = focv.SK_TEMPO
    #           AND ric.COD_CATEGORIA = focv.COD_CATEGORIA
    #           AND ric.SK_CANAL_VENDA_ORCADO = focv.SK_CANAL_VENDA_ORCADO
    #         WHERE
    #           1=1
    #             AND TPO_CANAL_VENDA = "DIGITAL"
    #           --AND (ric.SK_TEMPO = '2024-01-28' OR focv.SK_TEMPO = 20240128)
    #         GROUP BY
    #           1,
    #           2,
    #           3,
    #           4,
    #           5,
    #           6,
    #           VLR_RECEITA_BRUTA_DIA
    #         ) AS t1
    #     LEFT JOIN
    #     `hortifruti_prod.dim_loja` AS t3
    #     ON t1.SK_LOJA = t3.SK_LOJA
    #     WHERE
    #         1 = 1
    # 	    AND t1.SK_TEMPO >= '2024-03-04' AND t1.SK_TEMPO <= '2024-03-04'
    #     GROUP BY
    #     1
    #     ,2
    # LIMIT 1001"""
    #
    #     self.connection.set_query_script(query)
    #     self.connection._get_table_name_from_query()
    #     self.assertEqual("looqlake-prod.hortifruti_prod.fato_receita_item",
    #                      self.connection._get_table_name_from_query())
    #
    # def test_table_name_matcher_query_with_alias(self):
    #     query = """
    #     SELECT
    #         ID_LOJA as `ID Da Loja`,
    #         NOME_LOJA AS `Nome Loja`,
    #         CIDADE As `Nome da Cidade`,
    #         ESTADO aS `Nome do Estado`,
    #         ENDERECO as `Endereço`
    #     FROM
    #         `looqlake-prod.varejo_alimentar.DIM_LOJA`
    #     LIMIT
    #         10
    #          """
    #
    #     self.connection.set_query_script(query)
    #     self.connection._get_table_name_from_query()
    #     self.assertEqual("looqlake-prod.varejo_alimentar.DIM_LOJA",
    #                      self.connection._get_table_name_from_query())

        with open(join(dirname(__file__), "resources", "bigQueryMockedMetadata.json"), "r") as metadata_file:
            self.raw_metadata = json.load(metadata_file)
            metadata_file.close()

        self.connection = BigQueryConnection("MockedName")

    def test_convert_numeric_column(self):
        types = {'numeric_col': 'NUMERIC'}
        result = self.connection._convert_columns_type(self.data_frame, types)
        self.assertEqual(result['numeric_col'].dtype, 'float64')

    def test_convert_integer_column(self):
        types = {'integer_col': 'INTEGER'}
        result = self.connection._convert_columns_type(self.data_frame, types)
        self.assertEqual(result['integer_col'].dtype, 'int')

    def test_convert_record_column(self):
        types = {'record_col': 'RECORD'}
        result = self.connection._convert_columns_type(self.data_frame, types)
        self.assertIn('record_col.a', result.columns)
        self.assertIn('record_col.b', result.columns)

    def test_convert_timestamp_column(self):
        types = {'timestamp_col': 'TIMESTAMP'}
        result = self.connection._convert_columns_type(self.data_frame, types)
        self.assertEqual(result['timestamp_col'].dtype, 'datetime64[ns]')

    def test_convert_integer_column_with_fallback(self):
        self.data_frame['integer_col'] = ['1', np.nan, None]
        types = {'integer_col': 'INTEGER'}
        result = self.connection._convert_columns_type(self.data_frame, types)
        self.assertEqual(result['integer_col'].dtype, pd.Int64Dtype())


    def test_read_data_with_typing(self):
        self.connection.query_metadata = self.raw_metadata
        converted_types = self.connection._convert_metadata_to_pandas_type()

        data = read_csv(join(dirname(__file__), "resources", "bigQueryMockedData.csv"), dtype=converted_types, sep=";")

        self.assertTrue(isinstance(data.dtypes["CUSTO"], Float64Dtype))
        self.assertTrue(isinstance(data.dtypes["DATE"], StringDtype))
        self.assertTrue(isinstance(data.dtypes["ID_LOJA"], Int64Dtype))
        self.assertTrue(isinstance(data.dtypes["NULL_VALUES"], Int64Dtype))
        self.assertTrue(isinstance(data.dtypes["MIXED_VALUES"], Int64Dtype))

if __name__ == '__main__':
    unittest.main()
