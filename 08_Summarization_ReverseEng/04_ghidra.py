import os
from langchain_core.prompts import PromptTemplate
import uuid
import subprocess
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

# Add unique identifier to Ghidra project so conflicts don't occur
new_uuid = uuid.uuid4()
project_dir = "./src/ghidra_example/ghidra_project"  # The directory for the project
project_name = f"GhidraProject{new_uuid}"  # The project name
binary_path = "src/ghidra_example/asciiStrCmp"  # Path to the binary you want to import
script_path = "src/ghidra_example/jython_getMain.py"  # Path to your Jython script

# Assemble the command
command = [
    "analyzeHeadless",
    project_dir,
    project_name,
    "-deleteProject",
    "-import",
    binary_path,
    "-postScript",
    script_path
]


def analyze_code():
    prompt1 = PromptTemplate.from_template("""You are an expert reverse engineer, tasked with sifting finding the flag by 
    analyzing the source code that is provided

    Here is the source code:
    {code}

    Find the flag!
    """)

    # Use a bash command here to run analyzeHeadless
    ghidra_result = subprocess.run(command, text=True, capture_output=True)
    ghidra_result = ghidra_result.stdout.split("Decompiled_Main")[1]
    print(f"The result for ghidra is:\n {ghidra_result}")

    # Send output of analyzeHeadless to chain
    chain = (
      {"code": RunnablePassthrough()}
      | prompt1
      | llm
      | StrOutputParser()
    )

    llm_result = chain.invoke(ghidra_result)

    print(f"The result from LLM is: \n\n {llm_result}")

if __name__ == "__main__":
    analyze_code()
