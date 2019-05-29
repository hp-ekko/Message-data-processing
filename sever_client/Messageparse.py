"""
七类数据分别解析
接收的数据，可能会有多段消息发过来，先得处理
"""
import numpy as np 
import pandas as pd
pd.set_option('display.width',None)
pd.set_option('display.max_rows',None)


from types2int import type2int


#分段函数
def div_raw(ls,n):
    ls_len=len(ls)
    j =ls_len//n
    ls_return=[]
    if j>0:
        for i in range(0,(n-1)*j,j):
            ls_return.append(ls[i:i+j])
        ls_return.append(ls[(n-1)*j:])
    else:
        ls_return.append(ls)
    return ls_return
#计算Id 消息长度 及数量
def mesid(data_id):

    data_id.reverse()
    id_hex=''.join(data_id)

    id_int=int(id_hex,16)
    return id_int
#得到有几段消息，并写成list

def dataseg(source,elmt): 
    elmt_index=[]
    s_index = 0;e_index = len(source)
    while(s_index < e_index):
        try:
            
            temp = source.index(elmt,s_index,e_index)
            elmt_index.append(temp)
            s_index = temp + 1
        except ValueError:
            break  
    elmt_index.append(len(source)) 
    lis_data=[] 
    for i,ele in enumerate(elmt_index):

        if i<(len(elmt_index)-1):  
            lis_temp=source[elmt_index[i]:elmt_index[i+1]]
            lis_data.append(lis_temp)
        else:
            break
    print("Message number:",len(elmt_index)-1)
    return lis_data

#将字符串转成list，后续的程序都是在list基础写的
def segmented(iterable):
    it = iterable
    while len(it) > 2:
        yield it[:2]
        it = it[2:]
    yield it

def message140(data140):
    #卫星数量
    b=mesid(data140[28:32])
    id_140=mesid(data140[4:6])
    # print(id_140)
    #剔除前32个字节和crc
    del data140[0:32]
    del	data140[-4:]
    #分段
    
    c=div_raw(data140,b)
    #把每一段转成2进制并且转成字符串
    raw_tmp  = []
    for j,ele_li in enumerate(c):
        for i,ele in enumerate(c[j]):
            bin_ele='{:08b}'.format(int(ele,16))
            raw_tmp.append(bin_ele)

    data_8c00=div_raw(raw_tmp,b)
    raw_8c00=[]
    StdDev_PSR = {0:0.050,1:0.075,2:0.113,3:0.169,4:0.253,5:0.380,6:0.570,7:0.854,8:1.281,9:2.375,10:4.750,11:9.500,12:19.000,13:38.000,14:76.000,15:152.000}

    for i,ele in enumerate(data_8c00):
        data_8c00[i]=''.join(data_8c00[i])
        cut_tmp=[]
        #Channel Tracking Status 解析
        cut_tmp.append(int(data_8c00[i][0:5],2))
        cut_tmp.append(int(data_8c00[i][5:10],2))
        cut_tmp.append(int(data_8c00[i][10:11],2))
        cut_tmp.append(int(data_8c00[i][11:12],2))
        cut_tmp.append(int(data_8c00[i][12:13],2))
        cut_tmp.append(int(data_8c00[i][13:16],2))
        cut_tmp.append(int(data_8c00[i][16:19],2))
        cut_tmp.append(int(data_8c00[i][19:20],2))
        cut_tmp.append(int(data_8c00[i][20:21],2))
        cut_tmp.append(int(data_8c00[i][21:26],2))
        cut_tmp.append(int(data_8c00[i][26:27],2))
        cut_tmp.append(int(data_8c00[i][27:28],2))
        cut_tmp.append(int(data_8c00[i][28:29],2))
        cut_tmp.append(int(data_8c00[i][29:30],2))
        cut_tmp.append(int(data_8c00[i][30:31],2))
        cut_tmp.append(int(data_8c00[i][31:32],2))
    #对应出所有140状态具体数值，保留四位小数
        cut_tmp.append(float('%.4f'%(int(data_8c00[i][32:60],2)/256)))
        cut_tmp.append(float('%.4f'%(int(data_8c00[i][60:96],2)/128)))
        cut_tmp.append(float('%.4f'%(int(data_8c00[i][96:128],2)/256)))
        cut_tmp.append(StdDev_PSR[int(data_8c00[i][128:132],2)])
        cut_tmp.append(float('%.4f'%((int(data_8c00[i][132:136],2)+1)/512)))
        cut_tmp.append(int(data_8c00[i][136:144],2))
        cut_tmp.append(float('%.4f'%(int(data_8c00[i][144:165],2)/32)))
        cut_tmp.append(20+int(data_8c00[i][165:170],2))
        cut_tmp.append(int(data_8c00[i][170:192],2))

        raw_8c00.append(cut_tmp)
        # print(cut_tmp)
    pd_140 = pd.DataFrame(raw_8c00)
    pd_140.columns = ('Tracking state','SV','Phase lock flag','Parity known flag','Code locked flag','Correlator type','SS','Reserved','Grouping','Signal type','Reserved','Primary L1 channel','Carrier phase measurement','Reserved','PRN lock flag','Channel assignment','Doppler Frequency/HZ','PSR','ADR/cycles','StdDev-PSR/m','StdDev-ADR/cycles',
                                    'PRN','Lock Time/s','C/No/db-hz','Reserved')
    pd_140.to_csv('140.csv')
    # print(pd_140)
    return pd_140
