from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import chromadb
import os
import readline

# Define embedding function
embedding_function = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", task_type="retrieval_query")

# Open vector database
current_directory = f"{os.path.dirname(__file__)}/mitre_rag_data"
chroma_db = os.path.join(current_directory, f"{current_directory}/.chromadb")

persistent_client = chromadb.PersistentClient(path=chroma_db)
db = Chroma(
    client=persistent_client,
    collection_name="groups_collection",
    embedding_function=embedding_function,
)
db.get()
retriever = db.as_retriever(search_kwargs={"k":10})

# Instantiate LLM and QA chain
from langchain.chains.question_answering import load_qa_chain
llm = GoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
chain = load_qa_chain(llm, chain_type="stuff")

def perform_query(retriever, chain, query):
    relevant_docs = retriever.invoke(query)
    results = chain.invoke({'input_documents':relevant_docs, 'question':query})
    return(results['output_text'])

print("Welcome to my Mitre ATT&CK Q&A application.  Type a query and I'll answer it based on the latest data. Example:\n Write a short summary about APT 28")
while True:
    line = input("llm>> ")
    try:
        if line:
            print(perform_query(retriever, chain, line))
        else:
            break
    except:
        print()

# Perform query by retrieving context and invoking chain
# line = """What threat actors sent phishing messages to their targets?"""
# line = """What threat actors sent messages to their targets over social media accounts?"""
# line = "What are some phishing techniques used by threat actors?"
# line = "What techniques does APT 28 utilize?"
