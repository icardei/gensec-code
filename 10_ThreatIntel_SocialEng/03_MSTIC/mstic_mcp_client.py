import asyncio
from fast_agent.core.fastagent import FastAgent
import nest_asyncio
nest_asyncio.apply()

fast = FastAgent("MSTIC Agent")

@fast.agent(
    instruction = f"You are an assistant providing information on threat intelligence using tools for accessing information from Microsoft's Threat Intelligence Center and Google's VirusTotal. Attempt to answer the user's question about particular addresses.",
    model = "gpt-4.1",
    servers = ["mstic"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        print("Welcome to the MSTIC Agent.  Ask me a query about particular IP addresses and I will examine threat intelligence to generate a report.  Example: Can you give me more details about this ip: 77.246.107.91? How many samples are related to this ip? If you found samples related, can you give me more info about the first one?")
        try:
            await agent.interactive()
        except Exception:
            return

if __name__ == "__main__":
    asyncio.run(main())
