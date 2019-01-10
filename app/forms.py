from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, RadioField, \
    TextAreaField, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddInformationUserForm(FlaskForm):
    firstname = StringField(validators=[DataRequired()])
    lastname = StringField(validators=[DataRequired()])
    birthday_day = SelectField(
        choices=[('Day:', 'Day:'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                 ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
                 ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
                 ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
                 ('29', '29'), ('30', '30'), ('31', '31')]
    )
    birthday_month = SelectField(
        choices=[('Month:', 'Month:'), ('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'),
                 ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'), ('8', 'Aug'), ('9', 'Sep')
            , ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]
    )
    birthday_year = SelectField(
        choices=[('Year:', 'Year:'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015')
            , ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010')
            , ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005')
            , ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')
            , ('1999', '1999'), ('1998', '1998'), ('1997', '1997'), ('1996', '1996'), ('1995', '1995')
            , ('1994', '1994'), ('1993', '1993'), ('1992', '1992'), ('1991', '1991'), ('1990', '1990')
            , ('1989', '1989'), ('1988', '1988'), ('1987', '1987'), ('1986', '1986'), ('1985', '1985')
            , ('1984', '1984'), ('1983', '1983'), ('1982', '1982'), ('1981', '1981'), ('1980', '1980')
            , ('1979', '1979'), ('1978', '1978'), ('1977', '1977'), ('1976', '1976'), ('1975', '1975')
            , ('1974', '1974'), ('1973', '1973'), ('1972', '1972'), ('1971', '1971'), ('1970', '1970')]
    )
    gender = RadioField(choices=[('Man', 'Man'), ('Woman', 'Woman')])
    number = IntegerField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired(), Length(10)])
    submit = SubmitField('Submit')


class CreateTeamForm(FlaskForm):
    name_team = StringField('NameTeam', validators=[DataRequired()])
    submit = SubmitField('Submit')


class JoinTeamForm(FlaskForm):
    access_key = StringField('AccessKey', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CreateEventForm(FlaskForm):
    name_event = StringField('NameEvent', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category1 = StringField('Category1', validators=[DataRequired()])
    category2 = StringField('Category2')
    category3 = StringField('Category3')
    category4 = StringField('Category4')
    category5 = StringField('Category5')
    submit = SubmitField('Submit')


class JoinEventForm(FlaskForm):
    active_event = SelectField(choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')

class JoinEventCategoryForm(FlaskForm):
    active_event_f = TextField()
    category = SelectField(choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')
