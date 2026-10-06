import asyncio

import questionary
from fast_agent.core.fastagent import FastAgent
from fast_agent.llm.model_factory import ModelFactory
from fast_agent.llm.provider_types import Provider

fast = FastAgent("PDX CS Curl Agent", skills_directory="skills")

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
    instruction="""You are a Portland State University computer science web assistant.
Use the local pdx-cs-curl skill to fetch content from https://web.cs.pdx.edu.

{{agentSkills}}

{{env}}

The current date is {{currentDate}}.
""",
    model=model,
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
