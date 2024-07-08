import os
import json
import re
from llm_factory import get_ollama_model
from pdf_utils import extract_text_from_pdf, tokenize_trim_text
from langchain_core.messages import HumanMessage, SystemMessage
from database_handling.database_handling import init_db, file_already_processed, log_renamed_file
from settings import ConfigContract, get_config

def query_ollama_llm(model, messages):
    try:
        response = model._generate(messages=messages)
        if response.generations:
            return response.generations[0].message.content
        else:
            return "No response generated."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def process_pdf_file(pdf_path, model, context_prompt):
    # Extract and process the PDF text
    text = extract_text_from_pdf(pdf_path)
    trimmed_text = tokenize_trim_text(text)

    # Create messages
    messages = [
        SystemMessage(content=context_prompt),
        HumanMessage(content=trimmed_text)
    ]

    # Query the model with the messages
    response = query_ollama_llm(model, messages)
    
    # Debug print the raw response
    # print(f"Raw model response:\n{response}\n")

    try:
        # Clean the response by removing unwanted characters
        response = response.strip()
        response = re.sub(r'^```json|```$', '', response).strip()
        
        # Debug print the cleaned response
        #print(f"Cleaned model response:\n{response}\n")
        
        # Parse the response as JSON
        response_json = json.loads(response)
        
        company_name = response_json.get("company_name", "").replace(" ", "_")
        year = response_json.get("year", "")
        document_type = response_json.get("document_type", "").replace(" ", "_")

        combined_string = f"{company_name}_{year}_{document_type}"
        return combined_string
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {str(e)}")
        return None

if __name__ == "__main__":
    model_key = "phi3"
    temperature = 0.0
    ollama_model = get_ollama_model(model_key, temperature)
    config = get_config()
    DATABASE_FILE = config[ConfigContract.DATABASE_FILE]

    context_prompt = (
        "Extract and return only the following three pieces of information from the text in JSON format:\n"
        "{\n  \"company_name\": \"\",\n  \"year\": \"\",\n  \"document_type\": \"\" }\n"
        "1. The name of the company should be filled in the 'company_name' field.\n"
        "2. The year the document was published should be filled in the 'year' field.\n"
        "3. The type of document (e.g., annual report, financial statement) should be filled in the 'document_type' field. 2 words maximum.\n"
        "Do not include any additional text or explanations.\n"
    )

    directory = "Test_Documents"

    init_db(DATABASE_FILE)

    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
    else:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.pdf'):
                    original_path = os.path.join(root, filename)
                    if not file_already_processed(DATABASE_FILE, original_path):
                        combined_string = process_pdf_file(original_path, ollama_model, context_prompt)

                        if combined_string:
                            new_filename = f"{combined_string}.pdf"
                            new_path = os.path.join(root, new_filename)
                            
                            # Check if the new filename already exists to avoid overwriting
                            if os.path.exists(new_path):
                                print(f"File {new_filename} already exists. Skipping rename.")
                                log_renamed_file(DATABASE_FILE, filename, new_filename, original_path, new_path, "Skipped", "user")
                            else:
                                os.rename(original_path, new_path)
                                absolute_new_path = os.path.abspath(new_path)
                                print(f"Renamed {filename} to {new_filename}")
                                log_renamed_file(DATABASE_FILE, filename, new_filename, original_path, absolute_new_path, "Success", "user")