from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "keyyy"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)
app.app_context().push()


class Todo(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime)

    def __repr__(self):
        return '<Task %r>' %self.id


@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content, date_created=datetime.now())

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
            
        except:
            "There was an error while adding a task"
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))

    except:
        return "There was an error while deleting a task"


@app.route("/update/<int:id>", methods=["POST","GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        
        except:
            return "There was an error while updating the task"
    else:
        return render_template("update.html", task=task)

if __name__=="__main__":
    app.run(debug=True)