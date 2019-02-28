from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired

from jobplus.models import db, User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码',validators=[DataRequired(), Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
    
    def validate_password(self,field):
        user = User.query.filter_by(email = self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')



class RegisterForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[DataRequired(),Length(6,24)])
    submit = SubmitField('提交')
    

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已经存在')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')
            

    def create_user(self):
        user = User()
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()

        return user

    
