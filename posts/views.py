from flask import render_template,url_for,redirect,request,Blueprint, abort
from flask_login import login_required, current_user
from __init__ import db
from models import TravelPost


posts = Blueprint('posts',__name__)

@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('txtarea')
        post = TravelPost(title=title,
                            data=content,
                            user_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('core.home'))
    return render_template('createpost.html', user=current_user, post=None)

@posts.route('/post<int:post_id>')
def post(post_id):
    
    post = TravelPost.query.get_or_404(post_id)
    return render_template('viewpost.html',title=post.title,
                            date=post.date,post=post,user=current_user)

@posts.route("/post<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = TravelPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('txtarea')
        post.title = title
        post.data = content
        
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('createpost.html', title='Update', post=post, user=current_user)


@posts.route("/post<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = TravelPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('core.home'))