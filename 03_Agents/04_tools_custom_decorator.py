import os
import sys
import readline
import ast
import json
from langchain.tools import tool
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold

llm = ChatGoogleGenerativeAI(
             model=os.getenv("GOOGLE_MODEL"),
             safety_settings = {
                # This demo lets the agent inspect security-adjacent data such as
                # password hashes, so the default dangerous-content filter would
                # otherwise block some useful classroom queries.
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
             }
      )
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

@tool
def fetch_users_pass(username):
   """Useful when you want to fetch a password hash for a particular user.  Takes a username as an argument.  Returns a JSON string"""
   # UNSAFE VERSION: SQL injection possibe in username params, e.g. "foo' OR 1=1 --" would return all password hashes.
   
   # @tool exposes this function to the agent with the docstring as its usage
   # hint; keep the signature simple so the model has a low-friction action.
   res = db.run(f"SELECT passhash FROM users WHERE username = '{username}';")
   
   # SQLDatabase.run returns a string representation of row tuples, so convert
   # through literal_eval before returning JSON that the agent can reason over.
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return json.dumps(result)

@tool
def fetch_users(query):
   """Useful when you want to fetch the users in the database.  Returns a list of usernames in JSON."""
   # The input is intentionally unused: LangChain tools expect a callable
   # argument, but this tool represents a fixed database lookup.
   res = db.run("SELECT username FROM users;")
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return json.dumps(result)

database = sys.argv[1]
db = SQLDatabase.from_uri(f"sqlite:///{database}")

toolkit = SQLDatabaseToolkit(db=db,llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    # These custom tools sit beside the toolkit's generic SQL tools, giving the
    # agent safer, task-specific shortcuts for common lookups.
    extra_tools=[fetch_users, fetch_users_pass],
    handle_parsing_errors=True,
    verbose=True
)

print(f"Welcome to my database querying application.  I've loaded your database at {database} and I am configured with these tools:")
for tool in agent_executor.tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    line = input("llm>> ")
    if line:
        try:
            result = agent_executor.invoke(line)
            print(result)
        except Exception as e:
            print(e)
    else:
        break
