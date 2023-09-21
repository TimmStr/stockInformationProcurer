# import unittest
# import json
# from StockAnalysisService import app
#
# class TestFlaskApp(unittest.TestCase):
#
#     def setUp(self):
#         # Erstellen eines Flask-Testclients
#         self.app = app.test_client()
#
#     def test_start_analysis_endpoint(self):
#         # Beispielwerte für den Test
#         ticker = 'NASDAQ:GOOGL'
#         request_data = {'ticker': ticker}
#         response = self.app.get('/startAnalysis', query_string=request_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Started analysis', response.data)  # Ersetzen Sie 'Started analysis' durch die erwartete Antwort
#
#     def test_get_graphs_endpoint(self):
#         # Beispielwerte für den Test
#         symbol = 'AAPL'
#         date = '2023-09-17'
#         response = self.app.get(f'/get_graphs?symbol={symbol}&date={date}')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.content_type.startswith('image/'))  # Überprüfen Sie den Content-Type der Antwort
#
# if __name__ == '__main__':
#     unittest.main()