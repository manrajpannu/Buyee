from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField , SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from flask_wtf.file import FileField, FileRequired
from blog.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Shop Name',
		validators=[DataRequired(),Length(min=4,max=24)])

	email = StringField('Email', 
		validators=[DataRequired(),Email()])

	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user: 
			raise ValidationError('That username is taken. Please choose a new username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user: 
			raise ValidationError('That email is taken. Please choose a new email.')

class LoginForm(FlaskForm):
	
	email = StringField('Email', 
		validators=[DataRequired(),Email()])

	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')

	submit = SubmitField('Log in')

class PostForm(FlaskForm):
	title = StringField('Product Name', validators=[DataRequired()], render_kw={"placeholder": "Short sleeve t-shirt"})
	content = TextAreaField('Description', validators=[DataRequired()])
	category = SelectField('Category', validators=[InputRequired()],choices=[('Baby','Baby'), ('Beauty','Beauty'), ('Books','Books'), ('Camera & Photo','Camera & Photo'), ('Clothing & Accessories','Clothing & Accessories'), ('Consumer Electronics','Consumer Electronics'), ('Grocery & Gourmet Foods','Grocery & Gourmet Foods'), ('Health & Personal Care','Health & Personal Care'), ('Home & Garden','Home & Garden'),  ('Luggage & Travel','Luggage & Travel'), ('Accessories','Accessories'), ('Musical Instruments','Musical Instruments'), ('Office Products','Office Products'), ('Outdoors','Outdoors'), ('Personal Computers','Personal Computers'), ('Pet Supplies','Pet Supplies'), ('Shoes, Handbags, & Sunglasses','Shoes, Handbags, & Sunglasses'), ('Software','Software'), ('Sports','Sports'), ('Tools & Home Improvement','Tools & Home Improvement'), ('Toys','Toys'), ('Video Games','Video Games')])
	price = StringField('Price', validators=[InputRequired()], render_kw={"placeholder": "$ 0.00"})
	stock_amount = StringField('Stock Amount')
	image = FileField() # IMAGE	


	submit = SubmitField('Post')