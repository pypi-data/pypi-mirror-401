from collections import Counter
from functools import lru_cache
import argparse

@lru_cache(maxsize=10)
def get_unique_count(input_data):
    if not isinstance(input_data, str):
        raise TypeError('Input must be a string or a file path')
    try:
        with open(input_data, 'r', encoding='utf-8') as f:
            text = f.read()
    except (FileNotFoundError, OSError):
        text = input_data

    counts = Counter(text)
    unique_iterator = filter(lambda char: counts[char]  == 1, counts)
    unique_list = list(unique_iterator)

    return len(unique_list)


print(f"Result for 'abcabctj' :", get_unique_count("abcabctj"))
print(f"Result for 'abcdef':", get_unique_count("abcdef"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='main_app')
    parser.add_argument('--string', type=str)
    parser.add_argument('--file', type=str)

    args = parser.parse_args()

    #Перевіряю строку
    if args.string is not None:
        print(f"String: {args.string}")

    #Перевіряю файл
    elif args.file is not None:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text_from_file = f.read()
                print(f"String:\n{text_from_file}")
        except FileNotFoundError:
            print(f"File {args.file} not found.")
    #Якщо нічого не ввели
    else:
        print("Error: Use --string or --file arguments.")
