from wtforms import Form, TextField, BooleanField, PasswordField, validators


class RegisterForm(Form):
	username = TextField('Username', [validators.Length(min=4,max=15)])
	email = TextField('Email', [validators.Length(min=6,max=50)])
	password = PasswordField('Password', [validators.Required(),
		validators.EqualTo('confirm', message='Both passwords must be equal')])
	confirm = PasswordField('Confirm password')
	accept = BooleanField('I accept <a href="/terms">terms</a> and <a href="/services/">services</a>', 
		[validators.Required()])
	