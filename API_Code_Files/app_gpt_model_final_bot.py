# import openai
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # List of companies
# company_names = [
#     "Alfred Herbert (India) Ltd", "Balkrishna Industries Ltd", "Oriental Aromatics Ltd",
#     "DMCC Speciality Chemicals Ltd", "Gajra Bevel Gears Ltd", "Harrisons Malayalam Ltd",
#     "Linde India Ltd", "Kesoram Industries Ltd", "Milkfood Ltd", "Pfizer Ltd"
# ]


# # OpenAI API key configuration
# openai.api_key = "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"


# # Load company data from a JSON file
# def load_company_data(file_path):
#     """
#     Loads company data from a JSON file.
#     """
#     with open(file_path, 'r') as file:
#         return json.load(file)


# # Load company data (update path to your data file)
# company_data = load_company_data('E:\\Finchat_App_chatbot\\Data_Files\\Merge_top_10_companies_data.json')


# def find_company_name(user_query):
#     # Find the company name in user query if it matches any in the list
#     for name in company_names:
#         if name.lower() in user_query.lower():
#             return name
#     return None


# @app.route('/get_company_info', methods=['POST'])
# def get_company_info():
#     data = request.json
#     user_query = data.get('query')
#     print("Query received:", user_query)

#     if not user_query:
#         return jsonify({"error": "No query provided"}), 400

#     # Find the company name from the query
#     raw_company_name = find_company_name(user_query)
#     print("Identified Company Name:", raw_company_name)

#     company_info = None
#     if raw_company_name:
#         company_info = next((company for company in company_data if company['company_info'].get('COMPNAME') == raw_company_name), None)
    
#     print("Company Info Found:", company_info)

#     if not company_info:
#         prompt = f"User question: {user_query}"
#     else:
#         # Check for specific metrics in the query
#         if "revenue growth" in user_query.lower():
#             revenue_growth = company_info.get("profit_loss_info", {})
#             response_content = f"Revenue Growth Trend for {raw_company_name}: {json.dumps(revenue_growth, indent=4)}"
#         elif "profit margin" in user_query.lower():
#             profit_margin = company_info.get("profit_loss_info", {})
#             response_content = f"Profit Margins for {raw_company_name}: {json.dumps(profit_margin, indent=4)}"
#         elif "mutual funds" in user_query.lower():
#             shareholders = company_info.get("shareholders_info", {})
#             response_content = f"Shareholders for {raw_company_name}: {json.dumps(shareholders, indent=4)}"
#         else:
#             response_content = f"Here is some information about {raw_company_name}:\n{json.dumps(company_info, indent=4)}"

#         prompt = f"{response_content}\n\nUser question: {user_query}\nAnswer:"

#     print("Constructed Prompt for GPT:", prompt)

#     try:
#         # Call GPT model
#         response = openai.ChatCompletion.create(
#             model="gpt-4o-mini",  # Or your desired model
#             messages=[
#                 {"role": "system", "content": "You are a financial expert."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300
#         )
#         answer = response['choices'][0]['message']['content'].strip()
#         print("answer:", answer)
#         return jsonify({"answer": answer})
#     except Exception as e:
#         print("Error calling GPT API:", e)
#         return jsonify({"error": "Failed to retrieve response from GPT API"})

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5000)


import openai
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# List of companies
company_names = [
    "Alfred Herbert (India) Ltd", "Balkrishna Industries Ltd", "Oriental Aromatics Ltd",
    "DMCC Speciality Chemicals Ltd", "Gajra Bevel Gears Ltd", "Harrisons Malayalam Ltd",
    "Linde India Ltd", "Kesoram Industries Ltd", "Milkfood Ltd", "Pfizer Ltd"
]


# OpenAI API key configuration
openai.api_key = "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"


