import os

from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, FileField, \
    TextAreaField
from wtforms.validators import Length, Email, EqualTo, DataRequired, NumberRange

from jobplus.lib.tool import random_string
from jobplus.models import db, User, Company

rfile = UploadSet('RFile', extensions=('pdf', 'doc', 'docx', 'md'))
clogo = UploadSet('clogo', IMAGES)


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email('邮箱格式不正确')])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
    
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class RegisterForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='邮箱格式不正确')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message="密码长度为6-24")])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message="请输入相同的密码")])
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
    real_name = StringField('姓名')
    email = StringField('邮箱', validators=[DataRequired(), Email(message="邮箱格式不正确")])
    passwd = PasswordField('密码')
    phone = StringField('手机号', render_kw={"required": "required", "placeholder": "请输入11位手机号"})
    work_years = IntegerField('工作年限', validators=[NumberRange(min=0, max=100, message="请输入一个小于100的整数")],
                              render_kw={"placeholder": "请输入工作年龄，需要整数"})
    resume_file = FileField('工作简历', validators=[FileRequired(),
                                                FileAllowed(rfile,
                                                            message='只允许上传.doc/.pdf/.md后缀的文件')])
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') or len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.passwd.data:
            user.password = self.passwd.data
        if self.resume_file.data:
            # 获取文件后缀
            suffix = os.path.splitext(self.resume_file.data.filename)[1]
            # 生成随机的文件名
            filename = random_string() + suffix
            rfile.save(self.resume_file.data, name=filename)
            user.resume_url = filename

        user.phone = self.phone.data
        user.work_years = self.work_years.data
        db.session.add(user)
        db.session.commit()


class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码(不填写保持不变)')
    slogan = StringField('Slogan', validators=[DataRequired(), Length(3, 24)])
    company_logo = FileField('企业logo', validators=[FileRequired('文件未选择'),
                                                   FileAllowed(clogo, message='请上传图片类型文件')])
    trade = StringField('所处行业', validators=[Length(0, 64)])
    funding = StringField('融资阶段', validators=[Length(0, 64)])
    city = StringField('所在城市', validators=[Length(0, 64)])
    location = StringField('公司地址', validators=[Length(0, 64)])
    site = StringField('公司网站', validators=[Length(0, 64)])
    about = TextAreaField('公司详情', validators=[Length(0, 1024)])
    submit = SubmitField('提交')

    def updated_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.company_info:
            company_info = user.company_info

        else:
            company_info = Company()
            company_info.user_id = user.id

        self.populate_obj(company_info)
        if self.company_logo.data:
            # 获取文件后缀
            suffix = os.path.splitext(self.company_logo.data.filename)[1]
            # 生成随机的文件名
            filename = random_string() + suffix
            clogo.save(self.company_logo.data, name=filename)
            company_info.logo = filename
        db.session.add(user)
        db.session.add(company_info)
        db.session.commit()
