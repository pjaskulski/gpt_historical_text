""" test tiktoken """

import os
from pathlib import Path
import tiktoken


def count_tokens(filename:str, model:str) -> int:
    """ funkcja zlicza tokeny """
    num_of_tokens = 0
    enc = tiktoken.get_encoding(model)
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        num_of_tokens = len(enc.encode(text))

    return num_of_tokens


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # dane z pliku tekstowego
    data_folder = Path("..") / "data" / "psb_probki_200_txt_gpt3"
    data_file_list = data_folder.glob('*.txt')

    licznik = 0
    for data_file in data_file_list:
        licznik += 1
        if licznik > 50:
            break

        data_file_name = os.path.basename(data_file)
        count = count_tokens(data_file, 'gpt2')
        print(f'{data_file_name}, token = {count}')
