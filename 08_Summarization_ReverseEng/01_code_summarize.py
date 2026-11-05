import os
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import readline
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

def summarize(path):
    loader = GenericLoader.from_filesystem(
            path,
            glob="*",
            suffixes=[".py"],
            parser=LanguageParser(language="python"),
    )
    docs = loader.load()
    prompt = PromptTemplate.from_template("Summarize this Python code: {text}")

    chain = (
      {"text": RunnablePassthrough()} 
      | prompt
      | llm
      | StrOutputParser()
    )
    output = "\n".join([d.page_content for d in docs])
    result = chain.invoke(output)
    return(result)

print("Welcome to my code summarizer.  Give me a path to a Python program and I'll summarize it.  A blank line exits.")

while True:
    try:
        line = input("llm>> ")
        if line:
            result = summarize(line)
            print(result)
        else:
            break
    except Exception as e:
        print(e)
        break
