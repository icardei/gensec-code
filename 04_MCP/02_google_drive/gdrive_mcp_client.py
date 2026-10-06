import os
#from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
llm = ChatGoogleGenerativeAI(
             model=os.getenv("GOOGLE_MODEL"),
             safety_settings = {
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
             }
      )
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

async def run_agent():
    async with streamablehttp_client(f"{os.getenv('MCP_URL')}/mcp/") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)

            agent = create_agent(model=llm, tools=tools)

            print(f"Welcome to the Google Drive assistant. How can I help today?")

            while True:
                line = input("llm>> ")
                if line:
                    try:
                        result = await agent.ainvoke({"messages": [("user", line)]})
                        # Extract the actual message content from the agent's response
                        if "messages" in result:
                            messages = result["messages"]
                            if messages:
                                last_message = messages[-1]
                                if hasattr(last_message, 'content'):
                                    print(f"{last_message.content}")
                                else:
                                    print(f"{last_message}")
                            else:
                                print("No response from agent")
                        else:
                            print(f"Agent response: {result}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    break

if __name__ == "__main__":
    asyncio.run(run_agent())
