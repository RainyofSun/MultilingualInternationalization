#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @Time 11/8/2020 3:27 pm
# @Author Wenqiang
# @File Tanslate.py

import requests
import urllib
import csv

# 翻译参数

url = 'https://translate.googleapis.com/translate_a/single'

headers = {
    'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
}

def getParams(text='', sl='en', tl='fr'):
    params = {
        'client': 'gtx',
        'sl': sl,
        'tl': tl,
        'dt': 't',
        'ie': 'utf-8',
        'ue': 'utf-8',
        'q': '{}'.format(urllib.parse.quote(text)),
#        'q': '{}'.format(urllib.parse.quote(text)),
    }
    return params

cookie = 'CONSENT=YES+US.zh-CN+; _ga=GA1.3.1169692558.1570693086; HSID=AArLJ2jS-7vcjlE5d; SSID=AF8pEKP_pJFRYD0dh; APISID=pj8e7QA9qN5Lyatg/AVhYN0mJU-lOdUxSk; SAPISID=gm7y0DvOiHDKVgBY/AFoLVtPfpWYuGVygF; __Secure-3PAPISID=gm7y0DvOiHDKVgBY/AFoLVtPfpWYuGVygF; S=adwords-usermgmt=UrljsKLhrXFr7Uupeuox0QdECDTQkGOikPmWmW2cOmw; ANID=AHWqTUl3VY5o-Hq4ax09Abw_FQqD3poTAtSwqqu2wUA39sFjD-z7M7qm3g5PuFoO; SEARCH_SAMESITE=CgQIqJAB; OTZ=5561940_24_24__24_; SID=zwe4uML4CzbP0knsuZ1JZs7CQmeyhuTdBWJmUi_fW2zJTqu6vLa__3gyIGFCCH1qtClgXQ.; __Secure-3PSID=zwe4uML4CzbP0knsuZ1JZs7CQmeyhuTdBWJmUi_fW2zJTqu6SK5qWt9xNvM8Q4SVauQx_w.; _gid=GA1.3.1030345690.1597131697; 1P_JAR=2020-8-11-8; NID=204=xGny_iiWfSXkju9vNY5_WqvXLd2iWGUhDoIiqck2jGT6ClMW5TdBN0tHTQrCqa7P2ly2A6SUrejKd8S_FPpcnR7vEgIV-z2Yv8gPENMKu6NGjYxk7wSrZPiRtxPxJ_iNSE0k8Y6AoZ5E3Zv9ge8C9aCHg-L2Y4ya5LQZ4AzEFRIDqFBKsvAx-r0_GZAAQ4q5TjGhzwQRhLVK2pBZ2ibCD21RuQ3BVJjzm8BDWci8TCBMp7EjY8CivmN5QKUD2hoKp1vaNNIqkUSh4eBbx9FGzRoO9Xk3MHCkpB04cHf4skF9u0YPVhDprDZanylcqqzchu0L5zsGoq3lIKvNNl5QcG5U1Npegyg_3JPDMiEQrx3MGksg_AS43H9SOQAsNoqEqGN58S-4Tgt_rFrRQE2NXQWC1N7DXbCRrSnfOQx198w; SIDCC=AJi4QfFkUL8BG6ltnc-_yBREUWl_jZJtUMzv8bZtJ-Mrn3iTaZQEUs0aDTdoPUXRiqnYp991LC7K'

# Google翻译
def translate(contents=[], index=0):
    if index >= len(contents):
        return
    content = contents[index]
    if content.__contains__('='):
        split_content  = content.split('=')
        key = split_content[0]
        content = split_content[1]
        print("翻译内容", content)
        res_translate = requests.get(url, params=getParams(content))
        if res_translate.status_code == 200:
            print("翻译结果 ----" + urllib.parse.unquote(res_translate.text).split(';')[0].replace('[[[" ',''))
            translate(contents, index + 1)
        else:
            print('status_code:', res_translate.status_code)
            translate(contents, index + 1)

    else:
        translate(contents, index + 1)

# print(urllib.parse.quote('我是中国人2.'))

# translate([''' "en" = "英语" '''], 0)

source = '%2522en%2522%253D%2522%25E8%258B%25B1%25E8%25AF%25AD%2522'
target = '%2522en%2522%253D%2522%25E8%258B%25B1%25E8%25AF%25AD%2522'

# print(urllib.parse.unquote(source, 'utf-8'))
# print(urllib.parse.unquote(target, 'utf-8'))

