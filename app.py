from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app(test_config=None):
    """Create and configure the app."""
    app = Flask(__name__)

    # Default config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

    if test_config:
        app.config.update(test_config)  # Update with test config if provided

    db.init_app(app)  # Initialize db with the app

    @app.route('/')
    def index():
        """Display the list of tasks from the database."""
        tasks = Task.query.all()  # Fetch all tasks from the database
        return render_template('index.html', tasks=tasks)

    @app.route('/add', methods=['GET', 'POST'])
    def add_task():
        """Add a new task."""
        if request.method == 'POST':
            task_name = request.form.get('task')
            if task_name:  # Ensure task_name is not empty
                new_task = Task(task=task_name)
                db.session.add(new_task)
                db.session.commit()
                return redirect(url_for('index'))  # Redirect after adding

        return render_template('add_task.html')

    @app.route('/complete/<int:task_id>')
    def complete_task(task_id):
        """Mark a task as completed."""
        task = Task.query.get(task_id)  # Fetch task from DB
        if task:
            task.completed = True
            db.session.commit()
        return redirect(url_for('index'))

    @app.route('/delete/<int:task_id>')
    def delete_task(task_id):
        """Delete a task."""
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)  # Delete safely
            db.session.commit()
        return redirect(url_for('index'))

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app


# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.task}>"

if __name__ == '__main__':
    app = create_app()  # Initialize the app
    app.run(debug=True)
