# -*- coding: UTF-8 -*-

# transform function for h2p.py
#

import sys
import os
import re
import copy



# Check version 
# python 3.6.4 win32 (64bit) 
# windows 10 (64bit) 


def trans_str( text0):
    l1=copy.copy(text0)
    
    # 一律　置き換えするもの
    l1=l1.replace('<small>','<span class="gletter_small">')
    l1=l1.replace('</small>','</span>')
    l1=l1.replace('<font size="-1">','<span class="gletter_small">')
    l1=l1.replace('<font size=-1>','<span class="gletter_small">')
    l1=l1.replace('<font size="+1">','<span class="gletter_large">')
    l1=l1.replace('<font size="+2">','<span class="gletter_xlarge">')
    l1=l1.replace( '<b>', '<span class="gletter_bolder">')
    l1=l1.replace( '</b>', '</span>')
    l1=l1.replace( '<i>', '<span class="gletter_i">')
    l1=l1.replace( '</i>', '</span>')
    l1=l1.replace( '<u>', '<span class="gletter_uline">')
    l1=l1.replace( '</u>', '</span>')
    l1=l1.replace( '<strong>', '<span class="gletter_bolder">')
    l1=l1.replace( '</strong>', '</span>')
    l1=l1.replace('<center>','<div class="center_1">')
    l1=l1.replace('</center>', '</div>')
    l1=l1.replace( '<div style="text-align: right;">', '<div class="right_1">')
    l1=l1.replace( '<div align="right">', '<div class="right_1">')
    l1=l1.replace( '<div align=right>', '<div class="right_1">')
    l1=l1.replace( '<div align="left">', '<div class="left_1">')
    l1=l1.replace( '<div style="text-align: center;">', '<div class="center_1">')
    l1=l1.replace( '<div align="center">', '<div class="center_1">')
    l1=l1.replace('</font>','</span>')
    l1=l1.replace('<a name=', '<a id=')  # name 側だけ変更　</a>はそのままにしてある。
    l1=l1.replace('<td valign="top">','<td class="line1">')  # 一律　枠付きで変更しているので、適時、修正が必要。
    
    l2=trans_font_color(l1)
    l3=trans_hr(l2)
    l4=trans_br(l3)
    l5=trans_table(l4)
    l6=trans_center(l5)
    l7=trans_img_border(l6)
    
    check_font(l7)
    check_javascript(l7)
    check_small(l7)
    
    return l7
    

def trans_font_color( text0 ):
    l1=copy.copy(text0)
    
    while l1.find('<font color=') >= 0:
        id_start =l1.find('<font color=')
        id_end = l1[id_start:].find('>')
        color_code= re.findall( r'[a-xA-Z0-9]+', l1[id_start: id_start+id_end+1])
        #print (color_code)
        t0= '<span style="color: #' + color_code[2] + ';">'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
    
    
    while l1.find('<font size="-1" style=' ) >= 0:
        id_start =l1.find('<font size="-1" style=')
        id_end = l1[id_start:].find('>')
        t0= '<span' + l1[id_start+15: id_start+id_end-1] + ' font-size: small;">'
        #print(t0)
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
    
    while l1.find('<font size="-1" color=' ) >= 0:
        id_start =l1.find('<font size="-1" color=')
        id_end = l1[id_start:].find('>')
        t0= '<span style="color: ' + l1[id_start+23: id_start+id_end-1] + '; font-size: small;">'
        #print(t0)
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
    
    
    return l1



def trans_hr( text0 ):
    l1=copy.copy(text0)
    
    while l1.find('<hr ') >= 0:
        id_start =l1.find('<hr ')
        id_end = l1[id_start:].find('>')
        t0= '<hr>'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
    
    return l1
    

def trans_br( text0 ):
    l1=copy.copy(text0)
    
    while l1.find('<br ') >= 0:
        id_start =l1.find('<br ')
        id_end = l1[id_start:].find('>')
        t0= '<br>'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
    
    return l1


def trans_table( text0 ):
    l1=copy.copy(text0)
    
    while l1.find('<table border') >= 0:
        id_start =l1.find('<table border')
        id_end = l1[id_start:].find('>')
        t0= '<table class="width1">'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
        print (' found table--- please modify by manual.')
    
    while l1.find('<table cellpadding="2" cellspacing="2"') >= 0:
        id_start =l1.find('<table cellpadding="2" cellspacing="2"')
        id_end = l1[id_start:].find('>')
        t0= '<table class="kind1">'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
        print (' found table--- please modify by manual.')
    
    return l1


def trans_center( text0 ):
    l1=copy.copy(text0)
    
    while l1.find('<center ') >= 0:
        id_start =l1.find('<center ')
        id_end = l1[id_start:].find('>')
        t0= '<div class="center_1">'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
    
    return l1

def trans_img_border( text0 ):
    l1=copy.copy(text0)
    
    c0=0
    while l1[c0:].find('<img ') >= 0:
        id_start =l1[c0:].find('<img ')
        id_end = l1[c0+id_start:].find('>')
        t0=copy.copy( l1[c0+id_start: c0+id_start+id_end+1])
        t0=t0.replace(' border="0"','',1)
        #print (t0)
        l1=l1[:c0] + l1[c0:].replace(l1[c0+id_start: c0+id_start+id_end+1], t0,1)
        c0=c0+id_start+1
    
    return l1



def check_font( text0):
    l1=copy.copy(text0)
    
    while l1.find('<font') >= 0:
        id_start =l1.find('<font')
        id_end = l1[id_start:].find('>')
        print (' found font ', l1[id_start: id_start+id_end+1])
        t0='<checked>'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
        
def check_javascript( text0 ):
    
    if text0.find( 'javascript') >= 0:
        print (' found javascript--- please modify by manual.')

def check_small( text0):
    l1=copy.copy(text0)
    
    while l1.find('<small') >= 0:
        id_start =l1.find('<small')
        id_end = l1[id_start:].find('>')
        print (' found small ', l1[id_start: id_start+id_end+1])
        t0='<checked>'
        l1=l1.replace(l1[id_start: id_start+id_end+1], t0,1)
