from clone import create_app, db
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from clone.models import User, Post, Follow, Comment, Notification


app = create_app('default')
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(User=User, Post=Post, Follow=Follow, Comment=Comment, Notification=Notification)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run(debug=True)
