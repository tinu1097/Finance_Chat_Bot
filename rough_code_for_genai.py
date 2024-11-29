from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
import mysql.connector
import os
import hashlib

 
query = "what is the patient name ?"

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ' ',
    'database': 'mcq'
}

# Connect to MySQL
mysql_conn = mysql.connector.connect(**DATABASE_CONFIG)
mysql_cursor = mysql_conn.cursor()

# Compute file hash function
def compute_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Function to check if hash exists in MySQL
def hash_exists_in_mysql(file_hash, mysql_cursor):
    query = "SELECT COUNT(*) FROM pdf_hashes WHERE hash_value = %s"
    mysql_cursor.execute(query, (file_hash,))
    result = mysql_cursor.fetchone()
    return result[0] > 0

 
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index_name = "healthcare"

# Load PDF document and process
file_path = "Ritesh.pdf"
file_hash = compute_file_hash(file_path)
namespace = f"{os.path.splitext(os.path.basename(file_path))[0]}_{file_hash}"


llm = ChatGroq(temperature=0.5, model_name="llama-3.1-70b-versatile", max_tokens=8000)


prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer.if I is not present in the given context please don't answer
 
<context>
{context}
</context>
Question: {input}""")


def store_embeddings_in_pinecone(docs, index_name):
        # Initialize embeddings and store in Pinecone under the specific namespace
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name ,namespace=namespace)
    return db


if not hash_exists_in_mysql(file_hash, mysql_cursor):
    print(f"PDF with hash {file_hash} not found in MySQL. Creating embeddings and storing in Pinecone...")
     # Load the PDF and split into chunks
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    docs= text_splitter.split_documents(documents)

    db=store_embeddings_in_pinecone(docs, index_name)
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=db.as_retriever(type="mmr",kwargs={"fetch_k":10})
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    response=retrieval_chain.invoke({"input":query})
    print(response['answer'])


    # query = "what is the patient name and age"
    # print(db.similarity_search(query))

      # Store hash in MySQL for future reference
    insert_query = "INSERT INTO pdf_hashes (hash_value) VALUES (%s)"
    mysql_cursor.execute(insert_query, (file_hash,))
    mysql_conn.commit()

else:
    print("we are in else block")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print(namespace)
    db = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings ,namespace=namespace
)
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=db.as_retriever(type="mmr",kwargs={"fetch_k":10})
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    response=retrieval_chain.invoke({"input":query})
    print(response['answer']) 
    # query = "what this report is all about"
    # print(db.similarity_search(query))
    # print("everything is ok")