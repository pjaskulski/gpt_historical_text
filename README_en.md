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
  - [Indeterminism and hallucinations](#indeterminism-and-hallucinations)
  - [Nous-Hermes-13b Model Test](#nous-hermes-13b-model-test)
  - [Verifying the results returned by LLM - Guardrails](#verifying-the-results-returned-by-llm---guardrails)
  - [Example of information extraction from a PSB biography](#example-of-information-extraction-from-a-psb-biography)
  - [GPT and PSB Biographies - Remarks and Conclusions](#gpt-and-psb-biographies---remarks-and-conclusions)
  - [Automatic creation of knowledge graphs](#automatic-creation-of-knowledge-graphs)
  - [GPT-3.5-turbo Model Fine-tuning Test](#gpt-35-turbo-model-fine-tuning-test)
  - [Processing 250 Biographies with the Fine-tuned GPT-3.5-turbo Model](#processing-250-biographies-with-the-fine-tuned-gpt-35-turbo-model)

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

In the analyzed biographical entries, there are a total of **245** relationships or lack of relationships (when the content of the biographical entry does not contain information about relatives and in-laws; in the previous analysis using GPT-3, I did not notice several relationships), of which the GPT-4 model correctly identified **215** - achieving **88%** of correctness.
Taking more typical measures, the number of correctly found relationships is 208, all found relationships is 229, all actually occurring relationships in biographies is 235, which would give a value of precision = 0.9, recall = 0.88 and f1 = 0.889.

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

Since in the case of extracting information from texts, we are dealing with information we do not yet know (we do not have a database or knowledge graph), it would be difficult to perform factual verification other than manually comparing the text with the model's extracted data. However, such a process is time-consuming and would negate any benefit of automating the processing of large amounts of text. Whether the solution would be to repeat each query e.g. 3 times and consider the repeated answers as reliable and the others as requiring verification - it is hard to say, but it is after all possible that consistently in each test there would be incorrect and therefore unreliable information. Manual verification of data obtained through large language models seems - for today - inevitable. However, it can be supported by additional tools that verify the structure of the results returned by the LLM, or the probability of the extracted facts (e.g., the age of the person should be in the range of 0-110), the names of family relationships should come from a certain set, etc.

### Nous-Hermes-13b Model Test

Test results of the Nous-Hermes-13b model run locally (CPU only) on the same sample of 50 biographies on which the GPT-3 and GPT-4 models were tested for extracting family relationship information. The model tested (https://huggingface.co/NousResearch/Nous-Hermes-13b) is a version of Llama-13b. Since it is smaller than the GPT models and was run locally (which is quite time-consuming on a non-GPU computer), the processing of the biographies was simplified to a single question - about the father of the main character of the text.

Used prompt (in Polish):

```TXT
Based only on the information from the given text, write who was the father of <person>.
Save the result in JSON format.
For example:
Text: "Łukasz Kowalski (1901-1987) ur. w Bogatce z ojca Hieronima i matki Heleny z Kruszyńskich."
Result: {"ojciec": "Hieronim Kowalski"}
Text: "Marcin Wielopolski (1700-1776), szlachcic pomorski, ur. w Ustce. Ojcem W. był Antoni, herbu Trójnóg."
Result: {"ojciec": "Antoni Wielopolski"}
Text: "Eustachy Wikozy (zm. 1233), pochodzenie nienane, klucznik gnieźnieński."
Result: {"ojciec":"brak danych"}

Text: <data>
Result:
```

Where in place of `<person>` was inserted the name of the main character, while in place of `<date>`.
the simplified text of the biography. Compared to GPT-4, the Nous-Hermes-13b model can process a much smaller context size (2048 tokens), so both the question content, examples and the biography itself had to be limited. Biographies where they exceeded 1,700 tokens were limited to 3 initial and 2 final sentences, and those sentences where affinity keywords occurred. Shortening the text could unfortunately affect the model's performance.

| Person / Result | Correct? |
| ------------------------------------------------------------ | :---------: |
| **Aloe Franciszek Eljasz** | |
| {"ojciec": "Jan Baptysta d’Aloy i Henryka Rakocy"} | True? |
| **Bartoszewski Jan** | |
| "The father of Jan Bartoszewski is not mentioned in the given text." | True |
| **Bezprym** | |
| {"ojciec": "Bolesław Chrobry"} | True |
| **Dąbrowska_Pelagia** | |
| {"ojciec": "Michał Zgliczyński"} | True |
| **Daszyński Ignacy** | |
| ...Ignacy Daszyński miał ojca Ferdynanda. | True |
| **Dzierżek_Natalia** | |
| {"ojciec": "Henryk Dzierżek"} | True |
| **Eufrozyna** | |
| {"ojciec": "Kazimierz, ks. opolski"} | True |
| **Ewild al. Eywild** | |
| {"ojciec": "Eywild al. Eywild Jan"} | **False** |
| **Ezra ben Nisan** | |
| {"ojciec": "Ezra ben Nisan z Trok, inaczej Ezra Nisanowicz (ok. 1596–1666)"} | **False** |
| **Falęta** | |
| {"ojciec": "brak danych"} | True |
| **Fiorentini Władysław** | |
| {"ojciec": "Antoni Fiorentini"} | True |
| **Fuzorius Bartłomiej** | |
| {"ojciec": "Stanisław Lwowczyk"} | True |
| **Gliński Iwan** | |
| {"ojciec": "Lew Borysowicz"} | True |
| **Gołaski Jan** | |
| {"ojciec": "Jan Gołaski"} | **False** |
| **Grzegorzewski Jan** | |
| {"ojciec": "Jakub"} | True |
| **Guicciardini Galeazzo** | |
| {"ojciec": "Guicciardini Galeazzo"} | **False** |
| **Hincza z Rogowa** | |
| {"ojciec": "Hinczka z Rogowa (zm. przed 1415)"} | True |
| **Hirschenfeld-Mielecki Józef** | |
| {"ojciec": "brak danych"} | True |
| **Jadwiga Jagiellonka** | |
| {"ojciec": "Kazimierz Jagiellończyk"} | True |
| **Kakowski Aleksander** | |
| {"ojciec": "Franciszek Kakowski"} | True |
| **Krumhausen Gabriel** | |
| {"ojciec": "Joachim Krumhausen"} | True |
| **Łańcucki Wojciech** | |
| {"ojciec": "Stanisław Łańcucki"} | True |
| **Langfort Teodor Henryk** | |
| {"ojciec": "brak danych"} | True |
| **Leymiter Stanisław** | |
| {"ojciec": "Mikołaj Leymiter"} | True |
| **Mierzeński Aleksander** | |
| {"ojciec": "Abraham Mierzeński"} | True |
| **Mostowska z Bujwidów** | |
| {"ojciec": "Odo Bujwid, prof. bakteriologii UJ"} | True |
| **Patruus** | |
| {"ojciec": "Jan Patruus"} | **False** |
| **Pichgiel** | |
| {"ojciec": "Christian Pichgiel młodszy"} | **False** |
| **Pion Maurice** | |
| {"ojciec": "Antoine Claude Pion"} | True |
| **Piotrowiczowa z Rogolińskich** | |
| {"ojciec": "Zygmunt Rogoliński"} | True |
| **Popiel** | |
| {"ojciec": "Popiel"} | **False** |
| **Renard Benedykt** | |
| {"ojciec": ""} | True |
| **Rossi Piotr** | |
| {"ojciec": "Andrzej Rossi"} | True |
| **Sapieha_Jan_Fryderyk** | |
|  ...ojcem Jan Fryderyk Sapieha był Fryderyk | True |
| **Siemowit** | |
| The prompt asks to determine who was the father of Siemowit.. | **False** |
| **Śląska Aleksandra** | |
| {"ojciec": "Edmund Wąsik"} | True |
| **Słowicki Józef** | |
| {"ojciec": "Józef Słowicki"} | True |
| **Śniadecka Kornelia Ludwika**
| {"ojciec": "Jędrzej Śniadecki"} | True |
| **Spektor Mordechaj** | |
| {"ojciec": "Mordechaj Spektor"} | **False** |
| **Spycigniew_z_Dąbrowy** | |
| {"ojciec": "brak danych"} | True |
| **Stańczakowa ze Strancmanów** | |
| {"ojciec": "Adolf Strancman"} | True |
| **Stanisław_Cielątko** | |
| {"ojciec": "Jan Cielątko"} | True |
| **Strzelecki Wiesław Marian** | |
| {"ojciec": "Felicjan Strzelecki"} | True |
| **Swach Jerzy** | |
| {"ojciec": "Udalryk (Oldrzycha) Swach"} | True |
| **Świrski Jerzy Włodzimierz** | |
| {"ojciec": "Włodzimierz Świrski"} | True |
| **Szapira Majer** | |
| {"ojciec": "Jakub Szamszon (1861–1948)"} | True |
| **Szapocznikow_Alina** | |
| The father of Alina Szapocznikow is Jakub Szapocznik (1896-1938) | True |
| **Szczubioł_Andrzej** | |
| {"ojciec": "Stefan Szczubioł z Jasieńca i Ciechomic"} | True |
| **Sztaffel Izrael** | |
| {"ojciec": "Izrael Abraham Sztaffel"} | **False** |
| **Szumski Boksa** | |
| {"ojciec": "brak danych"} | True? |

In 2 doubtful cases a question mark was added to the True/False result (once the model returned both father and mother, the second time no data, meanwhile the biography mentions a probable father). **The result of the model's work is 40/50 correct answers which means 80% accuracy**, which seems a very good result. However, comparing it with the achievements of GPT-4, if you look only at the results for the 'father' category, the current best language model made only 1 error (98% accuracy) and the 'main character->father' relationship itself seems to be one of the easiest to obtain. Despite all this, however, Nous-Hermes-13b is many times a smaller and simpler model, is available for free for non-commercial use, can be run on a regular laptop without a GPU (but with 16GB RAM and it will run very slowly), but most importantly **processes texts in Polish**!

Other comments:

- the model sometimes has a problem with returning the result in the expected format,
- waiting time for the result, despite the shortening of the biographies is 2-7 minutes per biography,
- the model is very sensitive to the shape and content of the prompt, a small change was able to significantly degrade the result

### Verifying the results returned by LLM - Guardrails

The results returned by LLM are variable, not always in the correct expected format, not always true, even when high quality content is passed to the query context. Therefore, they require verification before further use, such as saving to a knowledge base. To facilitate this process, one can use [guardrails](https://shreyar.github.io/guardrails/), a Python language library that facilitates both the verification of the structure of the response and, to some extent, the verification of the facts.

The guardrails library uses specifications written as xml files in the Reliable AI Markup Language (RAIL) standard that describe the structure of the expected result, the format of the result fields, optional validations, and the prompt.

An example RAIL file for a query that returns basic hero/heroine biography data looks like this:

```XML
<rail version="0.1">

<output>
    <object name="person_info">
        <string name="place_of_birth" description="Miejsce urodzenia bohatera/bohaterki biogramu" />
        <string name="place_of_death" description="Miejsce śmierci bohatera/bohaterki biogramu" />
        <string name="place_of_burial" description="Miejsce pochówku bohatera/bohaterki biogramu " />
        <date name="date_of_birth" description="Data urodzenia bohatera/bohaterki biogramu" date_format='%Y-%m-%d'/>
        <date name="date_of_death" description="Data śmierci bohatera/bohaterki biogramu" date_format='%Y-%m-%d'/>
        <date name="date_of_burial" description="Data pochówku bohatera/bohaterki biogramu" date_format='%Y-%m-%d'/>
    </object>
</output>

<prompt>
Na podstawie podanego tekstu biografii wyszukaj miejsce urodzenia, miejsce śmierci i miejsce pochówku głównego bohatera/bohaterki.
Podaj także datę urodzenia i datę śmierci oraz datę pochówku.

Tekst: {{document}}

@xml_prefix_prompt

{output_schema}

@json_suffix_prompt
</prompt>
</rail>
```

Below is a simple script using the guardrails library and the RAIL specification stored in the person_basic.xml file:

```Python
""" guardrails - podstawowe informacje o postaci z biogramu  """
import os
from pathlib import Path
import guardrails as gd
import openai
from dotenv import load_dotenv


# api key
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_ORG_ID = os.environ.get('OPENAI_ORG_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

# biogram
file_path = Path(".") / 'Szpręga Teodor.txt'
with open(file_path, 'r',encoding='utf-8') as f:
    content = f.read()

# create a Guard object
rail_spec_path = Path(".") / 'person_basic.xml'
guard = gd.Guard.from_rail(rail_spec_path)

raw_llm_output, validated_output = guard(
    openai.ChatCompletion.create,
    prompt_params={"document": content},
    max_tokens=800,
    model="gpt-3.5-turbo-16k",
    temperature=0
)

# result
print(validated_output)
```

The result of the script:

```JSON
{
  "person_info": {
    "place_of_birth": "Czersk",
    "place_of_death": "Osieczna",
    "place_of_burial": "Osieczna",
    "date_of_birth": "1833-11-01",
    "date_of_death": "1911-07-26",
    "date_of_burial": null
  }
}
```

### Example of information extraction from a PSB biography

The analysed biography of Teodor Szpręga comes from the 49th volume of the PSB (Polski Słownik Biograficzny) published in 2013. Using the GPT-4 model, an attempt was made to extract from the text of the biography all the information necessary to prepare the data for input into the wikibase instance. In particular:

- basic data: date and place of birth, date and place of death, date and place of burial of the character
- data on functions, offices held by the character
- data on family relations
- data on institutions with which the biography's protagonist was associated
- data on the towns to which the biography's protagonist was connected
- data on persons (other than relatives) important to the biographical hero
and a one-sentence summary of the biography, which can be used as a description of the item in the wikibase
- nicknames, variants of names and surnames of the biography's protagonist.

Below is a list of prompts with results, the examples use fictional character data.

**Prompt for basic data**:

```TXT
Na podstawie podanego tekstu biografii wyszukaj miejsce urodzenia, miejsce śmierci i miejsce pochówku głównego bohatera/bohaterki.
Podaj także datę urodzenia i datę śmierci.
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
place_of_birth: miejsce urodzenia bohatera/bohaterki
place_of_death: miejsce śmierci bohatera/bohaterki
place_of_burial: miejsce pochówku bohatera/bohaterki
date_of_birth: data urodzenia bohatera/bohaterki
date_of_death: data śmierci bohatera/bohaterki
date_of_burial: data pochówku bohatera/bohaterki
Jeżeli jakiejś informacji brak w podanym tekście napisz: 'brak danych'

Przykład 1.
Tekst: "Soderini Carlos (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Ur. się 1 czerwca, we wsi Andalewo koło Wyszeborga. Jego bratanicą była Małgorzata Anna, żona
Winfrida de Loeve. S. ożenił się z Joanną, córką burgrabiego
krakowskiego Adama Kurozwęckiego. Zmarł w Hurczynianach, pochowano go na miejscowym cmentarzu parafialnym."
Wynik:
[{"place_of_birth":"Andalewo"},
 {"place_of_death":"Hurczyniany"},
 {"place_of_burial":"cmentarz parafialny w Hurczynianach"},
 {"date_of_birth":"1557-06-01"},
 {"date_of_death":"1591"},
 {"date_of_burial":"brak danych"}
]

Tekst: [TEKST_BIOGRAMU]
```

Result:

```JSON
[
  {"place_of_birth":"Czersk"},
  {"place_of_death":"Osieczna"},
  {"place_of_burial":"plac przed kościołem w Osiecznej"},
  {"date_of_birth":"1833-11-01"},
  {"date_of_death":"1911-07-26"},
  {"date_of_burial":"brak danych"}
]
```

**Note**: For this query, identical results were also returned by the `gpt-3.5-turbo' model.
(significantly cheaper than GPT-4), but for the other queries the quality of the gpt-4 model's answer was significantly better.

**Prompt for functions and offices held**:

```TXT
Na podstawie podanego tekstu biografii wyszukaj wszystkie urzędy i funkcje pełnione przez głównego bohatera/bohaterkę.
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
function: funkcja, urząd pełnione przez bohatera/bohaterkę

Przykład 1.
Tekst: "Soderini Carlos (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Jego bratanicą była Małgorzata Anna, żona
Winfrida de Loeve. S. ożenił się z Joanną, córką burgrabiego
krakowskiego Adama Kurozwęckiego."
Wynik:
[{"function":"kupiec"},
 {"function":"bankier"}
]

Tekst: [TEKST_BIOGRAMU]
```

Result:

```JSON
[
  {"role_or_office":"reformat"},
  {"role_or_office":"misjonarz"},
  {"role_or_office":"komisarz generalny w Poznańskiem"},
  {"role_or_office":"uczeń w gimnazjum katolickim w Chojnicach"},
  {"role_or_office":"zakonnik Zakonu Braci Mniejszych w Prow. Reformatów Niepokalanego Poczęcia NMP"},
  {"role_or_office":"student filozofii i teologii w klasztorze w Łąkach"},
  {"role_or_office":"kapłan"},
  {"role_or_office":"student teologii w Prow. Rekolektów Krzyża Świętego w Westfalii"},
  {"role_or_office":"wykładowca historii Kościoła w studium seminaryjnym w Miejskiej Górce"},
  {"role_or_office":"wicemagister nowicjatu w Wejherowie"},
  {"role_or_office":"kaznodzieja w Wejherowie"},
  {"role_or_office":"dyrektor Trzeciego Zakonu w Wejherowie"},
  {"role_or_office":"gwardian w Wejherowie"},
  {"role_or_office":"gwardian i dyrektor domu księży demerytów w Osiecznej"},
  {"role_or_office":"kaznodzieja w Zamartem i Miejskiej Górce"},
  {"role_or_office":"misjonarz apostolski"},
  {"role_or_office":"kapelan sióstr franciszkanek i ambasady austro-węgierskiej w Stambule"},
  {"role_or_office":"wikariusz w Kurzętniku"},
  {"role_or_office":"wikariusz w Zblewie"},
  {"role_or_office":"wikariusz parafii w Miejskiej Górce"},
  {"role_or_office":"duszpasterz w kościele zakonnym na Goruszkach"},
  {"role_or_office":"wikariusz parafii w Dubinie"},
  {"role_or_office":"zastępca prowincjała"},
  {"role_or_office":"komisarz generalny"},
  {"role_or_office":"dyrektor domu księży demerytów w Osiecznej"},
  {"role_or_office":"zastępca proboszcza parafii w Drzeczkowie"}
]
```

**Note**: all the information prepared by the model is correct, no function/office is likely to have been omitted, possible minor awkwardness may be noted - if the protagonist was deputising for a parish priest then (I think) he was not acting as `deputy parish priest', he was only temporarily a parish priest.

**Prompt for family relationships**:

```TXT
Na podstawie podanego tekstu wyszukaj wszystkich krewnych lub powinowatych głównego bohatera tekstu: {name}. Możliwe rodzaje pokrewieństwa: ojciec, matka, syn, córka, brat, siostra, żona, mąż, teść, teściowa, dziadek, babcia, wnuk, wnuczka, szwagier, szwagierka, siostrzeniec, siostrzenica, bratanek, bratanica, kuzyn, kuzynka, zięć, synowa.
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
family relation: rodzaj pokrewieństwa (kim osoba była dla bohatera/bohaterki )
person: nazwa (imię i nazwisko osoby związanej relacją z bohaterem)
Wypisz tylko rodzaje pokrewieństwa, które występują w tekście.
Jeżeli w tekście nie ma żadnych informacji o pokrewieństwach głównego bohatera napisz: "brak danych".

Przykład 1
Tekst: "Soderini Carlo (ok. 1537–1581), kupiec i bankier. Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym bratem Bernarda (zob.).
Jego bratanicą była Małgorzata Anna, żona Winfrida de Loeve. S. ożenił się z Joanną, córką burgrabiego krakowskiego Adama Kurozwęckiego."
Wynik:
[{"family_relation":"ojciec", "person":"Niccola Ricasoli"},
 {"family_relation":"matka": "person":"Annalena Ricasoli"},
 {"family_relation":"brat": "person":"Bernard"},
 {"family_relation":"bratanica": "person":"Małgorzata Anna"},
 {"family_relation":"żona": "person":"Joanna"},
 {"family_relation":"teść": "person":"Adam Kurozwęcki"}
]

Tekst: [TEKST_BIOGRAMU]
```

Result:

```JSON
[
  {"family_relation":"ojciec", "person":"Ignacy"},
  {"family_relation":"matka", "person":"Katarzyna Sabiniarz"}
]
```

**Note**: this is the correct result, all family relationships of the main character in the biography are listed.

**Prompt returning the institutions with which the biography's protagonist was associated**:

```TXT
Na podstawie podanego tekstu biografii wyszukaj instytucje związane z głównym bohaterem/bohaterką.
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
institution: nazwa instytucji związanej z bohaterem/bohaterką
place_of_institution: miejscowość w której położona jest instytucja związana z bohaterem/bohaterką
Miejscowość podaj w mianowniku.
Jeżeli jakiejś informacji brak w podanym tekście napisz: 'brak danych'

Przykład 1.
Tekst: "Soderini Carlos (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Ur. się 1 czerwca, we wsi Andalewo koło Wyszeborga.
Pracował w Banku Czeskim we Wrocławiu, później zaś praktykował w Izbie Celnej miasta Gdańska.
Zmarł w Hurczynianach, pochowano go na miejscowym cmentarzu parafialnym."
Wynik:
[{"institution":"Bank Czeski", "place_of_institution":"Wrocław"},
 {"institution":"Izba Celna", "place_of_institution":"Gdańsk"}
]

Tekst: [TEKST_BIOGRAMU]
```

Result:

```JSON
[
  {"institution":"Gimnazjum katolickie", "place_of_institution":"Chojnice"},
  {"institution":"Zakon Braci Mniejszych", "place_of_institution":"Wejherowo"},
  {"institution":"Klasztor w Łąkach", "place_of_institution":"Łąki"},
  {"institution":"Prowincja Rekolektów Krzyża Świętego", "place_of_institution":"Westfalia"},
  {"institution":"Studium seminaryjne", "place_of_institution":"Miejska Górka"},
  {"institution":"Dom księży demerytów", "place_of_institution":"Osieczna"},
  {"institution":"Klasztor przy kościele NMP (zwanej Draperis)", "place_of_institution":"Stambuł"},
  {"institution":"Kaplica ambasady austro-węgierskiej", "place_of_institution":"Stambuł"},
  {"institution":"Parafia w Kurzętniku", "place_of_institution":"Kurzętnik"},
  {"institution":"Parafia w Zblewie", "place_of_institution":"Zblewo"},
  {"institution":"Parafia w Miejskiej Górce", "place_of_institution":"Miejska Górka"},
  {"institution":"Kościół zakonny na Goruszkach", "place_of_institution":"Miejska Górka"},
  {"institution":"Parafia w Dubinie", "place_of_institution":"Dubin"},
  {"institution":"Parafia w Drzeczkowie", "place_of_institution":"Drzeczkowo"}
]
```
**Notes**: It is difficult to say where the model got the "embassy chapel" from, it is rather an example of hallucination - the text only mentions that the protagonist of the biography was a chaplain of the Austro-Hungarian embassy.

**Prompt for localities associated with the hero/heroine of the biography**:

```TXT
Na podstawie podanego tekstu biografii wyszukaj miejscowości związane z głównym bohaterem/bohaterką.
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
place: nazwa miejscowości związanej z bohaterem/bohaterką
date: data, kiedy bohater/bohaterka przebywał w danej miejscowości
Miejscowość podaj w mianowniku.
Jeżeli jakiejś informacji brak w podanym tekście napisz: 'brak danych'

Przykład 1.
Tekst: "Soderini Carlos (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Ur. się 1 czerwca, we wsi Andalewo koło Wyszeborga.
Pracował w Banku Czeskim we Wrocławiu w latach 1577-78, później zaś, od 1579 roku praktykował w Izbie Celnej miasta Gdańska.
Pod koniec życia zamieszkał w Elblągu w pobliżu portu.
Zmarł w Hurczynianach, pochowano go na miejscowym cmentarzu parafialnym."
Wynik:
[{"place":"Andalewo", "date":"1557-06-01"},
 {"place":"Wrocław", "date":"1577-1578"},
 {"place":"Gdańsk", "date":"1579"},
 {"place":"Elbląg", "date":"brak danych"},
 {"place":"Hurczyniany", "date":"1591"}
]

Tekst: [TEKST_BIOGRAMU]
```

Result:

```JSON
[
  {"place":"Czersk", "date":"1833-11-01"},
  {"place":"Chojnice", "date":"brak danych"},
  {"place":"Wejherowo", "date":"1856-05-05"},
  {"place":"Łąki", "date":"1857-05-06"},
  {"place":"Westfalia", "date":"brak danych"},
  {"place":"Miejska Górka", "date":"1861-09-02"},
  {"place":"Osieczna", "date":"1865-07"},
  {"place":"Zamarte", "date":"1870"},
  {"place":"Stambuł", "date":"1872-05"},
  {"place":"Adampol", "date":"brak danych"},
  {"place":"Rzym", "date":"1881-07-05"},
  {"place":"Kurzętnik", "date":"1884"},
  {"place":"Zblewo", "date":"1885-01"},
  {"place":"Goruszki", "date":"1887-07"},
  {"place":"Dubinie", "date":"1887-09-05"},
  {"place":"Poznań", "date":"brak danych"},
  {"place":"Asyż", "date":"1895-05-16"},
  {"place":"Drzeczkowo", "date":"1900-10-09"}
]
```

**Notes**: The locality in which the biography's protagonist died was not included, perhaps because it also occurred earlier, and the query did not make it clear that localities could occur multiple times with different dates.

One of the localities on the list appears in a modified form (Dubina) despite a clear indication
in the prompt for place names to be listed in the nominative.

The information concerning Poznań only mentions the hero's issuing of monastic rules, it does not necessarily mean that he stayed in this city, this result can therefore be considered questionable.

Vienna and Trieste, through which the hero travelled in 1872, are omitted.

**Prompt returning a list of important people for the main character in the biography**:

```TXT
Na podstawie podanego tekstu biografii wyszukaj osoby związane z głównym bohaterem/bohaterką, lecz pomiń krewnych i powinowatych.
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
name: imię i nazwisko osoby związanej z bohaterem/bohaterką
date: data, kiedy bohater/bohaterka spotkał/zetknał się z daną osobą
info: dodatkowe informacje o osobie np. funkcja, zawód
Jeżeli jakiejś informacji brak w podanym tekście napisz: 'brak danych'

Przykład 1.
Tekst: "Soderini Carlos (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Ur. się 1 czerwca, we wsi Andalewo koło Wyszeborga. Od 1567 roku uczył się w szkole wiejskiej
prowadzonej przez księdza Jana Tokalskiego z Krakowa. Następnie wstąpił na uniwersystet w Królewcu, gdzie zaprzyjaźnił się
ze Zdenkiem Kovacem, synem właściciela banku w Pradze, oraz z Czesławem Dąbkiem.
Pracował w Banku Czeskim we Wrocławiu w latach 1577-78, później zaś, od 1579 roku praktykował w Izbie Celnej miasta Gdańska.
Pod koniec życia zamieszkał w Elblągu w pobliżu portu, gdzie jeszcze w 1590 r. prowadził interesy handlowe z Morycem Wachowskim,
kupcem zbożowym.
Zmarł w Hurczynianach, pochowano go na miejscowym cmentarzu parafialnym."
Wynik:
[{"name":"Jan Tokalski", "date":"1567", "info":"ksiądz"},
 {"name":"Zdenek Kovac", "date":"brak danych","info":"syn właściciela banku"},
 {"name":"Czesław Dąbek", "date":"brak danych","info":"brak danych"},
 {"name":"Moryc Wachowski", "date":"1590", "info":"kupiec zbożowy"},
]

Tekst: [TEKST_BIOGRAMU]
```

Result:

```JSON
[
  {"name":"Jerzy Jeschke", "date":"1858", "info":"chełmiński biskup pomocniczy"},
  {"name":"Pacyfik Bydłowski", "date":"1881","info":"były prowincjał i definitór generalny zakonu"},
  {"name":"Bernardyn Dal Vago", "date":"brak danych","info":"generał reformatów"},
  {"name":"Roger Binkowski", "date":"1889", "info":"prowincjał"},
  {"name":"Alojzy Canali", "date":"1890", "info":"generał reformatów"},
  {"name":"Florian Stablewski", "date":"1900", "info":"arcybiskup gnieźnieński i poznański"},
  {"name":"Euzebiusz Stateczny", "date":"1904", "info":"brak danych"},
  {"name":"Dionizy Schuler", "date":"1906", "info":"generał zakonu"}
]
```
**Notes**: omitted Rev. Michał Ławrynowicz, whose account the protagonist was writing down - which probably means that he met him (?).

**Prompt creating a one-sentence summary of the biography**:

```TXT
Na podstawie podanego tekstu napisz jednozdaniowy opis głównego bohatera/bohaterki, który będzie opisem itemu w bazie wiedzy na temat tej postaci.

Przykład 1
Tekst: "Soderini Carlos (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Ur. się 1 czerwca, we wsi Andalewo koło Wyszeborga. Od 1567 roku uczył się w szkole wiejskiej
prowadzonej przez księdza Jana Tokalskiego z Krakowa. Następnie wstąpił na uniwersystet w Królewcu, gdzie zaprzyjaźnił się
ze Zdenkiem Kovacem, synem właściciela banku w Pradze.
Pracował w Banku Czeskim we Wrocławiu w latach 1577-78, później zaś, od 1579 roku praktykował jako młodszy asystent celny w Izbie Celnej miasta Gdańska.
Pod koniec życia zamieszkał w Elblągu w pobliżu portu, gdzie prowadził interesy handlowe z Morycem Wachowskim.
Zmarł w Hurczynianach, pochowano go na miejscowym cmentarzu parafialnym."
Wynik:
"Soderini Carlos (ok. 1557–1591), kupiec, bankier i asystent celny, studiował na Uniwersytecie w Królewcu."

Tekst: [TEKST_BIOGRAMU]
```

Result:

```TXT
"Szpręga Teodor (1833–1911), reformat, misjonarz i komisarz generalny, prowadził
nauczanie w szkole seminaryjnej, służył jako kapelan w Stambule i pracował na
odbudowę zakonu w Polsce."
```

Result with parameter `temperature` = 0.0:

```TXT
"Teodor Szpręga (1833-1911), reformat, misjonarz i komisarz generalny
w Poznańskiem, był wykładowcą historii Kościoła, kaznodzieją, kapelanem
sióstr franciszkanek i ambasady austro-węgierskiej w Stambule oraz dyrektorem
domu księży demerytów w Osiecznej."
```

Result prepared by the `gpt-3.5-turbo` model (also with parameter `temperature` = 0.0):

```TXT
Szpręga Teodor, w zakonie Anastazy (1833—1911), reformat, misjonarz i komisarz
generalny w Poznańskiem, autor przetłumaczonej na język polski "Reguły Trzeciego
Zakonu S. O. Franciszka".
```

**Prompt that searches for variants of a character's name, and their pesudonyms/cryptonyms**:

```TXT
Na podstawie podanego tekstu biografii wyszukaj wszystkie warianty nazwiska (także błędne),
imienia (także błędne) i pesudonimy lub kryptonimy
głównego bohatera/bohaterki (pomiń pseudonimy innych osób występujących w tekście).
Wynik przedstaw w formie listy obiektów JSON zawierających pola:
name_variant: wariant nazwiska bohatera/bohaterki
forname_variant: wariant imienia bohatera/bohaterki
nickname: pseudonim lub kryptonim bohatera/bohaterki

Przykład 1.
Tekst: "Soderini (Sodderini, Sodero) Carlos, pseud.: Carlito, Jan Będowski (ok. 1557–1591), kupiec i bankier.
Był jednym z pięciu synów Niccola i Annaleny Ricasoli, młodszym
bratem Bernarda (zob.). Jego bratanicą była Małgorzata Anna, żona
Winfrida de Loeve znanego też pod psed. Ikarus. S. ożenił się z Joanną, córką burgrabiego
krakowskiego Adama Kurozwęckiego."
Wynik:
[{"name_variant":"Sodderini"},
 {"name_variant":"Sodero"},
 {"forname_variant":"Karl"},
 {"nickname":"Carlito"},
 {"nickname":"Jan Będowski"},
]

Tekst: [TEKST_BIOGRAMU]
```

Result (for another biography - Wladyslaw Szpilman, as pesudonyms occur in it):

```JSON
[{"name_variant":"Spielman"},
{"forname_variant":"Wolf"},
{"nickname":"Al Legro"},
{"nickname":"Wiktor Karwiński"}
]
```

Another person's nickname also appears in the biography, but is omitted, according to the prompt and example.

The same prompt run by the 'gpt-3.5-turbo' model (`temperature` = 0.0) returns a worse result:

```JSON
[
  {"name_variant":"Spielman"},
  {"forname_variant":"Władysław"},
  {"nickname":"Al Legro"},
  {"nickname":"Wiktor Karwiński"},
]
```

### GPT and PSB Biographies - Remarks and Conclusions

- GPT-4 gives much better results than GPT-3 or GPT-3.5-turbo, even for the simplest questions about basic facts. If the biography is written in simple language and the data are provided directly, the results of gpt-3.5 and gpt-4 are similar, but the superiority of gpt-4 is visible in more difficult cases.
- The cost of using gpt-4 is 10 times higher than gpt-3.5. The cost of gpt-3 is lower than gpt-4, but considering the quality of the results, it makes less sense to use it for extracting information from biographies.
- Gpt-4, with a properly constructed prompt, is capable of extracting all the expected information from the text. The construction of the query and a suitable example in the prompt are of immense importance.
- Gpt-4 is capable of returning information in a structured form, such as a JSON object, with virtually no errors. However, you can additionally use libraries such as guardrails to verify and validate the format (and even the results).
- You will get better results if you ask for selected, specific information rather than a lot of information at once. A query limited to basic information or just family relationships will give very good results, but creating a large query that tries to extract all that data at once can make the results worse. For example, the model won't find the character's burial place, which it did flawlessly for a specific query. Unfortunately, this increases the cost of text processing, because for each biography, for example, you have to ask 6 questions each time you pass the text of the biography. The cost of processing 1 biography with the gpt-4 model then approaches several tens of cents.
- The length of the biographies is a problem, the standard gpt-4 model has a context length of 8 thousand tokens (for Polish this is about 4 thousand words), the 32k model with four times greater capabilities is not yet widely available, but even in its case many of the PSB biographies contain longer text, creating the need to shorten the text of the biography or process it in parts. For example, the longest PSB biography, of Stanislaw August Poniatowski, counts 78076 tokens (excluding the bibliography section). Depending on the topic of the question, knowing how to construct biographies, you can use different methods of shortening. For basic information, which is usually placed in the first and last sentences, you can limit the biography in this way. Information about family relationships is hidden in sentences that contain certain keywords related to kinship and affinity, this is also an easy way to limit the biography, for example, to the first few sentences and sentences that contain these words. Otherwise, you can use the option of converting text into numbers by dividing the text into fragments (e.g. sentences, paragraphs), creating embeddings for them and storing them in vector databases, then finding and gluing the most similar sentences/fragments to the subject of the query until the maximum available context size for the model is reached. However, this approach runs the risk of omitting historical information if it is scattered evenly throughout the content of the biography, e.g. important people for the protagonist of the biography will appear throughout his life and thus throughout most of the biography. In this case, it may be better to process the entire biography, but divided into parts.
- An attempt to use the cheaper gpt-3.5-turbo model to preprocess the biography, summarizing it to the content necessary to answer a question about, for example, basic data about the main character, places associated with a historical figure, failed. The model produced a reasonably correct summary, but lost some of the information, despite the inclusion of appropriate clues in the construction of the prompt. The resulting summary was therefore useless to the gpt-4 model, which could not find the information it was looking for in it.
- You can test queries using the ChatGPT Pro interface, which allows the use of the gpt-4 model, but the results may be different from those obtained when querying the model directly through the API, because by using the API we can influence the parameters of the model's operation, not in ChatGPT. In particular, when extracting information from biographies, you should reduce the value of the temperature parameter to zero.
- Data automatically extracted from biographies, of course, requires further processing before being entered into a database/knowledge base. Identification of persons, places, and institutions is necessary.
- Aligning the results is also important - the model does not always strictly follow the guidelines, for example, in the absence of data, the answer "no data" usually appears in the results, but sometimes "unknown".
- A separate issue specific to biographies is the question of modernizing pre-war spelling. The Polish Biographical Dictionary was published in 1935 and contains names in the form of Marjan (modern spelling: Marian), Apolonja (Apolonia).

An example of a larger analysis: a sample of 250 biographies from the Polish Biographical Dictionary:
[GPT_PSB](https://github.com/pjaskulski/gpt_psb)

### Automatic creation of knowledge graphs

All of the above examples of extracting knowledge from text were related to predetermined
types of information that needed to be extracted. What if it is not known what information is
contained in the historical study being processed, and we simply (!) want to extract all the facts
from the text? The LangChain library has an interesting component called [GraphIndexCreator](https://python.langchain.com/docs/modules/chains/additional/graph_qa) that serves exactly this purpose.

An example of a script processing a fragment of the biography of Adam Wacław, a prince of the Silesian Piast dynasty. For now GraphIndexCreator has some limitations, it works better for shorter texts and returns results in English, but the effect is still interesting.

```Python
import os
from langchain.llms import OpenAI
from langchain.indexes import GraphIndexCreator
from pathlib import Path
from dotenv import load_dotenv

# api key
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

text = """Adam Wacław (1574–1617) z rodu Piastów, książę cieszyński, tytułujący się także
księciem górnogłogowskim, choć tego księstwa już nie posiadał,
był synem Wacława Adama i drugiej jego żony, Katarzyny Sydonji, księżniczki saskiej.
Urodził się 12 XII 1574 r. Miał 5 lat, gdy umarł mu ojciec."""

index_creator = GraphIndexCreator(llm=OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY))
graph = index_creator.from_text(text)
result = graph.get_triples()

for item in result:
    print(item)
```

When you run the script, you get a series of triples (subject, object, predicate):

```TXT
('Adam Wacław', 'member of the Piast dynasty', 'is a')
('Adam Wacław', 'prince of Cieszyn', 'is a')
('Adam Wacław', 'prince of Górnogłogów', 'is a')
('Adam Wacław', 'Wacław Adam', 'is the son of')
('Adam Wacław', 'Katarzyna Sydonji', 'is the son of')
('Adam Wacław', '12 December 1574', 'was born on')
('Adam Wacław', 'his father died', 'was 5 years old when')
```

And this is the result of processing one of the further sentences of the biography
("_Dla poprawienia swego położenia wstąpił A. W. do służby w wojsku cesarskiem i jako dowódca oddziału, złożonego z jazdy, a więc na stanowisku podrzędnem, walczył z Turkami na Węgrzech..._"):

```TXT
('Adam Wacław', 'Imperial Army', 'joined the')
('Adam Wacław', 'a cavalry unit', 'was a commander of')
('Adam Wacław', 'the Turks', 'fought against')
```

## GPT-3.5-turbo Model Fine-tuning Test

The model was fine-tuned with 10 examples (jsonl file in the repository: link, script: fine_tuning_gpt35_test.py), which were supposed to teach it to extract basic information about a historical figure and return the result in JSON format.

A test was conducted on the standard model and the model after fine-tuning using the query (in Polish):

```
Na podstawie podanego tekstu biografii wyszukaj miejsce urodzenia,
miejsce śmierci, miejsce pochówku, datę urodzenia, datę śmierci
i datę pochówku głównego bohatera/bohaterki. Jeżeli w tekście brak danych
na ten temat, zapisz: brak danych. Wynik przedstaw w formie listy obiektów
JSON.

Tekst: Adam Wacław (1574–1617) z rodu Piastów, książę cieszyński,
tytułujący się także księciem górnogłogowskim, choć tego księstwa
już nie posiadał, był synem Wacława Adama i drugiej jego żony, Katarzyny
Sydonji, księżniczki saskiej. Urodził się 12 XII 1574 r. Miał 5 lat,
gdy umarł mu ojciec. W czasie jego małoletności rządziła księstwem
matka wraz z dodanymi jej przez cesarza opiekunami księcia. Przyjeżdżała
ona w tym celu od czasu do czasu do Cieszyna, po powtórnem wyjściu zamąż
– z wiedzą króla Stefana Batorego – za Emeryka Forgacha, żupana trenczyńskiego,
A.-W. wychowywał się przez 8 lat na dworze elektora saskiego, w r. 1595 objął
rządy w księstwie i w tym samym roku ożenił się z Elżbietą, córką ks. kurlandzkiego,
Kettlera. A.-W. umarł w Cieszynie na Brandysie 13 VII 1617; ciało jego złożono
najpierw na zamku i dopiero 4 IV następnego roku pochowano w kościele dominikanów
cieszyńskich, gdzie spoczywały zwłoki wszystkich jego poprzedników. Zostawił
5 dzieci, z których Fryderyk Wilhelm, ostatni cieszyński Piast męski, i Elżbieta
Lukrecja, ostatnia Piastówna, rządzili kolejno Księstwem.
```

Result for **standard** model: **gpt-3.5-turbo**:

```JSON
[
    {
      "imię": "Adam",
      "nazwisko": "Wacław",
      "miejsce_urodzenia": "brak danych",
      "miejsce_śmierci": "Cieszyn, Brandys",
      "miejsce_pochówku": "kościół dominikanów cieszyńskich",
      "data_urodzenia": "12 XII 1574",
      "data_śmierci": "13 VII 1617",
      "data_pochówku": "4 IV następnego roku"
    }
]
```

Result for the gpt_3.5-turbo model **after fine-tuning**:

```JSON
{
  "place_of_birth": { "place": "brak danych" },
  "place_of_death": { "place": "Cieszyn" },
  "place_of_burial": {
    "place": "Cieszyn",
    "note": "kościół dominikanów cieszyńskich"
  },
  "date_of_birth": { "date": "1574-12-12" },
  "date_of_death": { "date": "1617-07-13" },
  "date_of_burial": { "date": "1618-04-04" }
}
```

Fine-tuning cost: approx. $0.30, duration - approx. 10 minutes.

It is also possible to compare the result of the standard gpt-3.5-turbo model with a longer prompt, used during the gpt-4 test (link to the file with the prompt text):

```JSON
[
  {
    "place_of_birth": {
      "place": "brak danych"
    },
    "place_of_death": {
      "place": "Cieszyn, Brandys"
    },
    "place_of_burial": {
      "place": "kościół dominikanów cieszyńskich"
    },
    "date_of_birth": {
      "date": "1574-12-12"
    },
    "date_of_death": {
      "date": "1617-07-13"
    },
    "date_of_burial": {
      "date": "1618-04-04"
    }
  }
]
```

It must be admitted that the result obtained thanks to the fine-tuned model is indeed the best, comparable to GPT-4.

## Processing 250 Biographies with the Fine-tuned GPT-3.5-turbo Model

However, the results of the fine-tuned model should be checked on a larger sample, for example, the same series of 250 biographies that were processed by the GPT-4 model in a separate project. Below are the results of such a test.

The overall accuracy of the 3.5-turbo model results (fine-tuning) in terms of extracting basic data (place and date of birth, place and date of death, place and date of burial) from PSB character biographies (sample of 250 biographies, overall accuracy includes both found data and data not found returned by the model):

| Type of information | Correct      | Incorrect   |
| ---                 | ---          | ---         |
| Place of birth      | 182 (72.8%)  | 68 (27.2%)  |
| Place of death      | 222 (88.8%)  | 28 (11.2%)  |
| Place of burial     | 233 (93.2%)  | 17 (6.8%)   |
| Date of birth       | 226 (90.4%)  | 24 (9.6%)   |
| Date of death       | 226 (90.4%)  | 24 (9.6%)   |
| Date of burial      | 235 (94.0%)  | 15 (6%)     |
| Total               | 1315 (87.5%) | 185 (12.5%) |

Data gaps (1500 potential information: 250 biographies, 6 types of information):

| Type of information | No data     |
| ---                 | ---         |
| Place of birth      | 45          |
| Place of death      | 90          |
| Place of burial     | 137         |
| Date of birth       | 53          |
| Date of death       | 23          |
| Date of burial      | 220         |
| Total               | 568         |

The places and dates of burial are found the least often; indeed, such information often does not appear in the biographies.

If we only consider the information that was found (i.e., excluding missing data), the effectiveness of the gpt-3.5-turbo model after fine-tuning looks as follows (250 biographies were analyzed, GPT-4 results are also provided for comparison):

| Type of information | Found      | Correct      | Found (GPT-4) | Correct (GPT-4) |
| ---                 | ---        | ---          | ---           | ---             |
| Place of birth      | 205        | 137 (66.83%) | 154           | 137 (88.96%)    |
| Place of death      | 160        | 137 (85.62%) | 160           | 141 (88.12%)    |
| Place of burial     | 113        | 99 (87.61%)  | 111           | 101 (90.99%)    |
| Date of birth       | 197        | 174 (88.32%) | 180           | 177 (98.33%)    |
| Date of death       | 227        | 210 (92.51%) | 230           | 229 (99.57%)    |
| Date of burial      | 30         | 19 (63.33%)  | 26            | 23 (88.46%)     |
| Total               | 932        | 776 (83.26%) | 861           | 808 (93.84%)    |

Examining only the cases of missing data, the accuracy of the results returned by the model is higher, although a clearly weaker result in the case of the date of death is noticeable, where in nearly 1/3 of the biographies the model did not find information that was in the biography:

| Type of information | No data         | Correct      |
| ---                 | ---             | ---          |
| Place of birth      | 45              | 45 (100.00%) |
| Place of death      | 90              | 85 (94.44%)  |
| Place of burial     | 137             | 134 (97.81%) |
| Date of birth       | 53              | 52 (98.11%)  |
| Date of death       | 23              | 16 (69.57%)  |
| Date of burial      | 220             | 216 (98.18%) |
| Total               | 568             | 548 (96.48%) |

The results for the entire series of biographies show that the 3.5-turbo model after fine-tuning **is significantly weaker than the gpt-4 model** - see [results for gpt-4](https://github.com/pjaskulski/gpt_psb#analiza-poprawno%C5%9Bci-wynik%C3%B3w). What is not visible in the numbers alone, is the **frequent retrieval of correct but imprecise dates** (e.g., yearly when daily can be found in the biography - 53 cases for the date of death of the character!), or **frequent errors in the declension of geographical names** - such data were counted as correct, however with an appropriate note indicating that the model's answer was not perfect. **Considering this kind of data as incorrect would significantly worsen the model's result, e.g., for the date of death, the percentage of correctly extracted information would drop from 92 to 69!** Detailed results for each biography are available in the [repository](https://github.com/pjaskulski/gpt_psb/tree/main/results_evaluation_35ft/basic).