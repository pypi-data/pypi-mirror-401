import requests
import json

def get(url, params=None, headers=None):
    """Make a GET request to the API."""
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Raise error on bad status
    return response

def post(url, data=None, json_data=None, headers=None):
    """Make a POST request to the API."""
    response = requests.post(url, data=data, json=json_data, headers=headers)
    response.raise_for_status()
    return response

def print_response(response, format='text'):
    """Print the API response in the specified format."""
    if format == 'text':
        print(response.text)
    elif format == 'json':
        try:
            json_data = response.json()
            print(json.dumps(json_data, indent=4))
        except json.JSONDecodeError:
            print("Error: Response is not valid JSON.")
            print(response.text)
    elif format == 'headers':
        print(response.headers)
    else:
        raise ValueError("Unsupported format. Use 'text', 'json', or 'headers'.")