from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db') # 数据库文件保存在根目录
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)
