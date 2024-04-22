import pandas as pd
import os
file_name = 'test.csv'
# 获取当前工作目录
current_directory = os.getcwd()

# 构建CSV文件的相对路径
csv_file_path = os.path.join(current_directory, 'db', file_name)


def read():
    df = pd.read_csv(csv_file_path)
    df['reference'] = df['reference'].apply(eval)
    return df

def write(df):
    df.to_csv(csv_file_path, index=False, encoding='utf-8')

if (__name__ == '__main__'):
    df = read()
    print(df['summary'])