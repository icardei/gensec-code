import asyncio
from fast_agent.core.fastagent import FastAgent

fast = FastAgent("Package Agent", skills_directory="skills")

@fast.agent(
    instruction="""You are a package analysis agent. Use the most relevant local skills to answer the user's question.

{{agentSkills}}""",
    model="gemini3flash",
    use_history=True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
