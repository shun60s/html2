# -*- coding: UTF-8 -*-

#  <a タグと　<img タグのリンク先を表示する
#
#  htmlファイルをin-dirディレクトリーの中に入れておく。
#
#  python3 h2p_show_link.py
#

import os
import codecs
import glob   # サブディレクトリの探索に再帰的な glob を使っているため、python 
from html_parser1 import *
from h2h_sub1 import *

# Check version 
# python 3.6.4 win32 (64bit) 
# windows 10 (64bit) 



def show0( dic, tag0='a'):
    #
    list0=dic[tag0]
    if len(list0) > 0:
        for t in list0:
            print (t[0][1]) 


def get_list(dir_in):
    # set filename extension　ファイル拡張子を設定する
    ext0='.html'
    List0=glob.glob(dir_in ,recursive=True)
    List1=[s for s in List0 if s.endswith( ext0 ) ]
    print ('number of files ', len(List1))
    return List1


if __name__ == '__main__':

    # ローカルのhtmlのTOPディレクトリー
    dir_in=".\\in-dir\**"
    
    # 入力となるhtmlのファイル名を取得する
    file_list= get_list(dir_in)
    
    #
    for fin in file_list:
        if 1: # set 1 , if show input file name
            print ('processing --> ', fin)
    	
    	# 入力のファイルを読み込む
        
        if 1:  # set 1, if html charset is utf-8
            f=codecs.open(fin, 'r','utf-8')
            text1 = f.read()
            f.close()
        else:  # other, charset shift-jis when windows
            f=open(fin, 'r')
            text1 = f.read()
            f.close()
        
        parser1 = Class_TestParser1()
        parser1.feed( text1 )
        
        # 表示する
        show0( parser1.dic, tag0='a' )
        show0( parser1.dic, tag0='img' )
        
        # Class_TestParser1クラスを閉じる
        parser1.close()
        

        
    print ('')
    print ('Finish.')
