import json
from flask import Flask, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import Pinecone
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
from langchain.schema import Document
import pinecone
import os

# Load the .env file
load_dotenv()

app = Flask(__name__)

# Load data
with open("E:\\LLama3.1_70B\\Data_Files\\Merge_top_10_companies_data.json", "r") as f:
    raw_data = json.load(f)

def extract_company_data(json_data):
    documents = []

    for record in json_data:
        # Extract the company name
        company_name = record.get("name", "Unknown Company")

        # Extract other details
        company_info = record.get("company_info", {})
        profit_loss_info = record.get("profit_loss_info", [])
        shareholders_info = record.get("shareholders_info", [])

        # Format the information for clarity
        text = (
            f"Company Name: {company_name}\n\n"
            f"Company Info:\n{company_info}\n\n"
            f"Profit/Loss Information:\n"
            f"{profit_loss_info}\n\n"
            f"Shareholders Information:\n"
            f"{shareholders_info}\n"
        )

        documents.append({"company_name": company_name, "details": text})

    return documents

documents = extract_company_data(raw_data)

documents_1 = [
    Document(page_content=doc['details'], metadata={'company_name': doc['company_name']})
    for doc in documents
]

# Setup for Langchain and LLM
llm = ChatGroq(temperature=0.5, model_name="llama-3.1-70b-versatile", max_tokens=8000)
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context.
Think step by step before providing a detailed answer. If it is not present in the given context, please don't answer.

<context>
{context}
</context>
Question: {input}""")

index_name =  "llama-3-70"

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings, namespace="stocks")
document_chain = create_stuff_documents_chain(llm, prompt)
retriever = db.as_retriever(type="mmr", kwargs={"fetch_k": 10})
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Flask route for question answering
@app.route('/ask_questions', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Question not provided"}), 400

    # Use the retrieval chain to get an answer
    response = retrieval_chain.invoke({"input": question})
    answer = response.get('answer', "Sorry, I could not find an answer to your question.")

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
