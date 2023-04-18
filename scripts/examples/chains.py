from langchain import PromptTemplate, OpenAI, LLMChain


def single_input():
    llm = OpenAI(temperature=0)
    template = """Question: {question}
    
    Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

    question = "What MLB team won the World Series in the year of great recession began?"
    return llm_chain.predict(question=question)


def multi_inputs(temp, adj, person):
    llm = OpenAI(temperature=temp)
    template = """Write a {adjective} story about {person}."""
    prompt = PromptTemplate(template=template, input_variables=["adjective", "person"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
    return llm_chain.predict(adjective=adj, person=person)


m_answer = multi_inputs(0.4, "exciting", "Tom Brady")
print(m_answer)

