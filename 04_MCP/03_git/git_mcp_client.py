import asyncio
import os
from fast_agent.core.fastagent import FastAgent

fast = FastAgent("Git Agent")

@fast.agent(
    instruction=f"You are a git assistant for the repository located here at {os.path.dirname(os.path.dirname(os.getcwd()))}",
    # model="gemini25",
    model="responses.gpt-5-mini?web_search=off",
    servers=["git"],
    use_history=True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
