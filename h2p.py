# -*- coding: UTF-8 -*-

#  pythonのHTMLParserを利用して
#  html 4.01 (Shift_JIS)のTAGを html 5 (UTF-8)向けに変換するため補助ツール。
#
#　完全には変換してくれないので、変換の前後で手動で修正する必要がある。
#  特に、tableは手修正が必須。
#  TAGの<と>も間に改行があると変換されない。
#
#  <a nameは　単に、 <a idに置き換えてある。
#  必要に応じて、meta 文を　head内に　手動で追加すること。
#  空白行は削除する
#  もとになるhtmlの文字コードはShift_JISを想定している。
#  改行コードはwindows環境（\r\n）を想定している。
#  pythonの動作環境ははwindowsのpython 3.6
# -------------------------------------------------------------------------------
#
#  python3 h2p.py
#
#  もとになるhtml 4.01のファイルをin-dirディレクトリーの中に入れておく。
#  in-dirの下位のサブディレクトリーは1階層まで。
#  変換したものがout-dirディレクトリーへ出力される。
#
#  追加のstyle ファイルの内容を　head内に追加する。


import os
import codecs
import glob   # サブディレクトリの探索に再帰的な glob を使っているため、python 
from html_parser1 import *
from h2h_sub1 import *

# Check version 
# python 3.6.4 win32 (64bit) 
# windows 10 (64bit) 

class Class_header(object):
    def __init__(self, ):
        self.h_lines=[]
        self.h_lines.append( '<!DOCTYPE html>')
        self.h_lines.append( '<html lang="ja">')
        self.h_lines.append( '<head>')
        self.h_lines.append( ' <meta http-equiv="content-type" content="text/html; charset=utf-8">')
        self.h_lines.append( ' <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">')
        self.h_lines.append( '</head>')
        
        
    def add_title(self, title):
        # insert title
        t0= ' <title>' + title + '</title>'
        self.h_lines.insert( self.get_index( '</head>'), t0)
        
    
    def add_meta(self, meta):
        if len(meta) > 0:
            id=self.get_index( '<title>')
            for i,l in enumerate( meta ):
                self.h_lines.insert( id+i, ' ' + l)
        
    def get_index(self, text):
        # return the index of text 
        for i in range( len( self.h_lines)):
            if self.h_lines[i].find( text ) >= 0:
                head_index=i
                break
        return head_index
        
    def add_body_style(self, bcolor):
        # insert 
        if bcolor is not None:
            id= self.get_index( '-->')
            self.h_lines.insert( id, 'body {')
            t0= '    background-color: ' + bcolor + ';'
            self.h_lines.insert( id+1, t0)
            self.h_lines.insert( id+2, '}')

    def add_link_style(self, links):
        a_link=links[0]
        a_vlink=links[1]
        a_alink=links[2]
        # insert 
        if a_link is not None:
            id= self.get_index( '-->')
            t0= 'a:link { color: '  + a_link + '; }'
            self.h_lines.insert( id, t0)
        if a_vlink is not None:
            id= self.get_index( '-->')
            t0= 'a:visited { color: '  + a_vlink + '; }'
            self.h_lines.insert( id, t0)
        if a_alink is not None:
            id= self.get_index( '-->')
            t0= 'a:active { color: '  + a_alink + '; }'
            self.h_lines.insert( id, t0)

    def add_style(self, f_style):
    	# 
    	if os.path.exists( f_style):
            # スタイルを読み込む
            f=open(f_style, 'r')
            style_lines0 = f.readlines()
            f.close()
            
            style_lines2= del_cr( style_lines0)
            #
            id= self.get_index( '</head>')
            self.h_lines.insert( id, '<style>')
            self.h_lines.insert( id+1, '<!--')
            c0=id+2
            # スタイルをリストに追加する
            for i,l in enumerate(style_lines2):
    	        self.h_lines.insert( c0, l)
    	        c0 +=1
    	    #
            self.h_lines.insert( c0, '-->')
            self.h_lines.insert( c0+1, '</style>')
    

# helper function
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

def get_list(dir_in):
    # set filename extension　ファイル拡張子を設定する
    ext0='.html'
    List0=glob.glob(dir_in ,recursive=True)
    List1=[s for s in List0 if s.endswith( ext0 ) ]
    print ('number of files ', len(List1))
    return List1

def get_outfilename(dir_out, fin, dir_in):
	# return output filename
	
	# get local top directory name of dir_in
    top_dirname = os.path.dirname(dir_in.replace(os.path.sep,'/'))
    top_dirname = top_dirname.replace('./','')
	
    # create new directory if not exist
    if not os.path.isdir( dir_out ):
        os.mkdir( dir_out )
    
    # 2階層まで
    f_base=os.path.basename(fin)
    sub_dirname1 = os.path.basename(os.path.dirname(fin))
    
    if sub_dirname1 == top_dirname:
        fout= os.path.join(dir_out, f_base)
    else:
        dir1 = os.path.join(dir_out, sub_dirname1)
        # create new directory if not exist
        if not os.path.isdir( dir1 ):
            os.mkdir( dir1 )
        fout = os.path.join(dir1, f_base)
    
    return fout

def get_body_portion( text ):
    # return body contents portion
    id_body_start= text.find('<body')
    id_body_end= text[id_body_start:].find('>')
    id_body_end2= text.find('</body')
    # print ( text[id_body_start:id_body_start+id_body_end+1] )
    return text[id_body_start+id_body_end+2:id_body_end2]
    

def add_body_tag( line0):
    line0.insert(0,'<body>')
    line0.append('<!--')
    line0.append('This file uses UTF-8')
    line0.append('from 2019-4-19')
    line0.append('-->')
    line0.append('</body>')
    line0.append('</html>')

if __name__ == '__main__':

    # ローカルのhtmlのTOPディレクトリー
    # 但し、ディレクトリー構造は2階層まで
    dir_in=".\\in-dir\**"
    # 変更したhtmlの出力ディレクトリー
    dir_out='.\\out-dir\\'
    # 追加のstyle のファイル名
    style_file='style2.css'
    
    
    # 入力となるhtmlのファイル名を取得する
    file_list= get_list(dir_in)
    
    #
    for fin in file_list:
        print ('processing --> ', fin)
        # （ステップ１）　タイトルと背景色を読み込み、ヘッダ部分を作成する
    	# 入力のファイルを読み込む
        f=open(fin, 'r')
        text1 = f.read()
        f.close()
        
        #text = codecs.open(fin, 'r','utf-8').read()
        
        parser1 = Class_TestParser1()
        parser1.feed( text1 )
        
        # instance
        head0= Class_header()
        
        # make header
        head0.add_title(parser1.get_title())
        head0.add_style(style_file)
        head0.add_body_style( parser1.get_body_bcolor())
        head0.add_link_style( parser1.get_body_link())
        head0.add_meta( parser1.get_meta())
        
        # get body portion
        btext1= get_body_portion(text1)
        btext2= trans_str( btext1)
        body_lines1 = btext2.splitlines() # no cr code
        add_body_tag( body_lines1 )
        
        
        # Class_TestParser1クラスを閉じる
        parser1.close()
        
        # 出力ファイルへUTF-8で書き出し 
        fout= get_outfilename(dir_out, fin, dir_in)
        f=codecs.open(fout, 'w','utf-8')
        
        new_lines2= add_cr( head0.h_lines + body_lines1)
        for list0 in new_lines2:
            # 空行の場合はスキップする
            if len(list0.strip()) == 0:
                continue
            f.write(list0)
        
        f.close()
        
    print ('')
    print ('Finish.')
