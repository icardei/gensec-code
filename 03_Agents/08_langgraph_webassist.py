import os
import asyncio
import httpx
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.types import Send

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmCategory,
    HarmBlockThreshold,
)

# ---------------------------------------------------------------------
# LLM (Gemini)
# ---------------------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL"),
    safety_settings={
        # The summaries may include injuries, violence, or other sports news that
        # safety filters can over-classify when processing raw web headlines.
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    },
)

# ---------------------------------------------------------------------
# Graph state
# ---------------------------------------------------------------------

class State(TypedDict):
    # The graph state is the shared dictionary that flows through every node.
    # Nodes do not mutate it directly; each node returns a partial dictionary,
    # and LangGraph merges those keys into the accumulated state.
    query: str
    nba: str | None
    nfl: str | None

# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

async def fetch(url: str) -> str:
    # httpx.AsyncClient releases the event loop while waiting on the network,
    # which lets LangGraph run independent async branches without blocking.
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url)
        return r.text

async def extract_and_summarize(html: str) -> str:
    # The model call is also awaited: fetching and summarizing are both I/O-bound
    # steps, so async functions keep the graph responsive while those calls wait.
    prompt = f"""
You are given raw HTML from a sports headline feed.

1. Identify the main news article headlines on the page.
2. Ignore navigation, ads, and footers.
3. Summarize the current news in ONE concise paragraph.
4. Return only that paragraph as a string

HTML:
{html[:12000]}
"""
    resp = await llm.ainvoke(prompt)
    return resp.content[0]['text'].strip()

# ---------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------

async def nba_agent(state: State):
    # This node receives the full state, including the original query, but only
    # returns the key it owns.  LangGraph carries the other state keys forward.
    html = await fetch("https://www.espn.com/espn/rss/nba/news")
    summary = await extract_and_summarize(html)
    return {"nba": summary}

async def nfl_agent(state: State):
    # Returning only {"nfl": summary} makes this branch composable with the NBA
    # branch; when both run, their non-overlapping updates merge into one result.
    html = await fetch("https://www.espn.com/espn/rss/nfl/news")
    summary = await extract_and_summarize(html)
    return {"nfl": summary}

async def coordinator(state: State):
    # The coordinator is a pass-through entry node.  Returning an empty update
    # leaves the incoming state unchanged for the routing function.
    return {}

async def route(state: State):
    # Conditional routing functions inspect the current state and choose the next
    # node or nodes.  Because this router asks the LLM, it is async as well.
    prompt = f"""
User request: {state['query']}

Decide which sports news is requested.
Reply with exactly one word:
nba
nfl
both
"""
    resp = await llm.ainvoke(prompt)
    decision = resp.content[0]['text'].lower().strip()

    if decision == "nba":
        # Send passes an explicit state payload to the destination node.  Here it
        # forwards the same accumulated state that the coordinator received.
        return Send("nba", state)
    if decision == "nfl":
        return Send("nfl", state)
    # Returning multiple Send objects fans the same state out to both branches;
    # their returned partial updates are merged back into the final graph state.
    return [Send("nba", state), Send("nfl", state)]

# Graph

g = StateGraph(State)

g.add_node("coord", coordinator)
g.add_node("nba", nba_agent)
g.add_node("nfl", nfl_agent)

g.set_entry_point("coord")
g.add_conditional_edges(
           # After coord returns its empty update, LangGraph calls route with the
           # current state to decide which sport-specific node should receive it.
           "coord", 
           route, {
               "nba": "nba",
               "nfl": "nfl",
           }
)

g.add_edge("nba", END)
g.add_edge("nfl", END)

app = g.compile()

# Interactive prompt

print("Welcome to my sports headlines summary application.  Ask me to summarize news from a sport.")

while True:
    line = input("llm>> ")
    if line:
        try:
            # app.ainvoke drives the async graph.  asyncio.run creates the event
            # loop for this synchronous REPL iteration and waits for all awaited
            # fetch/model work in the selected branches to finish.
            result = asyncio.run(app.ainvoke({"query": line}))
            if result.get("nba"):
                print(result["nba"])
            if result.get("nfl"):
                print(result["nfl"])
        except Exception as e:
            print(e)
    else:
        break
