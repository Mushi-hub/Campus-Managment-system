#from zipfile import sizeFile
#from random import choices

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.choices import RadioField
from wtforms.validators import DataRequired

class AdminForm(FlaskForm):
    candidates_name= StringField(label='Candidate Names: ', validators=[DataRequired()])
    candidates_position= SelectField(label='Choose Candidates Position', choices=[('President','President')],
                                     validators=[DataRequired()])
    image = FileField("Upload Image: ", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Only images are allowed!')])

    vice_president_name = StringField(label='Vice President Name: ', validators=[DataRequired()])
    vice_position = SelectField(label='Choose Candidates Position', choices=[('Vice President', 'Vice President')],
                                      validators=[DataRequired()])
    vice_president_image = FileField("Upload Image: ",
                      validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Only images are allowed!')])


    submit = SubmitField("Save Candidate")


class LoginForm(FlaskForm):
    username=StringField(label='User Name:',validators=[DataRequired()])
    password=PasswordField(label='Enter Password:',validators=[DataRequired()])
    submit = SubmitField("Login")

class ViewForm(FlaskForm):
    submit = SubmitField("Delete")

class studentForm(FlaskForm):
    vote = RadioField("vote")
    submit = SubmitField("Submit Vote")

class usersForm(FlaskForm):
    users = FileField("Upload users file: ",
                      validators=[FileRequired(), FileAllowed(['xlsx', 'xls', 'xlsm','xlsb','cvs'], 'Only excel files are allowed!!')])
    submit = SubmitField("submit")