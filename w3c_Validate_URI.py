# -*- coding: UTF-8 -*-

# w3c Validate by URIを呼び出し、返信にErrorやWarningがあるファイル名を表示する
#
# python3 w3c_Validate_URI.py
#

import os
import glob   # サブディレクトリの探索に再帰的な glob を使っているため、python 3.5以上が必要
import urllib.request

# Check version 
# python 3.6.4 win32 (64bit) 
# windows 10 (64bit) 



def get_list(dir_in):
    # set filename extension　ファイル拡張子を設定する
    ext0='.html'
    List0=glob.glob(dir_in ,recursive=True)
    List1=[s for s in List0 if s.endswith( ext0 ) ]
    print ('number of files ', len(List1))
    return List1

def make_address(fin, dir_in, host_name):
    # w3c http address
    
    
    w3c_request_address='https://validator.w3.org/nu/?doc=http%3A%2F%2F' + host_name.replace('/','%2F')
    
    # get local top directory name
    top_dirname = os.path.dirname(dir_in.replace(os.path.sep,'/'))
    top_dirname = top_dirname.replace('./','')
    
    f_base=os.path.basename(fin)
    sub_dirname1 = os.path.basename(os.path.dirname(fin))
    # only two layer
    if sub_dirname1 == top_dirname:  # in the top directory (1st layer)
        return w3c_request_address + '%2F' + f_base
    else: # in the following directory (2nd layer)
        return w3c_request_address + '%2F' + sub_dirname1 + '%2F' + f_base


if __name__ == '__main__':
    
    # ローカルのhtmlのTOPディレクトリー
    # 但し、ディレクトリー構造は2階層まで
    dir_in=".\\in-dir\**"
    # クラウド上のホストのアドレスを指定する
    # クラウド上のホストに、ローカルのhtmlと同じものを上げておくこと
    host_name='www.xxx.xxxx.com/test'  # 末尾の/は不要
    
    
    # get html filenames
    file_list= get_list(dir_in)
    
    for fin in file_list:
        #
        w3c_request_address= make_address(fin, dir_in, host_name)
        print ( w3c_request_address )
        
        if 1: # set 0 to see just w3c_request_address
            req = urllib.request.Request(w3c_request_address)
            
            try:
                with urllib.request.urlopen(req) as res:
                    body = res.read()
            except urllib.error.HTTPError as err:
                print('urllib error', err.code)
                break
            except urllib.error.URLError as err:
                print('urllib error', err.reason)
                break
            
            # 下記のエラーまたはワーニングメッセージがあるときにファイル名を表示する
            if body.decode().find('<strong>Error</strong>') >=0 \
             or body.decode().find('<strong>Warning</strong>') >=0:
                 #
                 print ('-found, Error or Warning in ', fin)
        
    print ('')
    print ('Finish.')

