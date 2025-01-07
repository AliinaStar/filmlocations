from flask import Blueprint, render_template, request, abort, current_app
import requests
from .external_api import trending_movies, get_movie_details, search_movies

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def index():
    movies = trending_movies()
    if movies:
        movie_list = movies.get('results', [])[:6]
        return render_template('index.html', movies=movie_list)
    else:
        print("Не вдалося завантажити фільми.")
    return render_template('index.html', error="Не вдалося завантажити фільми")

@movies_bp.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    if not movie:
        abort(404)
    
    dummy_locations = [
        {
            'name': 'Локації ще не додано',
            'address': 'Інформація оновлюється',
            'rating': 'N/A',
            'image': '/api/placeholder/200/150'
        }
    ]
    
    return render_template('movie_details.html', 
                         movie=movie,
                         locations=dummy_locations)

@movies_bp.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return render_template('search.html', error="Будь ласка, введіть запит для пошуку.")
    
    movies = search_movies(query)
    if movies:
        movie_list = movies.get('results', [])
        return render_template('search.html', movies=movie_list, query=query)
    else:
        return render_template('search.html', error="Не вдалося знайти фільми за вашим запитом.")