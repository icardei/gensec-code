import asyncio
from fast_agent.core.fastagent import FastAgent
from fast_agent.llm.model_factory import ModelFactory
from fast_agent.llm.provider_types import Provider
import questionary

# Create the application
fast = FastAgent("Code Analysis Agent")

choices = []
for model in ModelFactory.MODEL_PRESETS:
    if ModelFactory.MODEL_PRESETS[model] == Provider.FAST_AGENT:
        continue
    choices.append(model)

choices.append("custom")

model = questionary.select(
    "Select the model to use for the agent:",
    choices=choices,
).ask()

if model == "custom":
    model = questionary.text(
        "Enter the model name (e.g., 'openai.gpt-4o', 'openai.gpt-4.1', etc.):"
    ).ask()



@fast.agent(
    instruction=f"You are a code analysis assistant. Your task is to analyze source code repositories using the tools provided.",
    model=model,
    servers=["github_remote"],
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
