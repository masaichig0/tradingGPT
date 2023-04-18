"""
Create Custom LLM Agent, an LLM agent consists:
    * PromptTemplate: This is the prompt template that can be used to instruct the language model on what to do.
    * LLM: This is the language model that powers the agent.
    * `stop` sequence: Instructs the LLM to stop generating as soon as thi string is found.
    * OutputParser: This determines how to parse the LLMOutput into an AgentAction or AgentFinish object.
"""

# Set up environment
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from langchain.utilities import PythonREPL
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re

# Set up tool
search = SerpAPIWrapper()
python_repl = PythonREPL()
tools = [Tool(name="Search",
              func=search.run,
              description="useful for when you need to answer questions about current events",
              return_direct=True)]
         #Tool(name="Python Code",
         #     func=python_repl.run,
         #     description="useful for when you need to run python code and visualize them",
         #     return_direct=True)]


# Prompt Template: set up the base template
template = """Answer the following questions as best you can. You have access to the following tools:
{tools}

Use the following format:

question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: teh result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final answer: the final answer to the original input question

Begin! If you use python code, please print the result to show me what you have done. Use lots of "Arg"s

Question: {input}
{agent_scratchpad} 
"""


# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation, in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


prompt = CustomPromptTemplate(template=template, tools=tools, input_variables=["input", "intermediate_steps"])


# Output Parser
class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment:)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output
            )
        # Pars out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: '{llm_output}'")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


output_parser = CustomOutputParser()


# Set up LLM
llm = OpenAI(temperature=0)


# Define the stop sequence
# Set up the Agent
llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [t.name for t in tools]
agent = LLMSingleActionAgent(llm_chain=llm_chain,
                             output_parser=output_parser,
                             stop=["\nFinal Answer:"],
                             allowed_toolks=tool_names)


# Use the Agent
agent_excutor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
agent_excutor.run("How many people lives in Canada now and how much population increase since last year?")