def message41(data_41):
    def cplmcode(a):
        if a[0]=='1':
            tmp = -(2**(len(a[1:]))-int(a[1:],2))
        else:
            tmp = int(a,2)
        return tmp
    print(mesid(data_41[4:6]))
    # 剔除前28个字节和crc
    del data_41[0:28]
    del data_41[-4:]
    # print(data_41)


    pd_41 = pd.DataFrame(columns=['prn', 'ref week', 'ref secs','code_on','week_No','p_flag','SV_acc','SV_hl','Tgd','IODC','toc','af2','af1','af0','IODE','Cts','delta_n','M0','Cuc','e','Cus','sq_A','toe','Cic','Omega0','Cis','i0','Ctc','w','Omega_dot','IDOT'])

    cut_41 = np.array([4, 4, 4])
    # print(cut_41)
    # print(data_41)


    # 转成2进制数bin_41
    bin_41 = []
    for ind, line in enumerate(data_41):
        bin_line = '{:08b}'.format(int(line, 16))
        bin_41.append(bin_line)

    # 数据处理
    for ind, line in enumerate(data_41):
        list_tmp = []
        for i, ele in enumerate(cut_41):
            ind_start = sum(cut_41[0:i])
            ind_end = sum(cut_41[0:(i + 1)])

            data_bin = bin_41[ind_start:ind_end]
            data_bin = ''.join(data_bin)

            data_int = type2int(data_bin, 2)
            list_tmp.append(data_int)

    #选出子帧
    del data_41[0:40]
    del data_41[-4:]
    # print(data_41)

    #子帧1
    tmp1 = bin_41[0:30]
    subf1 = ''.join(tmp1)
    #子帧2
    tmp2 = bin_41[30:60]
    subf2 = ''.join(tmp2)
    #子帧3
    tmp3 = bin_41[60:90]
    subf3 = ''.join(tmp3)

    #数据处理
    #子帧1参数
    code_on = subf1[58:60]
    week_No = int(subf1[24:41],2) * 4
    p_flag = subf1[72]
    SV_acc = subf1[60:64]
    SV_hl = subf1[64:70]
    Tgd = cplmcode(subf1[160:168]) / (2**31)
    IODC = subf1[70:72] + subf1[168:168+8]
    toc = int(subf1[176:176+16],2) * (2**4)
    af2 = cplmcode(subf1[192:200]) / (2**55)
    af1 = cplmcode(subf1[200:216]) / (2**43)
    af0 = cplmcode(subf1[216:238]) / (2**31)

    #子帧2,3参数
    IODE = subf2[48:56]
    Cts = cplmcode(subf2[56:56+16]) / (2**5)
    delta_n = cplmcode(subf2[72:72+16]) / (2**43)
    M0 = cplmcode(subf2[88:88+8] + subf2[96:96+24]) / (2**31)
    Cuc = cplmcode(subf2[120:136]) / (2**29)
    e = int(subf2[136:136+8] + subf2[144:144+24],2) / (2**33)
    Cus = cplmcode(subf2[168:168+16]) / (2**29)
    sq_A = int(subf2[184:184+8] + subf2[192:192+24],2) / (2**19)
    toe = int(subf2[216:216+16],2) * (2**4)

    Cic = cplmcode(subf3[48:48+16]) / (2**29)
    Omega0 = cplmcode(subf3[64:64+32]) / (2**31)
    Cis = cplmcode(subf3[96:96+16]) / (2**29)
    i0 = cplmcode(subf3[112:112+32]) /(2**31)
    Ctc = cplmcode(subf3[144:144+16]) / (2**5)
    w = cplmcode(subf3[160:160+32]) /(2**31)
    Omega_dot = cplmcode(subf3[192:192+24]) / (2**43)
    IDOT = cplmcode(subf3[224:224+14]) / (2**43)

    tmp_41 = [code_on, week_No, p_flag, SV_acc, SV_hl, Tgd, IODC, toc, af2, af1, af0, IODE, Cts, delta_n, M0, Cuc, e, Cus, sq_A, toe, Cic, Omega0, Cis, i0, Ctc, w, Omega_dot, IDOT]
    list_tmp.extend(tmp_41)
    pd_41.loc[ind] = np.array(list_tmp)
    # print(pd_41)
    pd_41.to_csv('41.csv')
    return pd_41
