from flask import Blueprint
from app.authorization.view import Login, Register, Logout, Account, ResetRequest, ResetToken

authorization = Blueprint('authorization', __name__)

authorization.add_url_rule('/login', view_func=Login.as_view('login'))
authorization.add_url_rule('/register', view_func=Register.as_view('register'))
authorization.add_url_rule('/logout', view_func=Logout.as_view('logout'))
authorization.add_url_rule('/account', view_func=Account.as_view('account'))
authorization.add_url_rule('/reset_password', view_func=ResetRequest.as_view('reset_request'))
authorization.add_url_rule('/reset_password/<token>', view_func=ResetToken.as_view('reset_token'))