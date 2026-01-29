import os
import json
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# ====== Debug Logger ======
def debug(msg: str):
    """Timestamped debug print."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")



def get_pii_columns_heuristic(columns: list) -> list:
    """
    Identifies PII columns using heuristic keyword matching when API is unavailable.
    """
    debug("No API key provided. Using heuristic method to identify PII columns...")
    
    # Common PII keywords (lowercase parts to check against column names)
    # These are aggressive checks to ensure compliance safety.
    pii_keywords = [
        "name", "first_name", "last_name", "surname", "fullname", "full_name",
        "email", "e-mail", "mail",
        "phone", "mobile", "cell", "tel", "contact",
        "address", "addr", "street", "zip", "postal",
        "ssn", "social", "security", "tin", "tax",
        "passport", "license", "driver", "id_number", 
        "card", "credit", "debit", "bank", "account", "billing", "financial",
        "ip", "mac_address", "device",
        "password", "secret", "token", "credential", "auth",
        "dob", "date_of_birth", "birth"
    ]
    
    detected_pii = []
    
    for col in columns:
        col_lower = col.lower()
        # Check if the column name contains any of the keywords
        if any(keyword in col_lower for keyword in pii_keywords):
            detected_pii.append(col)
            
    debug(f"Identified PII columns (Heuristic): {detected_pii}")
    return detected_pii


def get_pii_columns_from_openai(columns: list, api_key: str) -> list:
    """
    Uses OpenAI API to identify PII columns from a list of column names.
    """
    if not api_key:
        debug("No OpenAI API key provided. Skipping PII check.")
        return []

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = f"""
    You are a data privacy expert. Given the following list of column names from a dataset, identify which ones represent Personally Identifiable Information (PII) that should be removed to ensure privacy compliance.
    
    Common PII includes names, emails, phone numbers, addresses, social security numbers, etc.
    
    Return ONLY a valid JSON array of strings containing the exact names of the PII columns found in the list. Do not include any other text, explanation, or markdown formatting.
    
    Column names: {json.dumps(columns)}
    """
    
    payload = {
        "model": "gpt-4o", 
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that identifies PII columns."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }
    
    try:
        debug("Sending request to OpenAI API to identify PII columns...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        # Clean up response if it contains markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
            
        if content.endswith("```"):
            content = content[:-3]
            
        pii_columns = json.loads(content.strip())
        
        # Validate that the returned columns actually exist in the input
        valid_pii_columns = [col for col in pii_columns if col in columns]
        
        debug(f"Identified PII columns: {valid_pii_columns}")
        return valid_pii_columns
        
    except Exception as e:
        debug(f"Error calling OpenAI API: {e}")
        return []


def check_compliance_and_pii(df: pd.DataFrame, api_key: str = None) -> dict:
    """
    Analyzes the DataFrame for PII columns using OpenAI and removes them.
    
    Args:
        df (pd.DataFrame): The input dataframe.
        api_key (str): OpenAI API key. If None, tries to fetch from environment variable 'OPENAI_API_KEY'.
        
    Returns:
        dict: A dictionary containing the cleaned dataframe (as a dict or object) and metadata.
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
        
    columns = df.columns.tolist()
    debug(f"Analyzing columns: {columns}")
    
    if api_key:
        pii_columns = get_pii_columns_from_openai(columns, api_key)
    else:
        pii_columns = get_pii_columns_heuristic(columns)
    
    cleaned_df = df.drop(columns=pii_columns, errors='ignore')
    
    return {
        "original_columns": columns,
        "pii_columns_detected": pii_columns,
        "dataframe": cleaned_df,
        "cleaned_columns": cleaned_df.columns.tolist(),
        "cleaned_data_sample": cleaned_df.head().to_dict(orient='records')
    }


# ====== STEP 5: Example usage ======
if __name__ == "__main__":
    debug("===== Running Example Compliance Check =====")
    
    # Example DataFrame
    df = pd.DataFrame(
        {
            "user_name": ["Alice", "Bob", "Charlie"],
            "email": ["alice@gmail.com", "bob@yahoo.com", "charlie@outlook.com"],
            "age": [25, 30, 35],
            "zip_code": ["12345", "67890", "11223"],
            "constant": [1, 1, 1],
        }
    )

    # Try to get API key from env, otherwise ask user
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not found in environment.")
        print("Press Enter to use heuristics, or paste your API key.")
        try:
            val = input("API Key: ").strip()
            if val:
                api_key = val
            else:
                debug("Proceeding with heuristic elimination.")
        except:
             debug("Proceeding with heuristic elimination.")

    result = check_compliance_and_pii(df, api_key)
    debug("===== Final Report =====")
    print(result["dataframe"])


