""" langchain test with chrome vector db """
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_ORG_ID = os.environ.get('OPENAI_ORG_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

model = 'text-davinci-003'
llm = OpenAI(model_name=model, temperature=0.0, openai_api_key=OPENAI_API_KEY)

with open("../data/bodniak.txt", 'r', encoding='utf-8') as f:
    text_bodniak = f.read()

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_text(text_bodniak)
embeddings = OpenAIEmbeddings()

persist_directory = '../data_index/'
db = Chroma.from_texts(docs,
                       embeddings,persist_directory=persist_directory,
                       metadatas=[{"source": f"{i}-pl"} for i in range(len(docs))])

prompt_template = """Na podstawie następującego tekstu odpowiedz na pytanie podane
na końcu, wynik przedstaw w formie listy.

{summaries}

Pytanie: {question}
"""

PROMPT = PromptTemplate(
    input_variables=["summaries", "question"],
    template=prompt_template,
)

chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff",
                                 retriever=db.as_retriever(search_kwargs={"k": 3}),
                                 reduce_k_below_max_tokens=True,
                                 chain_type_kwargs=chain_type_kwargs)

query = "Wymień osoby towarzyszące królowi Zygmuntowi Augustowi w podróży do Gdańska, Malborga i Królewca."
result = qa({"question": query}, return_only_outputs=True)

print(result)
