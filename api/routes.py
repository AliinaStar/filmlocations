from flask import Blueprint, render_template, abort
from .external_api import trending_movies, get_movie_details

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def index():
    movies = trending_movies()
    if movies:
        movie_list = movies.get('results', [])[:5]
        return render_template('index.html', movies=movie_list)
    else:
        print("No movies found or error occurred.")  # Add this line for debugging
    return render_template('index.html', error="Не вдалося завантажити фільми")

@movies_bp.route('/details/<int:movie_id>')
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