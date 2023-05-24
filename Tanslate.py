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

# 默认英译汉
def getParams(text='', sl='en', tl='zh'):
    params = {
        'client': 'gtx',
        'sl': sl,
        'tl': tl,
        'dt': 't',
        'ie': 'utf-8',
        'ue': 'utf-8',
        'q': '{}'.format(urllib.parse.quote(text)),
    }
    return params

cookie = 'CONSENT=YES+US.zh-CN+; _ga=GA1.3.1169692558.1570693086; HSID=AArLJ2jS-7vcjlE5d; SSID=AF8pEKP_pJFRYD0dh; APISID=pj8e7QA9qN5Lyatg/AVhYN0mJU-lOdUxSk; SAPISID=gm7y0DvOiHDKVgBY/AFoLVtPfpWYuGVygF; __Secure-3PAPISID=gm7y0DvOiHDKVgBY/AFoLVtPfpWYuGVygF; S=adwords-usermgmt=UrljsKLhrXFr7Uupeuox0QdECDTQkGOikPmWmW2cOmw; ANID=AHWqTUl3VY5o-Hq4ax09Abw_FQqD3poTAtSwqqu2wUA39sFjD-z7M7qm3g5PuFoO; SEARCH_SAMESITE=CgQIqJAB; OTZ=5561940_24_24__24_; SID=zwe4uML4CzbP0knsuZ1JZs7CQmeyhuTdBWJmUi_fW2zJTqu6vLa__3gyIGFCCH1qtClgXQ.; __Secure-3PSID=zwe4uML4CzbP0knsuZ1JZs7CQmeyhuTdBWJmUi_fW2zJTqu6SK5qWt9xNvM8Q4SVauQx_w.; _gid=GA1.3.1030345690.1597131697; 1P_JAR=2020-8-11-8; NID=204=xGny_iiWfSXkju9vNY5_WqvXLd2iWGUhDoIiqck2jGT6ClMW5TdBN0tHTQrCqa7P2ly2A6SUrejKd8S_FPpcnR7vEgIV-z2Yv8gPENMKu6NGjYxk7wSrZPiRtxPxJ_iNSE0k8Y6AoZ5E3Zv9ge8C9aCHg-L2Y4ya5LQZ4AzEFRIDqFBKsvAx-r0_GZAAQ4q5TjGhzwQRhLVK2pBZ2ibCD21RuQ3BVJjzm8BDWci8TCBMp7EjY8CivmN5QKUD2hoKp1vaNNIqkUSh4eBbx9FGzRoO9Xk3MHCkpB04cHf4skF9u0YPVhDprDZanylcqqzchu0L5zsGoq3lIKvNNl5QcG5U1Npegyg_3JPDMiEQrx3MGksg_AS43H9SOQAsNoqEqGN58S-4Tgt_rFrRQE2NXQWC1N7DXbCRrSnfOQx198w; SIDCC=AJi4QfFkUL8BG6ltnc-_yBREUWl_jZJtUMzv8bZtJ-Mrn3iTaZQEUs0aDTdoPUXRiqnYp991LC7K'

def gen_for_txt(source_name='', target_name='', sl='en', tl='zh'):
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
                        split_strings = source_content.split('=')
                        key = split_strings[0]
                        # 取出数组最后一个值
                        value = split_strings[-1]
#                        print('key -----', key, '/////value -----',value)
                        # 翻译内容
                        res_translate = requests.get(url, params=getParams(value, sl, tl))
                        if res_translate.status_code == 200:
                            decode_result = urllib.parse.unquote(res_translate.text)
#                            print('翻译原始数据-----',decode_result)
                            value = decode_result.split(';')[0].replace('[[[" ','')
                            print('翻译结果 ----', value)
                        else:
                            print('status_code:', res_translate.status_code)
#                        print('key -----', key, '/////value -----',value)
                        line = key + '= ' + value + ';\n'
                        print("写入文件内容 -----" + line)
                        new.write(line)
                    else:
                        new.write(source_content)

# Google翻译 单词语测试
def translate(contents=[], index=0, sl='en', tl='zh'):
    if index >= len(contents):
        return
    content = contents[index]
    if content.__contains__('='):
        split_content  = content.split('=')
        key = split_content[0]
        content = split_content[1]
        print("翻译内容", content)
        res_translate = requests.get(url, params=getParams(content, sl, tl))
        if res_translate.status_code == 200:
            decode_result = urllib.parse.unquote(res_translate.text)
            # 处理带有分号的语句
            if decode_result.__contains__(';'):
                value = decode_result.split(';')[0].replace('[[[" ','')
                print('翻译结果 ----', value)
            # 处理不带有分号的语句
            else:
                value = decode_result.split('",')[0].replace('[[[" ','')
                print('翻译结果 不带有分号 ----', value)
        else:
            print('status_code:', res_translate.status_code)
            translate(contents, index + 1)

    else:
        translate(contents, index + 1)
        
if __name__ == '__main__':
#    translate(['''"en" = "It is currently a mobile network, and the speed test may consume more traffic. Do you want to continue the speed test?"'''], 0, sl='en', tl='fr')
    
    gen_for_txt(source_name='Localizable.strings', target_name="Localizable.strings", sl='en', tl='pt')

    pass