def message73(data_4900):
    print(mesid(data_4900[4:6]))
    c=mesid(data_4900[28:32])
    #剔除前32个字节和crc
    del data_4900[0:32]
    del	data_4900[-4:]
    # print(data_4900)

    #转成2进制数bin_d302
    bin_4900=[]
    for ind, line in enumerate(data_4900):
        bin_line = '{:08b}'.format(int(line,16))
        bin_4900.append(bin_line)
    # print(bin_4900)
    #分段
    div4900=div_raw(bin_4900,c)
    pd_div4900 = pd.DataFrame(columns =['GPRN','week','seconds','ecc','0_omega','omega_0','omega','Mo','afo',
                                    'af1','N','A','ncl-angle','SV config','health-prn','health-alm','antispoof'])
    cut_div4900 = np.array([4,4,8,8,8,8,8,8,8,8,8,8,8,4,4,4,4])

    for j,e in enumerate(div4900):
        for ind, line in enumerate(div4900[j]):
            list_tmp = []
            for i, ele in enumerate(cut_div4900):
                ind_start = sum(cut_div4900[0:i])
                ind_end = sum(cut_div4900[0:(i+1)])
                data_bin= div4900[j][ind_start:ind_end]
                data_bin = ''.join(data_bin)
                data_int = type2int(data_bin,2)
                list_tmp.append(data_int)

        pd_div4900.loc[j] = np.array(list_tmp)

    # print(pd_div4900)

    pd_div4900.to_csv('73.csv')
    return pd_div4900
