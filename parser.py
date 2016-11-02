#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
from bs4 import BeautifulSoup
import requests

import db_init

class Parser:

    links = {}
    tables = {}
    log = None
    
    def parse_url(self, url, suffix):
        html = requests.get(url)
        html.encoding = 'ISO-8859-7'
        soup = BeautifulSoup(html.content, 'html.parser')
    
        # fix .html suffixes in middle of url
        url = self.fix_url(url, suffix)
    
        tags = soup('a')
        for tag in tags:
            href = tag.get('href')
            if not re.match('index\d+\.html', href):        # end 2016
                link_url = self.create_url(url, href)
                self.parse_link(link_url, tag, suffix)


    def parse_link(self, url, tag, suffix):
    
        # (entirely useless) fix // in middle of url
        url = re.sub(r'^((?:(?!//).)*//(?:(?!//).)*)//', r'\1/', url)
    
        if (url.endswith('xls') or (url.endswith('.html') and 'index' not in url)):
            filename = url.rsplit('/')[-1]
            msg = 'Found table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
            
            self.download_table(url, suffix)
            
            self.tables[len(self.tables)+1] = url
            self.log.write(msg)
        
        elif url.endswith('gz'):
            filename = url.rsplit('/')[-1]
            msg = 'Found gz table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
            self.tables[len(self.tables)+1] = url
            self.log.write(msg)
    
        elif ('index' in url and 'old' not in url) or url.endswith('/'):
            msg = '------------------\nFound link: ' + url + ' ' + str(tag.contents) + '\n'
            self.log.write(msg)
            self.links[len(self.links)+1] = url
            if url == 'http://e-aitisi.sch.gr/triantamino_07/index.html':
                self.log.write('Crazy 2007 link to 2016 index\n')
            elif url == 'http://e-aitisi.sch.gr/eniaios_smea_orom_11_B/index.html':
                self.log.write('Crazy 2011 link to 2013 index\n')
            else:
                self.parse_url(url, suffix)
    
        else:
            msg = '--Not xls, html, or gz ' + url + ' ' + str(tag.contents) + '\n'
            self.log.write(msg)


    def create_url(self, url, href):
        if url.endswith('/index.html'):
            url = url[:-11]
        return url + '/' + href

    def fix_url(self, url, suffix):
        if suffix in url:       # initial index,html
            list = url.split(suffix)
            url = ''.join(list)
    
        rogue_suffixes = ['/indexAB.html', '/indexC.html', '/indexG.html',
                               '/indexABg.html', '/indexCg.html', '/indexGg.html']
        if any(x in url for x in rogue_suffixes):       # 2003-4
            splitter = re.search('/index.+?\.html', url).group(0)
            list = url.split(splitter)
            url = ''.join(list)
        if '-index.html' in url:        # ~2010 tadmon(TAD/ETAD)
            splitter = re.search('/\d?\D+\d?\D*-index.html', url).group(0)
            list = url.split(splitter)
            url = ''.join(list)
        if '_13/indexdior.html' in url:     # 2013
            splitter = re.search('/indexdior.html', url).group(0)
            list = url.split(splitter)
            url = ''.join(list)
    
        return url
    
    def download_table(self, url, suffix):
        filename = url.rsplit('/')[-1]
        path_pinaka = url[22:][:-len(filename)]     # len('http://e-aitisi.sch.gr') == 22
        if path_pinaka.rsplit('/')[-2].isdigit():      # date in path pinaka
            hmeromhnia = path_pinaka.rsplit('/')[-2]
            print(hmeromhnia)
        
        kathgoria = path_pinaka.split('/')[1]
        kathgoria = self.find_kathgoria(kathgoria)
        
        eidikothta = filename[:-4]
        year = suffix[6:][:-5]
        sxoliko_etos = year + '-' + str(int(year) + 1)
        
        full_path = 'data' + '/' + sxoliko_etos + path_pinaka
        
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path)
            except OSError as exc: # Guard against race condition (me: ??)
                if exc.errno != errno.EEXIST:
                    raise
        
        if not os.path.isfile(full_path + filename):
            response = requests.get(url)
            with open(full_path + filename, 'wb') as output:
                output.write(response.content)
            print('Downloaded')
        else: 
            print('Already there')      
            
        print(filename, path_pinaka, kathgoria, eidikothta, path_pinaka.rsplit('/')[-1])
    
        
    def find_kathgoria(self, kathgoria):
        
        # pinakes diorismwn
        if kathgoria.startswith('eniaios_diorismwn') or kathgoria.startswith('eniaioidior_13'):
            kathgoria = 'eniaios_diorismwn'
        elif kathgoria.startswith('triantamino'):
            kathgoria = 'triantamino'
        elif kathgoria.startswith('eikositetramino'):
            kathgoria = 'eikositetramino'
            
        # diorismoi eidikh kathgoria
        elif kathgoria.startswith('specialcat'):
            kathgoria = diorismwn_eidikh_kathgoria
            
        # eniaioi a/b-thmias
        elif kathgoria.startswith('eniaiosp'):
            if kathgoria.startswith('eniaiosp_zero'):
                kathgoria = 'eniaios_protovathmias_mhdenikhs_proyphresias'
            else: kathgoria = 'eniaios_protovathmias'
        elif kathgoria.startswith('eniaiosd'):
            if kathgoria.startswith('eniaiosd_zero'):
                kathgoria = 'eniaios_defterovathmias_mhdenikhs_proyphresias'
            else: 
                kathgoria = 'eniaios_defterovathmias'
            
        # oloimera-oromisthioi
        elif kathgoria.startswith('oloimera'):
            kathgoria = 'oromisthioi_oloimera'
        elif (kathgoria == 'eniaios_oromis8iwn_05_zero'):
            kathgoria = 'oromisthioi_defterovathmias_mhdenikhs_proyphresias'
        elif kathgoria.startswith('eniaios_oromis8iwn') or kathgoria.startswith('oromisthioi'):
            kathgoria = 'oromisthioi_defterovathmias'
        
        # mousika   
        elif kathgoria.startswith('mousika'):
            if kathgoria.startswith('mousika_orom'):
                kathgoria = 'mousika_sxoleia_oromisthioi'
            else: 
                kathgoria = 'mousika_sxoleia'
        
        # smea
        elif 'smea' in kathgoria:
            if kathgoria.startswith('eniaios_smea_oloim'):
                kathgoria = 'smea_oloimera'
            elif kathgoria.startswith('eniaios_smea_anap'):
                kathgoria = 'smea_anaplirotes'
            else: 
                kathgoria = 'smea_oromisthioi'
        
        # politeknoi 2009
        elif kathgoria == 'politeknoi2009':
            kathgoria == 'politeknoi2009'
        
        # tad/ead
        elif kathgoria.startswith('tad'):
            if kathgoria.startswith('tadmon'):
                kathgoria = 'tad_ead_monimoi'
            if kathgoria.startswith('tadanap'):
                kathgoria = 'tad_ead_anaplirotes'
            else:
                kathgoria = 'tad_ead_oromisthioi'
        
        # diagrafentes logw mh analhpshs yphresias
        elif kathgoria.startswith('diagrafentes'):
            kathgoria = 'diagrafentes_logw_mh_analhpshs_yphresias'
        
        # diagrafentes logw apolyshs
        elif kathgoria.startswith('kataggelia'):
            kathgoria = 'diagrafentes_logw_apolyshs'
            
        # meinotika thrakhs
        elif kathgoria.startswith('pe73'):
            kathgoria = 'meionotika_thrakhs'
            
        # meinotika thrakhs
        elif kathgoria.startswith('avlonas'):
            kathgoria = '2o_gymnasio_avlwna'
            
        return kathgoria
                
            
                         
    



