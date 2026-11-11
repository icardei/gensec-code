import os
import sys
import readline
import subprocess
import pexpect
import select
import threading
from langchain.agents import create_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.tools import BaseTool, tool
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

def read_output(proc):
    try:
        while True:
            # Read and print all available output from the process
            output = proc.read_nonblocking(size=1024, timeout=60)
            if output:
                print(output.decode(), end='')
    except pexpect.EOF:
        pass
    except Exception as e:
        print(f"Error reading output: {e}")

def open_shell_with_command(command_string):
    # Start the command with pexpect
    command_string += """ --output-dir="./data" """
    proc = pexpect.spawn(command_string)

    # Start a separate thread to read the output from the process
    output_thread = threading.Thread(target=read_output, args=(proc,))
    output_thread.daemon = True
    output_thread.start()

    try:
        while True:
            # Read user input
            user_input = input("Enter command: ")

            # If the user types 'exit', break the loop and close the shell
            if user_input.strip().lower() == 'exit':
                proc.sendline('exit')
                break

            # Send the user input to the shell process
            proc.sendline(user_input)

    except KeyboardInterrupt:
        print("\nTerminating the shell.")
    finally:
        # Clean up: Close the process
        proc.close()
        output_thread.join()


@tool("commix")
def commix(command: str):
    """This tool is an implementation of Commix"""
    print(f"this is the command: {command}")
    open_shell_with_command(f'commix {command}') 
    return command


tools = [commix]

instructions = sys.argv[1]

agent = create_agent(llm,tools=tools)

print(f"Welcome to my application.  I am configured with these tools")
for tool in tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent.invoke({
                "messages": [
                    SystemMessage(content=instructions),
                    HumanMessage(content=line),
                   ]
                })
            print(result['messages'][-1].content)
        else:
            break
    except Exception as e:
        print(e)
