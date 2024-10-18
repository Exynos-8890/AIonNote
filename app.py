from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import os, shutil
from tools.confident_keys import *
from tools.myapi import get_kimi_balance
from tools.db2mermaid import db2mermaid_code
from tools.read_db import read, write
from tools.run_prompt import run_index
from tools.edit_config import config_read,config_update_db_name


def copy_file(src_file: str, dest_file: str):
    shutil.copy(src_file, dest_file)

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
    data_content, _ = read()
    options_dict = data_content.set_index('id')['summary'].to_dict()
    print(options_dict)
    try:
        balance = get_kimi_balance()
    except:
        balance = 'Network Error'
    mermaid_code = db2mermaid_code()
    # print(config_read())
    return render_template('index.html',
                           mermaid_code=mermaid_code,
                           options = options_dict
                           ,balance = balance
                           )

@app.route('/config', methods=['GET'])
def config():
    files = os.listdir('./db')
    initial_file = config_read()['db_name']
    return render_template('config.html', files=files, initial_file=initial_file)

@app.route('/submit_config', methods=['POST'])
def submit_config():
    # format = request.form['format']
    file = request.form['file']
    config_update_db_name(file)
    return redirect(url_for('index'))

@app.route('/new_db', methods=['POST'])
def new_db():
    new_file = request.form['new_file']
    if not (new_file.endswith(".json") or new_file.endswith(".csv")):
        new_file += ".json"

    # 使用函数
    copy_file('./static/db_example.json', './db/' + new_file)
    
    config_update_db_name(new_file)
    # 重定向到首页
    return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        selected_option = request.form['option']
    else:  # GET 请求
        selected_option = request.args.get('option')
    
    if selected_option is not None:
        return redirect(url_for('edit_node', id=selected_option))
    else:
        return redirect(url_for('id'))  # 如果没有选择选项，重定向到首页

@app.route('/edit_node/<id>', methods=['GET', 'POST'])
def edit_node(id):
    if request.method == 'POST':
        if request.form.get('home') == 'home':
            return redirect(url_for('index'))
        data_content, data_structure = read()
        summary = request.form['summary-input']
        reference = request.form.getlist('selected-options')
        # turn reference to list of int
        # reference = [int(x) for x in reference]
        prompt = request.form['prompt-input']
        content = request.form['content-textarea']
        data_content.loc[data_content['id'] == int(id), ['summary', 'prompt', 'content']] = [summary, prompt, content]
        # data_structure[int(id)]['reference'] = reference
        for i in reference:
            data_structure.append({'id': int(id), 'reference': int(i)})
        write(data_content,data_structure)
        if request.form.get('submit_and_run') == 'submit_and_run':
            run_index(int(index))
            return redirect(url_for('edit_node', index=index))
        return redirect(url_for('index'))

    data_content,data_structure = read()
    try:
        id = int(id)
        row = data_content[data_content['id'] == id] # 选择 id 为 index 的行
    except (ValueError, IndexError):
        # 如果 index 不是有效的整数或者不在 DataFrame 的索引范围内
        return redirect(url_for('index'))
    print(row)
    summary_input_value = row['summary'].values[0]
    options_dict = data_structure[data_structure['id'] == id].set_index('id')['reference'].to_dict()
    # selected_options = row['reference']
    options_dict = data_content.set_index('id')['summary'].to_dict()
    selected_options = data_structure[data_structure['id'] == id]['reference'].to_list()
    prompt_input_value = row['prompt'].values[0]
    content_input_value = row['content'].values[0]
    return render_template('adjust.html', 
                           summary_input_value=summary_input_value,
                           options_dict=options_dict, 
                           selected_options=selected_options, 
                           prompt_input_value=prompt_input_value,
                           content_input_value=content_input_value
                           )

@app.route('/add',methods=['GET', 'POST'])
def add():
    # 设置单行文字输入表单的初始内容

    data_content, data_structure = read()
    if request.method == 'POST':
        if request.form.get('home') == 'home':
            return redirect(url_for('index'))
        summary = request.form['summary-input']
        reference = request.form.getlist('selected-options')
        # turn reference to list of int
        prompt = request.form['prompt-input']
        content = request.form['content-textarea']
        # new_row = pd.DataFrame({'summary': summary, 'reference': [reference], 'prompt': prompt, 'content': content})
        data_content.loc[data_content['id'] == int(id), ['summary', 'prompt', 'content']] = [summary, prompt, content]
        df = pd.concat([df, new_row], ignore_index=True)
        write(df)
        if request.form.get('submit_and_run') == 'submit_and_run':
            ID_to_run = df.index[-1]
            run_index(ID_to_run)
            return redirect(url_for('edit', index=ID_to_run))
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

@app.route('/edit/<index>',methods=['GET', 'POST'])
def edit(index):
    if request.method == 'POST':
        if request.form.get('home') == 'home':
            return redirect(url_for('index'))
        df = read()
        summary = request.form['summary-input']
        reference = request.form.getlist('selected-options')
        # turn reference to list of int
        reference = [int(x) for x in reference]
        if len(reference) == 0:
            reference = -1
        prompt = request.form['prompt-input']
        content = request.form['content-textarea']
        df.loc[int(index)] = {'summary': summary, 'reference': reference, 'prompt': prompt, 'content': content}
        write(df)
        if request.form.get('submit_and_run') == 'submit_and_run':
            run_index(int(index))
            return redirect(url_for('edit', index=index))
        return redirect(url_for('index'))

    df = read()
    print('typeof index:', type(index),'\nvalue of index:', index)
    index = int(index)
    print('typeof index:', type(index),'\nvalue of index:', index)
    row = df.iloc[index]
    summary_input_value = row['summary']
    options_dict = df['summary'].to_dict()
    if row['reference'] == -1:
        selected_options = []
    else:
        selected_options = row['reference']
    prompt_input_value = row['prompt']
    content_input_value = row['content']
    return render_template('adjust.html', 
                           summary_input_value=summary_input_value,
                           options_dict=options_dict, 
                           selected_options=selected_options, 
                           prompt_input_value=prompt_input_value,
                           content_input_value=content_input_value
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

@app.route('/running')
def running():
    # 在/running页面显示"running"
    message = "Running"
    
    # 模拟等待5秒后执行函数
    # func()
    
    # 函数执行完毕后重定向回根目录
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8000, debug=True)
