import argparse
from collections import Counter, defaultdict
import os
import re

MAX_FILE_SIZE = 20971520  # 20MB
MAX_PREDEFINED_WORD_COUNT = 10000
MAX_PREDEFINED_WORD_LENGTH = 256


def validate_file_size(file_path):
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File size of {file_path} is {file_size}, which exceeds {MAX_FILE_SIZE}"
        )


def load_predefined_words(predefined_words_file_path):
    lower_case_to_original_map = defaultdict(str)
    with open(predefined_words_file_path, "r") as file:
        for line in file.readlines():
            stripped_line = line.strip()
            if len(stripped_line) > MAX_PREDEFINED_WORD_LENGTH:
                raise ValueError(
                    f"Predefined word {stripped_line} is exceeding length of {MAX_PREDEFINED_WORD_LENGTH}"
                )
            stripped_lower_line = stripped_line.lower()
            if stripped_lower_line in lower_case_to_original_map:
                raise ValueError(f"Predefined word has duplicate word {stripped_line}")
            lower_case_to_original_map[stripped_lower_line] = stripped_line
    return lower_case_to_original_map


def count_matches(input_file_path, predefined_words_dict):
    match_counter = Counter()

    with open(input_file_path, "r") as file:
        for line in file.readlines():
            # Need to use regex here to remove punctuations. split() does not work here.
            words = re.findall(r"\b\w+\b", line.lower())
            for word in words:
                if word in predefined_words_dict:
                    original = predefined_words_dict[word]
                    match_counter[original] += 1

    return match_counter


def get_result_text(match_count):
    result_lines = []
    result_lines.append(f"{'Predefined word':<20} {'Match count':<15}")
    for word, count in match_count.items():
        result_lines.append(f"{word:<20} {count:<15}")
    return "\n".join(result_lines)


def main(input_file_path, predefined_words_file_path):
    validate_file_size(input_file_path)
    validate_file_size(predefined_words_file_path)

    predefined_words_dict = load_predefined_words(predefined_words_file_path)
    if len(predefined_words_dict) == 0:
        raise ValueError("Predefined words list is empty")
    if len(predefined_words_dict) > MAX_PREDEFINED_WORD_COUNT:
        raise ValueError(
            f"Predefined words list has size exceeds {MAX_PREDEFINED_WORD_COUNT}"
        )

    match_count = count_matches(input_file_path, predefined_words_dict)
    if len(match_count) == 0:
        raise ValueError("No match was found")
    print(get_result_text(match_count))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to the input file")
    parser.add_argument(
        "--predefined", required=True, help="Path to the predefined words file"
    )
    args = parser.parse_args()
    main(args.input, args.predefined)
