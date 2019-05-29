import socket,re
import sys
from Messageparse import Meparse
from tkinter import *
from tkinter.scrolledtext import *
import time
import threading
import datetime
import os
import pandas as pd
pd.set_option('display.max_colwidth',20)
# rawdata = 'aa44121c30060020580000008dc83207804a0b1b00000000ad24c43201000000e601000000f00200ffffff9f5a5db940ffffffffff07323f8df5436ab4e508c0ee9842d9c4f6ffbf99c1304053ee0540596797c0a079113e8607118374db9c3ffeffffffff9f3dbffeffffffffffbf3d0000000087e03abd'
# 时间匹配字符
result_data = {
    'data':[]
}
#界面
def makeApp():
    app = Tk()
    app.title("Message Parse")
    app.geometry("500x500")
    app.config(bg='#303030')
    Label(app, name="lb1", text="客户端",bg='#303030', fg="white", font=("Hack", 25, 'bold')).pack(side=TOP)
    Listbox(app, name="lbox", height=5,width=100, bg='#303030', fg="white", font=("Hack", 15)).pack(fill=BOTH)

    #第一个容器用于接收报文处理报文
    fm1=Frame(app,name='frm1', height=220,width=250,bg='#303030')
    fm1.pack(side=LEFT,fill=BOTH,expand=YES)
    #连接服务器
    Button(fm1, text="连接服务器",width=8,height=2,command=tosever).pack(side=TOP)
    # Button(fm1, text="断开连接", width=8, height=2, command=exit).pack(side=TOP)
       
    Label(fm1,name="lb2",text="报文接收",bg='#303030', fg="white", font=("Hack", 15, 'bold')).pack(side=TOP)
    Text(fm1, name="text1",height=10,width=100, bg='#303030', fg="white",).pack(side=TOP)
    #加一个框显示处理的结果
    Label(fm1,name="lb3",text="报文解析", bg='#303030', fg="white", font=("Hack", 15, 'bold')).pack(side=TOP)
    Text(fm1,name="text2", height=30,width=100, bg='#303030', fg="white",).pack(side=TOP)

    #第二个容器用于定位仿真
    fm2=Frame(app,name='frm2', height=220,width=250,bg='#303030')
    fm2.pack(side=LEFT,fill=BOTH,expand=YES)
    Label(fm2,name="lb3",text="处理结果", bg='#303030', fg="white", font=("Hack", 20, 'bold')).pack(side=TOP)
    Text(fm2, name="text3", height=10,width=50, bg='#303030', fg="white",font=("Arial", 12, 'bold')).pack(side=TOP, fill=BOTH, expand=True)
    return app

def ui_watcher():
    def _update_button():
        bt = app.children['bt1','bt2']
        thread = [t for t in threading.enumerate() if t.name == "client"]
        if thread:
            bt['state'] = "disabled"
        else:
            bt['state'] = 'normal'

    def _main():
        while True:
            _update_button()


    t = threading.Thread(name='uiWatcher', target=_main)
    t.start()

# def pauseThreading():
#     thread = [t for t in threading.enumerate()]
#     for t in thread:


def tosever():
    def Server():
        lb=app.children['lbox']#找控件
        fm1=app.children['frm1']
        t1=fm1.children['text1']
        t2=fm1.children['text2']
        # 服务器ipv4地址和端口号
        ip_port = ('127.0.0.1',1256)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ip_port)
        lb.insert(END,"连接成功，开始传输报文")
        # rawdata = ''
        while True:
            recv_data = str(s.recv(16384))
            t1.delete('1.0', END)
            t1.insert(END, "-------------------------------------------------\n")
            t1.insert(constants.END,str(recv_data))
            # print(recv_data[2:10])
            if recv_data[2:10] == 'aa44121c':
                t1.delete('1.0', END)
                t1.insert(constants.END, str(recv_data))
                tmp = Meparse(recv_data)
                t2.delete('1.0', END)
                t2.insert(constants.END, str(tmp))
                result_data['data'].append(tmp)

            if not recv_data:
                break
        s.close()

    t = threading.Thread(name='uiWatcher', target=Server)
    t.start()

    fm2 = app.children['frm2']
    text3 = fm2.children['text3']

    def printPandT():
        # pd_result = pd.DataFrame(columns = ["PRN","K","PSR"])
        if result_data['data']:
            if 'PSR'in result_data['data'][-1]:

            # if 'GPRN' in result_data['data'][-1]:
                
                result_data['data'][-1].drop_duplicates(['PRN'],keep='first',inplace=True)
                pd1_result = result_data['data'][-1][['PRN','PSR']]
                pd1_result['SQM1']='0'
                pd1_result['SQM2']='  0'
                pd1_result['SQM3']='  0'                                
                pd1_result['DQM']='0'
                pd1_result['MQM1']='0'
                pd1_result['MQM2']='0'
                pd1_result['MQM3']='0'

                # cols=pd1_result.columns
                # lencols=[int(len(c)*2)for c in cols]
                # pd1_result.columns = pd.MultiIndex.from_tuples(tuple((c[:ln],c[ln:]) for c,ln in zip(cols,lencols) ))


                text3.delete('1.0',END)
                text3.insert(END, str(pd1_result))
                # text3.insert(END, str(result_data['data'][-1][['GPRN']]))
                # print("需求：", result_data['data'][-1]['PSR'])
    def _main():
        while True:
            printPandT()
            time.sleep(1)

    t = threading.Thread(name='printP&T', target=_main)
    t.start()


app = makeApp()
if __name__ == "__main__":
    # rawdata='aa44121c30060020580000008dc83207804a0b1b00000000ad24c43201000000e601000000f00200ffffff9f5a5db940ffffffffff07323f8df5436ab4e508c0ee9842d9c4f6ffbf99c1304053ee0540596797c0a079113e8607118374db9c3ffeffffffff9f3dbffeffffffffffbf3d0000000087e03abd'

    # app.after(0,ui_watcher)
    app.mainloop()

