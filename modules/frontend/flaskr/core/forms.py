from wtforms import Form, BooleanField, StringField, EmailField, PasswordField, validators



class ContactForm(Form):
    name = StringField('name', [validators.Length(min=1, max=50)])
    email = EmailField('email', [validators.Length(max=50)])
    subject = StringField('subject', [validators.Length(min=6, max=50)])
    message = StringField('message', [validators.Length(min=10, max=1200)])


