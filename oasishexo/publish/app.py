from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import subprocess
import os
import signal
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# 初始化脚本执行状态标志和子进程对象
script_executing = False
process = None

def get_newest_files(folder_path):
    print("Scanning folder:", folder_path)
    newest_files = []
    
    # 获取文件夹中的文件和子文件夹
    files_and_dirs = os.listdir(folder_path)
    
    # 遍历文件和子文件夹
    for item in files_and_dirs:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            # 如果是文件，获取文件的创建时间和最后修改时间
            try:
                created_time = os.path.getctime(item_path)
                modified_time = os.path.getmtime(item_path)
                
                # 获取中国标准时间的时区对象
                cst = pytz.timezone('Asia/Shanghai')
                
                # 将修改时间转换为中国标准时间
                modified_time_cst = datetime.fromtimestamp(modified_time, tz=cst)
                
                # 将修改时间以指定格式格式化为字符串
                modified_time_formatted = modified_time_cst.strftime('%Y-%m-%d %H:%M:%S')
                
                # 创建包含文件名、修改时间和路径的元组
                file_info = (item, modified_time_formatted, item_path)
                newest_files.append(file_info)
                print("Scanning file:", item_path)
            except OSError as e:
                print("Error getting file info:", e)
        elif os.path.isdir(item_path):
            # 如果是文件夹，递归进入文件夹并获取其中的文件信息
            newest_files += get_newest_files(item_path)
    
    # 按修改时间排序
    newest_files.sort(key=lambda x: x[1], reverse=True)
    
    # 只保留前五个文件
    newest_files = newest_files[:5]
    
    return newest_files

@app.route('/')
def index():
    folder_path = "/hexo/nas/source"  # 指定文件夹路径
    newest_files = get_newest_files(folder_path)
    
    return render_template('index.html', newest_files=newest_files)

@app.route('/run-script')
def run_script():
    return render_template('run_script.html')

@socketio.on('execute_script')
def execute_script(script_name):
    global script_executing, process

    # 如果有脚本正在执行，则拒绝执行新的脚本
    if script_executing:
        emit('output', 'Another script is already running. Please wait until it finishes.')
        return

    script_executing = True

    command = f"{script_name}"  # 执行脚本
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            emit('output', line.strip())
    except Exception as e:
        emit('output', str(e))
    finally:
        script_executing = False

@socketio.on('terminate_script')
def terminate_script():
    global process

    if process:
        os.kill(process.pid, signal.SIGINT)  # 发送中断信号
        process = None  # 清除进程对象
        emit('output', 'Script execution terminated.')
    else:
        emit('output', 'No script is currently running.')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)
