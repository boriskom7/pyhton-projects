from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrettodolistpassword1'
Bootstrap(app)


##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), unique=True, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    completed_date = db.Column(db.DateTime, nullable=True)
    task_list = db.Column(db.String(250), nullable=False)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_tasks = db.session.query(Task).order_by(Task.completed_date)

    task_lists = db.session.query(List).all()

#    for table_name in db.session.query(Task.task_list).distinct():
#        task_lists.append(table_name.task_list)

    return render_template("index.html", tasks=all_tasks, task_lists=task_lists)


@app.route('/add-list', methods=["POST"])
def add_list():
    new_list = request.form['new_list']

    if new_list != "":
        list = List(
            name=new_list
        )
        db.session.add(list)
        db.session.commit()
    return redirect(url_for("home"))


@app.route('/<string:list_name>')
def show_list(list_name):
    list_tasks = db.session.query(Task).filter(Task.task_list == list_name).order_by(Task.completed_date.desc())

    task_lists = db.session.query(List).all()

    return render_template("index.html", tasks=list_tasks, task_lists=task_lists)


@app.route('/add/<string:list_name>', methods=["POST"])
def add_task(list_name):
    new_task = request.form['new_task']
    time = datetime.now()
    if new_task != "":
        task = Task(
            description=new_task,
            created=time,
            due_date=time,
            completed=False,
            completed_date=datetime(2100, 1, 1, 18, 00),
            task_list=list_name
        )
        db.session.add(task)
        db.session.commit()
    return redirect(url_for("show_list", list_name=list_name))

@app.route('/add/<string:list_name>/<int:task_id>', methods=["POST"])
def edit_task(list_name,task_id):
    edit_task = db.session.query(Task).get(task_id)

    edit_data = request.form['edit_task']

    if edit_data != "":
        edit_task.description = edit_data;
        db.session.commit()

    return redirect(url_for("show_list", list_name=edit_task.task_list))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task_to_change = Task.query.get(task_id)

    task_to_change.completed = not task_to_change.completed
    if task_to_change.completed:
        task_to_change.completed_date = datetime.now()
    else:
        task_to_change.completed_date = datetime(2100, 1, 1, 18, 00)

    db.session.commit()
    return redirect(url_for("show_list", list_name=task_to_change.task_list))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("show_list", list_name=task_to_delete.task_list))


if __name__ == "__main__":
    app.run(debug=True)
