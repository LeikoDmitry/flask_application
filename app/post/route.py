from flask import Blueprint
from app.post.view import CreatePost, Post, PostUpdate, PostDelete, UserPost


post = Blueprint('post', __name__)

post.add_url_rule('/post/new', view_func=CreatePost.as_view('new_post'))
post.add_url_rule('/post/<int:post_id>', view_func=Post.as_view('post'))
post.add_url_rule('/post/<int:post_id>/update', view_func=PostUpdate.as_view('update_post'))
post.add_url_rule('/post/<int:post_id>/delete', view_func=PostDelete.as_view('delete_post'))
post.add_url_rule('/user/post/<string:username>', view_func=UserPost.as_view('username_post'))