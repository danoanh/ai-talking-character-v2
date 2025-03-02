import requests
import base64

# Correct D-ID API Key
DID_API_KEY = "Ym1wemNYWm5jMk55YlVCd2NtbDJZWFJsY21Wc1lYa3VZWEJ3YkdWcFpDNWpiMjA6cG5TVFBBZkgwTzJXOHJQTnpIWUpN"  
# Encode API Key in Base64 for proper authentication
encoded_api_key = base64.b64encode(DID_API_KEY.encode()).decode()

# D-ID API URL
url = "https://api.d-id.com/talks"
headers = {"Authorization": f"Basic {encoded_api_key}"}

# Make the API request
response = requests.get(url, headers=headers)

# Handle API responses properly
if response.status_code == 200:
    data = response.json()
    
    if "talks" in data and len(data["talks"]) > 0:
        result_url = data["talks"][0].get("result_url", "No result URL found")
        print(f"Generated Video URL: {result_url}")
    else:
        print("Error: No talks available in response.")
        
elif response.status_code == 401:
    print("Error: Unauthorized - Check your API key and permissions")
elif response.status_code == 403:
    print("Error: Forbidden - You may have exceeded your API limits")
elif response.status_code == 429:
    print("Error: Too Many Requests - Rate limit exceeded, try again later")
else:
    print(f"Error {response.status_code}: {response.text}")
