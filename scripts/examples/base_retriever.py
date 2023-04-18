from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document


class BaseRetriever(ABC):
    @abstractmethod
    def get_relevant_documents(self, query: str) -> List[Document]:
        """
        Get texts relevant for a query.
        :param query: string to find relevant texts for
        :return: list of relevant documents
        """

# 1. Create an index
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.vectorstores import pinecone
loader = TextLoader("state_of_the_union.txt", encoding="utf8")


from langchain.indexes import VectorstoreIndexCreator
index = VectorstoreIndexCreator().from_loaders([loader])
query = "What did the president say about Ketanji Brown Jackson"
print(index.query(query))

# 2. Create a Retriever from that index


# 3. Create a question answering chain


# 4. Ask questions