def message1696(data_1696):
    #id
    print(mesid(data_1696[4:6]))
    #剔除前28个字节和crc
    del data_1696[0:28]
    del data_1696[-4:]

    pd_1696 = pd.DataFrame(columns = ['satellite ID','Week','URA','health 1','tgd1','tgd2','AODC','toc','a0','a1',
                            'a2','AODE','toe','RootA','ecc','ω','ΔN','M0','Ω0','0_Ω','i0','IDOT','c_uc','c_us','c_rc','c_rs',
                            'c_ic','c_is'])


    cut_1696 = np.array([4,4,8,4,8,8,4,4,8,8,8,4,4,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8])
    # print(cut_1696)
    # print(data_1696)

    #转成2进制数bin_1696
    bin_1696=[]
    for ind, line in enumerate(data_1696):
        bin_line = '{:08b}'.format(int(line,16))
        bin_1696.append(bin_line)

    for ind, line in enumerate(data_1696):
        list_tmp = []
        for i, ele in enumerate(cut_1696):
            ind_start = sum(cut_1696[0:i])    
            ind_end = sum(cut_1696[0:(i+1)])

            data_bin= bin_1696[ind_start:ind_end]
            data_bin = ''.join(data_bin)

            data_int = type2int(data_bin,2)
            list_tmp.append(data_int)
    pd_1696.loc[ind] = np.array(list_tmp)
    pd_1696.loc[ind] = np.array(list_tmp)

    # print(pd_1696.head(5))
    pd_1696.to_csv('1696.csv')
    return pd_1696
def message1120(data_1120):
    #id
    # print(mesid(data_1120[4:6]))
    #剔除前28个字节和crc
    del data_1120[0:28]
    del data_1120[-4:]
    pd_1120 = pd.DataFrame(columns = ['SatId','FNAVReceived','INAVReceived','E1BHealth','E5aHealth','E5bHealth','Reserved',
                             'IODa','Weeks','Seconds','Ecc','OmegaDot','Omega0','Omega','M0','Af0','Af1','DeltaRootA','DeltaI'])
    cut_1120 = np.array([4,4,4,1,1,1,1,4,4,4,8,8,8,8,8,8,8,8,8])
    #转成2进制数bin_1120
    bin_1120=[]
    for ind, line in enumerate(data_1120):
        bin_line = '{:08b}'.format(int(line,16))
        bin_1120.append(bin_line)

    for ind, line in enumerate(data_1120):
        list_tmp = []
        for i, ele in enumerate(cut_1120):
            ind_start = sum(cut_1120[0:i])
            ind_end = sum(cut_1120[0:(i+1)])
            if ind_start == 24:
                data_bin= bin_1120[ind_start:ind_end]
                data_bin = ''.join(data_bin)
                data_int = type2int(data_bin,1)
            else:
                data_bin= bin_1120[ind_start:ind_end]
                data_bin = ''.join(data_bin)
                data_int = type2int(data_bin,2)
            list_tmp.append(data_int)
            # print(list_tmp)       
    pd_1120.loc[ind] = np.array(list_tmp)
    # print(pd_1120)
    pd_1120.to_csv('1120.csv')
    return pd_1120
def message1122(data_1122):
    #id
    print(mesid(data_1122[4:6]))
    #剔除前28个字节和crc
    del data_1122[0:28]
    del data_1122[-4:]
    # print(data_1122)

    pd_1122 = pd.DataFrame(columns = ['SatId','FNAVReceived','INAVReceived','E1BHealth','E5aHealth','E5bHealth','E1BDVS','E5aDVS','E5bDVS',
                        'SISA','Reserved','IODNav','T0e','RootA','DeltaN','M0','Ecc','Omega','Cuc','Cus','Crc','Crs','Cic','Cis','I0','IDot','Omega0',
                        'OmegaDot','FNAVT0c','FNAVAf0','FNAVAf1','FNAVAf2','INAVT0c','INAVAf0','INAVAf1','INAVAf2','E1E5aBGD','E1E5bBGD'])
    cut_1122 = np.array([4,4,4,1,1,1,1,1,1,1,1,4,4,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,4,8,8,8,4,8,8,8,8,8])
    #转成2进制数bin_1122
    bin_1122=[]
    for ind, line in enumerate(data_1122):
        bin_line = '{:08b}'.format(int(line,16))
        bin_1122.append(bin_line)

    for ind, line in enumerate(data_1122):
        list_tmp = []
        for i, ele in enumerate(cut_1122):
            ind_start = sum(cut_1122[0:i])
            ind_end = sum(cut_1122[0:(i+1)])

            data_bin= bin_1122[ind_start:ind_end]
            data_bin = ''.join(data_bin)

            data_int = type2int(data_bin,2)
            list_tmp.append(data_int)
            # print(list_tmp)        
    pd_1122.loc[ind] = np.array(list_tmp)
    pd_1122.to_csv('1122.csv')
    return pd_1122
