from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField
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
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
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


class UserProfilesForm(FlaskForm):
    name = StringField('姓名')
    email = StringField('邮箱', validators=[DataRequired(), Length(8, 64),
                                          Email(message="电子邮箱不符合规范")])
    passwd = PasswordField('密码')
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume_url = StringField('简历地址')
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if len(phone) != 11 and phone[:2] not in ('13', '18', '15'):
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()
