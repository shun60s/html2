# -*- coding: UTF-8 -*-

#
#  html2html2.pyで　一度、html 5 (UTF-8)に変換したものを　更に　変換する。
#  変換する対象が無いときは、新たに書き出さない。
#　追加するスタイルをstyle_append.cssで指定する。
#  pythonの動作環境ははwindowsのpython 3.6
# -------------------------------------------------------------------------------
#
#  python3 html2html2.py
#
#  out-dirディレクトリーの中のものを
#  更に変換してout2-dirディレクトリーに出力する。

import sys
import os
import copy
import glob   # サブディレクトリの探索に再帰的な glob を使っているため、python 3.5以上が必要
import codecs

# Check version 
# python 3.6.4 win32 (64bit) 
# windows 10 (64bit) 


def trans_list( line0 , style_file, message_show=False):
    #
    new_line=[]
    find_style=False
    translated=False
    
    for (i, l) in enumerate(line0):
        # 空行の場合はスキップする
        if len(l.strip()) == 0:
            #print (' zero line')
            continue
        if l.find('<style>') >= 0:
            find_style= True
        
        # <style> 以降で　最初の --> の前に　追加のstyle を追加する
        if l.find('-->') >= 0 and find_style:
            add_style(new_line, style_file)
            new_line.append('-->')
            find_style= False
            
        else:
            
            l1=copy.copy(l)
            #trans
            if l1.find('■') >=0:
                l1= l1.replace( '■', '<span class="gothic1">■</span>')
                translated=True
            
            if l1.find('□') >=0:
                l1= l1.replace( '□', '<span class="gothic1">□</span>')
                translated=True
                
            if l1.find('<small style="font-weight: bold; color: rgb(0, 0, 153);">') >=0:
                l1= l1.replace('<small style="font-weight: bold; color: rgb(0, 0, 153);">', '<span class="gletter_small99">')
                translated=True
            
            # at last append l1
            new_line.append(l1)
            
            #*Checker
            
    
    return new_line, translated

def add_style( list0, f_style):
    # スタイルを読み込む
    f=open(f_style, 'r')
    style_lines0 = f.readlines()
    f.close()
    
    style_lines2= del_cr( style_lines0)
    # スタイルをリストに追加する
    for l in style_lines2:
    	list0.append(l)


def get_list(dir_in):
    # ファイル拡張子
    ext0='.html'
    List0=glob.glob(dir_in ,recursive=True)
    List1=[s for s in List0 if s.endswith( ext0 ) and not s.startswith(dir_out) ]
    print ('number of files ', len(List1))
    return List1

def del_cr(listx0):
    listx1=[]
    for list0 in listx0:
        # 改行を削除する \r \n
        listx=list0.replace('\r','')
        listx=listx.replace('\n','')
        listx1.append(listx)
    return listx1

def add_cr(listx0):
    listx1=[]
    for list0 in listx0:
        # 改行コードを追加する
        listx=list0 +'\r'+'\n'
        listx1.append(listx)
    return listx1


if __name__ == '__main__':
    
    # もとになるhtmlの入力ディレクトリー
    dir_in=".\\out-dir\**"
    # 変更したhtmlの出力ディレクトリー
    dir_out='.\\out2-dir\\'
    # 追加のstyle のファイル名
    style_file='style_append.css'
    
    # 入力となるhtmlのファイル名を取得する
    file_list= get_list(dir_in)
    
    # 出力ディレクトリーが存在しない場合は、作成する
    if not os.path.isdir( dir_out ):
        os.mkdir( dir_out )
    
    #
    for fin in file_list:
    
        # 入力のファイルを読み込む
        f=codecs.open(fin, 'r','utf-8')
        lines0 = f.readlines()
        f.close()
        
        #
        print (' ')
        print ('trans ', fin)
        lines2= del_cr( lines0)
        new_lines0, translated= trans_list( lines2, style_file, message_show=False)
        new_lines2= add_cr( new_lines0)
        
        # 変更されたファイルのみ書き出す
        if translated:
            # 出力ファイルへUTF-8で書き出し 
            fout= dir_out + os.path.basename(fin)
            
            f=codecs.open(fout, 'w','utf-8')
            for list0 in new_lines2:
                f.write(list0) 
            f.close()
            
            # finish  
            print ('write', fout)
        else:
            print ('no translated, no write')

