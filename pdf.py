from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone
import os


loader = PyMuPDFLoader("Docs\\PDFs\\2022-Annual-Review.pdf")
document = loader.load()

spliter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = spliter.split_documents(document)
print(type(docs[0]))
#embeddings = OpenAIEmbeddings()

#pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"),
#              environment=os.environ.get("PINECONE_ENVIRONMENT"))

#index_name = os.environ.get("PINECONE_INDEX_NAME")
#docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)


#query = "What is the growth margin profit in 2022?"
#docs = docsearch.similarity_search(query)

#print(docs[0].page_content)
