from myproject import app, db
from flask import render_template, url_for, redirect, flash, request, session
from myproject.forms import AddRun, LoginForm, RegistrationForm, AddWord, TrainForm
from myproject.models import Run, User, Dict
from datetime import datetime
from sqlalchemy import func
from flask_login import login_user, current_user, logout_user, login_required
import random

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/add_run', methods=['GET', 'POST'])
@login_required
def add_run():
    form = AddRun()

    if form.validate_on_submit():
        kilometers = form.kilometers.data
        date = datetime.now()

        new_run = Run(kilometers, date)
        db.session.add(new_run)
        db.session.commit()

        return redirect(url_for('overview'))

    return render_template('add_run.html',form=form)

@app.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
    total_km = db.session.query(func.sum(Run.kilometers)).scalar()  # Sum all kilometers
    return render_template('overview.html', total_km=total_km)

@app.route('/reset_db', methods=['GET', 'POST'])
@login_required
def reset_db():
    # Delete all entries in the Run table
    db.session.query(Run).delete()
    db.session.commit()

    return redirect(url_for('overview'))  # Redirect back to the overview page

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('index')

            return redirect(next)
    return render_template('login.html',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/add_word', methods=['GET', 'POST'])
@login_required
def add_word():
    form = AddWord()

    if form.validate_on_submit():
        word_spanish = form.word_spanish.data
        word_german = form.word_german.data
        created_at = datetime.now()

        new_word = Dict(word_spanish, word_german, created_at)
        db.session.add(new_word)
        db.session.commit()

        return redirect(url_for('dictionary'))

    return render_template('add_word.html',form=form)

@app.route('/dictionary', methods=['GET'])
@login_required
def dictionary():
    words = Dict.query.order_by(Dict.created_at.desc()).all()
    return render_template('dict.html', words=words)


@app.route('/train', methods=['GET', 'POST'])
@login_required
def train():
    # If a word is stored in session, retrieve it, else get the word with the lowest score
    current_word = None

    # If there's no word in the session, choose the word with the lowest score
    if 'word_id' not in session:
        words = Dict.query.order_by(Dict.score, db.func.random()).all()
        if words:
            current_word = words[0]  # Get the word with the lowest score
            session['word_id'] = current_word.id  # Store the current word ID in the session
        else:
            flash("No words available for training!", "warning")
            return redirect(url_for('dictionary'))  # Redirect to dictionary if no words are found
    else:
        # If a word is stored in the session, fetch it
        current_word = Dict.query.get(session['word_id'])

    form = TrainForm()

    if form.validate_on_submit():
        user_translation = form.translation.data.strip().lower()

        # Check if the user provided the correct translation
        if user_translation == current_word.word_spanish.lower():
            # If correct, increment the score in the database
            current_word.score += 1
            db.session.commit()  # Save the updated score

            flash("Correct! Well done!", "success")
            session.pop('word_id')  # Remove the word from the session
            return redirect(url_for('train'))  # Go to the next word
        else:
            flash("Incorrect, please try again.", "danger")
            # Stay on the same word

    return render_template('training.html', form=form, word=current_word)






@app.route('/delete_word/<int:word_id>', methods=['POST'])
@login_required
def delete_word(word_id):
    word_to_delete = Dict.query.get_or_404(word_id)

    try:
        db.session.delete(word_to_delete)
        db.session.commit()
        flash('Word deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('An error occurred while trying to delete the word.', 'danger')

    return redirect(url_for('dictionary'))


if __name__ == '__main__':
    app.run(debug=True)
