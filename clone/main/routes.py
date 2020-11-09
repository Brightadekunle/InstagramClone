import os
import secrets
import requests
from datetime import datetime
from clone import db
from flask import render_template, redirect, url_for, abort, current_app, request, flash, g, jsonify
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from . import main
from .forms import UpdateAccountForm, PostForm, CommentForm, SearchForm, MessageForm
from ..models import User, Post, Comment, Notification


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.all()
    image_posts = []
    comments = Comment.query.all()
    for post in posts:
        try:
            image_post = url_for('static', filename='images/' +
                                 post.image_1)
            image_posts.append([image_post, post])
            print(post.author.profile_picture)

        except Exception as e:
            pass

    return render_template('index.html', posts=posts, image_post=image_posts, comments=comments)


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        comment = Comment(body=request.form['comment'], post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published', 'success')
        return redirect(url_for('main.home'))


@main.route('/account/<username>', methods=['GET', 'POST'])
@login_required
def account(username):
    user = User.query.filter_by(username=username).first()
    form = PostForm()
    posts = user.posts.filter_by(author_id=user.id).all()
    image_posts = []
    if request.method == 'POST':
        if form.image_post.data:
            picture_file = save_picture(form.image_post.data)
            post = Post(image_1=picture_file,
                        author=current_user._get_current_object(), caption=form.caption.data)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been successfully uploaded!', 'success')
            return redirect(url_for('main.account', username=user.username))
    image_file = url_for('static', filename='images/' + user.profile_picture)

    for post in posts:
        image_post = url_for('static', filename='images/' +
                             post.image_1)
        # print(image_post)
        image_posts.append(image_post)

    return render_template('user.html', user=user, form=form, image_file=image_file, image_posts=image_posts)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_account(id):
    user = User.query.get(id)
    if user != current_user:
        abort(403)

    form = UpdateAccountForm()
    if request.method == 'POST':
        print('Yeah')
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            print(picture_file)
            user.profile_picture = picture_file
        user.email = form.email.data
        user.username = form.username.data
        db.session.add(user)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account', username=user.username))
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('update_profile.html', form=form, user=user)


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user!', 'warning')
        return redirect(url_for('main.home'))
    if current_user.is_following(user):
        flash('You are already following this user!', 'warning')
        return redirect(url_for('.account', username=user.username))
    current_user.follow(user)
    current_user.add_notification(
        name=user.username + ' just followed you', data=current_user.follow(user))
    db.session.commit()
    flash('You are now following %s.' % user.username, 'success')
    return redirect(url_for('main.account', username=user.username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user!', 'warning')
        return redirect(url_for('main.home'))
    if not current_user.is_following(user):
        flash('You are not following this user!', 'warning')
        return redirect(url_for('.account', username=user.username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You have unfollowed %s.' % user.username, 'success')
    return redirect(url_for('main.account', username=user.username))


@main.route('/followers/<username>')
@login_required
def followers(username):
    user = User.query.filter_by(username=username).first()
    followers = [follower for follower in user.followers]
    return render_template('followers.html', user=user, followers=followers)


@main.route('/followed_by/<username>')
@login_required
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    followed_by = [following for following in user.followed]
    return render_template('following.html', user=user, followed_by=followed_by)


@main.route('/following/<username>')
@login_required
def following(username):
    user = User.query.filter_by(username=username).first()
    return render_template('following.html', user=user)


@main.route('/like/<int:id>/<action>')
@login_required
def like_action(id, action):
    post = Post.query.filter_by(id=id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        current_user.add_notification(
            current_user.username + ' just liked your post', current_user.has_liked_post(post))
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)

    users, total = User.search(
        g.search_form.q.data, page, current_app.config['USERS_PER_PAGE'])
    print('users - ', users)
    details = []
    for user in users.all():
        image_file = url_for(
            'static', filename='images/' + user.profile_picture)
        details.append([user, image_file])

    return render_template('search.html', details=details)


@main.route('/notification')
@login_required
def notification():
    # since = request.args.get('since', 0.0, type=float)
    current_user.last_notification_read_time = datetime.utcnow()
    db.session.commit()
    notifications = current_user.notifications.order_by(
        Notification.timestamp.asc())

    return render_template('notifications.html', notifications=notifications)


@main.route('/delete-notification/<int:id>')
@login_required
def delete_notification(id):
    notifications = Notification.query.filter_by(id=id).first_or_404()
    db.session.delete(notifications)
    db.session.commit()
    return redirect(url_for('main.notification'))