# with open('ins国际化英语.txt', 'r') as strings:
#     lines = strings.readlines()
#     print(lines)
#     translate(contents=lines, index=0)

# 读取文件内容为 "key"="value";
def extract(name=''):
    if len(name) == 0:
        return
    with open(name, mode='r', encoding='utf-8') as en:
        lines = en.readlines()
        with open(name+'.csv', mode='w+', encoding='utf-8') as en_csv:
            csv_write = csv.writer(en_csv)
            for line in lines:
                if line.__contains__('='):
                    content = line.replace('\n', '')
                    index = content.index('=')
                    content = content[index:]
                    content = content.replace('= ', '').replace(';', '').replace('\"', '')
                    csv_write.writerow([content])
    print(name, 'finished')

def extract_for_txt(name=''):
    if len(name) == 0:
        return
    with open(name, mode='r', encoding='utf-8') as en:
        lines = en.readlines()
        with open(name+'-0.txt', mode='w+', encoding='utf-8') as txt:
            for line in lines:
                if line.__contains__('='):
                    content = line.replace('\n', '')
                    index = content.index('=')
                    content = content[index:]
                    content = content.replace('= ', '').replace(';', '').replace('\"', '')
                    txt.write(content)
                    txt.write("\n")
                else:
                    txt.write("\n")
    print(name, 'finished')

# extract(name='ins国际化英语.txt')
# extract(name='Report国际化/意大利语.strings')
# extract(name='Report国际化/法语.strings')

def gen(oldname='', csvname=''):
    with open(csvname + '.txt', mode='w+', encoding='utf-8') as language:
        with open(oldname, mode='r', encoding='utf-8') as old:
            with open(csvname) as csvf:
                old_lines = old.readlines()
                old_new_lines = []
                for old_line in old_lines:
                    if old_line.__contains__('='):
                        old_new_lines.append(old_line)

                csvf_lines = csv.reader(csvf)
                csvf_new_lines = []
                for csvf_line in csvf_lines:
                    csvf_new_lines.append(csvf_line)

                if len(old_new_lines) != len(csvf_new_lines):
                    return
                count = len(old_new_lines)
                for i in range(0, count):
                    old_content = old_new_lines[i]
                    index = old_content.index('=')
                    old_key = old_content[:index]

                    csvf_line = csvf_new_lines[i][0]

                    new_line = str(old_key) + '= \"' + str(csvf_line) + '\";\n'
                    language.write(new_line)
                    print(new_line)

def gen_for_txt(source_name='', target_name=''):
    with open(target_name + '-1.txt', mode='w+', encoding='utf-8') as new:
        with open(source_name, mode='r', encoding='utf-8') as source:
            with open(target_name, mode='r', encoding='utf-8') as target:
                source_new_lines = []
                source_lines = source.readlines()
                
                for line in source_lines:
                    source_new_lines.append(line)

                target_new_lines = []
                target_lines = target.readlines()
                
                for line in target_lines:
                    target_new_lines.append(line)

                if len(source_new_lines) != len(target_new_lines):
                    return
                count = len(source_new_lines)
                for i in range(0, count):
                    source_content = source_new_lines[i]
                    if source_content.__contains__('='):
                        index = source_content.index('=')
                        key = source_content[:index]
                        value = source_content[index:]

                        # 翻译内容
                        res_translate = requests.get(url, params=getParams(value))
                        if res_translate.status_code == 200:
                            value = urllib.parse.unquote(res_translate.text).split(';')[0].replace('[[[','')
                            print("翻译结果 ----" + value)
        
                        else:
                            print('status_code:', res_translate.status_code)
                        
                        line = key + '=' + value + '\";\n'
                        print("写入文件内容 -----" + line)
                        new.write(line)
                    else:
                        new.write(source_content)


if __name__ == '__main__':
    # names = ['alaboyu.csv', 'eyu.csv', 'fayu.csv', 'helanyu.csv', 'yidaliyu.csv']
    # for name in names:
    #     gen(oldname='ins国际化英语.txt', csvname='language/'+name)
    # extract_for_txt(name="Report国际化/Localizable.strings")
#    gen_for_txt(source_name='Localizable.strings', target_name="Localizable.strings")
#    with open('Localizable.strings', 'r') as strings:
#        lines = strings.readlines()
#        print(lines)
#        translate(contents=lines, index=0)
    translate([''' "en" = "It is currently a mobile network, and the speed test may consume more traffic. Do you want to continue the speed test?" '''], 0)

    pass




