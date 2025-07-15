from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import pickle
import os
import json

app = Flask(__name__)
CORS(app)

# Get the directory where server.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(BASE_DIR, 'model')

# Load the data
movies_df = pd.read_csv(os.path.join(model_dir, 'movies.csv'))
credits_df = pd.read_csv(os.path.join(model_dir, 'credits.csv'))
movies_df = movies_df.merge(credits_df, on="title", how="left")

# Load the model
db_movies = pickle.load(open(os.path.join(model_dir, 'movie_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(model_dir, 'similarity.pkl'), 'rb'))

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = db_movies['title'].tolist()
    return jsonify([{'id': i, 'title': title} for i, title in enumerate(movies)])

@app.route('/api/recommend', methods=['GET'])
def recommend_movies():
    movie = request.args.get('movie')
    count = int(request.args.get('count', 5))
    
    if not movie:
        return jsonify([])
    
    try:
        index = db_movies[db_movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = [{'title': db_movies.iloc[i[0]].title} for i in distances[1:count+1]]
        return jsonify(recommended_movies)
    except:
        return jsonify([])

@app.route('/api/genre', methods=['GET'])
def get_movies_by_genre():
    genre = request.args.get('genre')
    count = int(request.args.get('count', 5))
    
    if genre == 'All':
        movies = movies_df.sample(count)
    else:
        # Handle both JSON and plain text genre formats
        def genre_contains(genres_str, target_genre):
            if not genres_str or pd.isna(genres_str):
                return False
                
            try:
                # Try to parse as JSON
                if genres_str.startswith('['):
                    genre_data = json.loads(genres_str)
                    for g in genre_data:
                        if isinstance(g, dict) and 'name' in g and g['name'].strip() == target_genre:
                            return True
                        elif isinstance(g, str) and g.strip() == target_genre:
                            return True
                else:
                    # Fall back to comma splitting
                    genre_list = [g.strip() for g in genres_str.split(',')]
                    return target_genre in genre_list
            except:
                # If JSON parsing fails, fall back to comma splitting
                genre_list = [g.strip() for g in genres_str.split(',')]
                return target_genre in genre_list
                
            return False
            
        movies = movies_df[movies_df['genres'].apply(lambda x: genre_contains(x, genre))].sample(count)
    
    return jsonify([{'title': title} for title in movies['title'].values])

@app.route('/api/genres', methods=['GET'])
def get_genres():
    # Extract unique genres from the movies dataframe
    all_genres = set()
    for genres in movies_df['genres'].dropna():
        try:
            # Try to parse as JSON first
            genre_list = []
            # Check if it's a JSON string
            if genres.startswith('['):
                genre_data = json.loads(genres)
                for genre in genre_data:
                    if isinstance(genre, dict) and 'name' in genre:
                        genre_list.append(genre['name'].strip())
                    elif isinstance(genre, str):
                        genre_list.append(genre.strip())
            else:
                # Fall back to comma splitting if not JSON
                genre_list = [g.strip() for g in genres.split(',')]
            
            all_genres.update(genre_list)
        except:
            # If JSON parsing fails, fall back to comma splitting
            genre_list = [g.strip() for g in genres.split(',')]
            all_genres.update(genre_list)
    
    # Convert to list and sort
    genres_list = sorted(list(all_genres))
    return jsonify(genres_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 
