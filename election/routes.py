import pandas as pd

from election import app
from flask import render_template, flash, redirect, url_for, session,request
from werkzeug.utils import secure_filename
import os
import time
from election.forms import AdminForm, LoginForm,studentForm,usersForm
import mysql.connector


db = mysql.connector.connect(
    host=os.environ.get("MYSQLHOST", "mysql.railway.internal"),
    user=os.environ.get("MYSQLUSER", "root"),
    password=os.environ.get("MYSQLPASSWORD", "HwKpHgXmdRCIHwsjTqnPuzEcTmaVEEmt"),
    database=os.environ.get("MYSQLDATABASE", "railway"),
    port=int(os.environ.get("MYSQLPORT", 3306))
)





@app.route('/', methods=['GET', 'POST'])
def login():
    form= LoginForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True,buffered=True)
        cursor.execute("SELECT * FROM users WHERE user_id=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['user_id']
            session['role'] = user['role']


            if user['role'] == 'admin':
                return redirect(url_for('admin_page'))
            elif user['role'] == 'student':
                return redirect(url_for('voting_page'))

        else:
            flash("Invalid login details", "danger")

    return render_template('login.html', form=form)



@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    form = AdminForm()

 #   if 'user' not in session:
  #      return redirect(url_for('login'))
   # if session.get('role') != 'admin':
    #    flash("Access denied","danger")

    if form.validate_on_submit():
        name = form.candidates_name.data
        position = form.candidates_position.data
        file = form.image.data

        vice_name = form.vice_president_name.data
        vice_position = form.vice_position.data
        vice_file = form.vice_president_image.data

        upload_path = os.path.join(app.root_path, 'static/uploads')

        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        # Save president image
        filename = None
        if file:
            filename = secure_filename(file.filename)
            filename = str(int(time.time())) + "_" + filename
            file.save(os.path.join(upload_path, filename))


        vice_filename = None
        if vice_file:
            vice_filename = secure_filename(vice_file.filename)
            vice_filename = str(int(time.time())) + "_" + vice_filename
            vice_file.save(os.path.join(upload_path, vice_filename))


        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO candidates 
            (candidates_name, candidates_position, image,
             vice_president_name, vice_position, vice_president_image)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, position, filename, vice_name, vice_position, vice_filename)
        )
        db.commit()

        flash('Candidate saved successfully!!', 'success')
    else:
        if form.is_submitted():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error, 'danger')

    return render_template('Admin_form.html', form=form)


@app.route('/log out')
def logout_page():
    flash("log Out Successfully")
    return redirect(url_for('login_page'))


@app.route('/View candidates')
def view_candidates_page():
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM candidates",
    )
    candidates = cursor.fetchall()

    if candidates:
        return render_template('view_candidate.html', candidates=candidates)
    else:
        flash("Election is closed at the moment!!","danger")
        return render_template("election_closed.html")



@app.route('/delete_candidate/<int:id>', methods=['GET', 'POST'])
def delete_candidate(id):

    if 'user' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        flash("Access denied","danger")
        return redirect(url_for('login'))


    cursor = db.cursor()
    cursor.execute("DELETE FROM candidates WHERE Id = %s", (id,))
    db.commit()
    cursor.close()

    flash("Candidate Deleted Successfully", "success")
    return redirect(url_for('view_candidates_page'))

@app.route('/vote_student', methods=['GET', 'POST'])
def voting_page():
    form = studentForm()


    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session['role'] != 'student':
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        candidate_id = request.form['candidate']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM votes WHERE user_id = %s", (user_id,))
        existing_vote = cursor.fetchone()

        if existing_vote:
            flash("You have already voted!", "warning")
            return redirect(url_for('results_page'))

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO votes (user_id, candidate_id) VALUES (%s, %s)",
            (user_id, candidate_id)
        )
        db.commit()

        flash("Vote submitted successfully!", "success")
        return redirect(url_for('voting_page'))
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    return render_template('studentvote.html', candidates=candidates)

@app.route('/results')
def results_page():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            candidates.Id,
            candidates.candidates_name,
            candidates.vice_president_name,
            candidates.image,
            candidates.vice_president_image,
            COUNT(votes.candidate_id) AS total_votes
        FROM candidates
        LEFT JOIN votes ON candidates.Id = votes.candidate_id
        GROUP BY candidates.Id,
         candidates.candidates_name,
         candidates.vice_president_name,
         candidates.image,
         candidates.vice_president_image
        ORDER BY total_votes DESC
    """)

    results = cursor.fetchall()

    return render_template('results.html', results=results)

@app.route('/users_upload', methods=['POST','GET'])
def users_upload():
    form=usersForm()

    if request.method == 'POST':
        print("form is submitted successfully")
        file = request.files['file']
        if file:
            upload_folder= app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)

            filepath=os.path.join(upload_folder,file.filename)
            file.save(filepath)

            df= pd.read_excel(filepath)
            df=df[['user_id','password','role']]

            print(df.columns)

            cursor = db.cursor()

            try:
                for index, row in df.iterrows():
                    cursor.execute(
                        "INSERT INTO users (user_id,password,role) VALUES (%s,%s,%s)",(row['user_id'],row['password'],row['role'])
                    )
                    db.commit()
                    print("inserted successfully")
            except Exception as e:
                    print("error:",e)

    return render_template('users.html', form=form)





