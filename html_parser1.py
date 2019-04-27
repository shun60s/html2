# -*- coding: UTF-8 -*-

# make a dictionary of html tag elements by use python's HTML Parser

from html.parser import HTMLParser
import copy
import re

# Check version 
# python 3.6.4 win32 (64bit) 
# windows 10 (64bit) 


class Class_TestParser1(HTMLParser):
    
    def __init__(self, ):
        super().__init__()  # 元のクラスの初期化
        self.title_flag=False
        self.a_link=None
        self.a_vlink=None
        self.a_alink=None
        self.dic={}
        self.list_font=[]
        self.list_div =[]
        self.list_table =[]
        self.list_td =[]
        self.list_hr =[]
        self.list_br =[]
        self.list_name =[]
        self.list_id = []
        self.list_span =[]
        self.list_meta =[]
        self.list_a =[]
        self.list_img =[]
        self.list_misc= []
        
        self.dic['font']  = self.list_font
        self.dic['div']   = self.list_div
        self.dic['table'] = self.list_table
        self.dic['td']    = self.list_td
        self.dic['hr']    = self.list_hr
        self.dic['br']    = self.list_br
        self.dic['name']  = self.list_name
        self.dic['id']    = self.list_id
        self.dic['span']  = self.list_span
        self.dic['meta']  = self.list_meta
        self.dic['a']     = self.list_a
        self.dic['img']   = self.list_img
        self.dic['misc']  = self.list_misc
        
        
    def handle_starttag(self, tag, attrs):
        #print("START  :", tag, attrs)
        if tag == 'title':
            #print ('start title')
            #print ( self.getpos())
            self.title_flag=True
        elif tag== 'body':
            self.dic['body']= attrs
            #self.body_pos= self.getpos()
        elif tag == 'font':
            if attrs not in self.list_font:
                self.list_font.append( attrs )
        elif tag == 'div':
            if attrs not in self.list_div:
                self.list_div.append( attrs )
        elif tag == 'table':
            if attrs not in self.list_table:
                self.list_table.append( attrs )
        elif tag == 'td':
            if attrs not in self.list_td:
                self.list_td.append( attrs )
        elif tag == 'hr':
            if attrs not in self.list_hr:
                self.list_hr.append( attrs )
        elif tag == 'br':
            if attrs not in self.list_br:
                self.list_br.append( attrs )
        elif tag == 'name':
            if attrs not in self.list_name:
                self.list_name.append( attrs )
        elif tag == 'id':
            if attrs not in self.list_id:
                self.list_id.append( attrs )
        elif tag == 'span':
            if attrs not in self.list_span:
                self.list_span.append( attrs )
        elif tag == 'meta':
            if attrs not in self.list_meta:
                self.list_meta.append( attrs )
        elif tag == 'a':
            if attrs not in self.list_a:
                self.list_a.append( attrs )
        elif tag == 'img':
           if attrs not in self.list_img:
                self.list_img.append( attrs )
        else:  # misc これだけ tagが入っている
            if tag not in self.list_misc:
                self.list_misc.append( tag )

    def handle_endtag(self, tag):
        #print("END    :", tag)
        if tag == 'title':
            self.title_flag=False
    
    def handle_data(self, data):
        if self.title_flag:
            #print("DATA   :", data)
            self.dic['title']= data
    
    def get_title(self,):
        return copy.copy(self.dic['title'])
    
    def trans_hex(self, in_str):
        # pick up digits
        l2= re.findall( r'[0-9]+', in_str)
        if len(l2) >= 3:  # rgb
            r=format(int(l2[0]), 'x')
            g=format(int(l2[1]), 'x')
            b=format(int(l2[2]), 'x')
            return '#'+r+g+b
        else:
            print ('error: at trans_hex', l2)
            return  None 
    
    def get_body_bcolor(self,):
        b=self.dic['body']
        for list0 in b:
            if str(list0).find('background-color') >= 0:
                l2=list0[1][list0[1].find('background-color'):]
                return self.trans_hex(l2)
                
            if str(list0).find('bgcolor') >= 0:
                l2=list0[1]
                return list0[1]
                
        return None
        
    def get_body_link(self,):
        b=self.dic['body']
        
        for list0 in b:
            if str(list0).find("'link'") >= 0:
                if list0[1][0] == '#':
                    self.a_link=list0[1]
                else:
                    self.a_link= self.trans_hex(list0[1])
            	    
            elif str(list0).find("'vlink'") >= 0:
                if list0[1][0] == '#':
                    self.a_vlink=list0[1]
                else:
                    self.a_vlink= self.trans_hex(list0[1])
            elif str(list0).find("'alink'") >= 0:
                if list0[1][0] == '#':
                    self.a_alink=list0[1]
                else:
                    self.a_alink= self.trans_hex(list0[1])
        
        return [self.a_link, self.a_vlink, self.a_alink]
        
    def get_meta(self,):
        b=self.dic['meta']
        add_meta=[]
        for list0 in b:
            if str(list0[0]).find('ROBOTS') >= 0:
                add_meta.append('<meta name="ROBOTS" content="NOINDEX, NOFOLLOW">')
        
        return add_meta