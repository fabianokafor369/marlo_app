from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, url_for, request, flash, abort
from flask_sqlalchemy  import SQLAlchemy
from markupsafe import Markup
from itsdangerous import URLSafeTimedSerializer
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo, NumberRange
from scipy.stats import gmean, hmean
from numpy import mean
from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import InputRequired
from sqlalchemy.exc import IntegrityError
import math


#########################Config
#Here, configuration settings are made, including the app configuration, email and database config, etc.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

#Flask Extension Area
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)



from uuid import uuid4




#########################Database system
#This file holds the database table creation using the sqlalchemy module.
def IdColumn(*args, **kwargs):
    return db.Column(db.String, *args, nullable=False,
                  default=lambda: str(uuid4())
                  if 'primary_key' in kwargs else None,
                  **kwargs)

class Meeting(db.Model):
    __tablename__ = 'meeting'
    meeting_id = IdColumn(primary_key= True)
    meeting_name = db.Column(db.String(50))
    meeting_date = db.Column(db.DateTime, nullable=True)

    def __str__(self):
        return self.meeting_name

    def __repr__(self):
        return self.meeting_name


class Review(db.Model):
    __tablename__ = 'review'
    review_id = IdColumn(primary_key= True)
    meetingreviewed = db.Column(db.String(50), db.ForeignKey(Meeting.meeting_id), nullable=False)

    #general
    firstname = db.Column(db.String(35))
    lastname = db.Column(db.String(35))
    email = db.Column(db.String(60), unique=True)
    postmeeting_feeling = db.Column(db.Integer, default= 50)
    participation_score = db.Column(db.Integer, default= 50)
    meeting_id = db.relationship("Meeting")



###########################Admin Dashboard system
#Set up the admin system
class MyView(ModelView):
    page_size = 50
    column_searchable_list = ['firstname', 'email']
    column_filters = ['lastname', 'email']
    column_editable_list = ['firstname', 'lastname']
    column_list = ['email', "firstname", "lastname", "participation_score", "postmeeting_feeling"]
    column_display_pk = False
    can_create = False
    can_edit = False


class MeetingView(ModelView):
    page_size = 50
    column_display_pk = False
    create_modal = True
    edit_modal = True


admin = Admin(app, template_mode = 'bootstrap3', url= '/admin', )
admin.add_view(MyView(Review, db.session))
admin.add_view(MeetingView(Meeting, db.session))




########################Form creation
#Create the forms
class FeedbackForm(FlaskForm):
    firstname = StringField('First name', validators=[InputRequired(), Length(min=2, max=35)])
    lastname = StringField('Last name', validators=[InputRequired(), Length(min=2, max=35)])
    email = StringField('Email address', validators=[InputRequired(), Length(min=4, max=50)])
    postmeeting_feeling = IntegerField('How did you feel about this meeting', validators=[InputRequired(), NumberRange(min=0, max=100, message="Please select a number between 1 and 100")])
    participation_score = IntegerField("What is your perceived level of participation?", validators=[InputRequired(), NumberRange(min=1, max=100, message="Please select a number between 1 and 100")])
    meeting = SelectField()

    def __init__(self):
        super(FeedbackForm, self).__init__()
        self.meeting.choices = [(c.meeting_id, c.meeting_name) for c in Meeting.query.all()]




#Create the routes
def themeans(dlist):
    arithmetic_mean = mean(dlist)
    geometric_mean = gmean(dlist)
    harmonic_mean = hmean(dlist)
    return arithmetic_mean, geometric_mean, harmonic_mean



@app.route('/', methods=["GET", "POST"])
@app.route("/feedback", methods = ['GET', "POST"])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        try:
            meetname = Meeting.query.filter_by(meeting_id = form.meeting.data).first()
            feedback = Review(firstname=form.firstname.data, lastname=form.lastname.data,  email=form.email.data + "+" + meetname.meeting_name, postmeeting_feeling= form.postmeeting_feeling.data,  participation_score = form.participation_score.data, meetingreviewed = form.meeting.data)
            db.session.add(feedback)
            db.session.commit()

            flash(Markup("Feedback has been noted. Thanks for reaching out."), "success")

            return redirect(url_for('feedback'))

        except IntegrityError:
            db.session.rollback()
            flash("ERROR! Feedback for Email({}) already exists for that particular meeting session.".format(form.email.data), 'error')

    return render_template("feedback.html", form = form)




###############################initiate
#This file simply launches the whole app, allowing all the python files to call on themselves where necessary, hence making the app run.
if __name__ =="__main__":
    app.run(debug=True)
