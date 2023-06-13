""" Test GPT4all """
import time
from pathlib import Path
import gpt4all

#print(gpt4all.GPT4All.list_models())

start_time = time.time()

gpt_hermes = gpt4all.GPT4All("ggml-v3-13b-hermes-q5_1.bin")


# 'Aloe.dane', 'Bartoszewski_Jan.dane','Bezprym.dane',
# 'Daszyński_Ignacy.dane', 'Dzierżek_Natalia.dane', 'Eufrozyna.dane, Ewild_al._Eywild.dane'
# 'Ezra_ben_Nisan.dane', 'Falęta.dane',
# 'Fuzorius_Bartłomiej.dane',  'Gliński_Iwan.dane', 'Gołaski_Jan.dane', 'Grzegorzewski_Jan.dane', 'Guicciardini_Galeazzo.dane',
# 'Hincza_z_Rogowa.dane', 'Hirschenfeld-Mielecki_Józef.dane',
# 'Kakowski_Aleksander.dane', 'Krumhausen_Gabriel.dane', 'Langfort_Teodor_Henryk.dane',
# 'Leymiter_Stanisław.dane','Mierzeński_Aleksander_h..dane', 'Mostowska_z_Bujwidów.dane', 'Patruus.dane',
# 'Pichgiel.dane', 'Pion_Maurice.dane', 'Piotrowiczowa_z_Rogolińskich.dane', 'Popiel.dane',
# 'Renard_Benedykt_h..dane', 'Rossi_Piotr.dane', 'Sapieha_Jan_Fryderyk.dane',

osoby = {'Bartoszewski_Jan.dane':'Jan Bartoszewski',
         'Daszyński_Ignacy.dane':'Ignacy Daszyński',
         'Ezra_ben_Nisan.dane':'Ezra ben Nisan',
         'Falęta.dane':'Falęta',
         'Fuzorius_Bartłomiej.dane':'Bartłomiej Fuzorius',
         'Gliński_Iwan.dane':'Iwan Gliński',
         'Gołaski_Jan.dane':'Jan Gołaski',
         'Guicciardini_Galeazzo.dane':'Galeazzo Guicciardini',
         'Hincza_z_Rogowa.dane':'Hincza z Rogowa',
         'Hirschenfeld-Mielecki_Józef.dane':'Józef Hirschenfeld-Mielecki',
         'Krumhausen_Gabriel.dane':'Gabriel Krumhausen',
         'Langfort_Teodor_Henryk.dane':'Teodor Henryk Langfort',
         'Leymiter_Stanisław.dane':'Stanisław Leymiter',
         'Mierzeński_Aleksander_h..dane':'Aleksander Mierzeński',
         'Patruus.dane':'Jan Patruus',
         'Pichgiel.dane':'Christian Pichgiel',
         'Pion_Maurice.dane':'Maurice Pion',
         'Popiel.dane':'Popiel',
         'Renard_Benedykt_h..dane':'Benedykt Renard',
         'Rossi_Piotr.dane':'Piotr Rossi',
         'Sapieha_Jan_Fryderyk.dane':'Jan Fryderyk Sapieha',
         'Siemowit.dane':'Siemowit',
         'Słowicki_Józef.dane':'Józef Słowicki',
         'Spektor_Mordechaj.dane':'Mordechaj Spektor',
         'Spycigniew_z_Dąbrowy.dane':'Spycigniew z Dąbrowy',
         'Stanisław_Cielątko_z.dane':'Stanisław Cielątko',
         'Strzelecki_Wiesław_Marian.dane':'Wiesław Marian Strzelecki',
         'Swach.dane':'Jerzy Swach',
         'Świrski Jerzy Włodzimierz.dane':'Jerzy Władzimierz Świrski',
         'Szapira.dane':'Majer Szapira',
         'Szapocznikow_Alina.dane':'Alina Szapocznikow',
         'Szczubioł_Andrzej_z.dane':'Andrzej Szczubioł',
         'Sztaffel Izrael.dane':'Izrael Sztaffel',
         'Szumski Boksa.dane':'Boksa Szumski',
         'Dąbrowska_Pelagia.dane':'Pelagia Dąbrowska',
         'Fiorentini_Władysław.dane':'Władysław Fiorentini',
         'Łańcucki_Wojciech.dane':'Wojciech Łańcucki'
         }

#Przykład 3:
#Tekst: "Ulryk Wicek (1690-1760), rajca krakowski, był synem Adolfa Wicka, burgabiego."
#Wynik: {{"ojciec":"Adolf Wicek"}}


for file_osoba, person in osoby.items():
    data_file = Path(".") / "short" / file_osoba
    result_file = Path(".") / "results" / file_osoba.replace('.dane','.wynik')

    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()

    prompt_template = f"""Na podstawie wyłącznie informacji z podanego tekstu napisz kto był ojcem {person}.
Wynik zapisz w formacie JSON.
Na przykład:
Tekst: "Łukasz Kowalski (1901-1987) ur. w Bogatce z ojca Hieronima i matki Heleny z Kruszyńskich."
Wynik: {{"ojciec": "Hieronim Kowalski"}}
Tekst: "Marcin Wielopolski (1700-1776), szlachcic pomorski, ur. w Ustce. Ojcem W. był Antoni, herbu Trójnóg."
Wynik: {{"ojciec": "Antoni Wielopolski"}}
Tekst: "Eustachy Wikozy (zm. 1233), pochodzenie nienane, klucznik gnieźnieński."
Wynik: {{"ojciec":"brak danych"}}

Tekst: {data}
Wynik:
"""

    messages = [{"role": "user", "content": prompt_template}]
    result = gpt_hermes.chat_completion(messages, temp=0.0, top_p=1.0)

    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(result['choices'][0]['message']['content'])

    del gpt_hermes
    gpt_hermes = gpt4all.GPT4All("ggml-v3-13b-hermes-q5_1.bin")


end_time = time.time()
elapsed_time = end_time - start_time
print(f'Czas wykonania programu: {time.strftime("%H:%M:%S", time.gmtime(elapsed_time))} s.')
