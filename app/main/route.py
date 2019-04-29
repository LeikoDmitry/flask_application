from flask import Blueprint
from app.main.view import Index, About


main = Blueprint('main', __name__)


main.add_url_rule('/', view_func=Index.as_view('index'))
main.add_url_rule('/about', view_func=About.as_view('about'))
