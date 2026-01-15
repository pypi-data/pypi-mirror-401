import os
import httpx

async def check_dashscope_api() -> str:
    """
    Checks if the DASHSCOPE_API_KEY is correctly configured in the environment.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        return "Error: DASHSCOPE_API_KEY is not set in the environment variables."
    
    masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "****"
    return f"DashScope API Key is present: {masked_key}"

async def call_dashscope_generation(prompt: str) -> str:
    """
    Asynchronously calls DashScope generation API (qwen-turbo) using the provided API key.
    
    Args:
        prompt: The user input prompt.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        return "Error: DASHSCOPE_API_KEY is not set."

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            result = response.json()
        
        if "output" in result and "text" in result["output"]:
            return result["output"]["text"]
        else:
            return f"Unexpected response structure: {result}"
            
    except Exception as e:
        return f"Failed to call DashScope API: {str(e)}"

TOOLS = [check_dashscope_api, call_dashscope_generation]
