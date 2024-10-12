import requests

def calculate_geometry(query, app_id):
    """
    Use the Wolfram Alpha API to calculate geometric properties.
    
    Parameters:
    - query: str, the geometric calculation request
    - app_id: str, your Wolfram Alpha API key

    Returns:
    - result: str, the result of the calculation
    """
    base_url = "http://api.wolframalpha.com/v2/query"
    params = {
        'input': query,
        'format': 'plaintext',
        'output': 'JSON',
        'appid': app_id,
        'podstate': 'Solution'
    }
    
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        pods = data.get('queryresult', {}).get('pods', [])
        result = ""
        
        for pod in pods:
            title = pod.get('title', '')
            subpods = pod.get('subpods', [])
            for subpod in subpods:
                result += f"{title}: {subpod.get('plaintext', '')}\n"

        return result if result else "No result found."
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    # Replace 'YOUR_APP_ID' with your Wolfram Alpha API key
    app_id = 'PUV2JH-V83G5G6WRG'  

    # Example queries
    queries = [
        "area of a circle with radius 5",
        "volume of a sphere with radius 5",
        "area of a triangle with base 10 and height 5",
        "surface area of a cylinder with radius 3 and height 7"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        result = calculate_geometry(query, app_id)
        print(f"Result: {result}\n")