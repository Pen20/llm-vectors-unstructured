import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_neo4j import Neo4jVector
from langchain_openai import OpenAIEmbeddings



COURSES_PATH = "/workspaces/llm-vectors-unstructured/llm-vectors-unstructured/data/asciidoc/courses/llm-fundamentals/modules"
llm-vectors-unstructured/data/asciidoc/courses/llm-fundamentals/modules/1-introduction/lessons/1-neo4j-and-genai/lesson.adoc
# Load lesson documents
loader = DirectoryLoader(COURSES_PATH, glob="**/lesson.adoc", loader_cls=TextLoader)
docs = loader.load()

# Create a text splitter
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1500,
    chunk_overlap=200,
)
# Split documents into chunks
chunks = text_splitter.split_documents(docs)

print(chunks)
# Create a Neo4j vector store
neo4j_db = Neo4jVector.from_documents(
    chunks,
    OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY')),
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD'),
    database="neo4j",  
    index_name="chunkVector",
    node_label="Chunk", 
    text_node_property="text", 
    embedding_node_property="embedding",  
)
import os
from dotenv import load_dotenv
load_dotenv()


from openai import OpenAI

llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = llm.embeddings.create(
        input="Text to create embeddings for",
        model="text-embedding-ada-002"
    )

print(response.data[0].embedding)