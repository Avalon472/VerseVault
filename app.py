from flask import Flask, render_template, request
import requests

app = Flask(__name__)

pdb = "https://poetrydb.org"

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

if __name__ == "__main__":
    app.run(debug=True)