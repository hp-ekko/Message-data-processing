import socket, shutil
import os
import re
from new_func import *
import time
from tkinter import *
import threading
from tkinter.filedialog import *

# 数据路径匹配项
data_path = r'20150101\d{2}\-20150101\d{2}'
info = {
    'path':[]
}
def makeApp():
    app = Tk()
    app.geometry("600x800")
    app.config(bg='#303030')
    Label(app, name="lb1", text="服务器端",bg='#303030', fg="white", font=("Hack", 25, 'bold')).pack(side=TOP)
    Label(app, name="lb2", text="传输文件列表", bg='#303030', fg="white", font=("Hack", 20, 'bold')).pack(side=TOP)
    Listbox(app, name="lbox1", bg='#303030', height=5,  fg="white", font=("Hack", 15)).pack(fill=BOTH, expand=True)
    Button(app, name="bt1", text="选择文件", command=ui_getdata).pack()
    Listbox(app, name="lbox2", bg='#303030', height=5, fg="white", font=("Hack", 15)).pack(fill=BOTH, expand=True)
    Button(app, name="bt2", text="启动服务器", command=ServerByTreading).pack()
    Label(app, name="lb3", text="实时传输内容", bg='#303030', fg="white", font=("Hack", 20, 'bold')).pack(side=TOP)
    Text(app, name="text", bg='#303030', height=5, fg="white", font=("Hack", 13)).pack(fill=BOTH, expand=True)
    return app

def ui_getdata():
    f_names = askopenfilenames()
    lbox = app.children['lbox1']
    info['path'] = f_names
    if info['path']:
        for f in f_names:
            lbox.insert(END, f.split('/')[-1])

def ui_watcher():
    def _update_button():
        bt1 = app.children['bt1']
        bt2 = app.children['bt2']
        thread = [t for t in threading.enumerate() if t.name == "server"]
        if thread:
            bt1['state'] = bt2['state'] = "disabled"
        else:
            bt1['state'] = bt2['state'] = 'normal'

    def _main():
        while True:
            _update_button()
            time.sleep(0.1)

    t = threading.Thread(name='uiWatcher', target=_main)
    t.start()

def ServerByTreading():
    def Server():
        lb = app.children['lbox2']
        text = app.children['text']
        # 服务器ipv4地址和端口号
        ip_port = ('127.0.0.1', 1256)
        # 实例化对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定IP,端口
        s.bind(ip_port)
        # 启动监听,允许挂起5个请求
        lb.insert(END, "等待连接......")
        s.listen(5)

        while True:
            conn, addr = s.accept()
            lb.insert(END, ('建立连接！ 来自:  %s: %s ' % addr))
            # conn.send(('welcome!').encode())
            while True:

                for p in info['path']:
                    lb.insert(END, "正在传输：" + p.split('/')[-1])
                    send_list = send_data_list(p)
                    for sd in range(0, len(send_list)):
                        if sd == 0:
                            pass
                        else:
                            time.sleep((send_list[sd]['seconds'] - send_list[sd - 1]['seconds']) / 1000)
                        text.delete('1.0', END)
                        text.insert(END, "------------------------文件中第%s条数据：-------------------------\n" % (sd+1))
                        text.insert(END, send_list[sd]['data'] + '\n')

                        conn.send(send_list[sd]['data'].encode())
                    conn.send(''.encode())

                lb.insert(END, '等待连接......')
                break
            conn.close()
            lb.insert(END, "连接断开")

    t = threading.Thread(name="server", target=Server)
    t.start()

app = makeApp()
if __name__ == "__main__":
    app.after(0, ui_watcher)
    app.mainloop()