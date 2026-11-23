# Derived from https://github.com/OTRF/GenAI-Security-Adventures
# This script downloads the real-time Mitre ATT&CK information on a variety of
# attack groups, formats them in Markdown files, then loads them into a vector
# database (ChromaDB).  This is subsequently used in a RAG chain to handle
# queries through an LLM
import os
import re
import copy
import glob
from langchain_community.document_loaders import UnstructuredMarkdownLoader

current_directory = f"{os.path.dirname(__file__)}/mitre_rag_data/"
documents_directory = os.path.join(current_directory, "documents")

group_files = glob.glob(os.path.join(documents_directory, "*.md"))

# Loading Markdown files
md_docs = []
print("[+] Loading Group markdown files..")
for group in group_files:
    print(f' [*] Loading {os.path.basename(group)}')
    loader = UnstructuredMarkdownLoader(group)
    md_docs.extend(loader.load_and_split())

print(f'[+] Number of .md documents processed: {len(md_docs)}')

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
# Define the embedding function
embedding_function = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", task_type="retrieval_query")

# Load documents into Chroma and save it to disk
vectorstore = Chroma.from_documents(md_docs, embedding_function, collection_name="groups_collection", persist_directory=f"{current_directory}/.chromadb")
retriever = vectorstore.as_retriever()

print("RAG database initialized.")
document_data_sources = set()
for doc_metadata in retriever.vectorstore.get()['metadatas']:
    document_data_sources.add(doc_metadata['source']) 
for doc in document_data_sources:
    docpath = re.sub("^.*cs410g-src","cs410g-src",doc)
    print(f"  {docpath}")
