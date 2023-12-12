import unittest
from unittest.mock import patch, mock_open
import sw  # substitua pelo nome do seu módulo

class TestMain(unittest.TestCase):
    @patch('sw.requests.get')
    @patch('sw.json.dump')
    @patch('sw.os.path.exists', return_value=True)
    @patch('sw.os.makedirs')
    def test_fetch_data(self, mock_makedirs, mock_exists, mock_dump, mock_get):
        # Configure o mock para simular a resposta da API
        mock_get.return_value.json.return_value = {'results': [], 'next': None}

        fetcher = sw.DataFetcher()
        fetcher.fetch_data('people')

        # Verifique se os métodos foram chamados da maneira esperada
        mock_dump.assert_called_once()

    @patch('sw.json.load')
    @patch('sw.os.path.exists', return_value=True)
    def test_read_data(self, mock_exists, mock_load):
        fetcher = sw.DataFetcher()
        fetcher.read_data('people')

        # Verifique se os métodos foram chamados da maneira esperada
        mock_load.assert_called_once()

    @patch('sw.json.dump')
    @patch('sw.os.path.exists', return_value=True)
    def test_write_data(self, mock_exists, mock_dump):
        fetcher = sw.DataFetcher()
        fetcher.write_data('people', [])

        # Verifique se os métodos foram chamados da maneira esperada
        mock_dump.assert_called_once()

    def test_people_with_more_than_two_starships(self):
        main = sw.Main()
        people = [{'starships': [1, 2, 3]}, {'starships': [1, 2]}]
        result = main.people_with_more_than_two_starships(people)
        self.assertEqual(result, [{'starships': [1, 2, 3]}])

    def test_most_populated_planet(self):
        main = sw.Main()
        planets = [{'name': 'A', 'population': '1000'}, {'name': 'B', 'population': '2000'}, {'name': 'C', 'population': 'unknown'}]
        result = main.most_populated_planet(planets)
        self.assertEqual(result, {'name': 'B', 'population': '2000'})

    def test_people_data(self):
        main = sw.Main()
        people = [{'starships': ['url1', 'url2'], 'homeworld': 'urlA'}]
        starships = [{'url': 'url1'}, {'url': 'url2'}, {'url': 'url3'}]
        planets = [{'url': 'urlA'}, {'url': 'urlB'}]
        result = main.people_data(people, starships, planets)
        self.assertEqual(result, [{'starships': [{'url': 'url1'}, {'url': 'url2'}], 'homeworld': {'url': 'urlA'}}])

    def test_find_people_data(self):
        main = sw.Main()
        people_data = [{'url': 'url1'}, {'url': 'url2'}, {'url': 'url3'}]
        with patch.object(main.fetcher, 'read_data', return_value=people_data):
            result = main.find_people_data('url2')
        self.assertEqual(result, {'url': 'url2'})

if __name__ == '__main__':
    unittest.main()