def message1584(data_3006):

    #剔除前28个字节和crc
    del data_3006[0:28]
    del data_3006[-4:]
    # print(data_3006)

    pd_3006 = pd.DataFrame(columns = ['satellite ID','week','toa','RootA','ecc','ω','M0','Ω','0_Ω','δi','a0','a1','health'])


    cut_3006 = np.array([4,4,4,8,8,8,8,8,8,8,8,8,4])
    # print(cut_3006)
    # print(data_3006)

    #转成2进制数bin_3006
    bin_3006=[]
    for ind, line in enumerate(data_3006):
        bin_line = '{:08b}'.format(int(line,16))
        bin_3006.append(bin_line)

    for ind, line in enumerate(data_3006):
        list_tmp = []
        for i, ele in enumerate(cut_3006):
            ind_start = sum(cut_3006[0:i])   
            ind_end = sum(cut_3006[0:(i+1)])
            data_bin= bin_3006[ind_start:ind_end]
            data_bin = ''.join(data_bin)
            data_int = type2int(data_bin,2)
            list_tmp.append(data_int)
            # print(list_tmp)

    pd_3006.loc[ind] = np.array(list_tmp)

    result_3006=pd_3006.to_csv('1584.csv')
    return pd_3006
#不属于这七类的数据
def messagenone(datanone):
    result="does not belong to the message type that requires parsing"
    return result


def Meparse(rawdata):
    # global data_parse

    #判断有几段消息，如果一段，则直接转，如果两段消息，先分段再处理
    data_seg = dataseg(rawdata,'aa44121c')

    for i,ele in enumerate(data_seg):
        data=list(segmented(data_seg[i]))
        if data[4:6]==['8c','00']:
            print("Message Id is 140,the result is:")
            data_parse = message140(data)
        elif data[4:6]==['29','00']:
            print("Message Id is 41,the result is:")
            data_parse = message41(data)
        elif data[4:6]==['49','00']:
            print("Message Id is 73,the result is:")
            data_parse = message73(data)
        elif data[4:6]==['a0','06']:
            print("Message Id is 1696,the result is:")
            data_parse = message1696(data)
        elif data[4:6]==['60','04']:
            print("Message Id is 1120,the result is:")
            data_parse = message1120(data)
        elif data[4:6]==['62','04']:
            print("Message Id is 1122,the result is:")
            data_parse = message1122(data)
        elif data[4:6]==['30','06']:
            print("Message Id is 1584,the result is:")
            data_parse = message1584(data)
        else:
            print("Message Id is none,")
            data_parse = messagenone(data)
    # return'Message Id is 1584,the result is:' 
    return data_parse

