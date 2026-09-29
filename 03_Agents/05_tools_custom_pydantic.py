import os
import sys
import readline
import ast
import json
from pydantic import BaseModel, Field, model_validator
from langchain.tools import tool
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold

llm = ChatGoogleGenerativeAI(
             model=os.getenv("GOOGLE_MODEL"),
             safety_settings = {
                # This demo queries security-adjacent data such as password
                # hashes, so the default dangerous-content filter can interfere
                # with legitimate classroom prompts.
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
             }
      )
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

class FetchUsersPassInput(BaseModel):
    # LangChain uses this Pydantic model as the tool's input contract: the
    # Field description is surfaced to the LLM when it decides what arguments
    # to pass, and the type annotation becomes part of the generated schema.
    username: str = Field(description="Should be an alphanumeric string")

    @model_validator(mode="before")
    def is_alphanumeric(cls, values: dict[str,any]) -> dict[str,any]:
        # Validate before tool execution so malformed model-generated arguments
        # fail at the tool boundary rather than being interpolated into SQL.
        if values.get("username").isalnum():
            return values
        raise ValueError("Malformed username")

@tool("fetch_users_pass", args_schema=FetchUsersPassInput, return_direct=True)
def fetch_users_pass(username):
   """Useful when you want to fetch a password hash for a particular user.  
   Takes a username as an argument.  Returns a JSON string"""
   # args_schema binds FetchUsersPassInput to this tool, so only validated
   # alphanumeric usernames reach this query; return_direct sends the lookup
   # result straight back instead of asking the agent for another reasoning step.
   res = db.run(f"SELECT passhash FROM users WHERE username = '{username}';")

   
   # SQLDatabase.run returns a string representation of row tuples, so convert
   # through literal_eval before returning JSON that the agent can reason over.
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return json.dumps(result)

@tool
def fetch_users(query):
   """Useful when you want to fetch the users in the database.  Returns a list of usernames in JSON."""
   # This tool keeps a generic single-argument shape for LangChain, even though
   # the operation itself is a fixed enumeration of known usernames.
   res = db.run("SELECT username FROM users;")
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return json.dumps(result)

database = sys.argv[1]
db = SQLDatabase.from_uri(f"sqlite:///{database}")
toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    # Custom tools are registered alongside the generic SQL toolkit, giving the
    # agent task-specific paths whose inputs can be constrained with Pydantic.
    extra_tools=[fetch_users, fetch_users_pass],
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
