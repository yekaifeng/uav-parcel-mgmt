# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from flask import request, url_for, redirect, render_template, flash, g, Markup, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm, db
from forms import UavForm, LoginForm, ParcelForm, DateForm
from models import User, Parcel
import datetime

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/list/')
def listall():
    date = datetime.datetime.today().date()
    todayrecords = Parcel.query.filter_by(date=date).all()
    print todayrecords
    if len(todayrecords) is not 0:
        for item in todayrecords:
#            item.package_id = Markup(process_string(item.package_id))
#            item.package_status = Markup(process_string(item.package_status))
#            item.created_office = Markup(process_string(item.created_office))
#            item.customer_name = Markup(process_string(item.customer_name))
#            item.customer_phone = Markup(process_string(item.customer_phone))
#            item.customer_address = Markup(process_string(item.customer_address))
#            item.uav_name = Markup(process_string(item.uav_name))
            strdt = item.create_pkg_time.strftime("%Y-%m-%d %H:%M:%S")
            item.create_pkg_time = strdt

        return render_template('list.html', parcels=todayrecords)
    else:
        return render_template('list.html', parcels='')

@app.route('/new/')
@login_required
def new():
	form = ParcelForm()
	return render_template('new.html', form=form)

@app.route('/save/', methods = ['GET','POST'])
@login_required
def save():
	existed = None
	msg = None
	dt = datetime.datetime.today()
	form = ParcelForm()
	if form.validate_on_submit():
		new_item = Parcel(form.package_id.data, form.customer_name.data,
                         form.customer_phone.data, form.created_office.data,
                         current_user.user, dt, dt.date())

        existed = Parcel.query.filter_by(package_id=form.package_id.data).first()
        if existed is None:
		    db.session.add(new_item)
		    db.session.commit()
		    print "create record %s" % form.package_id.data
        else:
            existed.package_id = form.package_id.data
            existed.customer_name = form.customer_name.data
            existed.customer_phone = form.customer_phone.data
            existed.created_office = form.created_office.data
            existed.last_update_by = current_user.user
            db.session.add(existed)
            db.session.commit()
        #print form.package_id.data
        #print form.customer_name.data
        #print form.created_office.data
        flash('Saved!')
        msg = 'Saved!'

	return render_template('new.html', title=msg, form=form)

@app.route('/pickdate/', methods = ['GET','POST'])
@login_required
def pick():
    form = DateForm()

    return render_template('list.html', form=form)

@app.route('/view/<id>/')
def view(id):
	return render_template('view.html')

@app.route('/depart/')
@login_required
def depart():
    uavform = UavForm()
    date = datetime.datetime.today().date()
    todayrecords = Parcel.query.filter_by(date=date) \
        .filter_by(package_status=Parcel.CONST_PKG_STATUS['received']).all()
    if len(todayrecords) is not 0:
        for item in todayrecords:
            strdt = item.create_pkg_time.strftime("%Y-%m-%d %H:%M:%S")
            item.create_pkg_time = strdt

        return render_template('depart.html', parcels=todayrecords, form=uavform)
    else:
        return render_template('depart.html', parcels='', form=uavform)

@app.route('/updatedepart/', methods = ['GET','POST'])
@login_required
def updatedepart():
    dt = datetime.datetime.today()
    dataform = request.form
    # keys of dataform contain the order numbers
    if len(dataform) is not 0:
        uavid = dataform.get('name')
        for key in dataform.keys():
            existed = Parcel.query.filter_by(package_id=key).first()
            if existed is not None:
                existed.package_status = Parcel.CONST_PKG_STATUS['depart']
                existed.uav_name = uavid
                existed.send_pkg_time = dt
                existed.last_update_by = current_user.user
                db.session.add(existed)
        db.session.commit()
    return redirect(url_for('depart'))

@app.route('/arrive/')
@login_required
def arrive():
    date = datetime.datetime.today().date()
    todayrecords = Parcel.query.filter_by(date=date) \
        .filter_by(package_status=Parcel.CONST_PKG_STATUS['depart']).all()
    if len(todayrecords) is not 0:
        for item in todayrecords:
            strdt = item.create_pkg_time.strftime("%Y-%m-%d %H:%M:%S")
            item.create_pkg_time = strdt

        return render_template('arrive.html', parcels=todayrecords)
    else:
        return render_template('arrive.html', parcels='')

@app.route('/updatearrive/', methods = ['GET','POST'])
@login_required
def updatearrive():
    dt = datetime.datetime.today()
    dataform = request.form
    # keys of dataform contain the order numbers
    if len(dataform) is not 0:
        for key in dataform.keys():
            existed = Parcel.query.filter_by(package_id=key).first()
            if existed is not None:
                existed.package_status = Parcel.CONST_PKG_STATUS['arrival']
                existed.receive_pkg_time = dt
                existed.last_update_by = current_user.user
                db.session.add(existed)
        db.session.commit()
    return redirect(url_for('arrive'))

@app.route('/receive/')
@login_required
def receive():
    date = datetime.datetime.today().date()
    todayrecords = Parcel.query.filter_by(date=date) \
        .filter_by(package_status=Parcel.CONST_PKG_STATUS['arrival']).all()
    if len(todayrecords) is not 0:
        for item in todayrecords:
            strdt = item.create_pkg_time.strftime("%Y-%m-%d %H:%M:%S")
            item.create_pkg_time = strdt

        return render_template('receive.html', parcels=todayrecords)
    else:
        return render_template('receive.html', parcels='')

@app.route('/updatereceive/', methods = ['GET','POST'])
@login_required
def updatereceive():
    dt = datetime.datetime.today()
    dataform = request.form
    # keys of dataform contain the order numbers
    if len(dataform) is not 0:
        for key in dataform.keys():
            existed = Parcel.query.filter_by(package_id=key).first()
            if existed is not None:
                existed.package_status = Parcel.CONST_PKG_STATUS['signed']
                existed.receive_pkg_time = dt
                existed.last_update_by = current_user.user
                db.session.add(existed)
        db.session.commit()
    return redirect(url_for('receive'))

# === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    #print "userid: %s" % id
    return User.query.get(int(id))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    message = None
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.user.data).first()
        if user is None:
            message = "User Not Found!"
        elif form.password.data == user.password:
            login_user(user, remember=True)
            message = 'Signed In!'
            print "user logined! %s" % form.user.data
        else:
            message = "Incorrect Password!"
    return render_template('login.html',
        title = message,
        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

def process_string(str):
    if str is not None:
        global new
        new = "<ul>"
        sp = str.split("\r")
        print sp

        for s in sp:
            new += "<li>%s</li>" % s
        new += "</ul>"
        return new
    else:
        return ""
# ====================
