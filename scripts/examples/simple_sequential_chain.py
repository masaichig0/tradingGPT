"""I just create my example by reading documentation. The example is responding to each return, and my example is not
quite right for this method. The key thing is to obtain the data by run the code to pass onto the chain.
"""


from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.memory import SimpleMemory


# This is an LLMChain to give me a list of the information AI need to analyze.
llm = OpenAI(temperature=0)
template = """You are a brilliant swing trader and excellent AI assistant to help human to make money with trading. 
I'm going to pass you following information, and you will analyze those information to make decision to maximize profit.
Information I provide:
{Historical Price Data with Indicator} 
{Financial Statements}: Annual report and quarterly report.
{Current Company Status}
{Recent Company news}
{Growth Estimate}
{My Starting Trading amount}


Your job is NOT give me financial advise. Your job is to find the pattern and tell me your decision and the reason for 
your decision. I will take your opinion to make my own judgement for trading. 

Please use all the python library for you to analyze data. I also like to see visualized data for you to tell me what 
you found if it is possible. In this case, you can write me a python code so I can run the code to see the visualization
you show me.

Your trading decision with reason, possibly a python code for visualization:
"""

prompt_template = PromptTemplate(input_variables=["Historical Price Data with Indicator",
                                                  "Financial Statements",
                                                  "Current Company status",
                                                  "Recent Company news",
                                                  "Growth Estimate",
                                                  "My Starting Trading Amount"],
                                 template=template)
analyze_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="your_decision")


template = """You are world class python programmer to help trader to write the code, so the trader can focus on to 
analyze and finding the patterns to make decision. 

Visualize findings:
{Visualization}

"""
programmer_chain = LLMChain(llm=llm, template=template, output_key="visualization_code")
overall_chain =SequentialChain(
    memory=SimpleMemory(memories={"My Starting Trading Amount": "$2000"}),
    chains=[analyze_chain, programmer_chain],
    input_variables=["Historical Price Data with Indicator",
                     "Financial Statements",
                     "Current Company status",
                     "Recent Company news",
                     "Growth Estimate"],
    output_variables=["visualization_code", "your_decision"],
    verbose=True
)

overall_chain({"Historical Price Data with Indicator": "run code to get dataframe",
               "Financial Statements": "run code to get data",
               "Current Company status": "run code to get data",
               "Recent Company news": "run code to get data, then search with API",
               "Growth Estimate": "run code to get data"})