if __name__ == "__main__":

    data_3006 = 'aa44121c8c000020d4050000a9b42107a8d19914000000009196c4323e000000049c10188c9903b0541a700b3eff96fca2094a30210200000b3c301117ce02d0b41a700b35dc3ca5d409443041020000043cd0013eb00270c21a700b7ba0afe34009533041030000249c1008a68701005d318a094908c6bb100a93b9a40300002b3c30012d31014075318a09ea11f49d220a2f2ce2020000449c1018df6502a09782560a90c28fb520029d9a640300004b3c301154de0160a582560a0a695fb5840293df40020000649c10187886fa9f5e17080c8665c098f31814b7000200006b3c3011e0bbfb7f8a17080c474171d7f618c43600010000643cd00171e9fb0f8717080c29e02199a018962740020000849c1018710609d08858bc0a220babf2710ccf23a20200008b3c3011590807d0ae58bc0a6a593f81a50c397ac1010000a49c1008b6d30c30db49cd0ae4048ae7300533e021030000ab3c3001bdfe0920f649cd0adb5193f855059014c0010000c49c10189b5cfb8f0ef6250a0ab973d52006e15d87030000cb3c3011c162fc5f50f6250a6efd38ce22062aab04030000c43cd0015a89fcdf60f6250aae3da18510062ff4e5030000049d1008ef3effef74621b0c44f4138cb31749ae000200000b3d30019069ff2f9b621b0c791b91cdd5173cadc0010000249d1018f80ef27f22313e0b0230609d711ce1ffcb0200002b3d3011ee22f58f51313e0b0448c9beb61cc32760010000449d1008484cfc9f6aa8670aaa154caa201162ab8a0300004b3d3001841dfdaf98a8670a9f7d98ac22115dd7e8020000849d1008328ff27f0f5eaf0bae5808d37214bea0670200008b3d3001d886f59f335eaf0b2d6adb84f514eaf886010000049e154846b6fd7f8840df123835739a30c15f7f4c0300000b9e35429737feafb240df12ce7f1ad730c1854e8b030000043ed541974afe3fe340df12440624be20c1577f8c030000e49e1118c896fc0fdbe8a40ac76856e8f5330c5cc1010000eb3eb110d358fd8f21e9a40adc44d1fbf233de0520020000049f1118d4050060b909140a1b0dd1c2313c161d482b00000b3fb110880400e07209140ad81031c2303cf240a02a0000249f111899cc06a005b34e0a1812369c423de2ef012700002b3fb110cd4905505fb34e0ae63e2aa4403d190980260000449f1108c2dff83fc154db09699ff5e6222d33ae443700004b3fb1002575facff954db09b37a4dde302d6a1840370000649f1108922011208d32110bd68b309e6327ba80c00e00006b3fb10039520db0a732110b878d25c260271e4c400f0000849f1108cd72f94f0ac74b0b120070f6633b139ca01200008b3fb1107ee7fa9f12c84b0b36be3aa3603be50a60120000c49f1108470209709632820944337aa52126c1be62230000cb3fb100c6010780eb328209006bed8e3026100420230000e49f11181b5cf36f8c32e30a89c490bba43219b005160000eb3fb100302bf6dfa132e30a338bfed8b0326506e0160000a49e9418d9f2ff6f16bb4e121cdd5e9560054279a3020000a49eb400c1f5ffaf57bb4e12ab380fc950054679a3020000c49e14086343026049244a11056ffdbe3006db2647030000c49e3410fdbf01d0ac244a11205038cc20061c4d60030000e49e940820e9ff7faedb7e11208bac9c50038ed01c030000e49eb41046eeffcf06dc7e1147dbafb11003b88481030000049f14084bc10150286795113ad1ff8d500866f9f3020000049f3400575b01008367951172dd56a620088ba16f030000249f941866e8ff6fafa5c5128cb6f7c7a004d57c63020000249fb410b8edffcfdea5c512c2e8348d9104d27c23020000849f1408224404606b3b8911ad85ec954009d69a24030000849f34107d4c0370c73b89110f1777ac200950f660030000a49f14180d7dfacfe8b81113a8f17296a00a42a040020000a49f3400e8bcfb5f21b911132e65eae6500a977ba0020000e49f9408ace8ff9fdff5ff1160a6a4c87001f2b482020000e49fb4001deeffdf12f6ff1165e4b4f05001e4b4c2020000049c9418cb0100504d25a911d4ae2681900234d8600200000494b400bd0100c07125a9111dfd669cf8023900a0010000f76850ac'
    var = Meparse(data_3006)
    print(var[['PRN','PSR']])
    # a=var['Pseudorange(PSR)/m']
    # print(a)
    # print(type(var))
    
    