import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'todo.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + DATABASE
db = SQLAlchemy(app)  # generate database object


class Todo(db.Model): # class for a to_do item
    id = db.Column(db.Integer, primary_key=True)  # id of the item
    title = db.Column(db.String(80))  # name of todo
    complete = db.Column(db.Boolean)  # boolean if done or not


@app.route("/")
def index():  # render all to_do item in the database when the page is loaded
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)  # render index.html with the list of to_do items


@app.route("/add", methods=["POST"])  # add new to_do item, POST request to databse
def add():
    title = request.form.get("title")  # get to_do title from request
    new_todo = Todo(title=title, complete=False)  # create new to_do item
    db.session.add(new_todo)  # add to_do item to database
    db.session.commit()  # commit changes to database
    return redirect(url_for("index"))  # redirect to index page


@app.route("/complete/<string:todo_id>")
def complete(todo_id):  # mark to_do item as complete
    todo = Todo.query.filter_by(id=todo_id).first()  # get to_do item from database
    todo.complete = not todo.complete  # change complete status
    db.session.commit()  # commit changes to database
    return redirect(url_for("index"))


@app.route("/delete/<string:todo_id>")
def delete(todo_id):  # method to delete to_do item
    todo = Todo.query.filter_by(id=todo_id).first()  # find to_do item in database
    db.session.delete(todo)  # delete to_do item from database
    db.session.commit()  # commit changes to database
    return redirect(url_for("index"))


if __name__ == "__main__":  # entry point for the application
    db.create_all()  # create database if it doesn't exist
    app.run(debug=True)  # run the flask app
