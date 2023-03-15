# GPT3 - Large Language Model as a tool for extracting knowledge from text - tests on excerpts from historical publications.

Testy modeli GPT 3.5 udostępnionych przez API OpenAI przeprowadzane na fragmentach publikacji i opracowań historycznych w celu automatycznej ekstrakcji informacji, wyciągania ustrukturyzowanych danych ze źródeł dostępnych w formie nieustrukturyzowanej. Testowany materiał to głównie fragmenty
biografii postaci historycznych.

[Notatki](#notatki)
  - [Wstępne informacje](#wstępne-informacje)
  - [Literatura, blogi, repozytoria](#literatura)
  - [Porównanie dostępnych modeli GPT](#porównanie-dostępnych-modeli-gpt)
  - [Uwagi techniczne](#uwagi-techniczne)
  - [Poprawność odpowiedzi](#poprawność-odpowiedzi)
  - [Wiedza z kontekstu](#wiedza-z-kontekstu)

[Przykłady](#przykłady)
  - [Relacje rodzinne postaci](#relacje-rodzinne)
  - [Funkcje i urzędy](#funkcje-i-urzędy-głównej-postaci)
  - [Lista instytucji](#lista-instytucji)
  - [Imię, nazwisko, data śmierci](#wynik-w-formie-tabeli)
  - [Lista urzędów](#lista-urzędów)
  - [Lista urzędów i funkcji w formie xml](#lista-urzędów-i-funkcji-w-xml)
  - [Relacje rodzinne](#relacje-rodzinne-nr-2)
  - [Konwersja tekstu do formatu TEI](#tei-xml-output)
  - [Analiza NER fragmentu publikacji](#analiza-ner-fragmentu-publikacji)
  - [Inne przykłady](#inne-przykłady)
  - [Analiza 50 biogramów - relacje rodzinne](#analiza-relacji-rodzinnych-na-serii-biografii)


## Notatki

### Wstępne informacje

Definicja GPT-3 (napisana przez ChatGPT):
"GPT-3 (Generative Pretrained Transformer 3) jest trzecią wersją sztucznej inteligencji opracowaną przez OpenAI. Jest to jeden z największych modeli językowych na świecie, który został wytrenowany na ogromnych zbiorach danych tekstowych, aby rozumieć i generować język ludzki. GPT-3 jest używany do wielu zastosowań, takich jak generowanie tekstu, tłumaczenie, odpowiadanie na pytania i rozumienie tekstu. Model ten wykorzystuje architekturę Transformer i jest w stanie uczyć się zadanie z niewielką ilością danych, co czyni go bardzo efektywnym i elastycznym narzędziem dla różnych zastosowań."

Testy GPT-3 zostały przeprowadzone poprzez API udostępnione przez firmę OpenAI, wykorzystano głównie model `text-davinci-003` (nazywany czasem modelem GPT-3.5).

Istnieją ograniczenia podczas korzystania z API dotyczące liczby zapytań na minutę (3 tys.) i liczby przetworzonych tokenów na minutę (250 tys.).

Token jest rozumiany trochę inaczej niż zwykle w NLP, tu dłuższe wyrazy są rozbijane na krótkie tokeny 3-4 znaki, oprócz tego tokenem są też znaki interpunkcyjne itp. Podawane jest że średnio token to 4 znaki w języku angielskim, na stronie OpenAI jest narzędzie w którym (https://beta.openai.com/tokenizer) można wkleić tekst i zobaczyć ile zawiera tokenów.

Przykładowo biografia Edwarda Józefa Sedlaczka (Polski Słownik Biograficzny t. XXXVI, 1995-6, s. 137-138) zawiera 4433 znaków co przekłada się na 2291 tokenów. W przypadku tekstów polskich sytuację pogarszają polskie znaki, wygląda na to że każdy dwubajtowy unicodowy znak jest traktowany jako osobny token.

### Literatura

- _"Structured information extraction from complex scientific text with fine-tuned large language models"_ (Alexander Dunn, John Dagdelen, Nicholas Walker, Sanghoon Lee, Andrew S. Rosen, Gerbrand Ceder, Kristin Persson and Anubhav Jain) [link](https://arxiv.org/pdf/2212.05238.pdf)

- _"Text Pattern Extraction: Comparing GPT-3 & Human-in-the-Loop Tool"_ (Maeda Hanafi) [link](https://towardsdatascience.com/text-pattern-extraction-comparing-gpt-3-human-in-the-loop-tool-f2380fd13cf1)

- _"Getting tabular data from unstructured text with GPT-3: an ongoing experiment"_ (ROBERTO ROCHA) [link](https://robertorocha.info/getting-tabular-data-from-unstructured-text-with-gpt-3-an-ongoing-experiment/)

- _"Advanced NER With GPT-3 and GPT-J"_ (Maxime Cupani) [link](https://towardsdatascience.com/advanced-ner-with-gpt-3-and-gpt-j-ce43dc6cdb9c)

- _"Relationship Extraction with GPT-3. Accelerate knowledge graph construction with GPT-3"_ (Sixing Huang) [link](https://medium.com/geekculture/relationship-extraction-with-gpt-3-bb019dcf41e5)

- _"Language Models are Few-Shot Learners"_ (Tom B. Brown et al.) [link](https://arxiv.org/abs/2005.14165)

- _"Training language models to follow instructions with human feedback"_ (Long Ouyang et al., OpenAI) [link](https://arxiv.org/pdf/2203.02155.pdf)


### Porównanie dostępnych modeli GPT

Najlepszy model `text-davinci-003` (to jednocześnie najdroższy model językowy w OpenAI) ma ograniczenie do 4000 tokenów, przy czym dotyczy to wejścia i wyjścia razem.

Modele słabsze np. `text-curie-001` czy `text-babbage-001` dają w przypadku wyciągania danych z przekazanego tekstu wyraźnie gorsze wyniki np.:

Funkcje/urzędy z biografii Edwarda Sedlaczka wg. `text-davinci-003` (przy standardowych ustawieniach parametrów, np. `temperature` = 0.5):

1. Kierownik literacki dwutygodnika lwowskiego „Przyjaciel Domowy” (1 VI 1882)
2. Kancelista w konsulacie austriackim w Warszawie (1886)
3. Konsulat austriacki w Kijowie (do 1895)
4. Wicekonsulat w Batumi, Rosja (1896–7)
5. Agencja konsularna w Nowosielicy, Rosja
6. Agencja konsularna w Burgas, Bułgaria
7. Wicekonsulat w Batumi, Rosja
8. Wicekonsulat Burgas, Bułgaria
9. Wicekonsulat Ploieşti, Rumunia
10. Redaktor serii Wydawnictwa Towarzystwa imienia Piotra Skargi (ok 1910).

Funkcje/urzędy wg modelu `text-curie-001` (parametry jak wyżej):

- literat
- urzędnik
- kierownik literacki dwutygodnika lwowskiego „Przyjaciel Domowy”
- posada kancelisty w konsulacie austriackim w Warszawie
- kierował kolejno wicekonsulatem w Batumi (Rosja, 1896–7), a od r.n. – agencją konsularną w Nowosielicy (Rosja), agencją konsularną w Burgas (Bułgaria), wicekonsulatem w Batumi, wicekonsulatem w Burgas i wicekonsulatem w Ploieşti (Rumunia)

Te słabsze modele, mają też większe ograniczenia: do 2 tys. tokenów w jednym zapytaniu, są jednak znacznie tańsze.

### Uwagi techniczne

Parametr `temperature` ma wartość 0.0 - 1.0, niższa wartość powoduje że odpowiedź jest bardziej konkretna, deterministyczna, mniej losowa i mniej kreatywna. Wyższa pozwala modelowi na więcej elastyczności. Alternatywnie można modyfikować domyślną wartość parametru `top_p` = 1.0, zmniejszając jego wartość - nie jest jednak zalecane jednoczesne modyfikowanie obu parametrów (zob. [API reference](https://beta.openai.com/docs/api-reference/completions/create)).

Wielokrotne uruchamianie tego samego zapytania może dawać nieco inne wyniki, jeżeli wartość parametru temperature jest większa od zera.

Zapytania uruchamiane przez API nie znają kontekstu zapytań uruchamianych chwilę przed,
inaczej niż w trakcie rozmowy z ChatGPT, należy za każdym razem podawać całą informację w zapytaniu.

Ogromne znaczenie ma konstrukcja zapytania (prompt), całkiem poprawnie działają pytania w języku angielskim dotyczące podanego polskiego tekstu, czasem dają nawet lepsze rezultaty. Zadanie zlecone modelowi powinno być napisane językiem prostym, konkretnym, ale nie musi być bardzo krótkie. Dobry wpływ na jakość odpowiedzi mają podane modelowi przykłady, czego i w jakiej formie się spodziewamy.

Odpowiedzi modelu davinci-003 zadawane przez API, często różnią się od wyników pytań zadanych
podczas 'rozmowy' z ChatGPT.

### Poprawność odpowiedzi

Model `text-davinci-003` jest zoptymalizowany do generowania tekstów, sprawiających wrażenie że są przygotowane przez człowieka, lecz bez gwarancji że wszystkie informacje w nich są prawdziwe. Dotyczy to także sytuacji gdy nie zleca się modelowi wygenerowania tekstu na jakiś temat na podstawie jego wewnętrznej wiedzy, lecz model ma wyciągnąć informację z przekazanego mu tekstu. Szczególnie gdy parametr `temperature` ma wyższą wartość, model potrafi 'zaokrąglać' informacje - jest bardziej kreatywny, np. przy przetwarzaniu biografii Edwarda Sedlaczka z parametrem `temperature` = 1.0 model zapytany o funkcje i urzędy tej postaci generuje m.in. informację:

1. Kierownik literacki prasy lwowskiej ("Dziennik dla Wszystkich”, „Dziennik Polski”, „Gazeta Lwowska”, „Gazeta Narodowa”, „Przyjaciel Domowy”) i warszawskiej („Biesiada Literacka”, „Echo”, „Kłosy”, „Kurier Codzienny”, „Kurier Warszawski”, „Niwa", "Słowo", "Tygodnik Ilustrowany", "Tygodni Mód i Powieści" , "Tygodnik Powszechny" i "Wiek").

Tymczasem w rzeczywistości bohater biografii był kierownikiem literackim tylko pisma "Przyjaciel Domowy".

Po obniżeniu wartości `temperature` do 0.0 zwracana jest już prawdziwa informacja:

1. Kierownik literacki dwutygodnika lwowskiego „Przyjaciel Domowy” (1 VI 1882)

Wpływ ma jakość odpowiedzi mają także parametry `frequency_penalty` (standardowo wartość 0.8)
i `presence penalty`: kontrolujący tendencję modelu do powtarzania generowanych słów oraz zachęcający model do generowania nowatorskich sformułowań. Manipulowanie nimi spowodowało na przykładowym biogramie Sedlaczka wygenerowanie fałszywego przybliżenia, zamiast:

3. Kancelista w austriackim konsulacie w Kijowie (1895)

otrzymujemy:

3. Konsul w Kijowie (1882-1895)

gdzie odpowiedni fragment biografii brzmi: _"Później pełnił takąż funkcję w austriackim konsulacie w Kijowie (do r. 1895)"_. Ta skłonność do 'halucynacji' jest jednym z głównych problemów przy ekstrakcji informacji z tekstów historycznych, oczywiście dane wyciągane przez model musiałyby być weryfikowane przez ludzkiego eksperta, warto również przeprowadzić test na większej próbie testów i ocenić poprawność (i kompletność) zwracanych przez model danych.

Najbardziej przydatne wartości parametrów (w przypadku wyciągania informacji z tekstów):
- temperature: 0
- top p: 1.0
- frequency penalty: 0.0
- presence penalty: 0.0

### Wiedza z kontekstu

To w czym model bywa zadziwiająco dobry, to umiejętność wyciągania informacji z kontekstu. Dłuższy fragment tej samej biografii Sedlaczka związany jego pracą kancelisty brzmi: _"W r. 1886 S. otrzymał posadę kancelisty w konsulacie austriackim w Warszawie – zapewne za poparciem Władysława Łozińskiego, który opiekował się jego karierą także w l.n. Później pełnił takąż funkcję w austriackim konsulacie w Kijowie (do r. 1895)"_.
z czego model (uruchomiony z właściwymi parametrami!) wyciąga informację:

3. Kancelista w austriackim konsulacie w Kijowie (1895)

Co nie jest przecież (nazwa funkcji/urzędu) podane wprost.

Podobny przykład występuje w biografii Ludwika Mortęskiego (Polski Słownik Biograficzny t. XXII, 1977, s. 9-11), model wyszukał informację o urzędzie sprawowanym przez bohatera biografii:

2. Kasztelan elbląski (1516–1539)

na podstawie wpisu _"Jako kasztelan gdański brał M. udział w licznych komisjach powoływanych przez króla dla rozstrzygania spraw spornych na terenie Prus Królewskich. Dn. 4 III 1516 przeszedł M. na kasztelanię elbląską (po zmarłym Janie Wulkowskim) i trzymał ją do śmierci."_.


## Przykłady

Model: text-davinci-003<br>
Text: biografia Ludwika Mortęskiego (zm. 1539), w języku polskim.
(Polski Słownik Biograficzny t. XXII, 1977, s. 9-11)

### Relacje rodzinne

**Prompt**: From this text extract information about parents, wife, children and grandchildren for the person Ludwik Mortęski

**Result**:
Parents: Ludwik (possibly) and Anna

Wife: Elżbieta z Dąbrówki

Children: Katarzyna, Dorota, Gertruda, Elżbieta, Małgorzata, Ludwik and Melchior

Grandchildren: Magdalena Mortęskiej and Ludwik

### Funkcje i urzędy głównej postaci

**Prompt**: From this text, extract information about the offices, functions and positions held by the person Ludwik Mortęski, present them in the form of a list

**Result**:
Offices, Functions and Positions Held by Ludwik Mortęski:

1. Kasztelan gdański (1512–1516)
2. Kasztelan elbląski (1516–1539)
3. Representative of Prussian States to King Kazimierz Jagiellończyk (1492)
4. Member of the Delegation of Prussian States to the Election of a Polish King (1506)
5. Podkomorzy chełmiński at the Malbork Assembly of Prussian States with Representatives of King Aleksander Jagiellończyk (1503)
6. Representative of Prussian States to Bishop Hiob von Dobenecka (1507)
7. Representative of Prussian States to King Zygmunt I at the Krakow Sejm and Malbork Assembly (1508, 1509, 1511)
8. Defender of Nobility Rights in Discussions at Assemblies and Sejmik in Elbląg, Malbork, Grudziądz and Gdańsk (1507-1530).
9. Opponent to Wojewodas Jan Dabrowski and Mikołaj Wulkowski in 1509
10. Member on Commissions Appointed by the King for Resolving Disputes in Prussia Królewskich(after 1512).
11. Starostwo pokrzywnickie(1505).
12. Starostwo Pokrzywno with Villages Okonin, Nicwałd, Węgrowo Skarszewo Nowawieś i Wiewiórki as a Feudal Estate from Zygmunt Stary for Military Service(1521).

### Lista instytucji

**Prompt**:
From this text, extract information about institutions related to the the person Ludwik Mortęski, present them in the form of a list.

**Result**:
Institutions related to Ludwik Mortęski:

1. Stały Sejmik Prus Królewskich
2. Kapituła Warmińska
3. Rada Pruska
4. Sejmik w Malborku (listopad 1530)
5. Sejmik w Grudziądzu (12/1511)
6. Sejm w Krakowie (1/18/1508)
7. Sejm w Malborku (28/5-8/6/1508)
8. Zamek Radzyń w ziemi chełmińskiej
9. Zamek Pokrzywno
10. Kasztelania Gdańska (4/3/1512)
11. Kasztelania Elbląska (4/3/1516)

### Wynik w formie tabeli

**Prompt**: From this text give the name, surname and date of death of the main character. Show the result in the form of a table.

{TEXT}

```
| Name | Surname | Date of death |
```

**Result**:

```
| ------ | ----------------------- | ---- |
| Ludwik | Mortęski (de Mortangen) | 1539 |
| ------ | ----------------------- | ---- |
```

### Lista urzędów

Text: biografia Mikołaja z Woli (zm. 1346 lub 1347) - w języku polskim.
(Polski Słownik Biograficzny t. XXI, 1976, s. 151)

**Prompt**: From this text, extract information about the offices,
held by the person Mikołaj z Woli, present them in the form of a list

**Result**:

List of offices held by Mikołaj z Woli:
- Kasztelan kruszwicki
- Starosta kujawski
- Podkomorzy brzeski
- Asesor sądu ziemskiego w Inowrocławiu

### Lista urzędów i funkcji w xml

Text: biografia Edwarda Józefa Sedlaczka
(Polski Słownik Biograficzny t. XXXVI, 1995-6, s. 137-138)

**Prompt**: From this text, extract information about the offices,
functions and positions held by the person Edward Józef Sedlaczek, present them in
the form of xml: `<xml><person><office>office, function or position</office><person></xml>`


**Result**:

```
<xml>
  <person>
    <name>Edward Józef Sedlaczek</name>
    <office>Literat</office>
    <office>Kierownik literacki dwutygodnika lwowskiego „Przyjaciel Domowy”</office>
    <office>Kancelista w konsulacie austriackim w Warszawie</office>
    <office>Kierował wicekonsulatem w Batumi (Rosja, 1896–7)</office>
    <office>Agencją konsularną w Nowosielicy (Rosja)</office>
    <office>Agencją konsularną w Burgas (Bułgaria)</office >
    < office > Wicekonsulatem w Batumi </ office >
  	< office > Wicekonsulatem w Burgas </ office >
  	< office > Wicekonsulatem w Ploieşti (Rumunia) </ office >
  	< office > Redagował serię Wydawnictwa Tow. im. P. Skargi </ office >
  </person>
</xml
```

### Relacje rodzinne nr 2

Text: biografia Andrzeja Rosickiego (1814-1904),
(Polski Słownik Biograficzny t. XXXII, 1989-1991, s. 82)

**Prompt**: From this text extract information about parents, wife, siblings, children and grandchildren for the main character

**Result**:

Parents: Walenty and Marianna z Idzikowskich

Wife: Anna z Robowskich

Siblings: Unknown

Children: Józefa Konstancja (born 1859), Antonina Wiktoria (born 1863) and Piotr Michał (born 1862)

Grandchildren: Unknown

### TEI XML output

Text: Fragment Bullarium Poloniae.

**Prompt**: Tag text and convert to TEI XML format.

**Result**:

```
<tei xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Francisco Cruswicz magistro in theologia</title>
      </titleStmt>
    </fileDesc>
  </teiHeader>

  <text xml:lang="lat">
    <p><persName ref="#Cruswicz">Francisco Cruswicz</persName>, magistro in theologia [in civitate Constantiensi commoranti]: Eidem decano eccl. s. Floriani extra muros Crac. (<amt type="currency" quantity="15" unit="argentum polonorum">15 m. arg.</amt> p.), canonica-tus in eccl. s. Michaelis in castro Crac.(<amt type="currency" quantity="12" unit="argentum polonorum">12 m.</amt>. arg p.), per obitum apud SA ea vacante Nicolai Falkemberg vacans, confertur.;s. m scholastico et cantori ac custodi Crac.<num value="11">XI</num>,<num value = "13">XIII</num>. </p>
  </text>
</tei>
```

### Analiza NER fragmentu publikacji

Text: Fragment publikacji Stanisława Bodniaka _"Polska a Bałtyk za ostatniego z Jagiellona"_ (1946):

Było to w roku 1552. Już od czerwca bawił król Zygmunt August w pomorskiej  ziemi, lipiec i sierpień spędził w Gdańsku, we wrześniu po kilkudniowym  pobycie w Malborgu w czasie sejmiku podążył do Królewca na zaproszenie ks. Albrechta. Towarzyszyli mu w podróży hetman Jan Tarnowski, marszałek koronny Piotr Kmita, bp. Stanisław Hozjusz, kanclerz Jan Ocieski, podkanclerzy Jan Przerębski i inni przedniejsi senatorowie i dostojnicy polscy obok przedstawicieli świata umysłowego w osobach Marcina Kromera, Szymona Maricjusa-Czystochlebskiego i Łukasza Górnickiego. Orszak dworzan i rycerstwa przenosił 5 tysięcy osób.
Najokazalej podejmował swego władcę Gdańsk, cały roztaczając przed nim przepych, na jaki pozwalało miastu u ujścia Wisły rosnące pod polskim panowaniem bogactwo. Stawił się tam z Zachodniego Pomorza ks. Barnim XI w 300 koni i ze znaczną liczbą pomorskiej szlachty, ażeby spotkać się ze swym dostojnym krewniakiem i suwerenem z tytułu lenna na Lęborgu i Bytowie. W programie gdańskim przyjęcia, obfitującym w uczty, zabawy i gry rycerskie, nie zapomniano o morzu.
W dniu 13 lipca zwiedził król w towarzystwie ks. Barnima statek na stoczni  w Gdańsku i przyglądał się jego spuszczeniu na wodę. W tydzień później (20 VII) wybrał się barką, wybitą czerwonym suknem i przybraną chorągiewkami, na obejrzenie warowni, nazywanej wówczas „Latarnią” albo „wieżą”,* położonej u ujścia Wisły. Gdy tam wchodził, grzmiały na jego cześć działa warowni i okrętu „Żelazny Henryk", naprzeciw niej umieszczonego , miotając na morze ogniste kule, Po posiłku w warowni powrócił na swą barkę i popłynął dalej — na Bałtyk, wtedy spokojny. Wielu także panów polskich z otoczenia zapuściło się daleko na fale, korzystając z pogody.

**Prompt**: W podanym tekście wyszukaj informacje o osobach, znalezione osoby wypisz w formie listy, jeżeli są znane funkcje lub urzędy osób umieść te informacje w nawiasach obok osób:

**Wynik**:

- Zygmunt August (król)
- Jan Tarnowski (hetman)
- Piotr Kmita (marszałek koronny)
- Stanisław Hozjusz (bp)
- Jan Ocieski (kanclerz)
- Jan Przerębski (podkanclerzy)
- Marcin Kromer
- Szymon Maricjus-Czystochlebski
- Łukasz Górnicki
- Barnim XI (książę)


### Inne przykłady

Skrypty do tych i pozostałych przykładów w folderze `src`, wyniki w folderze `output`.

### Analiza relacji rodzinnych na serii biografii

Jak model GPT-3 ('davinci-003') radzi sobie z rozpoznawaniem relacji rodzinnych można spróbować ocenić 
na większej próbce 50 biogramów wybranych z t. 1-51 Polskiego Słownika Biograficznego. Biogramy mają różną długość, od mniej więcej 1 tys. znaków do kilkudziesięciu tys. Ograniczeniem jest liczba tokenów, które 'davinci' jest w stanie przetworzyć w jednym zapytaniu - 4000 wliczając wygenerowaną odpowiedź. W przypadku dłuższych biogramów zostały one wstępnie 'streszczone': uwzględniono 5 pierwszych i pięć ostatnich zdań (pomijając najpierw część bibliograficzną biogramu) oraz wszystkie zdania pomiędzy nimi jeżeli zawierały treść wskazującą na informacje o rodzinie i krewnych (biogram został podzielony na zdania za pomocą spaCy, w zdaniach analizowano formy podstawowe tokenów i porównywano z przygotowanym słownikiem pojęć związanych z pokrewieństwem). Skracanie biogramów może oczywiście wpłynąć negatywnie na wyniki. W teście skupiono się na pokrewieństwie w stosunku do głównego bohatera/bohaterki biogramu.

Teksty biogramów przetwarzane były promptem o treści:

```
Na podstawie podanego tekstu wyszukaj
wszystkich krewnych lub powinowatych głównego bohatera tekstu.
Możliwe rodzaje pokrewieństwa: ojciec, matka, syn, córka, brat, siostra, żona, mąż,
teść, teściowa, dziadek, babcia, wnuk, wnuczka, szwagier, szwagierka, siostrzeniec,
siostrzenica, bratanek, bratanica, kuzyn, kuzynka, zięć, synowa, teść bratanicy.
Wynik wypisz w formie listy nienumerowanej, w formie:
główny bohater -> rodzaj pokrewieństwa -> osoba
Każda pozycja w osobnej linii. Na przykład:
- główny bohater -> brat -> Jan Kowalski
- główny bohater -> siostra -> Anna
Pomiń rodzaj pokrewieństwa jeżeli nie występuje w tekście.
Jeżeli w tekście nie ma żadnych informacji o pokrewieństwach głównego bohatera
napisz: brak danych.
```

(kod skryptu w pliku psb_relacje_rodzinne.py)

Dla 36 z 50 biogramów model znalazł jakieś relacje - w sumie 182 przypadki pokrewieństwa głównego bohatera z inną osobą. Po szczegółowym przeanalizowaniu, **38 z nich było błędne (20.9%)**, **144 oceniono jako prawdziwe (79.1%)**.

Szczegółowa lista **znalezionych** relacji:

| Postać -> rodzaj pokrewieństwa/relacja -> osoba spokrewniona | Prawidłowa? |
| ------------------------------------------------------------ | :---------: |
| **Aloe Franciszek Eljasz** | |
| główny bohater -> ojciec -> Jan Baptysty d'Aloy | True |
| główny bohater -> matka -> Henryka Rakocy | True |
| główny bohater -> brat -> Emanuel | True |
| główny bohater -> siostry-> piękne siostry | **False** |
| **Bezprym** | |
| główny bohater -> ojciec -> Bolesław Chrobry | True |
| główny bohater -> matka -> nieznana Węgierka | True |
| główny bohater -> brat -> Mieszko II | True |
| główny bohater -> brat -> Otto | True |
| główny bohater-> teść bratanicy-> cesarz Konrad II | **False** |
| **Dąbrowska_Pelagia** | |
| główny bohater -> żona -> Dąbrowska Pelagia | **False** |
| główny bohater -> synowie -> brak danych | **False** |
| **Daszyński Ignacy** | |
| główny bohater -> ojciec -> Ferdynand | True |
| główny bohater -> matka -> Kamila z Mierzeńskich | True |
| główny bohater -> brat -> Feliks | True |
| główny bohater-> żona (pierwsza)-> Maria z Paszkowskich | True |
| główny bohater-> żona (druga)-> Cecylia Kempnerówna | True |
| **Dzierżek_Natalia** | |
| Główny bohater -> matka -> Maria z Piątkowskich Nieczuja-Dzierżków | True |
| Główny bohater -> ojciec -> Henryk | True |
| Główny bohater -> siostra rodzona-> Henryka Piątkowskiego | **False** |
| Główny bohater -> teść bratanicy-> Tadeusz Gałecki | **False** |
| Główny bohater -> synowa teścia bratanicy-> Teresa z Wołowskich Prażmowska | **False** |
| **Eufrozyna** | |
| Główny bohater -> ojciec -> Kazimierz | True |
| Główny bohater -> matka -> Eufrozyna | **False** |
| Główny bohater -> syn -> Władysław Łokietek | True |
| Główny bohater -> syn -> Kazimierz | True |
| Główny bohater-> syn-> Ziemowit | True |
| Główny bohater-> mąż-> Mszczuja II | True |
| **Ewild al. Eywild** | |
| Główny bohater -> ojciec -> Stanisław Brzeski | **False** |
| główny bohater -> brat -> Eynur | True |
| główny bohater -> dziadek -> Jawilt | **False** |
| główny bohater -> wnukowie-> Dowgird i Daszko Eywiltowicze | **False** |
| **Fuzorius Bartłomiej** | |
| Główny bohater -> ojciec -> Stanisław Lwowczyk | True |
| **Gliński Iwan** | |
| główny bohater -> ojciec -> Lew Borysowicz | True |
| główny bohater -> brat rodzony -> Michał Mamaj | **False** |
| główny bohater -> bratanica -> Helena | True |
| **Hincza z Rogowa** | |
| główny bohater -> ojciec -> Hinczka z Rogowa | True |
| główny bohater -> brat -> Jakub | True |
| główny bohater -> siostra -> Małgorzata | True |
| główny bohater -> żona-> Dorota z Koziegłowskich h. Lis | True |
| główny bohater-> teść bratanicy-> Bartłomiej Gruszczyński | **False** |
| **Jadwiga Jagiellonka** | |
| główny bohater -> ojciec -> Kazimierz Jagiellończyk | True |
| główny bohater -> matka -> Elżbieta Rakuszanka | True |
| główny bohater -> brat -> Aleksander Jagiellończyk | True |
| główny bohater -> siostra-> Sonka Jagiellonka | **False** |
| główny bohater-> żona-> Jerzy Bawarski | **False** |
| główny bohater-> córka-> Elżbieta Bawarska | True |
| główny bohater-> córka-> Małgorzata Bawarska | True |
| główny bohater-> teść bratanicy -> Ludwik Bawarski | **False** |
| **Kakowski Aleksander** | |
| główny bohater -> ojciec -> Franciszek | True |
| główny bohater -> matka -> Paulina z Ossowskich | True |
| **Krumhausen Gabriel** | |
| główny bohater -> ojciec -> Joachim | True |
| główny bohater -> matka -> Gertruda | True |
| główny bohater -> brat -> Joachim | True |
| główny bohater -> żona-> Konstancja Falcke | True |
| **Łańcucki Wojciech** | |
| główny bohater -> ojciec -> Stanisław | True |
| **Leymiter Stanisław** | |
| główny bohater -> ojciec -> Mikołaj | True |
| główny bohater -> matka -> Benigna | True |
| główny bohater -> żona -> Zofia | True |
| główny bohater -> syn -> Jan | True |
| główny bohater -> syn-> Stanisław | True |
| główny bohater-> córka-> Barbara | True |
| główny bohater-> córka-> Benigna | True |
| główny bohater-> teść-> Jan Tesznar | True |
| główny bohater-> brat teściowej-> Mikołaj Kreidler | **False** |
| główny bohater-> siostra teściowa-> Agnieszka Tesznarowa | **False** |
| główny bohater-> siostra teściowa-> Katarzyna Tesznarowa | **False** |
| **Mierzeński Aleksander** | |
| główny bohater -> brat -> Jan Mierzeński | True |
| główny bohater -> brat -> Samuel Mierzeński | True |
| główny bohater -> syn brata -> Jan Mierzeński | True |
| główny bohater -> synowa syna brata-> Mariana z Kawcenich | **False** |
| **Mostowska z Bujwidów** | |
| główny bohater -> ojciec -> Odo Bujwid | True |
| główny bohater -> matka -> Kazimiera z Klimontowiczów | True |
| główny bohater -> siostra -> Kazimiera Rouppertowa | True |
| główny bohater -> siostra-> Jadwiga Demelowa | True |
| główny bohater-> siostra-> Helena Jurgielewiczowa | True |
| główny bohater-> mąż-> Włodzimierz Mostowski | True |
| główny bohater-> syn-> Jerzy Mostowski | True |
| główny bohater-> syn-> Czesław Mostowski | True |
| **Patruus** | |
| główny bohater -> ojciec -> Jan Patruus z Koła | **False** |
| główny bohater -> syn -> Jan | True |
| **Pichgiel** | |
| główny bohater -> ojciec -> Matthias Pichel | **False** |
| główny bohater -> matka -> Barbara z domu Biettin | True |
| główny bohater -> syn -> Christian Pichgiel młodszy | True |
| główny bohater -> syn -> Johan Pichgiel | True |
| główny bohater -> syn-> Daniel Pichgiel | True |
| główny bohater-> syn-> Emanuel Pichgiel | True |
| główny bohater-> kuzyn-> Matthias Pichgiel młodszy | True |
| **Pion Maurice** | |
| główny bohater -> ojciec -> Antoine Claude | True |
| główny bohater -> matka -> Anna z domu Pauli | True |
| główny bohater -> żona -> Aleksandra Antonina z Budzyńskich | True |
| główny bohater -> synowie-> Adolf Stanisław, Władysław Stanisław | True |
| główny bohater-> córki-> Adela, Kornelia | True |
| główny bohater-> młodsza siostra-> Eugenia | True |
| **Piotrowiczowa z Rogolińskich** | |
| główny bohater -> ojciec -> Zygmunt Rogoliński | True |
| główny bohater -> matka -> Ansberty z Badeńskich | True |
| główny bohater -> mąż -> Konstantego Piotrowicza | True |
| główny bohater -> teść bratanicy-> Józef Dworzaczek | **False** |
| **Renard Benedykt** | |
| główny bohater -> ojciec -> Andrzej | True |
| główny bohater -> brat -> Jan Baptysta | True |
| główny bohater -> siostra -> Anna Orzelska | **False** |
| główny bohater -> siostra-> Anna Katarzyna | True |
| **Rossi Piotr** | |
| główny bohater -> ojciec -> Andrzej | True |
| główny bohater -> żona -> Małgorzata | True |
| główny bohater -> syn -> Andrzej | True |
| główny bohater -> syn -> Kornel | True |
| główny bohater-> syn-> Klemens | True |
| główny bohater-> córka-> Izabella | True |
| główny bohater-> córka-> Feliksa | True |
| **Sapieha_Jan_Fryderyk** | |
| główny bohater -> ojciec -> Fryderyk | True |
| główny bohater -> matka -> Ewa ze Skaszewskich | True |
| główny bohater -> brat -> Tomasz Kazimierz | True |
| główny bohater -> brat stryjeczny-> Jan Ferdynand | True |
| główny bohater-> kuzyn-> Kazimierz Leon Sapieha | True |
| główny bohater-> hetman P. J. Sapieha (stryjeczny wujek) | **False** |
| główny bohater-> syn-> Mikołaj Leon | True |
| główny bohater-> syn-> Kazimierz Władysław | True |
| głowny bohater-> syn-> Paweł Franciszek | True |
| **Śląska Aleksandra** | |
| główny bohater -> ojciec -> Edmund Wąsik | True |
| główny bohater -> matka -> Helena z Masłowskich | True |
| główny bohater -> siostra przyrodnia-> Bożena Jewasińska | True |
| główny bohater -> brat-> Olgierd Edmund Wąsik | True |
| główny bohater -> mąż pierwszy-> Czesław Michał Górski | True |
| główny bohater -> syn-> Szczęsny Tadeusz Górski | True |
| główny bohater -> mąż drugi-> Stanisław Śląski | **False** |
| **Słowicki Józef** | |
| główny bohater -> ojciec -> Józef | True |
| **Śniadecka Kornelia Ludwika**
| główny bohater -> ojciec -> Jędrzej Śniadecki | True |
| główny bohater -> matka -> Konstancja z Mikułowskich | True |
| główny bohater -> siostra -> Zofia Balińska | True |
| główny bohater -> brat-> Józef Konstanty Śniadecki | True |
| główny bohater-> teść bratanicy-> Kazimierz Sulistrowski | **False** |
| główny bohater-> stryj-> Jan Śniadecki | True |
| główny bohater-> siostrzenica-> Antonina Śniadecka | **False** |
| główny bohater-> stryjenka-> Salomea Bécu | **False** |
| główny bohater-> wujek (brat ojca) -> Ignacy Abramowicz | **False** |
| główny bohater-> wujek (brat ojca) -> Mikołaj Abramowicz | **False** |
| **Spektor Mordechaj** | |
| główny bohater -> żona -> Izabela z Frydbergów | True |
| **Stańczakowa ze Strancmanów** | |
| główny bohater -> ojciec -> Adolf Strancman | True |
| główny bohater -> matka -> Maria Weinfeld | True |
| główny bohater -> brat -> Jan Strancman | True |
| główny bohater -> mąż-> Zdzisław Stańczak | True |
| główny bohater-> córka-> Anna Stańczak | True |
| główny bohater-> zięć-> Tadeusz Sobolewski | True |
| **Stanisław_Cielątko** | |
| główny bohater -> ojciec -> Jan | True |
| główny bohater -> brat -> Jan Cielątki z Liszyna i Prusiecka | True |
| główny bohater -> brat -> Mikołaj | True |
| główny bohater-> siostrzenica-> Małgorzata Marta | **False** |
| główny bohater-> teść bratanicy-> Piotr Cikowski z Mikluszowic | True |
| **Strzelecki Wiesław Marian** | |
| główny bohater -> ojciec -> Felicjan | True |
| główny bohater -> matka -> Stefania z Łękawskich | True |
| główny bohater -> syn -> Krzysztof | True |
| główny bohater-> żona-> Barbara z Krzemińskich | True |
| **Świrski Jerzy Włodzimierz** | |
| główny bohater -> ojciec -> Włodzimierz | True |
| główny bohater -> matka -> Celina z Wasiłowskich | True |
| główny bohater -> brat -> Małgorzata | **False** |
| główny bohater -> siostrzenica-> Maria Konopnicka | **False** |
| **Szapira Majer** | |
| główny bohater -> ojciec -> Jakub Szamszon | True |
| główny bohater -> matka -> Margula Szor | True |
| główny bohater -> brat -> Abraham | True |
| główny bohater-> dziadek-> Samuel Izaak Szor | True |
| główny bohater-> żona-> Małka Towa | True |
| główny bohater-> teść bratanicy-> Salomon Moskowicz | **False** |
| **Szapocznikow_Alina** | |
| główny bohater -> ojciec -> Jakub | True |
| główny bohater -> matka -> Regina | True |
| główny bohater -> brat -> Mirosław | True |
| główny bohater-> syn-> Piotr Stanisławski | True |
| **Szczubioł_Andrzej** | |
| główny bohater -> ojciec -> Stefan z Jasieńca i Ciechomic | True |
| główny bohater -> matka -> Sędka | True |
| główny bohater -> brat -> Mikołaj z Ciechomic | True |
| główny bohater -> brat-> Jan z Dłotowa | True |
| główny bohater-> żona-> Anna | True |
| główny bohater-> syn-> Maciej | True |
| główny bohater-> syn-> Szymon zwany Gostyńskim z Ciechomic | True |
| główny bohater-> syn-> Andrzej | True |
| główny bohater-> teść bratanicy -> Ścibor z Sąchocina h. Rogala | **False** |
| **Szumski Boksa** | |
| główny bohater -> ojciec -> Krzesław z Szumska | True |
| główny bohater -> brat -> Jan (Jaszek) Rej z Nagłowic | True |
| główny bohater -> żona -> Stachna h. Poraj | True |
| główny bohater -> syn-> Jan Rey | True |
| główny bohater-> teść-> Chociemir Garnka (Garnysza) z Pojałowic i Suchcic | **False** |
| główny bohater-> teściowa-> Świątka, żona Mikołaja z Barczkowic, następnie Wisława z Kościelca | **False** |
| główny bohater-> bratanek-> Jan Rey (zm. 1468) | True |
| główny bohater-> bratanek-> Stogniew, żonaty z Małgorzatą | True |

Ważne jest oczywiście także to czego model **nie znajduje**.