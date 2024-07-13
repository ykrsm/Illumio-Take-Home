import argparse
from collections import Counter, defaultdict
import re


def load_predefined_words(predefined_words_file_path):
    lower_case_to_original_map = defaultdict(str)
    with open(predefined_words_file_path, "r") as file:
        for line in file.readlines():
            stripped_line = line.strip()
            lower_case_to_original_map[line.strip().lower()] = stripped_line
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
    predefined_words_dict = load_predefined_words(predefined_words_file_path)
    if len(predefined_words_dict) == 0:
        raise ValueError("Predefined words list is empty")

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
