from langchain.agents import initialize_agent, load_tools
from langchain.callbacks import CometCallbackHandler, StdOutCallbackHandler
from langchain.callbacks.base import CallbackManager
from langchain.llms import OpenAI

comet_callback = CometCallbackHandler(
    project_name="comet-example-langchain",
    complexity_metrics=True,
    stream_logs=True,
    tags=["agent"],
)
manager = CallbackManager([StdOutCallbackHandler(), comet_callback])
llm = OpenAI(temperature=0.9, callback_manager=manager, verbose=True)

tools = load_tools(["serpapi", "llm-math"], llm=llm, callback_manager=manager)
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    callback_manager=manager,
    verbose=True,
)
agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
comet_callback.flush_tracker(agent, finish=True)