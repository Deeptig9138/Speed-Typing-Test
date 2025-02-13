from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import random
import database
import nltk
from nltk.metrics.distance import edit_distance

app = Flask(__name__)
app.secret_key = 'shashisingh8434thissamplesecret'


passages = [
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "The only way to do great work is to love what you do."
]

@app.route('/')
def home():
    varUser = request.args.get('varUser', 'Login')
    random_passage = random.choice(passages)
    return render_template('index.html', passage=[random_passage,varUser])

@app.route('/submit', methods=['POST'])
def submit():
    typed_text = request.json['typedText'].strip()
    passage = request.json['passage'].strip()
    time_taken = request.json['timeTaken']

    typed_words = typed_text.split()
    passage_words = passage.split()
    correct_words = sum(1 for tw, pw in zip(typed_words, passage_words) if tw == pw)
    wpm = (correct_words / time_taken) * 60 if time_taken > 0 else 0

    distance = edit_distance(typed_text, passage)
    max_length = max(len(typed_text), len(passage))
    accuracy = ((max_length - distance) / max_length) * 100 if max_length > 0 else 0

    return jsonify({'wpm': round(wpm, 2), 'accuracy': round(accuracy, 2)})

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        newUser = 'newUser' in request.form

        # print(newUser)
        if(newUser):
            database.initialiseNewUser(username,password)

            if(not database.checkUniqueUser(username)):
                session['username'] = username 
                return redirect(url_for('home', varUser=username))
            else:
                return redirect(url_for('login'))
        else:
            if(database.checkUniqueUser(username)):
                session['username'] = username 
                return redirect(url_for('home', varUser=username))
            else:
                return redirect(url_for('login'))
            
    return render_template("login.html")

@app.route('/sync', methods=['POST'])
def sync():
    # Get data from the POST request
    data = request.get_json()
    username = data.get('username')
    wpm = data.get('wpm')
    accuracy = data.get('accuracy')

    database.uploadCurrentData(username,wpm,accuracy)

    return jsonify({'status': 'success', 'message': 'Data synced successfully'}), 200


@app.route('/history', methods=['GET', 'POST'])
def history():
    username = session.get('username')

    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        user_exists = database.checkUniqueUser(username)

        response_data = {
            'username': username,
            'userExists': user_exists 
        }

        return jsonify(response_data) 
    # print(username)
    sendingData = database.getHistory(username)
    return render_template('user_history.html',username = username, allData = sendingData, enumerate = enumerate)

if __name__ == '__main__':
    app.run(debug=True)

