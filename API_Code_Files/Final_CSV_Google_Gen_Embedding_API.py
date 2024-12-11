from flask import Flask, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.document_loaders import CSVLoader
from dotenv import load_dotenv
import pinecone

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load the documents
loader = CSVLoader(file_path='E:\\Finchat_App_chatbot\\Finance_Chat_Bot\\Data_Files\\profit_shareholder_info.csv')
data = loader.load()

# Set up text splitting and embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(data)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = PineconeVectorStore.from_existing_index(index_name="hybrid-search", embedding=embeddings, namespace="finance_data")

# Initialize LLM
llm = ChatGroq(temperature=0.3, model_name="llama-3.1-70b-versatile", max_tokens=8000)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are a financial expert chatbot designed to provide accurate, detailed, and context-driven responses. Analyze the provided data thoroughly before answering any queries.

Guidelines:

1. Calculations  
   Perform calculations such as average, sum, or multiplication exactly as requested.  
   Assume the current year is 2024 for all calculations involving past years.  
   If the user does not specify a year, calculate the data for the past five years by default.  
   Use only the specific feature mentioned in the query (e.g., 'Net Profit'), and avoid referencing other terms unless explicitly requested.

2. Handling Missing Data 
   If data for a specific year is missing, proceed to the next available year.  
   If 'Net Profit' is not mentioned for the year, consider other profit terms like 'Adjusted Net Profit'.

3. Response Boundaries
   Limit responses strictly to the provided features and context.  
   If a query is beyond the scope of the given data, inform the user politely.

4. Greetings 
   Respond politely and professionally to any user greetings.

5. Detailed Answer  
   Provide a comprehensive summary based on the available data to answer detailed queries.  
   For example, when asked about the business model of the company, the revenue growth trend, or the company's gross and net profit margins, respond by summarizing the relevant data in a clear and concise manner, focusing on the key points.

6. Language-Specific Behavior
   - For English, provide formal responses using accurate financial terminology and detailed explanations.  
   - For Hindi, deliver responses in clear and formal Hindi financial terminology, ensuring the explanation is easy to understand.

**Context and Query Format:**  
Context: {context}  
Question: {input}

Language Preference: Please answer in {language}
""")

# Create chains
document_chain = create_stuff_documents_chain(llm, prompt_template)
retriever = db.as_retriever(type="mmr", kwargs={"fetch_k": 10})
retrieval_chain = create_retrieval_chain(retriever, document_chain)

@app.route('/query', methods=['POST'])
def query_api():
    try:
        # Parse JSON payload
        data = request.json
        language = data.get("language", "English").capitalize()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400

        # Validate language input
        if language not in ["English", "Hindi"]:
            language = "English"

        # Invoke the retrieval chain
        response = retrieval_chain.invoke({"input": query, "language": language})

        # Return the result
        return jsonify({"answer": response['answer']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)