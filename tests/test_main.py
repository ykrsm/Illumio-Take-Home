from collections import Counter, defaultdict
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from main import (
    count_matches,
    get_result_text,
    load_predefined_words,
    main,
    validate_file_size,
)


class TestMain(unittest.TestCase):
    @patch("main.get_result_text")
    @patch("main.count_matches")
    @patch("main.load_predefined_words")
    @patch("main.validate_file_size")
    def test_main(
        self,
        mock_validate_file_size,
        mock_load_predefined_words,
        mock_count_matches,
        mock_get_result_text,
    ):
        mock_load_predefined_words_return_value = {"word1": "Word1"}
        mock_load_predefined_words.return_value = (
            mock_load_predefined_words_return_value
        )
        mock_count_matches_return_value = Counter(
            {
                "Word1": 3,
                "Word2": 1,
                "word3": 1,
            }
        )
        mock_count_matches.return_value = mock_count_matches_return_value

        input_file_path = "input_file_path"
        predefined_words_file_path = "predefined_words_file_path"
        main(input_file_path, predefined_words_file_path)
        mock_validate_file_size.assert_has_calls(
            [call(input_file_path), call(predefined_words_file_path)]
        )
        mock_load_predefined_words.assert_called_once_with(predefined_words_file_path)
        mock_count_matches.assert_called_once_with(
            input_file_path, mock_load_predefined_words_return_value
        )
        mock_get_result_text.assert_called_once_with(mock_count_matches_return_value)

    @patch("main.load_predefined_words")
    @patch("main.validate_file_size")
    def test_main_empty_predefined_words(self, _, mock_load_predefined_words):
        mock_load_predefined_words.return_value = {}
        with self.assertRaises(ValueError) as e:
            main("input_file_path", "predefined_words_file_path")
        self.assertEqual(str(e.exception), "Predefined words list is empty")

    @patch("main.load_predefined_words")
    @patch("main.validate_file_size")
    def test_main_empty_predefined_words_exceeds_max(
        self,
        _,
        mock_load_predefined_words,
    ):
        mock_load_predefined_words_return_value = MagicMock()
        mock_load_predefined_words_return_value.__len__.return_value = 10001
        mock_load_predefined_words.return_value = (
            mock_load_predefined_words_return_value
        )
        with self.assertRaises(ValueError) as e:
            main("input_file_path", "predefined_words_file_path")
        self.assertTrue("Predefined words list has size exceeds" in str(e.exception))

    @patch("os.path.getsize")
    def test_validate_file_size(self, mock_getsize):
        mock_getsize.return_value = 20971521
        with self.assertRaises(ValueError) as e:
            validate_file_size("filepath")
        self.assertEqual(
            str(e.exception),
            "File size of filepath is 20971521, which exceeds 20971520",
        )

    @patch("main.count_matches")
    @patch("main.load_predefined_words")
    @patch("main.validate_file_size")
    def test_main_no_match_found(
        self, _, mock_load_predefined_words, mock_count_matches
    ):
        mock_load_predefined_words.return_value = {"word1": "Word1"}
        mock_count_matches.return_value = Counter()
        with self.assertRaises(ValueError) as e:
            main("input_file_path", "predefined_words_file_path")
        self.assertEqual(str(e.exception), "No match was found")

    def test_load_predefined_words(self):
        file_content = """Name 
        Detect 
        AI"""
        predefined_words_file_path = "predefined_words_file_path"
        mock_file_open = mock_open(read_data=file_content)
        with patch("builtins.open", mock_file_open):
            actual = load_predefined_words(predefined_words_file_path)
        expected = defaultdict(str, {"name": "Name", "detect": "Detect", "ai": "AI"})
        self.assertEqual(actual, expected)
        mock_file_open.assert_called_once_with(predefined_words_file_path, "r")

    def test_load_predefined_words_exceed_max(self):
        exceeding_length_word = "a" * 257
        file_content = exceeding_length_word
        predefined_words_file_path = "predefined_words_file_path"
        mock_file_open = mock_open(read_data=file_content)
        with patch("builtins.open", mock_file_open):
            with self.assertRaises(ValueError) as e:
                load_predefined_words(predefined_words_file_path)
        self.assertTrue("Predefined word" in str(e.exception))
        self.assertTrue("is exceeding length of 256" in str(e.exception))

    def test_load_predefined_words_with_duplicate(self):
        file_content = """Name
        Detect
        Detect
        """
        predefined_words_file_path = "predefined_words_file_path"
        mock_file_open = mock_open(read_data=file_content)
        with patch("builtins.open", mock_file_open):
            with self.assertRaises(ValueError) as e:
                load_predefined_words(predefined_words_file_path)
        self.assertEqual(str(e.exception), "Predefined word has duplicate word Detect")

    def test_count_matches(self):
        predefined_words_dict = defaultdict(
            str,
            {
                "name": "Name",
                "detect": "Detect",
                "ai": "AI",
            },
        )
        file_content = """Detecting first names is tricky to do even with AI. 
        how do you say a street name is not a first name?
        """
        input_file_path = "input_file_path"
        mock_file_open = mock_open(read_data=file_content)
        with patch("builtins.open", mock_file_open):
            actual = count_matches(input_file_path, predefined_words_dict)
        expected = Counter(
            {
                "AI": 1,
                "Name": 2,
            }
        )
        self.assertEqual(actual, expected)
        mock_file_open.assert_called_once_with(input_file_path, "r")

    def test_count_matches_punctuation(self):
        predefined_words_dict = defaultdict(
            str,
            {
                "dot": "Dot",
                "question": "Question",
                "colon": "Colon",
                "comma": "Comma",
                "parentheses": "parentheses",
            },
        )
        file_content = """dot.
        question?
        semicolon;
        colon:
        comma,
        (parentheses)
        """
        input_file_path = "input_file_path"
        mock_file_open = mock_open(read_data=file_content)
        with patch("builtins.open", mock_file_open):
            actual = count_matches(input_file_path, predefined_words_dict)
        expected = Counter(
            {
                "Dot": 1,
                "Question": 1,
                "Colon": 1,
                "Comma": 1,
                "parentheses": 1,
            }
        )
        self.assertEqual(actual, expected)
        mock_file_open.assert_called_once_with(input_file_path, "r")

    def test_count_matches_symbols(self):
        predefined_words_dict = defaultdict(
            str,
            {
                "dash": "Dash",
                "underscore_underscore": "underscore_underscore",
            },
        )
        file_content = """dash-dash
        underscore_underscore
        """
        input_file_path = "input_file_path"
        mock_file_open = mock_open(read_data=file_content)
        with patch("builtins.open", mock_file_open):
            actual = count_matches(input_file_path, predefined_words_dict)
        expected = Counter(
            {
                "Dash": 2,
                "underscore_underscore": 1,
            }
        )
        self.assertEqual(actual, expected)
        mock_file_open.assert_called_once_with(input_file_path, "r")

    def test_get_result_text(self):
        match_count = Counter(
            {
                "Word1": 3,
                "Word2": 1,
                "word3": 1,
            }
        )
        actual = get_result_text(match_count)
        expected = (
            "Predefined word      Match count    \n"
            "Word1                3              \n"
            "Word2                1              \n"
            "word3                1              "
        )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