# Load company data from a JSON file
def load_company_data(file_path):
    """
    Loads company data from a JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


# Load company data (update path to your data file)
company_data = load_company_data('E:\\Finchat_App_chatbot\\Data_Files\\Merge_top_10_companies_data.json')


def find_company_name(user_query):
    # Find the company name in user query if it matches any in the list
    for name in company_names:
        if name.lower() in user_query.lower():
            return name
    return None


# @app.route('/get_company_info', methods=['POST'])
# def get_company_info():
#     data = request.json
#     user_query = data.get('query')
#     print("Query:", user_query)

#     # Find the company name from the query
#     raw_company_name = find_company_name(user_query)
#     print("Identified Company Name:", raw_company_name)

#     # Get detailed company information if the name is found
#     company_info = next((company for company in company_data if company['company_info'].get('COMPNAME') == raw_company_name), None)

#     print("company_info",company_info)

#     if not company_info:
#         prompt = f"User question: {user_query}\nAnswer:"
#     else:
#         # Check for specific metrics in the query and calculate accordingly
#         if "revenue growth" in user_query.lower():
#             revenue_growth = company_info.get("profit_loss_info")
#             response_content = f"Revenue Growth Trend for {raw_company_name}: {json.dumps(revenue_growth, indent=4)}"
#         elif "profit margin" in user_query.lower():
#             profit_margin  = company_info.get("profit_loss_info")
#             response_content = f"Profit Margins for {raw_company_name}: {json.dumps(profit_margin, indent=4)}"
#         elif "Mutual Funds" in user_query.lower():
#             shareholders  = company_info.get("shareholders_info")
#             response_content = f"shareholders for {raw_company_name}: {json.dumps(shareholders, indent=4)}"
#         else:
#             # Default information if no specific metric is requested
#             response_content = f"Here is some information about {raw_company_name}:\n{json.dumps(company_info, indent=4)}"

#         # Construct the prompt with matched data or calculated metrics
#         prompt = f"{response_content}\n\nUser question: {user_query}\nAnswer:"
#         print("Prompt:", prompt)

#     # Call the GPT model using OpenAI API
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",  # Or another model as needed
#         messages=[
#             {"role": "system", "content": "You are a financial expert."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=150
#     )

#     answer = response['choices'][0]['message']['content'].strip()
#     print("answer",answer)
#     return jsonify({"answer": answer})

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5000)

@app.route('/get_company_info', methods=['POST'])
def get_company_info():
    data = request.json
    user_query = data.get('query')
    print("Query received:", user_query)

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Find the company name from the query
    raw_company_name = find_company_name(user_query)
    print("Identified Company Name:", raw_company_name)

    company_info = None
    if raw_company_name:
        company_info = next((company for company in company_data if company['company_info'].get('COMPNAME') == raw_company_name), None)
    
    print("Company Info Found:", company_info)

    if not company_info:
        prompt = f"User question: {user_query}"
    else:
        # Check for specific metrics in the query
        if "revenue growth" in user_query.lower():
            revenue_growth = company_info.get("profit_loss_info", {})
            response_content = f"Revenue Growth Trend for {raw_company_name}: {json.dumps(revenue_growth, indent=4)}"
        elif "profit margin" in user_query.lower():
            profit_margin = company_info.get("profit_loss_info", {})
            response_content = f"Profit Margins for {raw_company_name}: {json.dumps(profit_margin, indent=4)}"
        elif "mutual funds" in user_query.lower():
            shareholders = company_info.get("shareholders_info", {})
            response_content = f"Shareholders for {raw_company_name}: {json.dumps(shareholders, indent=4)}"
        else:
            response_content = f"Here is some information about {raw_company_name}:\n{json.dumps(company_info, indent=4)}"

        prompt = f"{response_content}\n\nUser question: {user_query}\nAnswer:"

    print("Constructed Prompt for GPT:", prompt)

    try:
        # Call GPT model
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Or your desired model
            messages=[
                {"role": "system", "content": "You are a financial expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        answer = response['choices'][0]['message']['content'].strip()
        print("answer:", answer)
        return jsonify({"answer": answer})
    except Exception as e:
        print("Error calling GPT API:", e)
        return jsonify({"error": "Failed to retrieve response from GPT API"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
