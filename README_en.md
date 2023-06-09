# GPT3/GPT4 - Large Language Model as a tool for extracting knowledge from text - tests on excerpts from historical publications

(Polish version: GPT3/GPT4 - Large Language Model jako narzędzie do wydobywania wiedzy z tekstu - testy na fragmentach publikacji historycznych - [link](https://github.com/pjaskulski/gpt_historical_text))


Tests of GPT-3 and GPT-4 models provided by OpenAI's API are conducted on excerpts of historical publications and studies for the purpose of automatic information extraction and deriving structured data from unstructured sources. The test material primarily consists of excerpts from biographies of historical figures.

[Notes](#notes)
  - [Preliminary information](#preliminary-information)
  - [References](#references)
  - [Comparison of available GPT models](#comparison-of-available-gpt-models)
  - [Technical notes](#technical-notes)
  - [Correctness of answers](#correctness-of-answers)
  - [Knowledge from context](#knowledge-from-context)

[Examples](#examples)
  - [Family relationships](#family-relationships)
  - [Functions and offices of the main character](#functions-and-offices-of-the-main-character)
  - [List of institutions](#list-of-institutions)
  - [The result in the form of a table](#the-result-in-the-form-of-a-table)
  - [List of offices](#list-of-offices)
  - [List of offices and functions in xml](#list-of-offices-and-functions-in-xml)
  - [Family relationships - test 2](#family-relationships---test-2)
  - [TEI XML output](#tei-xml-output)
  - [NER analysis of an excerpt from a publication](#ner-analysis-of-an-excerpt-from-a-publication)
  - [Other examples](#other-examples)
  - [Analysis of family relations on a series of biographies](#analysis-of-family-relations-on-a-series-of-biographies)
  - [Analysis of family relationships in a series of biographies - GPT-4 model](#analysis-of-family-relationships-in-a-series-of-biographies---gpt-4-model)
  - [Processing of the Historical and Geographical Dictionary entry into XML format - GPT4](#processing-of-the-historical-and-geographical-dictionary-entry-into-xml-format---gpt4)
  - [Formatting results - JSON](#formatting-results---json)

## Notes

### Preliminary information

Definition of GPT-3 (written by ChatGPT):
"GPT-3 (Generative Pretrained Transformer 3) is the third version of artificial intelligence developed by OpenAI. It is one of the largest language models in the world, trained on massive text datasets to understand and generate human language. GPT-3 is used for many applications, such as text generation, translation, answering questions, and text comprehension. The model utilizes the Transformer architecture and can learn tasks with a small amount of data, making it a highly efficient and flexible tool for various applications."

GPT-3 tests were conducted through the API provided by OpenAI, mainly using the `text-davinci-003` model.

There are limitations when using the API regarding the number of requests per minute (3,000) and the number of processed tokens per minute (250,000).

A token is understood a bit differently than usual in NLP; here, longer words are broken down into shorter 3-4 character tokens, in addition to punctuation marks, etc. It is stated that on average, a token consists of 4 characters in English. On the OpenAI website, there is a tool (https://beta.openai.com/tokenizer) where you can paste text and see how many tokens it contains.

For example, the biography of Edward Józef Sedlaczek (Polish Biographical Dictionary vol. XXXVI, 1995-6, pp. 137-138) contains 4,433 characters, which translates to 2,291 tokens. In the case of Polish texts, the situation is worsened by Polish characters, as it seems that each double-byte Unicode character is treated as a separate token.

### References

- _"Structured information extraction from complex scientific text with fine-tuned large language models"_ (Alexander Dunn, John Dagdelen, Nicholas Walker, Sanghoon Lee, Andrew S. Rosen, Gerbrand Ceder, Kristin Persson and Anubhav Jain) [link](https://arxiv.org/pdf/2212.05238.pdf)

- _"Text Pattern Extraction: Comparing GPT-3 & Human-in-the-Loop Tool"_ (Maeda Hanafi) [link](https://towardsdatascience.com/text-pattern-extraction-comparing-gpt-3-human-in-the-loop-tool-f2380fd13cf1)

- _"Getting tabular data from unstructured text with GPT-3: an ongoing experiment"_ (ROBERTO ROCHA) [link](https://robertorocha.info/getting-tabular-data-from-unstructured-text-with-gpt-3-an-ongoing-experiment/)

- _"Advanced NER With GPT-3 and GPT-J"_ (Maxime Cupani) [link](https://towardsdatascience.com/advanced-ner-with-gpt-3-and-gpt-j-ce43dc6cdb9c)

- _"Relationship Extraction with GPT-3. Accelerate knowledge graph construction with GPT-3"_ (Sixing Huang) [link](https://medium.com/geekculture/relationship-extraction-with-gpt-3-bb019dcf41e5)

- _"Language Models are Few-Shot Learners"_ (Tom B. Brown et al.) [link](https://arxiv.org/abs/2005.14165)

- _"Training language models to follow instructions with human feedback"_ (Long Ouyang et al., OpenAI) [link](https://arxiv.org/pdf/2203.02155.pdf)


### Comparison of available GPT models

The best model `text-davinci-003` (which is also the most expensive language model in OpenAI) has a limitation of 4,000 tokens, which applies to both input and output combined.

Weaker models, such as `text-curie-001` or `text-babbage-001`, provide noticeably worse results when extracting data from the provided text, for example:

Roles/positions from Edward Sedlaczek's biography according to `text-davinci-003` (with standard parameter settings, e.g., `temperature` = 0.5):

(biographies are processed in Polish, all model results will also be presented in Polish)

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

Functions/offices according to the `text-curie-001` model (parameters as above):

- literat
- urzędnik
- kierownik literacki dwutygodnika lwowskiego „Przyjaciel Domowy”
- posada kancelisty w konsulacie austriackim w Warszawie
- kierował kolejno wicekonsulatem w Batumi (Rosja, 1896–7), a od r.n. – agencją konsularną w Nowosielicy (Rosja), agencją konsularną w Burgas (Bułgaria), wicekonsulatem w Batumi, wicekonsulatem w Burgas i wicekonsulatem w Ploieşti (Rumunia)

These weaker models, also have greater limitations: up to 2,000 tokens per query, but are much cheaper.

### Technical notes

The `temperature` parameter has a value of 0.0 - 1.0; a lower value makes the response more specific, deterministic, less random, and less creative. A higher value allows the model more flexibility. Alternatively, you can modify the default value of the `top_p` parameter = 1.0 by reducing its value - however, it is not recommended to modify both parameters simultaneously (see [API reference](https://beta.openai.com/docs/api-reference/completions/create)).

Running the same query multiple times may yield slightly different results if the temperature parameter value is greater than zero.

Queries run through the API do not know the context of queries run moments before, unlike during a conversation with ChatGPT, so you need to provide all the information in the query each time.

The construction of the query (prompt) is of great importance. Questions in English concerning the provided Polish text work quite correctly and sometimes even yield better results. The task assigned to the model should be written in simple, specific language, but it does not have to be very short. Providing the model with examples of what we expect and in what form has a positive impact on the quality of the response.

Responses from the `davinci-003` model given through the API often differ from the results of questions asked during a 'conversation' with ChatGPT.

### Correctness of answers

The `text-davinci-003` model is optimized for generating texts that give the impression of being prepared by a human, but without a guarantee that all information in them is true. This also applies to situations where the model is not asked to generate text on a given topic based on its internal knowledge, but rather to extract information from the provided text. Especially when the temperature parameter has a higher value, the model tends to 'round off' information - it becomes more creative, for example, when processing Edward Sedlaczek's biography with the `temperature` parameter = 1.0, the model, when asked about the roles and positions of this figure, generates information such as:

1. Kierownik literacki prasy lwowskiej ("Dziennik dla Wszystkich”, „Dziennik Polski”, „Gazeta Lwowska”, „Gazeta Narodowa”, „Przyjaciel Domowy”) i warszawskiej („Biesiada Literacka”, „Echo”, „Kłosy”, „Kurier Codzienny”, „Kurier Warszawski”, „Niwa", "Słowo", "Tygodnik Ilustrowany", "Tygodni Mód i Powieści" , "Tygodnik Powszechny" i "Wiek").

In reality, the subject of the biography was the literary editor of only the magazine "Przyjaciel Domowy" (The Home Friend).

After reducing the `temperature` value to 0.0, the true information is returned:

1. Kierownik literacki dwutygodnika lwowskiego „Przyjaciel Domowy” (1 VI 1882)

The quality of the response is also influenced by the parameters `frequency_penalty` (default value 0.8) and `presence_penalty`: controlling the model's tendency to repeat generated words and encouraging the model to generate innovative formulations. Manipulating these parameters resulted in a false approximation in the example of Sedlaczek's biogram, instead of:

3. Kancelista w austriackim konsulacie w Kijowie (1895)

the result is:

3. Konsul w Kijowie (1882-1895)

where the relevant fragment of the biography reads: "_Later, he held a similar position at the Austrian consulate in Kyiv (until 1895)_". This tendency to 'hallucinate' is one of the main problems when extracting information from historical texts. Of course, the data extracted by the model would have to be verified by a human expert. It is also worthwhile to conduct a test on a larger sample of tests and assess the correctness (and completeness) of the data returned by the model.

The most useful parameter values (for extracting information from texts) are:

- temperature: 0
- top p: 1.0
- frequency penalty: 0.0
- presence penalty: 0.0

### Knowledge from context

One thing the model is surprisingly good at is extracting information from context. A longer fragment of the same biography of Sedlaczek related to his work as a clerk reads: "In 1886, S. received a position as a clerk in the Austrian consulate in Warsaw - probably with the support of Władysław Łoziński, who also took care of his career in the following years. Later, he held a similar position at the Austrian consulate in Kyiv (until 1895)". From this, the model (run with the appropriate parameters!) extracts the information:

3. Kancelista w austriackim konsulacie w Kijowie (1895)

Which, after all, is not (the name of the function/office) stated explicitly (only 'similar position' is mentioned).

A similar example can be found in the biography of Ludwik Mortęski (Polski Słownik Biograficzny vol. XXII, 1977, pp. 9-11), where the model found information about the office held by the biography's subject:

2. Kasztelan elbląski (1516–1539) - Castellan of Elbląg (1516-1539)

based on the entry "As the castellan of Gdańsk, M. took part in numerous commissions appointed by the king to settle disputed matters in the territory of Royal Prussia. On March 4, 1516, M. moved to the Elbląg castellany (after the deceased Jan Wulkowski) and held it until his death.".


## Examples

Model: text-davinci-003<br>
Text: biografia Ludwika Mortęskiego (zm. 1539), w języku polskim.
(Polski Słownik Biograficzny t. XXII, 1977, s. 9-11)

### Family relationships

**Prompt**: From this text extract information about parents, wife, children and grandchildren for the person Ludwik Mortęski

**Result**:
Parents: Ludwik (possibly) and Anna

Wife: Elżbieta z Dąbrówki

Children: Katarzyna, Dorota, Gertruda, Elżbieta, Małgorzata, Ludwik and Melchior

Grandchildren: Magdalena Mortęskiej and Ludwik

### Functions and offices of the main character

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

### List of institutions

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

### The result in the form of a table

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

### List of offices

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

### List of offices and functions in xml

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

### Family relationships - test 2

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

### NER analysis of an excerpt from a publication

Text: Excerpt from Stanislaw Bodniak's publication _"Polska a Bałtyk za ostatniego z Jagiellona"_ (1946) (Poland and the Baltic during the last of the Jagiellons):

Było to w roku 1552. Już od czerwca bawił król Zygmunt August w pomorskiej  ziemi, lipiec i sierpień spędził w Gdańsku, we wrześniu po kilkudniowym  pobycie w Malborgu w czasie sejmiku podążył do Królewca na zaproszenie ks. Albrechta. Towarzyszyli mu w podróży hetman Jan Tarnowski, marszałek koronny Piotr Kmita, bp. Stanisław Hozjusz, kanclerz Jan Ocieski, podkanclerzy Jan Przerębski i inni przedniejsi senatorowie i dostojnicy polscy obok przedstawicieli świata umysłowego w osobach Marcina Kromera, Szymona Maricjusa-Czystochlebskiego i Łukasza Górnickiego. Orszak dworzan i rycerstwa przenosił 5 tysięcy osób.
Najokazalej podejmował swego władcę Gdańsk, cały roztaczając przed nim przepych, na jaki pozwalało miastu u ujścia Wisły rosnące pod polskim panowaniem bogactwo. Stawił się tam z Zachodniego Pomorza ks. Barnim XI w 300 koni i ze znaczną liczbą pomorskiej szlachty, ażeby spotkać się ze swym dostojnym krewniakiem i suwerenem z tytułu lenna na Lęborgu i Bytowie. W programie gdańskim przyjęcia, obfitującym w uczty, zabawy i gry rycerskie, nie zapomniano o morzu.
W dniu 13 lipca zwiedził król w towarzystwie ks. Barnima statek na stoczni  w Gdańsku i przyglądał się jego spuszczeniu na wodę. W tydzień później (20 VII) wybrał się barką, wybitą czerwonym suknem i przybraną chorągiewkami, na obejrzenie warowni, nazywanej wówczas „Latarnią” albo „wieżą”,* położonej u ujścia Wisły. Gdy tam wchodził, grzmiały na jego cześć działa warowni i okrętu „Żelazny Henryk", naprzeciw niej umieszczonego , miotając na morze ogniste kule, Po posiłku w warowni powrócił na swą barkę i popłynął dalej — na Bałtyk, wtedy spokojny. Wielu także panów polskich z otoczenia zapuściło się daleko na fale, korzystając z pogody.

**Prompt**: W podanym tekście wyszukaj informacje o osobach, znalezione osoby wypisz w formie listy, jeżeli są znane funkcje lub urzędy osób umieść te informacje w nawiasach obok osób:
(In the given text search for information about people, list the people found, if the functions or offices of the people are known put this information in brackets next to the people:)

**Result**:

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


### Other examples

Scripts for these and other examples in the `src` folder, results in the `output` folder.

### Analysis of family relations on a series of biographies

(_see also later in the text an analogous analysis performed with GPT-4_)

How well the GPT-3 model (`davinci-003`) can recognize family relationships can be tried to evaluate on a larger sample of 50 biographical entries randomly selected from volumes 1-51 of the Polish Biographical Dictionary. The biographical entries vary in length, from about 1,000 characters to tens of thousands. The limitation is the number of tokens that 'davinci' can process in a single query - 4,000, including the generated response. For longer biographical entries, they were initially 'summarized': the first 5 and last 5 sentences were included (omitting the bibliographic part of the entry first) and all the sentences between them if they contained content indicating information about family and relatives (the biographical entry was divided into sentences using spaCy, the base forms of tokens in sentences were analyzed and compared with a prepared dictionary of concepts related to kinship). Shortening the biographical entries can, of course, negatively affect the results (sentences are taken out of context, and sometimes the spaCy model 'pl_core_news_lg' used incorrectly divided the text into sentences). The test focused on kinship in relation to the main character of the biographical entry.

The texts of the biographies were processed with a prompt that read (in Polish):

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

(script code in file psb_relations_family.py)

For 36 out of 50 biographical entries, the model found some relationships - a total of 182 cases of kinship between the main character and another person. After a detailed analysis, **38** of them were incorrect (**20.9%**), while **144** were assessed as **true** (**79.1%**).

A detailed list of **found** relationships:

| Character -> type of relationship/relationship -> related person | Correct? |
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

It is, of course, also important what the model **does not find**. For 14 biographical entries, the model assessed that there were no data on family relationships for the main character. In 5 of these cases, this is likely an error (15 missing relationships).

| Character | Correct? |
| ---    | ---   |
| Bartoszewski Jan | True |
| Ezra_ben_Nisan | True (w biogramie jest tylko niejasna wzmianka, że miał jakieś córki)
| Falęta | True
| Fiorentini Władysław | **False** (jest informacja o ojcu, dziadku i żonie)
| Gołaski Jan | True
| Grzegorzewski Jan | **False** (jest informacja o ojcu i matce)
| Guicciardini Galeazzo | True (występuje tylko niesjasna wzmianka o jego bracie, niewymienionym z imienia)
| Hirschenfeld-Mielecki Józef | True
| Langfort Teodor Henryk | True
| Popiel | True
| Siemowit | **False** (w biogramie wymieniony ojciec, matka, syn, wnuk i prawnuk)
| Spycigniew z Dąbrowy | **False** (w biogramie występuje inf. o prawdopodobnym synu i wnuku, być może problemem jest skrót S-a na oznaczenie głównego bohatera)
| Swach | **False** (jest inf. o ojcu, matce i bracie) |
| Sztaffel Izrael | True |

In the biographical entries where the model found relatives of the main character, it sometimes happened that this was only a part of the information about family relationships - this problem occurred in 12 out of 36 biographical entries (26 missing family relationships). A detailed list is provided below.

| Character | Does it include all relationships? Which ones are missing? |
| ---    | ---                               |
| Aloe Franciszek Eljasz  |  True |
| Bezprym  |  True |
| Dąbrowska Pelagia | **False**, pominięta matka Pelagia i ojciec Michał, ciotki Waleria i Ignacja, mąż Jarosław. Może to wynikać ze specyficzneg stylu podania tych informacji i stosowania skrótów: "Ur. 10 IX w Dubience (w Lubelskiem) z Pelagii z Piotrowskich i Michała Zgliczyńskiego, wcześnie osierocona, wychowywała się u ciotek Walerii i Ignacji Piotrowskich." |
| Daszyński Ignacy | True |
| Dzierżek Natalia | True |
| Eufrozyna | **False**, pominięta informacja o pierwszym mężu - Kazimierzu |
| Ewild al. Eywild | True |
| Fuzorius Bartłomiej | True |
| Gliński Iwan | **False**, pominięta informacja o bracie Wasylu |
| Hincza z Rogowa | True (jest wzmianka o małoletnich dzieciach ale bez konkretów) |
| Jadwiga Jagiellonka | True (część informacji jest pomylona - Jerzy Bawarski nie jest żoną bohaterki tylko mężem, ale inf. została znaleziona...) |
| Kakowski Aleksander | True |
| Krumhausen Gabriel | **False**, pominięta informacja o 'dziadku po kądzieli' |
| Łańcucki Wojciech | True |
| Leymiter Stanisław | **False**, pominięta inf. o szwagrze i 2 szwagierkach, bracie oraz o zięciach (z tym że córki wyszły za mąż po śmierci bohatera), biogram napisany dość zawile, jeżeli chodzi o opis rodziny bohatera. |
| Mierzeński Aleksander | **False**, pominięta informacja o ojcu i matce. |
| Mostowska z Bujwidów | True |
| Patruus | True (są tylko wzmianki o nieznanych z imienia synach i córkach) |
| Pichgiel | **False**, pominięta inf. o stryju i o żonie bohatera biogramu |
| Pion Maurice | True |
| Piotrowiczowa z Rogolińskich | True |
| Renard Benedykt | True |
| Rossi Piotr | **False**, pominięta informacja o teściu |
| Sapieha Jan Fryderyk | **False**, brak informacji o dziadku i o zięciu |
| Śląska Aleksandra | True (brak tylko inf. o 'dalekiej krewnej' Eugenii Deutsch) |
| Słowicki Józef | True |
| Śniadecka Kornelia Ludwika | **False**, brak informacji o szwagrze (mężu siostry), fragment o krewnych dość zawiły. |
| Spektor Mordechaj - True (krewni są wzmiankowani, ale bez konkretów) |
| Stańczakowa ze Strancmanów | True |
| Stanisław_Cielątko | True (pominięty mąż bratanicy ale czy to w sumie pokrewieństwo?) |
| Strzelecki Wiesław Marian | True |
| Świrski Jerzy Włodzimierz | True (ale część ze znalezionych relacji jest niepoprawnego typu, siostrzenica zamiast ciotka, brat zamiast siostra) |
| Szapira Majer | True |
| Szapocznikow Alina | **False**, pominięta informacja o 2 mężach |
| Szczubioł Andrzej | True |
| Szumski Boksa | **False**, pominięta informacja o przodku - dziad lub pradziad Jakub |

If we analyze the data from the three tables above, there are 223 relationships in the biographical entries, the model mentioned 182, of which 38 were incorrect, which means **64.5%** accuracy (144 correct). It is a completely different question whether and how the obtained data can be used, for example, to build knowledge bases.

### Analysis of family relationships in a series of biographies - GPT-4 model

The previous tests concerned the operation of the GPT-3 model ('davinci-003'); I do not yet have access to the API with GPT-4, but one can try to assess what results the latest model might achieve through the operation of ChatGPT Plus with the GPT-4 model enabled. One of the problematic biographical entries: 'Natalia Dzierżek (1861-1931)' for which 5 relationships were found, including 3 incorrect ones, this time was processed entirely correctly:

- główna bohaterka -> ojciec -> Henryk Dzierżek
- główna bohaterka -> matka -> Maria z Piątkowskich Nieczuja-Dzierżków
- główna bohaterka -> wujek (brat matki) -> Henryk Piątkowski

Similarly, the processing result for Pelagia Dąbrowska (1843-1909) improved, where the previous GPT-3 model found only two and incorrect relationships, and now GPT-4 returns the correct list:

- Główna bohaterka -> ojciec -> Michał Zgliczyński
- Główna bohaterka -> matka -> Pelagia z Piotrowskich
- Główna bohaterka -> mąż -> Jarosław Dąbrowski
- Główna bohaterka -> syn -> trzech synów
- Główna bohaterka -> ciotka -> Waleria Piotrowska
- Główna bohaterka -> ciotka -> Ignacja Piotrowska
- Główna bohaterka -> wuj -> Piotr Falkenhagen-Zaleski.

The prompt used underwent minor modifications:

```
Na podstawie podanego tekstu wyszukaj wszystkich krewnych lub powinowatych głównej bohaterki/bohatera tekstu: {name}. Możliwe rodzaje pokrewieństwa: ojciec, matka, syn, córka, brat, siostra, żona, mąż, teść, teściowa, dziadek, babcia, wnuk, wnuczka, szwagier, szwagierka, siostrzeniec, siostrzenica, bratanek, bratanica, kuzyn, kuzynka, zięć, synowa.
Wynik wypisz jako listę nienumerowaną w formie: główna bohaterka -> rodzaj pokrewieństwa (kim osoba była dla niej) -> osoba.
Każda pozycja w osobnej linii. Na przykład:
- główna bohaterka -> brat -> Jan Kowalski
- główna bohaterka -> siostra -> Anna
Wypisz tylko rodzaje pokrewieństwa, które występują w tekście.
Jeżeli w tekście nie ma żadnych informacji o pokrewieństwach głównego bohatera/bohaterki napisz: brak danych.
```

What do the results look like for the entire series of 50 biographical entries?

| Character -> type of relationship/relationship -> related person | Correct? |
| ------------------------------------------------------------ | :---------: |
| **Aloe Franciszek Eljasz** | |
| główny bohater -> ojciec -> Jan Baptysta d'Aloy | True |
| główny bohater -> matka -> Henryka Rakocy | True |
| główny bohater -> brat -> Emanuel d'Aloy  | True |
| główny bohater -> siostry -> piękne siostry Aloe (imię niepodane) | True |
| **Bartoszewski Jan** | |
| brak danych | True |
| **Bezprym** | |
| główny bohater -> ojciec -> Bolesław Chrobry | True |
| główny bohater -> matka -> nieznana z imienia Węgierka (być może córka księcia Gejzy) | True |
| główny bohater -> brat -> Mieszko II  | True |
| główny bohater -> brat -> Otton | True |
| **Dąbrowska_Pelagia** | |
| główna bohaterka -> ojciec -> Michał Zgliczyński | True |
| główna bohaterka -> matka -> Pelagia z Piotrowskich  | True |
| główna bohaterka -> mąż -> Jarosław Dąbrowski | True |
| główna bohaterka -> ciotka -> Waleria Piotrowska | True |
| główna bohaterka -> ciotka -> Ignacja Piotrowska | True |
| główna bohaterka -> wuj -> Piotr Falkenhagen-Zaleski | True |
| główna bohaterka -> syn -> (trzej synowie, imiona nie podane) | True |
| **Daszyński Ignacy** | |
| główny bohater -> ojciec -> Ferdynand Daszyński | True |
| główny bohater -> matka -> Kamila Daszyńska z Mierzeńskich | True |
| główny bohater -> brat -> Feliks Daszyński | True |
| główny bohater -> żona (pierwsza) -> Maria Daszyńska z Paszkowskich | True |
| główny bohater -> żona (druga) -> Cecylia Daszyńska z domu Kempnerówna | True |
| **Dzierżek_Natalia** | |
| główna bohaterka -> ojciec -> Henryk Dzierżek | True |
| główna bohaterka -> matka -> Maria z Piątkowskich Nieczuja-Dzierżków | True |
| główna bohaterka -> wujek (brat matki) -> Henryk Piątkowski | True |
| **Eufrozyna** | |
| główna bohaterka -> ojciec -> Kazimierz, ks. opolski | True |
| główna bohaterka -> mąż (pierwszy) -> Kazimierz, ks. kujawski | True |
| główna bohaterka -> syn -> Władysław Łokietek | True |
| główna bohaterka -> syn -> Kazimierz | True |
| główna bohaterka -> syn -> Ziemowit | True |
| główna bohaterka -> mąż (drugi) -> Mszczuj II, ks. pomorski | True |
| **Ewild al. Eywild** | |
| główny bohater -> brat -> Eynurem | True |
| **Ezra ben Nisan** | |
| główny bohater -> ojciec -> Nisan | True |
| główny bohater -> córka -> córka Jana Kazimierza (niepodane imię) | **False** |
| **Falęta** | |
| brak danych | True |
| **Fiorentini Władysław** | |
| główny bohater -> ojciec -> Antoni | True |
| główny bohater -> dziadek -> Franciszek | True |
| główny bohater -> żona -> Anna | True |
| główny bohater -> teść -> Bazyle Popow | True |
| główny bohater -> teściowa -> Bogumiła z Gizbertów | True |
| **Fuzorius Bartłomiej** | |
| główny bohater -> ojciec -> Stanisław Lwowczyk | True |
| **Gliński Iwan** | |
| główny bohater -> ojciec -> Lew Borysowicz | True |
| główny bohater -> brat -> Michał | True |
| główny bohater -> brat -> Wasyl | True |
| główny bohater -> bratanica -> Helena | True |
| **Gołaski Jan** | |
| brak danych | True
| **Grzegorzewski Jan** | |
| główny bohater -> ojciec -> Jakub Grzegorzewski | True |
| główny bohater -> matka -> Anna Grzegorzewska z domu Zaleska | True |
| **Guicciardini Galeazzo** | |
| główny bohater -> brat -> nieznane imię | True |
| **Hincza z Rogowa** | |
| główny bohater -> ojciec -> Hinczka z Rogowa | True |
| główny bohater -> brat -> Jakub | True |
| główny bohater -> brat -> Henryk | True |
| główny bohater -> żona -> Dorota z Koziegłowskich | True |
| główny bohater -> siostra -> Małgorzata | True |
| **Hirschenfeld-Mielecki Józef** | |
| brak danych | True |
| **Jadwiga Jagiellonka** | |
| główna bohaterka -> ojciec -> Kazimierz Jagiellończyk | True |
| główna bohaterka -> matka -> Elżbieta Rakuszanka | True |
| główna bohaterka -> mąż -> Jerzy Bawarski | True |
| główna bohaterka -> brat -> Władysław Jagiellończyk | True |
| główna bohaterka -> brat -> Aleksander Jagiellończyk | True |
| główna bohaterka -> brat -> Zygmunt I Jagiellończyk | True |
| główna bohaterka -> córka -> Elżbieta | True |
| główna bohaterka -> córka -> Małgorzata | True |
| główna bohaterka -> wnuk -> Ruprecht hr. Palatynatu | **False** |
| brak -> syn -> Ludwik | **False** |
| brak -> syn -> Ruprecht | **False** |
| brak -> wnuk -> (niewymieniony z imienia) | **False** |
| **Kakowski Aleksander** | |
| łówny bohater -> ojciec -> Franciszek Kakowski | True |
| główny bohater -> matka -> Paulina Kakowska z domu Ossowska | True |
| **Krumhausen Gabriel** | |
| główny bohater -> ojciec -> Joachim Krumhausen | True |
| główny bohater -> matka -> Gertruda Krumhausen z domu Schumann | True |
| główny bohater -> żona -> Konstancja Krumhausen z domu Falcke  | True |
| główny bohater -> dziadek (po kądzieli) -> Stanisław Bornbach | True |
| główny bohater -> brat -> Joachim Krumhausen | True |
| **Łańcucki Wojciech** | |
| główny bohater -> ojciec -> Stanisław | True |
| **Langfort Teodor Henryk** | |
| brak danych | True
| **Leymiter Stanisław** | |
| główny bohater -> ojciec -> Mikołaj | True |
| główny bohater -> matka -> Benigna | True |
| główny bohater -> żona -> Zofia | True |
| główny bohater -> teść -> Jan Tesznar | True |
| główny bohater -> syn -> Jan | True |
| główny bohater -> syn -> Stanisław | True |
| główny bohater -> córka -> Barbara | True |
| główny bohater -> córka -> Benigna | True |
| główny bohater -> szwagier -> Jan Wierzyniek | True |
| główny bohater -> szwagier -> Mikołaj Kreidler | True |
| brak -> szwagierka -> Agnieszka | **False** |
| brak -> szwagierka -> Katarzynę | **False** |
| brak -> szwagierka -> Jan Tesznar | **False** |
| brak -> brat -> Mikołaj Leymiter | **False** |
| brak -> zięć -> Wincenty Beck | **False** |
| brak -> zięć -> Jan Tretkop | **False** |
| **Mierzeński Aleksander** | |
| główny bohater -> ojciec -> Abraham | True |
| główny bohater -> matka -> Elżbieta Morsztynówna | True |
| główny bohater -> brat -> Jan Mierzeński | True |
| główny bohater -> brat -> Samuel Mierzeński | True |
| główny bohater -> brat -> Krzysztof Mierzeński | True |
| główny bohater -> brat -> Daniel Mierzeński | True |
| **Mostowska z Bujwidów** | |
| Mostowska z Bujwidów Zofia -> ojciec -> Odo Bujwida | True |
| Mostowska z Bujwidów Zofia -> matka -> Kazimiera z Klimontowiczów | True |
| Mostowska z Bujwidów Zofia -> siostra -> Kazimiera Rouppertowa | True |
| Mostowska z Bujwidów Zofia -> siostra -> Jadwiga Demelowa | True |
| Mostowska z Bujwidów Zofia -> siostra -> Helena Jurgielewiczowa | True |
| Mostowska z Bujwidów Zofia -> mąż -> Włodzimierz Mostowski | True |
| Mostowska z Bujwidów Zofia -> syn -> Jerzy Mostowski | True |
| Mostowska z Bujwidów Zofia -> syn -> Czesław Mostowski | True |
| **Patruus** | |
| główny bohater -> ojciec -> Jan «ojciec» (zm. 1538) | **False** |
| główny bohater -> syn -> Jan | True |
| główny bohater -> żona -> nieznana | True |
| **Pichgiel** | |
| główny bohater -> stryj -> Matthias Pichel | True |
| główny bohater -> kuzyn -> Matthias Pichgiel młodszy | True |
| główny bohater -> syn -> Christian Pichgiel młodszy | True |
| główny bohater -> żona -> Barbara z domu Biettin | True |
| główny bohater -> syn -> Christian | True (dublet) |
| główny bohater -> syn -> Johan | True |
| główny bohater -> syn -> Daniel | True |
| główny bohater -> syn -> Emanuel | True |
| **Pion Maurice** | |
| główny bohater -> ojciec -> Antoine Claude | True |
| główny bohater -> matka -> Anne z domu Pauli | True |
| główny bohater -> żona -> Aleksandra Antonina z Budzyńskich | True |
| główny bohater -> córka -> Adela | True |
| główny bohater -> syn -> Adolf Stanisław | True |
| główny bohater -> syn -> Władysław Stanisław | True |
| główny bohater -> córka -> Kornelia, zamężna Quattrini | True |
| główny bohater -> siostra -> Eugenia, zamężna Koss | True |
| **Piotrowiczowa z Rogolińskich** | |
| główna bohaterka -> ojciec -> Zygmunt Rogoliński | True |
| główna bohaterka -> matka -> Ansberty z Badeńskich | True |
| główna bohaterka -> mąż -> Konstanty Piotrowicz | True |
| **Popiel** | |
| główny bohater -> syn -> dwóch synów (ich imion nie podano) | True |
| **Renard Benedykt** | |
| główny bohater -> ojciec -> Andrzej | True |
| główny bohater -> brat -> Jan Baptysta | True |
| główny bohater -> siostra -> Anna Katarzyna (Anna Orzelska) | True ? |
| **Rossi Piotr** | |
| główny bohater -> ojciec -> Andrzej | True |
| główny bohater -> żona -> Małgorzata (córka Józefa Baltazary) | True |
| główny bohater -> syn -> Andrzej (ur. 1790) | True |
| główny bohater -> syn -> Kornel (ur. 1791) | True |
| główny bohater -> syn -> Klemens (ur. 1794) | True |
| główny bohater -> córka -> Izabella (ur. 1792) | True |
| główny bohater -> córka -> Feliksa (ur. 1793) | True |
| brak -> teść -> Józef Baltazary | **False** |
| **Sapieha_Jan_Fryderyk** | |
| główny bohater -> dziadek -> Mikołaj (wojewoda witebski) | True |
| główny bohater -> ojciec -> Fryderyk (podkomorzy włodzimierski) | True |
| główny bohater -> matka -> Ewa ze Skaszewskich | True |
| główny bohater -> brat -> Tomasz Kazimierz (oboźny litewski) | True |
| główny bohater -> brat -> Aleksander Kazimierz (biskup wileński) | True |
| główny bohater -> brat -> Krzysztof Franciszek (krajczy litewski) | True |
| główny bohater -> kuzyn -> Kazimierz Leon Sapieha | True |
| główny bohater -> żona -> Konstancja | True |
| główny bohater -> córka -> Ludwika Konstancja (żona ks. Konstantego Szujskiego, pisarza wielkiego litewskiego) | True |
| główny bohater -> syn -> Mikołaj Leon (wojewoda bracławski) | True |
| główny bohater -> syn -> Kazimierz Władysław (wojewoda trocki) | True |
| główny bohater -> syn -> Paweł Franciszek (biskup żmudzki) | True |
| brak -> brata stryjecznego -> Jana Ferdynanda | **False** |
| **Siemowit** | |
| Siemowit -> ojciec -> Piast | True |
| Siemowit -> matka -> Rzepicha (Rzepka) | True |
| Siemowit -> syn -> Lestik (Lestek) | True |
| Siemowit -> wnuk -> Siemomysł | True |
| Siemowit -> prawnuk -> Mieszko I | True |
| **Śląska Aleksandra** | |
| Aleksandra Śląska -> ojciec -> Edmund Wąsik | True |
| Aleksandra Śląska -> matka -> Helena Wąsik (z domu Masłowska) | True |
| Aleksandra Śląska -> siostra przyrodnia -> Bożena Jewasińska (Naturska) | True |
| Aleksandra Śląska -> brat -> Olgierd Edmund Wąsik | True |
| Aleksandra Śląska -> krewne -> Eugenia Deutsch (z domu Taczanowska) | True |
| Aleksandra Śląska -> mąż (1) -> Czesław Michał Górski | True |
| Aleksandra Śląska -> syn -> Szczęsny Tadeusz Górski | True |
| Aleksandra Śląska -> mąż (2) -> Janusz Warmiński | True |
| **Słowicki Józef** | |
| Słowicki Józef -> ojciec -> Józef Słowicki | True |
| **Śniadecka Kornelia Ludwika**
| główna bohaterka -> ojciec -> Jędrzej Śniadecki | True |
| główna bohaterka -> matka -> Konstancja z Mikułowskich | True |
| główna bohaterka -> siostra -> Zofia Balińska | True |
| główna bohaterka -> brat -> Józef Konstanty Śniadecki | True |
| główna bohaterka -> szwagier -> Michał Baliński | True |
| główna bohaterka -> bratanek -> Jan Śniadecki | **False** |
| główna bohaterka -> szwagierka -> Antonina Śniadecka | True |
| główna bohaterka -> teść -> Kazimierz Sulistrowski | **False** |
| główna bohaterka -> siostrzeniec -> Ignacy Abramowicz | **False** |
| główna bohaterka -> siostrzeniec -> Mikołaj Abramowicz | **False** |
| główna bohaterka -> szwagier -> Aleksander Skirmunt | **False** |
| główna bohaterka -> mąż -> Michał Czajkowski (Mehmed Sadyk) | True |
| **Spektor Mordechaj** | |
| główny bohater -> ojciec -> kramarz, chasyd | True |
| główny bohater -> matka (niewymieniona z imienia) | True |
| główny bohater -> brat (niewymieniony z imienia) | True |
| główny bohater -> żona -> Izabela z Frydbergów | True |
| główny bohater -> syn | **False** |
| główny bohater -> córka | **False** |
| **Spycigniew_z_Dąbrowy** | |
| główny bohater -> syn -> Zawisza | True |
| główny bohater -> wnuk -> Spycigniew | True |
| **Stańczakowa ze Strancmanów** | |
| główna bohaterka -> ojciec -> Adolf Strancman (Franciszek Kotarbiński) | True |
| główna bohaterka -> matka -> Maria Weinfeld (Helena z Koprowskich Kotarbińska) | True |
| główna bohaterka -> brat -> Jan | True |
| główna bohaterka -> mąż -> Zdzisław Stańczak | True |
| główna bohaterka -> córka -> Anna | True |
| główna bohaterka -> zięć -> Tadeusz Sobolewski | True |
| **Stanisław_Cielątko** | |
| główny bohater -> ojciec -> Jan | True |
| główny bohater -> brat -> Jan Cielątki z Liszyna i Prusiecka | True |
| główny bohater -> brat -> Mikołaj | True |
| główny bohater -> szwagierka -> Anna z Oględowa | True |
| główny bohater -> siostrzenica -> Małgorzata Marta | **False** |
| główny bohater -> zięć (Małgorzaty Marty) -> Mikołaj Cikowski | **False** |
| główny bohater -> teść (Małgorzaty Marty) -> Piotr Cikowski z Mikluszowic | **False** ? |
| **Strzelecki Wiesław Marian** | |
| główny bohater -> ojciec -> Felicjan | True |
| główny bohater -> matka -> Stefania z Łękawskich | True |
| główny bohater -> żona -> Barbara z Krzemińskich | True |
| główny bohater -> syn -> Krzysztof | True |
| **Swach Jerzy** | |
| główny bohater -> ojciec -> Udalryk (Oldrzych) | True |
| główny bohater -> matka -> Katarzyna | True |
| główny bohater -> brat -> Karol Antoni | True |
| **Świrski Jerzy Włodzimierz** | |
| główny bohater -> ojciec -> Włodzimierz | True |
| główny bohater -> matka -> Celina z Wasiłowskich | True |
| główny bohater -> siostra -> Małgorzata (1. v. Kucharska, 2. v. Łyszkowska) | True |
| główny bohater -> siostrzeniec -> Maria Konopnicka | **False** |
| główny bohater -> żona -> pierwsza żona (imię nieznane) | True |
| główny bohater -> żona -> Maria Wiercińska | True |
| **Szapira Majer** | |
| główny bohater -> ojciec -> Jakub Szamszon | True |
| główny bohater -> matka -> Margula Szor | True |
| główny bohater -> dziadek -> Samuel Izaak Szor | True |
| główny bohater -> brat -> Abraham | True |
| główny bohater -> żona -> Małka Towa | True |
| **Szapocznikow_Alina** | |
| główna bohaterka -> ojciec -> Jakub | True |
| główna bohaterka -> matka -> Regina (Ryfka) z Auerbachów | True |
| główna bohaterka -> brat -> Mirosław | True |
| główna bohaterka -> mąż (1) -> Ryszard Stanisławski | True |
| główna bohaterka -> mąż (2) -> Roman Cieślewicz | True |
| główna bohaterka -> syn -> Piotr Stanisławski (adoptowany) | True |
| **Szczubioł_Andrzej** | |
| główny bohater -> ojciec -> Stefan (Szczepan) z Jasieńca i Ciechomic | True |
| główny bohater -> matka -> Sędka (imię nieznane) | True |
| główny bohater -> brat -> Mikołaj z Ciechomic | True |
| główny bohater -> brat -> Jan z Dłotowa (Dłutowo) | True |
| główny bohater -> żona (1) -> nieznana | True |
| główny bohater -> syn (z 1. małżeństwa) -> Maciej | True |
| główny bohater -> syn (z 1. małżeństwa) -> Szymon zwany Gostyńskim z Ciechomic | True |
| główny bohater -> żona (2) -> Anna | True |
| główny bohater -> syn (z 2. małżeństwa) -> Andrzej | True |
| główny bohater -> synowa -> Anna, córka Ścibora z Sąchocina | **False** |
| **Sztaffel Izrael** | |
| brak danych | True |
| **Szumski Boksa** | |
| główny bohater -> dziadek lub pradziadek -> Jakub | True |
| główny bohater -> prawdopodobny ojciec -> Krzesław z Szumska | True |
| główny bohater -> brat -> Jan (Jaszek) Rej z Nagłowic | True |
| główny bohater -> żona -> Stachna h. Poraj | True |
| główny bohater -> syn -> Jan Rey | True |
| główny bohater -> bratanek -> Jan Rey | True |
| główny bohater -> bratanek -> Stogniew | True |
| brak -> dziad -> Jakub | **False** |
| brak -> synowa -> Prakseda | **False** |
| brak -> szwgier -> Chociemir Garnek (Garnysz) z Pojałowic i Suchcic | **False** |
| brak -> szwagierka -> Świątka | **False** |

In the analyzed biographical entries, there are a total of **245** relationships or lack of relationships (when the content of the biographical entry does not contain information about relatives and in-laws; in the previous analysis using GPT-3, I did not notice several relationships), of which the GPT-4 model correctly identified **215** - achieving **88%** accuracy.

This is clearly a better result than the previous one achieved by GPT3 (model 'davinci-003'), but also in line with expectations, since, according to OpenAI's technical report on GPT4 (https://arxiv.org/abs/2303.08774), the new model is 29% better at avoiding 'closed domain hallucinations', i.e. making up false information, despite instructions that the information is to come only from the given context, e.g. an anlized article.

For some biographies, e.g. 'Śniadecka Kornelia Ludwika' , 'Leymiter Stanisław' or 'Stanisław Cielątko' the errors are numerous, perhaps this is due to the length and intricacy of the sentences. Perhaps this is influenced by the structure of the task - information about the family relations of the main character is expected, if it is given not directly, e.g. 'The sister of John Kowalski's wife was Amelia...' this requires the transformation of the given information to the required form -> 'sister-in-law'.

Still a certain problem is the non-deterministic nature of large language models, the same prompt run repeatedly can give slightly different results, even with the same correctness, but slightly differently worded. Despite the explicitly recommended response format in the above analysis (main character -> relationship -> person), it happened that the model returned either the phrase "main character/woman" or provided the actual first and last name of the main character here. It also happened that family relations of other people appearing in the text were returned. So the result is not always a ready-made product for further analysis, it needs to be processed and made consistent.

### Processing of the Historical and Geographical Dictionary entry into XML format - GPT4

Test of automatic processing of a fragment of the Historical and Geographical Dictionary (entry [Balice](http://www.slownik.ihpan.edu.pl/search.php?id=2348), part of item 3) using the GPT4 model (via API, temperature parameter = 0) into XML format. The prompt used:

```
Przetwórz proszę poniższy tekst zawierający regesty na plik XML. Regest zaczyna się od daty np. 1245 lub zakresu dat 1245-56 lub daty przybliżonej np. a. 1456, po której następuje treść regestu, a po niej - w nawiasie - źródło informacji. Po nawiasie pojawia się średnik oddzielający regesty. Jeżeli nie ma daty na początku, oznacza to, że data jest taka sama jak w poprzednim regeście. W treści regestu oznacz występujące w niej osoby tagiem <persName>, miejsca tagiem <placeName>, nazwy geograficzne tagiem <geogName> zaś nazwy urzędów zawodów lub funkcji tagiem <occupation>. Pamiętaj, że jednoliterowe skróty, takie jak 'B.', oznaczają miejscowość, której dotyczą regesty. Osoby pojawiające się w treści regestu to postacie średniowieczne, które nie miały nazwisk za to dopisywały do imienia miejscowość z której pochodzą np. Jan z Grzędowa, w takich przypadkach oznacz osobę tagiem <persName> z miejscowością włącznie.

Przykład regestu:
a. 1396 kaszt. wiśl. Jaśko za zasługi przy chrystianizacji Litwy dostał od Władysława Jag. m. Wojsław [nie zid.] i kilka wsi w ziemi krak. w tym wieś Grzędy w pow. sand., którą sprzedał Krzesławowi z Wolicy. Synem Jaśka był Jan z B. (J. Ossoliński, Pamiętnik 1595-1621, Wr. 1952, s. 4);

Przykład wyniku:
<s type="regest">
<date>a. 1396</date>
<content><occupation>kaszt. wiśl.</occupation> <persName>Jaśko</persName> za zasługi przy chrystianizacji <geogName>Litwy</geogName> dostał od <persName>Władysława Jag.</persName> m. <placeName>Wojsław</placeName> [nie zid.] i kilka wsi w ziemi krak. w tym wieś <placeNme>Grzędy</PlaceName> w pow. sand., którą sprzedał <persName>Krzesławowi z Wolicy</persName>. Synem <persName>Jaśka</persName> był <persName>Jan z B.</persName></content>
<biblio>(J. Ossoliński, Pamiętnik 1595-1621, Wr. 1952, s. 4)</biblio>;
</s>

Przykład regestu:
1467 Albert kmieć z B. (KRK 3 s. 23);

Przykład wyniku:
<s type="regest">
<date>1467</date>
<content><persName>Albert</persName> <occupation>kmieć</occupation> z <placeName>B.</placeName></content>
</s>

Oto tekst do przetworzenia:
1229 papież Grzegorz IX potwierdza kl. tyn. posiadanie m. in. B. (Tyn. 11b - bulla interpol. w XV w., por. J. Wyrozumski, Państwowa gospodarka solna w Polsce do schyłku XIV w., Kr. 1968, s. 25); a. 1286 komes Grzegorz zw. Żegocic dz. B., zabraniał kl. dominikanów w Krakowie przeprowadzić wodę z rz. Rudawy przez Krowodrzę, → też p. 6 (KK 1, 86); 1304-6 komes Andrzej z B. (KK 2, 242; 1, 114 przy tym dok. wisiała jego pieczęć); 1321, 1351-2, 1363 Grzegorz z B. (AS 2, 7; Mp. 3, 761; Wp. 3, 1495; ZDM 1, 63; KMK 1, 27); 1366 Jan z B. (ZDM 1, 117); 1367 Betico kmieć z B. (KRK 2 s. 13); 1387-96 Jan, Jaśko z Goźlic [pow. sand.], B. i Ossolina [pow. sand.], kaszt. wiśl. 1388-96, wg Długosza zabity przez Grota ze Słupczy [pow. sand.] w sporze o granice wsi Dwikozy [pow. sand.] (AGZ 5, 16; AS 2, 61; KK 2, 392, 401; Mp. 4, 1022; ZDM 6, 1540, 1548, 1584; KUJ 1, 8; AKP 8, 63; Proch. 12; DH 3 s. 552 na s. 372 i 466 wiadomości odnoszą się do kaszt. wiśl. Mikołaja z Bogorii [pow. sand.], a nie z Ossolina; MH 10 s. 148-9; Bon. 1 s. 86); a. 1396 kaszt. wiśl. Jaśko za zasługi przy chrystianizacji Litwy dostał od Władysława Jag. m. Wojsław [nie zid.] i kilka wsi w ziemi krak. (J. Ossoliński, Pamiętnik 1595-1621, Wr. 1952, s. 4);
```

The result in the form of XML:

```XML
<regests>
    <s type="regest">
        <date>1229</date>
        <content><persName>papież Grzegorz IX</persName> potwierdza <placeName>kl. tyn.</placeName>
        posiadanie m. in. <placeName>B.</placeName></content>
        <biblio>(Tyn. 11b - bulla interpol. w XV w., por. J. Wyrozumski, Państwowa gospodarka solna w Polsce do schyłku XIV w., Kr. 1968, s. 25)</biblio>;
    </s>
    <s type="regest">
        <date>a. 1286</date>
        <content><occupation>kom</occupation> <persName>Grzegorz zw. Żegocic</persName> dz.
        <placeName>B.</placeName>, zabraniał <placeName>kl. dominikanów</placeName> w
        <placeName>Krakowie</placeName> przeprowadzić wodę z rz. <geogName>Rudawy</geogName> przez
        <placeName>Krowodrzę</placeName>, → też p. 6</content>
        <biblio>(KK 1, 86)</biblio>;
    </s>
    <s type="regest">
        <date>1304-6</date>
        <content><occupation>kom</occupation> <persName>Andrzej z B.</persName></content>
        <biblio>(KK 2, 242; 1, 114 przy tym dok. wisiała jego pieczęć)</biblio>;
    </s>
    <s type="regest">
        <date>1321</date>
        <content><persName>Grzegorz z B.</persName></content>
        <biblio>(AS 2, 7; Mp. 3, 761; Wp. 3, 1495; ZDM 1, 63; KMK 1, 27)</biblio>;
    </s>
    <s type="regest">
        <date>1351-2</date>
        <content><persName>Grzegorz z B.</persName></content>
    </s>
    <s type="regest">
        <date>1363</date>
        <content><persName>Grzegorz z B.</persName></content>
    </s>
    <s type="regest">
        <date>1366</date>
        <content><persName>Jan z B.</persName></content>
        <biblio>(ZDM 1, 117)</biblio>;
    </s>
    <s type="regest">
        <date>1367</date>
        <content><persName>Betico</persName> <occupation>kmieć</occupation> z <placeName>B.</placeName>
        </content>
        <biblio>(KRK 2 s. 13)</biblio>;
    </s>
    <s type="regest">
        <date>1387-96</date>
        <content><persName>Jan</persName>, <persName>Jaśko z Goźlic</persName> [pow. sand.],
        <placeName>B.</placeName> i <placeName>Ossolina</placeName> [pow. sand.],
        <occupation>kaszt. wiśl.</occupation> 1388-96, wg <persName>Długosza</persName> zabity
        przez <persName>Grota ze Słupczy</persName> [pow. sand.] w sporze o granice wsi
        <placeName>Dwikozy</placeName> [pow. sand.]</content>
        <biblio>(AGZ 5, 16; AS 2, 61; KK 2, 392, 401; Mp. 4, 1022; ZDM 6, 1540, 1548, 1584; KUJ 1, 8; AKP 8, 63; Proch. 12; DH 3 s. 552 na s. 372 i 466 wiadomości odnoszą się do kaszt. wiśl. Mikołaja z Bogorii [pow. sand.], a nie z Ossolina; MH 10 s. 148-9; Bon. 1 s. 86)</biblio>;
    </s>
    <s type="regest">
        <date>a. 1396</date>
        <content><occupation>kaszt. wiśl.</occupation> <persName>Jaśko</persName> za zasługi
        przy chrystianizacji <geogName>Litwy</geogName> dostał od <persName>Władysława Jag.</persName>
        m. <placeName>Wojsław</placeName> [nie zid.] i kilka wsi w ziemi krak.</content>
        <biblio>(J. Ossoliński, Pamiętnik 1595-1621, Wr. 1952, s. 4)</biblio>;
    </s>
</regests>
```

However, it is important to remember that the context that GPT models can handle is limited, and using the API costs money, so you may want to consider a hybrid solution. For example, you could use more conventional methods (Python, spaCy, regex, etc.) to split the input text from the SHG dictionary into points, sub-points, and regests, and then use the LLM model to tag the content of the regests themselves (without the bibliography, which can also be handled by simpler methods).

### Formatting results - JSON

In the examples of extracting information from biographies of historical figures, the result was presented in the form of a list, however, a more convenient option for further processing would be the result in JSON format. The GPT model is of course capable of doing this. The modification of the prompt involves replacing the part describing the result format in the form of a list with the text (in Polish):

```TXT
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
relacja: rodzaj pokrewieństwa (kim osoba była dla bohatera/bohaterki )
osoba: nazwa (imię i nazwisko osoby związanej relacją z bohaterem)
```

and also providing a new example result:

```TXT
Przykład: "Soderini Carlos (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Jego bratanicą była Małgorzata Anna, żona
Winfrida de Loeve. S. ożenił się z Joanną, córką burgrabiego
krakowskiego Adama Kurozwęckiego."
Wynik:
```
```JSON
[{"relacja":"ojciec", "osoba":"Niccola"},
 {"relacja":"matka", "osoba":"Annalena Ricasoli"},
 {"relacja":"brat", "osoba":"Bernard"},
 {"relacja":"bratanica", "osoba":"Małgorzata Anna"},
 {"relacja":"żona", "osoba":"Joanna"},
 {"relacja":"teść", "osoba":"Adam Kurozwęcki"}
]
```

the script processes the biography, e.g., of Jadwiga Jagiellonka, returning the result in JSON format, facilitating later automatic processing, comparing the result with the expected one, etc.

```JSON
[{"relacja":"ojciec", "osoba":"Kazimierz Jagiellończyk"},
 {"relacja":"matka", "osoba":"Elżbieta Rakuszanka"},
 {"relacja":"mąż", "osoba":"Jerzy Bawarski"},
 {"relacja":"syn", "osoba":"Ludwik"},
 {"relacja":"syn", "osoba":"Ruprecht"},
 {"relacja":"córka", "osoba":"Elżbieta"},
 {"relacja":"córka", "osoba":"Małgorzata"},
 {"relacja":"brat", "osoba":"Władysław Jagiellończyk"},
 {"relacja":"brat", "osoba":"Aleksander"},
 {"relacja":"brat", "osoba":"Zygmunt I"},
 {"relacja":"teść", "osoba":"Ludwik Bogaty"},
 {"relacja":"zięć", "osoba":"Ruprecht hr. Palatynatu"}
]
 ```

By the way, what is the cost of processing the biography of Jadwiga Jagiellonka? The biography text is less than 5000 characters (2504 tokens), while the answer is 264 tokens, the price for using the GPT-4 model via the API is $0.03 for input data, $0.06 for the generated response (prices per 1,000 tokens). In the case of the discussed biography, this currently means a cost of $0.09 (June 2023). Therefore, it is not a cheap process.

### Indeterminism and hallucinations

Extracting information from studies and historical sources requires accuracy and correctness of results. The language model, despite its immense capabilities in the field of text processing
will also produce incorrect answers ('hallucinations'), it will also 'change its mind'. Setting the model's run parameter 'temperature' to 0 reduces its creative tendencies, which is a desirable effect for extracting knowledge from text, but the result of queries to the API returned by the GPT-4 model can and will still vary slightly with each call. LLMs are inherently non-deterministic (see https://platform.openai.com/docs/guides/gpt/faq - point: "Why are model outputs inconsistent?"). This effect can be observed by repeatedly running the same query on the
family relations of Jadwiga Jagiellonka, which processes the same biographical text ([link](https://github.com/pjaskulski/gpt_historical_text/blob/main/src/psb_relacje_rodzinne_biogram.py) to the script). The query (prompt) was accompanied by an example of the data to be processed and an example of the result (few-shot learning). About 80-90% of the answers remain the same (and correct),
However, the rest of the result changes, sometimes the answers are correct, sometimes they are completely wrong. It seems, based on a simple observation, that the variability applies to the more difficult to extract relations like 'son-in-law', 'father-in-law', 'grandson', while relations like 'father', 'mother', 'husband', 'daughter', 'son', 'brother' are searched for
conventionally and correctly. Perhaps it is the way the content is formulated in the biography to be analyzed that matters. The more elaborate, "literary" the description, the greater the chance that the model will misinterpret the information.

10 tests were performed on the biography of Jadwiga Jagiellonka, the extracted information was practically different each time - with the same content of the prompt and input text. Of these, 10 relationships were repeated for each test:

```JSON
 {"relacja":"ojciec", "osoba":"Kazimierz Jagiellończyk"},
 {"relacja":"matka", "osoba":"Elżbieta Rakuszanka"},
 {"relacja":"mąż", "osoba":"Jerzy Bawarski"},
 {"relacja":"syn", "osoba":"Ludwik"},
 {"relacja":"syn", "osoba":"Ruprecht"},
 {"relacja":"córka", "osoba":"Elżbieta"},
 {"relacja":"córka", "osoba":"Małgorzata"},
 {"relacja":"brat", "osoba":"Władysław Jagiellończyk"},
 {"relacja":"brat", "osoba":"Aleksander"},
 {"relacja":"brat", "osoba":"Zygmunt I"},
```

In addition, other relationships could appear, from 1 to 4. In two tests, the additional relationships were not present.


```TXT
test 1:
 {"relacja":"teść", "osoba":"Ludwik Bogaty"} = OK
 {"relacja":"zięć", "osoba":"Ruprecht hr. Palatynatu"} = OK
test 2:
 {"relacja":"teściowa", "osoba":"Dorota Koniecpolska"} = ERR
 {"relacja":"zięć", "osoba":"Ruprecht hr. Palatynatu"} = OK
 {"relacja":"wnuczka", "osoba":"Małgorzata"} = ERR
test 3:
 {"relacja":"wnuk", "osoba":"Ruprecht hr. Palatynatu"} = ERR
test 4:
 {"relacja":"siostrzeniec", "osoba":"Ruprecht hr. Palatynatu"} = ERR
 {"relacja":"wnuk", "osoba":"wnuk Jadwigi Jagiellonki"} = OK
test 5:
 No additional relations
test 6:
 {"relacja":"zięć", "osoba":"Ruprecht hr. Palatynatu"} = OK
 {"relacja":"wnuk", "osoba":"wnuk Jadwigi Jagiellonki"} = OK
test 7:
 {"relacja":"wnuk", "osoba":"Ruprecht hr. Palatynatu"} = ERR
test 8
 No additional relations
test 9
 {"relacja":"teściowa", "osoba":"Dorota Koniecpolska"} = ERR
 {"relacja":"zięć", "osoba":"Ruprecht hr. Palatynatu"} = OK
 {"relacja":"wnuczka", "osoba":"Małgorzata"} = ERR
test 10:
 {"relacja":"wnuk", "osoba":"Ruprecht hr. Palatynatu"} = ERR
 {"relacja":"siostrzeniec", "osoba":"Ruprecht hr. Palatynatu"} = ERR
 {"relacja":"szwagierka", "osoba":"Anna, księżna wdowa cieszyńska"} = ERR
 {"relacja":"siostrzenica", "osoba":"Małgorzata, ksieni benedyktynek w Neuburg"} = ERR
```

As you can see, in 6 out of 10 tests there are accounts that are untrue, they cannot be justified in any way by the content of the biographical text, less damaging seems to be the complete failure to find existing accounts which happened in 2 tests.

Since in the case of extracting information from texts, we are dealing with information we do not yet know (we do not have a database or knowledge graph), it would be difficult to perform factual verification other than manually comparing the text with the model's extracted data. However, such a process is time-consuming and would negate any benefit of automating the processing of large amounts of text. Whether the solution would be to repeat each query e.g. 3 times and consider the repeated answers as reliable and the others as requiring verification - it is hard to say, but it is after all possible that consistently in each test there would be incorrect and therefore unreliable information. Manual verification of data obtained through large language models seems - for today - inevitable.