from flask import Flask, render_template, request, jsonify
import os
import git

app = Flask(__name__)


NOTES_DIR = os.path.join(os.getcwd(), 'notes')

if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)
if not os.path.exists(os.path.join(NOTES_DIR, '.git')):
    repo = git.Repo.init(NOTES_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_note', methods=['POST'])
def save_note():
    content = request.json.get('content')
    filename = request.json.get('filename')

    with open(os.path.join(NOTES_DIR, filename), 'w') as file:
        file.write(content)

    repo = git.Repo(NOTES_DIR)
    repo.index.add([filename])
    repo.index.commit("Updated note: " + filename)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
