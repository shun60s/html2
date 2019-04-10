# -*- coding: UTF-8 -*-


#  html 4.01 (Shift_JIS)のTAGを html 5 (UTF-8)向けに変換するため補助ツール。
#　完全には変換してくれないので、変換の前後で手動で修正する必要がある。
#　特に、1行にTAGが重なっていると（例　<meta   <head  <title ... </head   <body)と失敗するので
#　あらかじめ、もとのhtml を1行毎1tag に修正すること。
#  table と td と font と color　と　hrは 不完全な対応
#  <a name の　</a>は行末に移動するため、適時　修正が必要。
#  <body ... は　一律 <body>へ置き換え。必要に応じて、style文の中で属性を定義する。
#  スタイルシートstyle.css の中身を読み込んで <style> ..</style>の間にコピーする。
#  空白行は削除する
#  もとになるhtmlの文字コードはShift_JISを、
#  改行コードはwindows環境（\r\n）を想定している。
#  pythonの動作環境ははwindowsのpython 3.6
# -------------------------------------------------------------------------------
#
#  python3 html2html.py
#
#  もとになるhtml 4.01のファイルをin-dirディレクトリーの中に入れておく。
#  変換したものがout-dirディレクトリーへ出力される。


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
    
    for (i, l) in enumerate(line0):
        # 空行の場合はスキップする
        if len(l.strip()) == 0:
            #print (' zero line')
            continue
        
        if l.find( '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01') >= 0:
            new_line.append( '<!DOCTYPE html>')
            new_line.append( '<html lang="ja">')
            new_line.append( '<head>')
        elif l.find( 'content="text/html; charset=Shift_JIS') >= 0:
            new_line.append( ' <meta http-equiv="content-type" content="text/html; charset=utf-8">')
            new_line.append( ' <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">')
        
        elif l.find('<html>') >=0:
            pass
        elif l.find('<head>') >=0:
            pass
        elif l.find('</head>') >= 0:
            new_line.append('<style>')
            new_line.append('<!--')
            add_style(new_line, style_file)
            new_line.append('-->')
            new_line.append('</style>')
            new_line.append('</head>')
        elif l.find('</body>') >=0:
            new_line.append('<!--')
            new_line.append('This file uses charset utf-8')
            new_line.append('form 2019-xx-xx')
            new_line.append('-->')
            new_line.append(l)
        elif l.find('<body') >= 0:
            new_line.append('<body>')
            # new_line.append(l.lstrip())  # 左寄せする
        else:
            
            l1=copy.copy(l)
            #trans
            if l1.find('<span style="font-style: italic;">') >=0:
                l1= l1.replace( '<span style="font-style: italic;">', '<span class="gletter_i">')
            
            if l1.find('<div style="text-align: center;">') >=0:
                l1=l1.replace( '<div style="text-align: center;">', '<div class="center_1">')
                
            if l1.find('<div style="text-align: right;">') >=0:
                l1=l1.replace( '<div style="text-align: right;">', '<div class="right_1">')
            
            if l1.find('<span style="text-decoration: underline;">') >=0:
                l1=l1.replace( '<span style="text-decoration: underline;">', '<span class="gletter_uline">')
            
            if l1.find('<u>') >=0:
                l1=l1.replace( '<u>', '<span class="gletter_uline">')
            if l1.find('</u>') >=0:
                l1=l1.replace( '</u>', '</span>')
            
            if l1.find('<b>') >=0:
                l1=l1.replace( '<b>', '<span class="gletter_bolder">')
            if l1.find('</b>') >=0:
                l1=l1.replace( '</b>', '</span>')
            if l1.find('<span style="font-weight: bold;">') >=0:
                l1=l1.replace( '<span style="font-weight: bold;">', '<span class="gletter_bolder">')
            
            if l1.find('<strong>') >=0:
                l1=l1.replace( '<strong>', '<span class="gletter_bolder">')
            if l1.find('</strong>') >=0:
                l1=l1.replace( '</strong>', '</span>')
            
            if l1.find('<span style="color: rgb(255, 0, 0);">') >=0:
                l1=l1.replace( '<span style="color: rgb(255, 0, 0);">','<span class="gletter_red">')
            
            if l1.find('<font color="#ff0000">') >=0:   
                l1=l1.replace('<font color="#ff0000">','<span class="gletter_red">')
            
            if l1.find('<font color="#ff0000" size="-1">') >=0:   
                l1=l1.replace('<font color="#ff0000" size="-1">','<span class="gletter_small_red">')
            
            if l1.find('<font color="red" size="-1">') >=0:   
                l1=l1.replace('<font color="red" size="-1">','<span class="gletter_small_red">')
            
            if l1.find('<font color="#ff6666">') >=0:   
                l1=l1.replace('<font color="#ff6666">','<span class="gletter_f6">')
                
            if l1.find('<font color="#3333ff">') >=0:   
                l1=l1.replace('<font color="#3333ff">','<span class="gletter_3f">')
                
            if l1.find('<font color="#330099">') >=0:   
                l1=l1.replace('<font color="#330099">','<span class="gletter_39">')
                
            if l1.find('<font color="#990000">') >=0:   
                l1=l1.replace('<font color="#990000">','<span class="gletter_990">')
                
            if l1.find('<font size="-1">') >=0:   
                l1=l1.replace('<font size="-1">','<span class="gletter_small">')
            
            if l1.find('</font>') >=0:   
                l1=l1.replace('</font>','</span>')
            
            if l1.find('<small>') >=0:  
                l1=l1.replace('<small>','<span class="gletter_small">')
            
            if l1.find('</small>') >=0:   
                l1=l1.replace('</small>','</span>')
                if message_show:
                    print ('* find </small>', i)
            
            if l1.find('<div style="margin-left: 40px;">') >=0:   
                l1=l1.replace('<div style="margin-left: 40px;">','<div class="margin_l40">')   
            
            
            if l1.find('<a name=') >= 0:
                l2=l1.replace('<a name=', '<a id=')
                l3=l2.replace('</a>', '')
                l1=l3.rstrip() + '</a>'
                if message_show:
                    print ('* find <a name tag', i)
            
            # table
            if l1.find('<table') >= 0:
                l1='<table class="width1">'
                if message_show:
                    print ('* find <table .. tag, changed only <table class=..>', i)
                
            if l1.find('<td style="vertical-align: top;">') >= 0:
                l1=l1.replace('<td style="vertical-align: top;">','<td class="top1">')
                
            if l1.find('<td valign="top">') >= 0:
                l1=l1.replace('<td valign="top">','<td class="top1">')
            
            #
            if l1.find('<div align=') >=0:
                if message_show:
                    print ('* find <div align= ', i)
            
            # may bug
            if l1.find('<br style="font-style: italic;">') >= 0:
                l1=l1.replace('<br style="font-style: italic;">','<br>')
                if message_show:
                    print("*warning: <br style... was changed to <br>",i)
                    
            if l1.find('<br style="font-weight: bold;">') >= 0:
                l1=l1.replace('<br style="font-weight: bold;">','<br>')
                if message_show:
                    print("*warning: <br style... was changed to <br>",i)
            
            # at last append l1
            new_line.append(l1)
            
            #*Checker
            # NOINDEX, NOFOLLOW
            if l1.find('content="NOINDEX, NOFOLLOW"') >=0:
                if message_show:
                    print ('* find <meta ... NOINDEX NOFOLLOW', i)
            # color
            if l1.find('color') >= 0:
                print ('* find color .. ', i)
            # <hr ...
            if l1.find('<hr ') >= 0:
                print ('* find <hr .. tag', i)
            # font
            if l1.find('<font') >= 0:
                print ('* find font .. ', i)
            # <td ...
            if l1.find('<td ') >= 0:
            	if l1.find('<td class') < 0:
                    print ('* find <td .. tag', i)
            # <pre ...
            if l1.find('<pre ') >= 0:
                print ('* find <pre .. tag', i)
            # style=
            if l1.find('style=') >= 0:
                print ('* find style= .. tag', i)
            
    
    return new_line

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
    dir_in=".\\in-dir\**"
    # 変更したhtmlの出力ディレクトリー
    dir_out='.\\out-dir\\'
    # 追加のstyle のファイル名
    style_file='style.css'
    
    # 入力となるhtmlのファイル名を取得する
    file_list= get_list(dir_in)
    
    # 出力ディレクトリーが存在しない場合は、作成する
    if not os.path.isdir( dir_out ):
        os.mkdir( dir_out )
    
    #
    for fin in file_list:
    
        # 入力のファイルを読み込む
        f=open(fin, 'r')
        lines0 = f.readlines()
        f.close()
        
        #
        print (' ')
        print ('trans ', fin)
        lines2= del_cr( lines0)
        new_lines0= trans_list( lines2, style_file, message_show=True)
        new_lines2= add_cr( new_lines0)
        
        # 出力ファイルへUTF-8で書き出し 
        fout= dir_out + os.path.basename(fin)
        
        f=codecs.open(fout, 'w','utf-8')
        for list0 in new_lines2:
            f.write(list0) 
        f.close()
        
        # finish  
        print ('write', fout)
        

