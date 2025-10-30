from flask import Flask, render_template, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)

pdb = "https://poetrydb.org"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'poetry.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poem_title = db.Column(db.String(200), nullable=False)
    poet_name = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(100))

    def __repr__(self):
        return f'<Favorite {self.poem_title}>'

#Routes for static content
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/poem")
def get_poem():
    title = request.args.get("title")

    r = requests.get(f"{pdb}/title/{title}")
    if r.status_code != 200:
        return f"Poem: {title} was not found", 404
    
    data = r.json()[0]
    poem_title = data['title']
    author = data.get('author')
    lines = data.get('lines', [])
    linecount = data.get('linecount')

    return render_template("poem.html", title = poem_title, author = author, 
                           lines = lines, linecount = linecount)

@app.route("/random")
def get_random():

    r = requests.get(f"{pdb}/random")
    if r.status_code != 200:
        return f"Random poem was not found", 404
    
    data = r.json()[0]
    poem_title = data['title']
    author = data.get('author')
    lines = data.get('lines', [])
    linecount = data.get('linecount')

    return render_template("poem.html", title = poem_title, author = author,
                            lines = lines, linecount = linecount)

@app.route("/poet")
def get_poetWorks():
    poet = request.args.get("poet")

    r = requests.get(f"{pdb}/author/{poet}")
    if r.status_code != 200:
        return f"Poet: {poet} could not be found"
    data = r.json()

    info = [(poem['title'], int(poem['linecount'])) for poem in data]

    info = sorted(info, key = lambda x: x[1])


    poet = data[0]['author']

    return render_template("poet.html", poet = poet, info = info)

#Routes for DB content
@app.route('/favorites')
def favorites():
    favList = Favorite.query.all()
    return render_template('favorites.html', favoriteList = favList)

@app.route('/add_favorite', methods = ['Post'])
def add_favorite():
    data = request.json
    favItem = Favorite(
        poem_title = data['title'],
        poet_name = data['author'],
        quote = data['quote'],
        tags = data.get('tags')
    )
    db.session.add(favItem)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/reset_favorites', methods = ['Post'])
def reset_favorites():
    try:
        db.drop_all()
        db.create_all()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'error'})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)