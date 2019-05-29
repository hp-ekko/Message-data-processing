import re
import os


def get_path(time):

    # 根据需求时间得到文件位置，返回文件绝对位置
    month_time = time[0:6]
    # 数据所处月文件夹
    hours_time = time
    # 数据具体文件名
    path = 'C:\\Users\zch\Desktop\chuanshu\server'
    # 数据文件位置
    month_file = os.path.join(path,month_time)
    # 绝对月文件位置
    hours_file = os.path.join(month_file,hours_time)
    # 绝对小时文件位置
    return hours_file

def get_raw_info(file_name):

    # 读取raw文件中的二进制信息，并将信息存入一个字符串
    # 输入：文件名称
    # 输出：字符串
    day_path = get_path(file_name)
    d = open(day_path,'rb')
    d.seek(0,0)
    list = []

    while True:
        byte = d.read(1024)
        data = int.from_bytes(byte, byteorder = 'big', signed = False)
        if len(byte) == 0:
            break
        else:
            list.append(str('{:x}'.format(data)).zfill(2))
    d.close()
    info = ''.join(list)

    return info

def cut_into_slices(data):

    # 将得到的数据按照同步码分割，并存入列表
    # 输入：字符串
    # 输出：列表

    sync = r'aa4412'
    result = re.split(sync,data)
    last = []
    for data in result:
        if len(data) == 0:
            continue
        i = sync + data
        last.append(i)

    return last

def get_the_time(data):

    # 对于时间的提取还是有问题
    wk = data[30:32] + data[28:30]
    ms = data[38:40] + data[36:38] + data[34:36] + data[32:34]
    time_week = int(wk, 16)
    time_status = int(data[26:28], 16)
    time_ox = int(ms, 16)

    return time_status,time_week,time_ox

def send_data_list(time):
    info = get_raw_info(time)
    data_list = cut_into_slices(info)
    data_dict = []
    for i in data_list:
        status, week, time = get_the_time(i)
        if status not in [180, 200]:
            continue
        data = {
            'status': status,
            'weeks': week,
            'seconds': time,
            'data': i
        }
        data_dict.append(data)
    after_sorted = sorted(data_dict, key=lambda data_dict: data_dict['seconds'])
    re_list = after_sorted
    for i in range(0, len(after_sorted)):
        for j in range(i+1, len(after_sorted)):
            while after_sorted[i]['seconds'] == after_sorted[j]['seconds']:
                re_list[i]['data'] = re_list[i]['data'] + re_list[j]['data']
                re_list.pop(j)
            else:
                break
    return re_list


if __name__ == '__main__':
    sd = send_data_list('2015010100')
    for s in sd:
        print(s)