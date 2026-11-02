import asyncio
from fast_agent.core.fastagent import FastAgent
import sys

user_instructions = sys.argv[1]

fast = FastAgent("Command Agent", skills_directory="skills")

@fast.agent(
    instruction = user_instructions + "\n\n{{agentSkills}}",
    model = "gemini3flash",
    use_history = True
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
