from flask import Flask, render_template, send_file
from flask_wtf.csrf import CSRFProtect
from config.config import init_db, get_db
from config.auth import auth_bp, csrf
from api.routes import movies_bp
import os
from io import BytesIO

from PIL import Image

KEY = os.getenv('KEY')

app = Flask(__name__, template_folder='templates')
app.secret_key = KEY

csrf.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(movies_bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/location-details')
def location_details():
    return render_template('location-details.html')

@app.route('/api/placeholder/<int:width>/<int:height>')
def placeholder(width, height):
    img = Image.new('RGB', (width, height), color=(200, 200, 200))
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)