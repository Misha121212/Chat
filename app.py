from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))

    def __repr__(self):
        return '<Message %r>' % self.text

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    msg = Message(text=message)
    db.session.add(msg)
    db.session.commit()
    emit('response', {'data': message}, broadcast=True)

if __name__ == '__main__':
    db.create_all()
    socketio.run(app)