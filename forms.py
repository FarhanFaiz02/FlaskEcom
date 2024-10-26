from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    address = TextAreaField('Shipping Address', validators=[DataRequired()])
    submit = SubmitField('Place Order')