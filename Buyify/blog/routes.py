from flask import render_template, url_for, flash, redirect, request
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, PostForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
	user = User.query.all()
	return render_template('home.html',title='Buyify',users=user)

@app.route('/about')
def about():
	return render_template('about.html',title = 'About me')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()

		flash(f'Your shop has been created! You are now able to log in!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))

		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html',title='Login',form=form)	

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
	image_file = url_for('static', filename='profile_pic/' +  current_user.image_file)
	return render_template('account.html',title=current_user.username, image_file=image_file)	

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user, price=form.price.data,stock_amount=form.stock_amount.data,category=form.category.data)
		db.session.add(post)
		db.session.commit()
		flash('Your product has been created!','success')
		return redirect(url_for('home'))
	return render_template('create_post.html',title='New Post', form =form)	