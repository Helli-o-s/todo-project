from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default='Medium')
    complete = db.Column(db.Boolean, default=False)

@app.route("/")
def home():
    # Separate incomplete and completed todos
    incomplete_list = Todo.query.filter_by(complete=False).order_by(Todo.due_date).all()
    complete_list = Todo.query.filter_by(complete=True).order_by(Todo.due_date).all()
    return render_template("base.html", incomplete_list=incomplete_list, complete_list=complete_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    due_date_str = request.form.get("due_date")
    priority = request.form.get("priority")

    due_date = None
    if due_date_str:
        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()

    new_todo = Todo(title=title, due_date=due_date, priority=priority, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.cli.command("init-db")
def init_db():
    """Clear existing data and create new tables."""
    db.create_all()
    print("Initialized the database.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)