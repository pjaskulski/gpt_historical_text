""" langchain test """
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import PromptTemplate


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_ORG_ID = os.environ.get('OPENAI_ORG_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

#model = 'text-davinci-003'
model = 'gpt-4'
llm = OpenAI(model_name=model, temperature=0.0, openai_api_key=OPENAI_API_KEY)

if not os.path.exists('../data/bodniak_small_index.faiss'):
    loader = TextLoader('../data/bodniak_small.txt', encoding='utf-8')
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(docs, embeddings)
    db.save_local('../data/', 'bodniak_small_index.faiss')
else:
    db = FAISS.load_local('../data/', 'bodniak_small_index.faiss')

query = "wymień osoby towarzyszące królowi Zygmuntowi Augustowi w podróży do Gdańska"
docs = db.similarity_search(query)
context = docs[0].page_content

template = """Na podstawie podanego tekstu {query}. Wynik przedstaw w formie
listy nienumerowanej\n\n {context}"""

prompt = PromptTemplate(
    input_variables=['query', 'context'],
    template=template,
)

result = llm(prompt.format(query=query, context=context))
print(result)
