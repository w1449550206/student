#!/usr/bin/env python3

import os

import pymysql
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

# 项目文件夹的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'upload')

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://vicky:wangwenqi5261@localhost/student1221'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    gender = db.Column(db.String(10))
    chinese = db.Column(db.Float)
    math = db.Column(db.Float)


@app.route('/')
def home():
    users = Student.query.all()
    return render_template('home.html', users=users)


@app.route('/modify', methods=('GET', 'POST'))
def modify():
    if request.method == 'POST':
        uid = int(request.form['uid'])
        user = Student.query.get(uid)
        user.gender = request.form['gender']
        user.chinese = int(request.form['chinese'])
        user.math = int(request.form['math'])
        db.session.add(user)
        db.session.commit()

        # 保存上传的头像
        upload_img = request.files['avatar']  # 取出上传的图片对象
        filepath = os.path.join(UPLOAD_DIR, user.name)  # 计算出文件保存的绝对路径
        upload_img.save(filepath)  # 保存文件

        return redirect('/')
    else:
        uid = int(request.args['uid'])
        user = Student.query.get(uid)
        return render_template('modify.html', user=user)


@app.route('/info')
def info():
    uid = int(request.args['uid'])
    user = Student.query.get(uid)
    return render_template('info.html', user=user)


@app.route('/top5')
def top5():
    order_condition = db.desc(Student.chinese + Student.math)
    users = Student.query.order_by(order_condition).limit(5)
    return render_template('top5.html', users=users)


if __name__ == '__main__':
    app.debug = True
    app.run()
