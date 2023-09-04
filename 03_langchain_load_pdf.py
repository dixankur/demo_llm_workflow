from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = PyPDFLoader("./data/first-call-SNOW-ticket-categorization.pdf")
pages = loader.load()

print(pages[0])

print(pages[0].page_content)

data_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=0)
chunks = data_splitter.split_documents(pages)

print(f'Total number of chunks generated: {len(chunks)}')

print(chunks[0].page_content)

