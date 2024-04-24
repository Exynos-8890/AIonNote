from flask import Flask, render_template, url_for, request, redirect, flash
import pandas as pd
import os
import click
# from openai import OpenAI
# from tools.read_db import read
from tools.db2mermaid import db2mermaid_code
from tools.read_db import read, write

app = Flask(__name__)
app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db') # 数据库文件保存在根目录
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# db = SQLAlchemy(app)

# class Task(db.Model):
# id = db.Column(db.Integer, primary_key=True)
# name = db.Column(db.String(100), nullable=False)
# description = db.Column(db.Text)

# def __repr__(self):
#     return f"Task('{self.name}')" 

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('add'))
    return render_template('index.html',mermaid_code=db2mermaid_code())

@app.route('/add',methods=['GET', 'POST'])
def add():
    # 设置单行文字输入表单的初始内容

    df = read()
    if request.method == 'POST':
        summary = request.form['summary-input']
        reference = request.form.getlist('selected-options')
        # turn reference to list of int
        reference = [int(x) for x in reference]
        prompt = request.form['prompt-input']
        content = request.form['content-textarea']
        new_row = pd.DataFrame({'summary': summary, 'reference': [reference], 'prompt': prompt, 'content': content})
        df = pd.concat([df, new_row], ignore_index=True)
        write(df)
        # print(df)
        # flash('添加成功')
        return redirect(url_for('index'))

    summary_input_value = "节点缩写"

    # 设置多选框的选项
    options_dict = df['summary'].to_dict()
    selected_options = []

    prompt_input_value = "请在此输入问题"

    return render_template('adjust.html', 
                           summary_input_value=summary_input_value,
                           options_dict=options_dict, 
                           selected_options=selected_options, prompt_input_value=prompt_input_value
                           )


@app.route('/test',methods=['GET', 'POST'])
def given_tasks():
    if request.method == 'POST':
        option1_checked = request.form.get("option1")  # Check if Option 1 is checked
        option2_checked = request.form.get("option2")  # Check if Option 2 is checked

        print(request.form.getlist("option1"))
        if option1_checked:
            print("Option 1 is checked")
        if option2_checked:
            print("Option 2 is checked")

    return '''<form method="post">
    <input type="checkbox" name="option1" value="value1"> Option 1<br>
    <input type="checkbox" name="option2" value="value2"> Option 2<br>
    <input type="submit" value="Submit">
    </form>'''

if __name__ == '__main__':
    app.run(debug=True)
