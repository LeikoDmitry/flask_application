import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, views, request, abort
from app.models import User, Article
from app.form import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, ResetPasswordForm, PasswordForm
from app import db, bcrypt, app, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


class Index(views.View):

    per_page = 4

    def dispatch_request(self):
        page_param = request.args.get('page')
        try:
            page = int(page_param)
        except TypeError:
            page = 1
        posts = Article.query.order_by(Article.date_posted.desc()).paginate(per_page=self.per_page, page=page)
        return render_template('index.html', posts=posts)


class About(views.View):
    def dispatch_request(self):
        return render_template('about.html', title='About')


class Login(views.View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(pw_hash=user.password, password=form.password.data):
                login_user(user=user, remember=form.remember.data)
                return redirect(url_for('index'))
            flash('Login Unsuccessful. Please check email or password', 'danger')
        return render_template('login.html', form=form)


class Register(views.View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, password=hashed_password, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form, title='Register')


class Logout(views.View):
    methods = ['GET']

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))


class Account(views.View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                current_user.image_file = self.save_file(form.picture.data)
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash(f'Account Updated for {form.username.data}', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/{}'.format(current_user.image_file))
        return render_template('account.html', title='Account', image_file=image_file, form=form)

    def save_file(self, form_picture):
        random_hex = secrets.token_hex(16)
        name, ext = os.path.splitext(form_picture.filename)
        file_image = '{}{}{}'.format(name, random_hex, ext)
        path = os.path.join(app.root_path, 'static/profile_pics/', file_image)
        output_size = (125, 125)
        image = Image.open(form_picture)
        image.thumbnail(output_size)
        image.save(path)
        return file_image


class CreatePost(views.View):
    methods = ['GET', 'POST']
    @login_required
    def dispatch_request(self):
        form = PostForm()
        if form.validate_on_submit():
            post = Article(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('index'))
        return render_template('create_post.html', title='New post', form=form, legend='Create Post')


class Post(views.View):
    methods = ['GET', 'POST']

    def dispatch_request(self, post_id):
        post = Article.query.get_or_404(post_id)
        return render_template('post.html', title='Post - {}'.format(post_id), post=post)


class PostUpdate(views.View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self, post_id):
        post = Article.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.add(post)
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('post', post_id=post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
            return render_template('create_post.html', title='Update post', form=form, legend='Update Post')


class PostDelete(views.View):
    methods = ['POST']

    @login_required
    def dispatch_request(self, post_id):
        post = Article.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'info')
        return redirect(url_for('index'))


class UserPost(views.View):

    per_page = 2

    def dispatch_request(self, username):
        page_param = request.args.get('page')
        try:
            page = int(page_param)
        except TypeError:
            page = 1
        user = User.query.filter_by(username=username).first_or_404()
        posts = Article.query\
            .filter_by(author=user)\
            .order_by(Article.date_posted.desc())\
            .paginate(per_page=self.per_page, page=page)
        return render_template('user_post.html', posts=posts, user=user)


class ResetRequest(views.View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            self.send_email(user=user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        return render_template('reset_request.html', title='Reset Password', form=form)

    def send_email(self, user: User):
        token = user.get_reset_token()
        msg = Message('Password Reset Request',
                      sender='noreply@flask.com',
                      recipients=[user.email])
        msg.html = f'''To reset your password, visit the following link:<br/>
        <a href='{url_for('reset_token', token=token, _external=True)}'>Reset Token</a><br/>
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
        mail.send(msg)
        return self


class ResetToken(views.View):
    methods = ['GET', 'POST']

    def dispatch_request(self, token):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        user = User.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('reset_request'))
        form = PasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return render_template('reset_token.html', title='Reset Password', form=form)















