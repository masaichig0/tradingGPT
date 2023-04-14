# Use LLM class

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate


def llm(model_name: str, n: int, best_of: int, temperature: float, text: list):
    """

    :param model_name: model name
    :param temperature:
    :param n: Number of generation.
    :param best_of:
    :param text: Question to the model.
    :return:
    """
    llms = OpenAI(model_name=model_name, n=n, best_of=best_of, temperature=temperature)
    llm_result = llms.generate(text)
    return llm_result


def llm_chain(product_name):
    """
    This example is for tool like specific case.
    e.g. User type for their prodct to generate their company name.
    prompt to set "What is a good name for a company that makes {user's product}?"
    :return:
    """
    llm = OpenAI(temperature=1)
    prompt = PromptTemplate(template="What is a good name for a company that makes {product}?",
                            input_variables=["product"])
    human_message_prompt = HumanMessagePromptTemplate(prompt=prompt)
    chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
    chat = ChatOpenAI(temperature=1)
    chain = LLMChain(llm=chat, prompt=chat_prompt_template)

    second_prompt = PromptTemplate(input_variables=["company_name"],
                                   template="Write a catchphrase for the following company: {company_name}")
    chain_two = LLMChain(llm=llm, prompt=second_prompt)

    third_prompt = PromptTemplate(input_variables=["company_vision"],
                                  template="Write a marketing strategy: {company_vision}")
    chain_three = LLMChain(llm=chat, prompt=third_prompt)

    forth_prompt = PromptTemplate(input_variables=['business_plan'],
                                  template="Write a business plan step-by-step. We are start-up with 3 employee: {business_plan}")
    chain_four = LLMChain(llm=chat, prompt=forth_prompt)
    from langchain.chains import SimpleSequentialChain
    overall_chain = SimpleSequentialChain(chains=[chain, chain_two, chain_three, chain_four], verbose=True)
    return overall_chain.run(product_name)

