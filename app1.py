from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL database connection parameters
db_config = {
    'host': 'localhost',  # Change if your host is different
    'user': 'root',  # Your MySQL username
    'password': 'akshita@2002',  # Your MySQL password
    'database': 'quizdb'  # Your database name
}

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Ensure all required fields are present
        student_name = request.form.get('student_name')
        email = request.form.get('email')
        father_name = request.form.get('father_name')
        contact_no = request.form.get('contact_no')
        
        if not student_name or not email or not father_name or not contact_no:
            # Handle the error: missing fields
            return "Error: All fields are required", 400

        score = 0
        
        # Check answers
        correct_answers = {
            'question1': 'List',
            'question2': 'List',
            'question3': 'def',
            'question4': '[1, 2, 3]',
            'question5': 'False',
            'question6': '1var',
            'question7': 'Returns length of an object',
            'question8': 'False',
            'question9': 'except',
            'question10': 'List',
            'question11': 'H',
            'question12': '22',
            'question13': 'append()',
            'question14': 'Both',
            'question15': '#',
            'question16': 'True',
            'question17': 'for i in range(5):',
            'question18': 'input()',
            'question19': 'class',
            'question20': 'HelloHelloHello'
         
        }

        for question, correct_answer in correct_answers.items():
            if request.form.get(question) == correct_answer:
                score += 1

        # print(f"Student Name: {student_name}")
        # print(f"Email: {email}")
        # print(f"Father's Name: {father_name}")
        # print(f"Contact Number: {contact_no}")
        # print(f"Score: {score}")

        # Store the score and student details in the database
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO quiz_scores (student_name, email, father_name, contact_no, score) VALUES (%s, %s, %s, %s, %s)', 
                           (student_name, email, father_name, contact_no, score))
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error: {e}")

        return redirect(url_for('thank_you', score=score,student_name=student_name))

    return render_template('quiz.html')

@app.route('/result')
def thank_you():
    score = request.args.get('score', type=int)
    student_name = request.args.get('student_name', default='Student')  # Default value in case it's not provided
    return render_template('result.html', score=score, student_name=student_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
