#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests
import random
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(16)

base_url = "http://localhost:5000/api/quiz"

count = 0
answers = []
correct_answer = ""

#Landing Page
@app.route('/')
def index():
    return render_template('index.html')

#Add question to question bank
@app.route('/new_question')
def new_question():
    return render_template('new_question.html', categories=get_categories())

@app.route('/add_question', methods=['POST'])
def add_question():
    try:
        category = request.form['category']
        question = request.form['question']
        correct_answer = request.form['correct_answer']
        incorrect_answers = request.form.getlist('incorrect_answers')
        incorrect_answers_str = ",".join(incorrect_answers)
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO question_bank (category, question, correct_answer, incorrect_answers) VALUES (?, ?, ?, ?)", (category, question, correct_answer, incorrect_answers_str))
            conn.commit()
        
        msg = "Record successfully added"

    except Exception as e:
        conn.rollback()
        msg = "Error in insert operation"

    finally:
        return render_template('result.html', msg= msg)

#Delete question from question bank based on id
@app.route('/delete_question', methods=['GET'])
def delete_question_form():
    return render_template('delete_question.html')

@app.route('/delete_question_from_db', methods=['POST', 'DELETE'])
def delete_question_from_db():
    id = request.form.get('id') 
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            #check if question with id exists in question bank
            cursor.execute("SELECT * FROM question_bank WHERE id = ?", (id,))
            row = cursor.fetchone()
            if not row:
                return render_template('result.html', msg="Question ID: " + id + "  does not exist")
            else :
                #delete question from question bank
                cursor.execute("DELETE FROM question_bank WHERE id = ?", (id,))
                conn.commit()
                msg = "Question successfully deleted"
                return render_template('result.html', msg=msg)

    except Exception as e:
        conn.rollback()
        msg = "Error in delete operation"
        return render_template('result.html', msg=msg)

#Add category to question bank
@app.route('/new_category')
def new_category():
    return render_template('new_category.html')

@app.route('/add_category', methods=['POST'])
def add_category():
    try:
        category = request.form['category']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO category (category) VALUES (?)", (category,))
            conn.commit()
        
        msg = "Record successfully added"

    except Exception as e:
        conn.rollback()
        msg = "Error in insert operation"

    finally:
        return render_template('result.html', msg= msg)

#Pull categories from question bank
def get_categories():
    categories = []
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category FROM category")
            categories = cursor.fetchall()
            categories = [category[0] for category in categories]
            return categories
    
    except Exception as e:
        conn.rollback()
        msg = "Error in select operation"
        return render_template('result.html', msg=msg)


#Return all questions in question bank
@app.route('/question_bank', methods=['GET'])
def question_bank():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM question_bank")
    rows = cursor.fetchall()
    return render_template("list.html",rows = rows) 

#Set route for my api
@app.route('/api/quiz', methods=['GET'])
def quiz():
    # Get parameters from the request
    category = request.args.get('category')
    count = request.args.get('count')

    # Build the SQL query based on the parameters
    query = "SELECT * FROM question_bank"
    conditions = []

    if category:
        conditions.append(f"category = '{category}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # If count is provided, limit the number of rows returned
    if count:
        query += f" LIMIT {count}"

    # Connect to the database and fetch data
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # Convert the rows to a list of dictionaries for JSON response
    results = [{'id': row['id'], 'category': row['category'], 'question': row['question'], 'correct_answer': row['correct_answer'], 'incorrect_answers': row['incorrect_answers'].split(',')} for row in rows]

    return json.dumps(results, sort_keys=False)

#Generate API Page
@app.route('/api_generate')
def api_generate():
    return render_template('generate_api.html', categories=get_categories())

@app.route('/generate_url', methods=['GET'])
def generate_url():
    global base_url
    category = request.args.get('category')
    print(category)
    count = request.args.get('count')
    print(count)

    if category == "" and count == "":
        generated_url = base_url
    elif category == "":
        generated_url = f"{base_url}?count={count}"
    elif count == "":
        generated_url = f"{base_url}?category={category}"
    else:
        generated_url = f"{base_url}?category={category}&count={count}"

    return render_template('generate_api.html', generated_url=generated_url)

#Quiz Game

def ask_params():
    global count
    no_qsts = int(request.form['num_questions'])
    count = no_qsts
    category = request.form['category']

    params = {
        "count": no_qsts,
        "category": category,
    }
    return params

def build_url(base_url, params):
    url = requests.get(base_url, params=params)
    return url.url

#Game Index Page
@app.route('/game_index')
def game_index():
    session.clear()
    return render_template('game_index.html', categories=get_categories())

#Start with the game page.
@app.route('/game_start', methods=['POST'])
def start_game():
    params = ask_params()
    url = build_url(base_url, params)
    session['url'] = url  # Set the 'url' in the session
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    global correct_answer
    url = session.get('url') 
    if not url:
        return redirect(url_for('game_index'))  # Redirect to game_index if 'url' is not in session

    data = requests.get(url).json()
    total_questions = len(data)

    current_question = session.get('current_question', 1)

    if request.method == 'POST':
        selected_answer = request.form.get('selected_answer')

        if selected_answer == correct_answer:
            session['score'] = session.get('score', 0) + 1

    session['current_question'] = current_question + 1


    if 1 <= current_question <= total_questions:
        question = data[current_question - 1]['question']
        correct_answer = data[current_question - 1]['correct_answer']
        incorrect_answers = data[current_question - 1]['incorrect_answers']

        answers = [correct_answer] + incorrect_answers
        random.shuffle(answers)

        session['current_question'] = current_question + 1

        return render_template('game_start.html', current_question=current_question, total_questions=total_questions, question=question, answers=answers)
    else:
        print(session.get('score', 0))
        session.pop('current_question', None)  
        return render_template('game_over.html', score=session.get('score', 0), total_questions=total_questions)

#Route for play again
@app.route('/play_again', methods=['GET'])
def play_again():
    session.clear()
    global count
    count = 0  
    return redirect(url_for('game_index'))

#Route for game over
@app.route('/game_over')
def game_over():
    score = session.get('score', 0)
    return render_template('game_over.html', score=score)

if __name__ == '__main__':
    try:
        conn = sqlite3.connect('database.db')
        print("Database connected successfully")
        conn.execute('CREATE TABLE IF NOT EXISTS question_bank (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, question TEXT, correct_answer TEXT, incorrect_answers TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT)')
        print("Table created successfully") 
        conn.close()
        app.run(debug = True)
    
    except:
        print("App failed on boot")
        conn.close()
        app.run(debug = True)