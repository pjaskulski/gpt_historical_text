# GPT3 - Large Language Model as a tool for extracting knowledge from text - tests on historical examples.

Testy modeli GPT 3.5 udostępnionych przez API OpenAI przeprowadzane na fragmentach publikacji i opracowań historycznych w celu automatycznej ekstrakcji informacji, wyciągania ustrukturyzowanych danych ze źródeł dostępnych w formie nieustrukturyzowanej. Testowany materiał to głównie fragmenty
biografii postaci historycznych.

[Notatki](#notatki)
  - [Wstępne informacje](#wstępne-informacje)
  - [Porównanie dostępnych modeli](#porównanie-dostępnych-modeli)
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
  - [Inne przykłady](#inne-przykłady)


## Notatki

### Wstępne informacje

Testy zostały przeprowadzone poprzez API udostępnione przez firmę OpenAI.

Istnieją ograniczenia podczas korzystania z API dotyczące liczby zapytań na minutę (3 tys.) i liczby przetworzonych tokenów na minutę (250 tys.).

Token jest rozumiany trochę inaczej niż zwykle w NLP, tu dłuższe wyrazy są rozbijane na krótkie tokeny 3-4 znaki, oprócz tego tokenem są też znaki interpunkcyjne itp. Podawane jest że średnio token to 4 znaki w języku angielskim, na stronie OpenAI jest narzędzie w którym (https://beta.openai.com/tokenizer) można wkleić tekst i zobaczyć ile zawiera tokenów.

Przykładowo biografia Edwarda Józefa Sedlaczka (Polski Słownik Biograficzny t. XXXVI, 1995-6, s. 137-138) zawiera 4433 znaków co przekłada się na 2291 tokenów. W przypadku tekstów polskich sytuację pogarszają polskie znaki, wygląda na to że każdy dwubajtowy unicodowy znak jest traktowany jako osobny token.

### Porównanie dostępnych modeli

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

Parametr `temperature` ma domyślnie wartość 0.5, jego zmniejszenie że odpowiedź jest bardziej konkretna, deterministyczna, mniej losowa. Podobny wpływ ma obniżenie domyślnej wartości parametru `top_p` = 1.0.

Wielokrotne uruchamianie tego samego zapytania może dawać nieco inne wyniki.

Zapytania uruchamiane przez API nie znają kontekstu zapytań uruchamianych chwilę przed,
inaczej niż w trakcie rozmowy z ChatGPT, należy za każdym razem podawać całą informację w zapytaniu.

Ogromne znaczenie ma konstrukcja zapytania (prompt), wydaje się że pytania w języku angielskim nawet w odniesieniu do polskiego tekstu dają lepsze rezultaty. Zadanie zlecone modelowi powinno być napisane
językiem prostym, konkretnym, ale nie musi być bardzo krótkie. Dobry wpływ na jakość odpowiedzi mają podane modelowi przykłady, czego i w jakiej formie się spodziewamy.

### Poprawność odpowiedzi

Model `text-davinci-003` jest zoptymalizowany do generowania tekstów, sprawiających wrażenie że są przygotowane przez człowieka, lecz bez gwarancji że wszystkie informacje w nich są prawdziwe. Dotyczy to także sytuacji gdy nie zleca się modelowi wygenerowania tekstu na jakiś temat na podstawie jego wewnętrznej wiedzy, ale też przypadku gdy model ma wyciągnąć informację z przekazanego mu tekstu. Szczególnie gdy parametr `temperature` ma wyższą wartość, model potrafi 'zaokrąglać' informacje, np. przy przetwarzaniu biografii Edwarda Sedlaczka z parametrem `temperature` = 1.0 model zapytany o funkcje i urzędy tej postaci generuje m.in. informację:

1. Kierownik literacki prasy lwowskiej ("Dziennik dla Wszystkich”, „Dziennik Polski”, „Gazeta Lwowska”, „Gazeta Narodowa”, „Przyjaciel Domowy”) i warszawskiej („Biesiada Literacka”, „Echo”, „Kłosy”, „Kurier Codzienny”, „Kurier Warszawski”, „Niwa", "Słowo", "Tygodnik Ilustrowany", "Tygodni Mód i Powieści" , "Tygodnik Powszechny" i "Wiek").

Tymczasem w rzeczywistości bohater biografii był kierownikiem literackim tylko pisma "Przyjaciel Domowy".

Po obniżeniu wartości `temperature` do 0.0 zwracana jest już prawdziwa informacja:

1. Kierownik literacki dwutygodnika lwowskiego „Przyjaciel Domowy” (1 VI 1882)

Ciekawy wpływ ma poprawność odpowiedzi ma także parametr `frequency_penalty` (standardowo wartość 0.8) zmniejszenie go do zera powoduje na przykładowym biogramie Sedlaczka generowanie fałszywych przybliżeń, zamiast:

3. Kancelista w austriackim konsulacie w Kijowie (1895)

otrzymujemy:

3. Konsul w Kijowie (1882-1895)

gdzie odpowiedni fragment biografii brzmi: _"Później pełnił takąż funkcję w austriackim konsulacie w Kijowie (do r. 1895)"_.

### Wiedza z kontekstu

To w czym model bywa zadziwiająco dobry, to umiejętność wyciągania informacji z kontekstu. Np. w tej samej biografii fragment tekstu brzmi: _"W r. 1886 S. otrzymał posadę kancelisty w konsulacie austriackim w Warszawie – zapewne za poparciem Władysława Łozińskiego, który opiekował się jego karierą także w l.n. Później pełnił takąż funkcję w austriackim konsulacie w Kijowie (do r. 1895)"_.
z czego model wyciąga informację:

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

### Inne przykłady

Skrypty do tych i pozostałych przykładów w folderze `src`, wyniki w folderze `output`.
