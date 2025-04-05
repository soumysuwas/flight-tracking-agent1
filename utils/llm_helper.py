import os
import json
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Create cache folder
os.makedirs("cache", exist_ok=True)

def get_cached_response(prompt, model):
    """Check if we already have a cached response for this prompt"""
    import hashlib
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    cache_path = f"cache/{model}_{prompt_hash}.json"
    
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as f:
            return json.load(f)
    return None

def save_to_cache(prompt, model, response):
    """Save response to cache to avoid repeated API calls"""
    import hashlib
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    cache_path = f"cache/{model}_{prompt_hash}.json"
    
    with open(cache_path, 'w') as f:
        json.dump(response, f)

def call_perplexity(prompt):
    """Call Perplexity API to get a response"""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error with Perplexity API: {response.status_code}")
        print(response.text)
        return None

def call_gemini(prompt):
    """Call Gemini API to get a response"""
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    if response:
        return response.text
    else:
        print("Error with Gemini API")
        return None

def query_llm(prompt, model="perplexity"):
    """Query an LLM with caching to save API calls"""
    # Check cache first
    cached = get_cached_response(prompt, model)
    if cached:
        print(f"Using cached {model} response")
        return cached
    
    print(f"Calling {model} API...")
    
    # Call appropriate API
    if model == "perplexity":
        response = call_perplexity(prompt)
    else:  # gemini
        response = call_gemini(prompt)
    
    if response:
        # Save to cache
        save_to_cache(prompt, model, response)
        return response
    else:
        return "Error: Unable to get response from LLM"
