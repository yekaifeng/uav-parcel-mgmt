# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from flask.ext.wtf import Form, TextField, TextAreaField, DateTimeField, PasswordField, BooleanField
from flask.ext.wtf import Required, DateField, FormField, FieldList, SelectField

class ExampleForm(Form):
	title = TextField(u'Título', validators = [Required()])
	content = TextAreaField(u'Conteúdo')
	date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')

class LoginForm(Form):
	user = TextField(u'用户名', validators = [Required()])
	password = PasswordField(u'密码', validators = [Required()])

class ParcelForm(Form):
	package_id = TextField(u'运单号', validators = [Required()])
	customer_name = TextField(u'客户姓名')
	customer_phone = TextField(u'客户电话')
	created_office = TextField(u'站点')

class DateForm(Form):
    date = DateField(u'Date', format='%Y-%m-%d')

class UavForm(Form):
	name = SelectField(u'无人机ID', choices=[(u'亿航00001',u'亿航00001'),
	(u'易瓦特00001',u'易瓦特00001'), (u'洲际00001',u'洲际00001') ])
