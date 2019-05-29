
# 不同数据类型的转换，double ulong等
# 参数dat：数据；flag：1表示有符号/GPSec，2表示无符号/Enum,3表示Float
def type2int(dat,flag):
    # 根据字符串长度判断数据类型
    dat_len = len(dat)
    global num
    # 8:Char/UChar
    if dat_len == 8:
        if flag == 1:
            #有符号负数
            if dat[0]=='1':
                num = -(256-int(dat,2))
            #有符号正数
            else:
                num = int(dat,2)
        elif flag == 2:
            num = int(dat,2)

    # 16:Short/UShort
    if dat_len == 16:
        # 重排列
        dat_sort = dat[8:16]+dat[0:8]
        if flag == 1:
            #有符号负数
            if dat_sort[0]=='1':
                num = -(65536-int(dat_sort,2))
            #有符号正数
            else:
                num = int(dat_sort,2)
        elif flag ==2:
            num = int(dat_sort,2)
        # print(dat_sort)

    # 32:Long/ULong/Float/Enum/GPSec
    if dat_len == 32:
        # Long/GPSec
        dat_sort = dat[24:32]+dat[16:24]+dat[8:16]+dat[0:8]
        if flag == 1:
            #有符号负数
            if dat_sort[0]=='1':
                num = -(4294967296-int(dat_sort,2))
            #有符号正数
            else:
                num = int(dat_sort,2)
        # ULong/Enum
        elif flag == 2:
            num = int(dat_sort,2)
        # Float
        elif flag == 3:
            factor = len('%d'% int(dat_sort[1:9],2))
            factor = pow(10,factor)
            S = pow(-1,int(dat_sort[0],2))
            E = int(dat_sort[1:9],2)
            M = int(dat_sort[9:32],2)/factor
            num = S*(1+M)*pow(2,E-127)

    # 64:Double
    if dat_len ==64:
        dat_sort = dat[56:64]+dat[48:56]+dat[40:48]+dat[32:40]+dat[24:32]+dat[16:24]+dat[8:16]+dat[0:8]
        sign = int(dat_sort[0])
        index = int(dat_sort[1:12], 2) - (2 ** (10) - 1)
        fractional_part = dat_sort[12:]
        dec = int('1' + fractional_part[:index], 2)
        fra = fractional_part[index:]

        sum = 0
        tmp = 0.5
        for c in fra:
            sum += tmp * float(c)
            tmp /= 2

        if sign:
            num = -(dec + sum)
        else:
            num = dec + sum
        
    return num

if __name__ == "__main__":
    dat = '0000000000000000000000000000000000000000000000001110111001000000'
    # dat = '0011001000000000'
    #dat = '0000000010000001'
    flag = 2
    a = type2int(dat,flag)
    print (a)





