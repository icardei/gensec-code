import asyncio
from fast_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("SQLite Agent")

@fast.agent(
    instruction=f"You are a Sqlite3 database look up tool. Perform queries on the database given the user's input.  Utilize the user input verbatim when sending the query to the database and print the query that was sent to the database",

    # CAUTION: the older version of fastagent has compatibility problems with Gemini models.
    #          switching to OpenAI models. You need to set the OPENAI_API_KEY env var.

    # model="gemini3", # Alternates at https://fast-agent.ai/models/llm_providers
    # model="google.gemini-3.8-flash", 
    model="responses.gpt-5-mini?web_search=off",
    servers=["sqlite_stdio"],
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        if True:
            import traceback

            try:
                    await agent.interactive()
            except Exception as exc:
                traceback.print_exc()
                print(type(exc).__name__)
                print(getattr(exc, "message", str(exc)))
                print(getattr(exc, "details", "No additional details"))


if __name__ == "__main__":
    asyncio.run(main())
