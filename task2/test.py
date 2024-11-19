import unittest
from unittest.mock import patch
from solution import get_category_pages, count_animals_by_letter, write_to_csv
import requests
import os

class TestWikiBeasts(unittest.TestCase):
    @patch('solution.requests.get')
    def test_get_category_pages_single_page(self, mock_get):
        """Test getting category pages without continuation"""
        mock_response = {
            "query": {
                "categorymembers": [
                    {"pageid": 1, "title": "Аист"},
                    {"pageid": 2, "title": "Белка"},
                ]
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        expected = ["Аист", "Белка"]
        result = get_category_pages("Категория:Животные по алфавиту")
        self.assertEqual(result, expected)
        mock_get.assert_called_once()

    @patch('solution.requests.get')
    def test_get_category_pages_multiple_pages(self, mock_get):
        """Test getting category pages with continuation"""
        # First response contains continuation
        mock_response1 = {
            "query": {
                "categorymembers": [
                    {"pageid": 1, "title": "Аист"},
                    {"pageid": 2, "title": "Белка"},
                ]
            },
            "continue": {
                "cmcontinue": "page|3"
            }
        }
        # Second response without continuation
        mock_response2 = {
            "query": {
                "categorymembers": [
                    {"pageid": 3, "title": "Волк"},
                ]
            }
        }
        mock_get.side_effect = [
            unittest.mock.Mock(status_code=200, json=lambda: mock_response1),
            unittest.mock.Mock(status_code=200, json=lambda: mock_response2)
        ]

        expected = ["Аист", "Белка", "Волк"]
        result = get_category_pages("Категория:Животные по алфавиту")
        self.assertEqual(result, expected)
        self.assertEqual(mock_get.call_count, 2)

    def test_count_animals_by_letter(self):
        """Test counting animals by first letter"""
        titles = ["Аист", "Антилопа", "Белка", "Бобр", "Волк"]
        expected_counts = {"А": 2, "Б": 2, "В": 1}
        result = count_animals_by_letter(titles)
        self.assertEqual(result, expected_counts)

    def test_write_to_csv(self):
        """Test writing data to CSV file"""
        counts = {"А": 642, "Б": 412, "В": 300}
        filename = 'test_beasts.csv'
        write_to_csv(counts, filename)

        # Check that the file exists
        self.assertTrue(os.path.exists(filename))

        # Check the contents of the file
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        expected_content = "А,642\nБ,412\nВ,300\n"
        self.assertEqual(content.strip(), expected_content.strip())

        # Remove the test file
        os.remove(filename)

    @patch('solution.requests.get')
    def test_get_category_pages_http_error(self, mock_get):
        """Test handling HTTP errors when getting category pages"""
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

        with self.assertRaises(requests.HTTPError):
            get_category_pages("Категория:Животные по алфавиту")

if __name__ == '__main__':
    unittest.main()
