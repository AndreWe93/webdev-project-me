from myproject import app, db
from flask import render_template, url_for, redirect
from myproject.forms import AddRun
from myproject.models import Run
from datetime import datetime
from sqlalchemy import func

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/add_run', methods=['GET', 'POST'])
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
def overview():
    total_km = db.session.query(func.sum(Run.kilometers)).scalar()  # Sum all kilometers
    return render_template('overview.html', total_km=total_km)

@app.route('/reset_db', methods=['POST'])
def reset_db():
    # Delete all entries in the Run table
    db.session.query(Run).delete()
    db.session.commit()

    return redirect(url_for('overview'))  # Redirect back to the overview page


if __name__ == '__main__':
    app.run(debug=True)
