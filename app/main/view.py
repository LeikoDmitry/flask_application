from flask import render_template, views, request
from app.models import Article


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