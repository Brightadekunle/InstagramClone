from flask import request
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileAllowed, FileField


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    profile_picture = FileField('Update profile picture', validators=[
        FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update Profile')


class PostForm(FlaskForm):
    image_post = FileField('New Post', validators=[
        FileAllowed(['jpg', 'png'])])
    caption = StringField('Caption', validators=[
        DataRequired(), Length(1, 64)])

    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    q = StringField(_l('search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
                            DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('submit')
