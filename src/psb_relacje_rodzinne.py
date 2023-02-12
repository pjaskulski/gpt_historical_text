""" openai test - extraction info about parents, children, wife,
    husband from bio
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import openai
import spacy


def get_data_gpt3(text:str='', prompt:str='') -> str:
    """ zwraca wynik zapytania do GPT-3 """
    result = ''

    response = openai.Completion.create(
         model="text-davinci-003",
         prompt=f"{prompt}\n\n {text}",
         temperature=0.0,
         max_tokens=800,
         top_p=1.0,
         frequency_penalty=0.0,
         presence_penalty=0.0)

    result = response['choices'][0]['text']

    return result


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

#OPENAI_ORG_ID = os.environ.get('OPENAI_ORG_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

# spacy do podziału tekstu na zdania
nlp = spacy.load('pl_core_news_sm')

# dane z pliku tekstowego
data_folder = Path("..") / "data" / "psb_probki_200_txt_gpt3"

data_file_list = data_folder.glob('*.txt')
max_char = 5000

licznik = 0
for data_file in data_file_list:
    # ograniczona liczba biogramów
    licznik += 1
    #if licznik < 7:
    #    continue
    if licznik > 5:
        break

    # if 'Pion_Maurice' not in data_file.as_posix():
    #     continue

    print(data_file)
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()

    data_file_name = os.path.basename(data_file)

    if len(data) > max_char:
        data_parts = []
        part = first = ''

        doc = nlp(data)
        for i, sent in enumerate(doc.sents):
            if i == 0:
                first = part = sent.text
            if len(part + ' ' + sent.text) > max_char:
                data_parts.append(part)
                part = first + ' ' + sent.text
            else:
                part += ' ' + sent.text
        if part and part != first:
            data_parts.append(part)

    else:
        data_parts = [data]


    #prompt = "From this text extract information about parents, wife, siblings, children" \
    #         "and grandchildren for the main character:"

    prompt = "From the given text, search all the family relations of the main character, " \
             "based solely on the facts in the text. " \
             "Write the result in the form of a list. " \
             "If there is no such information in the text write: no data."

    # "możliwe rodzaje relacji rodzinnych: ojciec, matka, brat, siostra, żona, mąż, teść, teściowa, dziadek, babcia, wnuk, wnuczka," \
    # "szwagier, szwagierka, siostrzeniec, siostrzenica, bratanek, bratanica, kuzyn, kuzynka, zięć, synowa)" \


    prompt = "Na podstawie podanego tekstu wyszukaj " \
             "wszystkie relacje rodzinne głównego bohatera (tylko jego krewnych, powinowatych, teściów, szwagrów, szwagierki). " \
             "Wynik wypisz w formie listy nienumerowanej " \
             "z rodzajem pokrewieństwa w nawiasie. Na przykład: " \
             "- Jan Kowalski (brat) " \
             "- Anna (siostra) " \
             "Jeżeli w tekście nie ma takich informacji napisz: brak danych."

    # prompt = "Na podstawie podanego tekstu wyszukaj " \
    #          "wszystkie relacje rodzinne głównego bohatera, jego krewnych lub powinowatych. " \
    #          "Wynik wypisz w formie listy nienumerowanej. " \
    #          "Możliwe rodzaje relacji rodzinnych: ojciec, matka, syn, córka, brat, siostra, żona, mąż, teść, teściowa, dziadek, babcia, wnuk, wnuczka," \
    #          "szwagier, szwagierka, siostrzeniec, siostrzenica, bratanek, bratanica, kuzyn, kuzynka, zięć, synowa, teść bratanicy." \
    #          "w formie: główny bohater -> rodzaj pokrewieństwa -> osoba będąca krewnym lub powinowatym " \
    #          "Na przykład: " \
    #          "- główny bohater -> brat -> Jan Kowalski" \
    #          "- główny bohater -> siostra -> Anna (siostra) " \
    #          "Jeżeli w tekście nie ma takich informacji napisz: brak danych."

    #prompt = "Proszę wydobyć dane o relacjach rodzinnych głównego bohatera " \
    #         "tekstu, w tym imiona i nazwiska członków rodziny, ich funkcje i role, a także " \
    #         "szczegółowe informacje o ich powiązaniach i relacjach między sobą. " \
    #         "Wynik wypisz w formie nienumerowanej listy osób." \
    #         "Jeżeli w tekście nie ma takich informacji napisz: brak danych."

    output = []
    for data_part in data_parts:
        output.append(get_data_gpt3(data_part, prompt))

    output_lines = []
    for item in output:
        lines = item.split('\n')
        for line in lines:
            line = line.strip()
            if line and line not in output_lines:
                output_lines.append(line)

    file_output = Path("..") / "output" / "psb_probki_200_txt_gpt3" / data_file_name.replace('.txt', '.relacje')
    with open(file_output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
