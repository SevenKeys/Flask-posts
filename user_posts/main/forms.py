from wtforms import Form, TextField, IntegerField, TextAreaField, validators

class PostForm(Form):
    title = TextField('Title', [validators.Length(min=3,max=50)])
    rating = IntegerField('Rating')
    description = TextAreaField('Description', [validators.Length(min=3,max=50)])
