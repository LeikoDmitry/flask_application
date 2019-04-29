from app import app
from app.view.blog import (Index, About, Login, Register, Logout, Account,
                           CreatePost, Post, PostUpdate, PostDelete, UserPost, ResetToken, ResetRequest)

app.add_url_rule('/', view_func=Index.as_view('index'))
app.add_url_rule('/about', view_func=About.as_view('about'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/register', view_func=Register.as_view('register'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/account', view_func=Account.as_view('account'))
app.add_url_rule('/post/new', view_func=CreatePost.as_view('new_post'))
app.add_url_rule('/post/<int:post_id>', view_func=Post.as_view('post'))
app.add_url_rule('/post/<int:post_id>/update', view_func=PostUpdate.as_view('update_post'))
app.add_url_rule('/post/<int:post_id>/delete', view_func=PostDelete.as_view('delete_post'))
app.add_url_rule('/user/post/<string:username>', view_func=UserPost.as_view('username_post'))
app.add_url_rule('/reset_password', view_func=ResetRequest.as_view('reset_request'))
app.add_url_rule('/reset_password/<token>', view_func=ResetToken.as_view('reset_token'))