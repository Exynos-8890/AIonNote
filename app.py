from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import click
# from openai import OpenAI
# from tools.read_db import read
from tools.db2mermaid import db2mermaid_code
from tools.read_db import read

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db') # 数据库文件保存在根目录
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# db = SQLAlchemy(app)

# class Task(db.Model):
# id = db.Column(db.Integer, primary_key=True)
# name = db.Column(db.String(100), nullable=False)
# description = db.Column(db.Text)

# def __repr__(self):
#     return f"Task('{self.name}')" 

@app.route('/')
def index():
    return render_template('index.html',flow_definition=db2mermaid_code())

@app.route('/test')
def given_tasks():
    # 假设这是从数据库获取的任务数据
    tasks = [
        {"id": "1", "name": "开始", "next": ["2"]},
        {"id": "2", "name": "任务1", "next": ["3"]},
        {"id": "3", "name": "任务2", "next": ["4"]},
        {"id": "4", "name": "结束", "next": []}
    ]

    # 生成 Mermaid 流程图定义
    flow_definition = "graph LR;\n"
    for task in tasks:
        for next_task in task["next"]:
            flow_definition += f"{task['id']}({task['name']}) --> {next_task};\n"

    return render_template('index.html', flow_definition=flow_definition)

if __name__ == '__main__':
    app.run(debug=True)
