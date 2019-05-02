from flask import render_template, url_for, flash, redirect, views, request, abort
from app.models import User, Article
from app.post.form import PostForm
from app import db
from flask_login import current_user, login_required


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
            return redirect(url_for('main.index'))
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
            return redirect(url_for('post.post', post_id=post.id))
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
        return redirect(url_for('main.index'))


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
