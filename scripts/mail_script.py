from hello import app, mail
from flask import current_app
from flask_mail import Message

app_ctx = app.app_context()
app_ctx.push()
current_app.name

msg = Message('Test από τον Φοίβο', sender='fivoskaralis@gmail.com', recipients=['bataille3@yahoo.com'])
msg.body = 'TEST body'
msg.html = '<b>Φοορςςς</b> γεια σου κούκλα'
with app.app_context():
    mail.send(msg)
