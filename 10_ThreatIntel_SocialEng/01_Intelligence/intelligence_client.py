import asyncio
from fast_agent.core.fastagent import FastAgent
from fast_agent.llm.model_factory import ModelFactory
from fast_agent.llm.provider_types import Provider
import questionary

# Create the application
fast = FastAgent("Intelligence Agent", skills_directory="skills")

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
    instruction="""You are a threat intelligence agent. Use the most relevant local skills to answer the user's question.

When an email address is provided, follow the email orchestrator skill first, then use the leaf skills it points to.

{{agentSkills}}

{{env}}

The current date is {{currentDate}}.""",
    model=model,
    use_history=True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
