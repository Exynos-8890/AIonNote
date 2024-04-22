from flask import Flask, render_template
from flask import url_for
# from flask_sqlalchemy import SQLAlchemy
import os
import click
from openai import OpenAI

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db') # 数据库文件保存在根目录
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# db = SQLAlchemy(app)

@app.route('/')
def flowchart():
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
