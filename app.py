from myproject import app, db
from flask import render_template, url_for, redirect, flash, request
from myproject.forms import AddRun, LoginForm, RegistrationForm
from myproject.models import Run, User
from datetime import datetime
from sqlalchemy import func
from flask_login import login_user, current_user, logout_user, login_required

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



if __name__ == '__main__':
    app.run(debug=True)
