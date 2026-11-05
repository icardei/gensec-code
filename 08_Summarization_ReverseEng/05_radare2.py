import os
import r2pipe
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")

# This funtction utilizes r2pipe to decompile the binary using the r2dec.
def analyze_code(program):
    """This function can be used to decompile the binary into the C code"""

    prompt1 = PromptTemplate.from_template("""You are an expert reverse engineer, tasked with sifting finding the flag by analyzing the code that is provided.

    Here is the code:
    {code}

    Find the flag!
    """)

    try:
        # Open the binary using r2pipe
        r2 = r2pipe.open(program)

        # Perform initial analysis with radare2
        # Do not show output of these two commands
        _ = r2.cmd("aaa")  # Analyze all functions and references
        _ = r2.cmd("s main")  # Seek to the main function, if exists
        
        # Attempt to decompile the main function
        output = r2.cmd("pdd")
        
        # Check if output is empty, meaning decompilation failed
        if not output.strip():
            raise ValueError("Decompilation failed or main function not found.")
        print(output)
        
    except Exception as e:
        # Error handling with specific message
        return f"Error during decompilation: {e}"

    print(f"The result from radare2 is:\n {output}")

    # Send output to chain
    chain = (
      {'code':RunnablePassthrough()}
      | prompt1
      | llm
      | StrOutputParser()
    )

    llm_result = chain.invoke(output)

    print(f"The result from LLM is: \n\n {llm_result}")

if __name__ == "__main__":
    analyze_code("./src/ghidra_example/asciiStrCmp")
