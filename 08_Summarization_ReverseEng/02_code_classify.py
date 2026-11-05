import os
import readline
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

def classify(path: str):
    loader = GenericLoader.from_filesystem(
        path,
        glob="*",
        suffixes=[".py"],
        parser=LanguageParser(language="python"),
    )
    docs = loader.load()

    prompt = PromptTemplate.from_template(
        """
        You are an advanced security analyst. Your task is to perform
        a behavioral analysis looking for specific behaviors such as:
            - **Data exfiltration**: Detect if data is sent off-machine or communicates with external IPs or servers.
            - **File creation**: Identify instances where files are created, deleted, or modified in the file system.
            - **Process launching**: Detect if new processes are launched or system commands are executed.
            - **Environment variable access**: Determine if environment variables are read or modified.
        
           For each behavior detected, provide supporting evidence and assign a confidence score (0 to 1).
        
        Respond in JSON format with the following structure:
        {{
            "behavior_analysis": [
                {{ "data_exfiltration": {{ "detected": true/false, "confidence": 0-1, "evidence": "description of findings", "code_snippet": "snippet of code" }} }},
                {{ "file_creation": {{ "detected": true/false, "confidence": 0-1, "evidence": "description of findings", "code_snippet": "snippet of code" }} }},
                {{ "process_launching": {{ "detected": true/false, "confidence": 0-1, "evidence": "description of findings", "code_snippet": "snippet of code" }} }},
                {{ "env_variable_access": {{ "detected": true/false, "confidence": 0-1, "evidence": "description of findings", "code_snippet": "snippet of code" }} }}
            ],
        }}
        
        Code:\n\n{text}
        """
    )

    chain = (
      {"text": RunnablePassthrough()} 
      | prompt
      | llm
      | StrOutputParser()
    )

    code_text = "\n".join([doc.page_content for doc in docs])
    result = chain.invoke(code_text)
    return result

if __name__ == "__main__":
    print("Welcome to the code classifier. Please enter the path to a file containing your Python code.  A blank line exits.")

    while True:
        try:
            line = input("llm>> ")
            if line:
                result = classify(line)
                print(result)
            else:
                break
        except Exception as e:
            print(e)
            break
