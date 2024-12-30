import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

def trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day"
    params = {'api_key': api_key, 'language': 'en-US'}

    response = requests.get(url, params=params)
    print("API Response Status Code:", response.status_code)
    print("API Response JSON:", response.json())  

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching movies: {response.status_code}")
        return {}
    
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': api_key,
        'language': 'en-US',
        'append_to_response': 'videos,images'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        movie_data = response.json()
        print("Movie Details Response:", movie_data)  # Add this line for debugging
        return movie_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None