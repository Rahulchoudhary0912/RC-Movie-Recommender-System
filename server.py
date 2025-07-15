import os
import pickle

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

current_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(current_dir, 'model')

# Load models and data
with open(os.path.join(model_dir, 'movie_list.pkl'), 'rb') as f:
    db_movies = pickle.load(f)
with open(os.path.join(model_dir, 'similarity.pkl'), 'rb') as f:
    similarity = pickle.load(f)
movies_df = pd.read_csv(os.path.join(model_dir, 'movies.csv'))
credits_df = pd.read_csv(os.path.join(model_dir, 'credits.csv'))

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/movies')
def get_movies():
    return jsonify([{'title': title} for title in db_movies['title'].values])

@app.route('/api/genres')
def get_genres():
    genres = set()
    for genre_list in movies_df['genres']:
        for genre in str(genre_list).split(','):
            genres.add(genre.strip())
    return jsonify(sorted(list(genres)))

@app.route('/api/recommend')
def recommend():
    movie = request.args.get('movie')
    count = int(request.args.get('count', 5))
    if movie not in db_movies['title'].values:
        return jsonify([])
    idx = db_movies[db_movies['title'] == movie].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recommended = []
    for i, _ in sim_scores[1:count+1]:
        recommended.append({'title': db_movies.iloc[i]['title']})
    return jsonify(recommended)

@app.route('/api/genre')
def recommend_by_genre():
    genre = request.args.get('genre')
    count = int(request.args.get('count', 5))
    filtered = movies_df if genre == 'All' else movies_df[movies_df['genres'].str.contains(genre, na=False)]
    sample = filtered.sample(n=min(count, len(filtered)), random_state=42)
    return jsonify([{'title': row['title']} for _, row in sample.iterrows()])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False) 