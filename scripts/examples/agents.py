from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.utilities import PythonREPL, SerpAPIWrapper


# Load langage model we're going to use to control agent.
llm = OpenAI(temperature=0)

# Next, create custom tool
python_repl = PythonREPL()
params = {"engine": "bing", "gl": "can", "hl": "en"}
search = SerpAPIWrapper(params=params)
tools = [Tool(name="Search",
              func=search.run,
              description="useful for when you need to answer questions about current events",
              return_direct=True),
         Tool(name="Python Code",
              func=python_repl.run,
              description="useful for when you need to use python library to figure out the problems.",
              return_direct=True)]


# Finally, let's initialize an aget with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("Create array with 100 random numbers, then create pandas Series. Please print the til of the Series.")

