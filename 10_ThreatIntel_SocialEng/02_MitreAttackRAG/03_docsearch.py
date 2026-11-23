from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import readline
import re

vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", task_type="retrieval_query"),
    collection_name="groups_collection",
    persist_directory="./mitre_rag_data/.chromadb"
)

def search_db(query):
    print(f'[+] Test similarity search with query: {query}')
    relevant_docs = vectorstore.similarity_search(query)
    print(f"Search returned {len(relevant_docs)} documents")
    for doc in relevant_docs:
        docpath = re.sub("^.*cs475-src","cs475-src",doc.metadata['source'])
        print(f"  {docpath}")

print("Welcome to my Mitre ATT&CK document database.  Type a phrase and I'll return the most relevant documents. Example:\nWrite a short summary about APT 28")
while True:
    line = input(">> ")
    try:
        if line:
            search_db(line)
        else:
            break
    except:
        print()
