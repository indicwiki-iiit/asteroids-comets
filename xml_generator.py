import json, pandas, random
from hashlib import sha1
from jinja2 import Environment, FileSystemLoader
import string
from datetime import datetime
import pandas as pd

tewiki = '''<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="te">
	<siteinfo>
		<sitename>tewiki</sitename>
		<dbname>indicwiki</dbname>
		<base>https://tewiki.iiit.ac.in/index.php/%E0%B0%AE%E0%B1%8A%E0%B0%A6%E0%B0%9F%E0%B0%BF_%E0%B0%AA%E0%B1%87%E0%B0%9C%E0%B1%80</base>
		<generator>MediaWiki 1.34.0</generator>
		<case>first-letter</case>
		<namespaces>
			<namespace key="-2" case="first-letter">మీడియా</namespace>
			<namespace key="-1" case="first-letter">ప్రత్యేక</namespace>
			<namespace key="0" case="first-letter" />
			<namespace key="1" case="first-letter">చర్చ</namespace>
			<namespace key="2" case="first-letter">వాడుకరి</namespace>
			<namespace key="3" case="first-letter">వాడుకరి చర్చ</namespace>
			<namespace key="4" case="first-letter">Project</namespace>
			<namespace key="5" case="first-letter">Project చర్చ</namespace>
			<namespace key="6" case="first-letter">దస్త్రం</namespace>
			<namespace key="7" case="first-letter">దస్త్రంపై చర్చ</namespace>
			<namespace key="8" case="first-letter">మీడియావికీ</namespace>
			<namespace key="9" case="first-letter">మీడియావికీ చర్చ</namespace>
			<namespace key="10" case="first-letter">మూస</namespace>
			<namespace key="11" case="first-letter">మూస చర్చ</namespace>
			<namespace key="12" case="first-letter">సహాయం</namespace>
			<namespace key="13" case="first-letter">సహాయం చర్చ</namespace>
			<namespace key="14" case="first-letter">వర్గం</namespace>
			<namespace key="15" case="first-letter">వర్గం చర్చ</namespace>
			<namespace key="828" case="first-letter">మాడ్యూల్</namespace>
			<namespace key="829" case="first-letter">మాడ్యూల్ చర్చ</namespace>
			<namespace key="2300" case="first-letter">Gadget</namespace>
			<namespace key="2301" case="first-letter">Gadget talk</namespace>
			<namespace key="2302" case="case-sensitive">Gadget definition</namespace>
			<namespace key="2303" case="case-sensitive">Gadget definition talk</namespace>
			<namespace key="2600" case="first-letter">Topic</namespace>
		</namespaces>
	</siteinfo>'''

page_id = 400001
user_id = '61' #not assigned to me yet - need to change this (?)
username = 'Valalithak'#change this also

def sha36(page_id):
	page_id = str(page_id).encode('utf-8')
	sha16 =sha1(page_id).hexdigest()
	sha10 =int(sha16, 16)

	chars =[]
	alphabets = string.digits +string.ascii_lowercase
	while sha10>0:
		sha10, r = divmod(sha10, 36)
		chars.append(alphabets[r])
	
	return ''.join(reversed(chars)) 

def addPage(title, wikiText):
	global user_id, username
	pglen = len(wikiText)
	title = title.replace('&','అండ్')
	time =datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
	page = '''\n\n
	<page>
		<title>'''+title+'''</title>
		<ns>0</ns>
		<id>'''+str(page_id)+'''</id>
		<revision>
			<id>'''+str(page_id)+'''</id>
			<timestamp>'''+time+'''</timestamp>
			<contributor>
				<username>'''+username+'''</username>
				<id>'''+str(user_id)+'''</id>
			</contributor>
			<comment>xmlpagecreated</comment>
			<model>wikitext</model>
			<format>text/x-wiki</format>
			<text xml:space ="preserve" bytes="'''+str(pglen)+'''">
			\n'''+wikiText+'''
			</text>
		</revision>
	</page>
	\n\n'''

	return page

def xmlGenerator(titles,textTemplate, dataFrame):
	codes = dataFrame['Code'].tolist()
	#indices = [6,17,31,210,782,134,104]
	#codes= []
	#for i in indices:
	#	codes.append(dataFrame.loc[i]['Code'])
	#codes = random.sample(codes,4)
	#codes = codes +['C-2014-0009']
	#print(len(codes))
	word_counts = []
	pages = ""
	titles_list = []
	global page_id
	for code in codes:
		details = dataFrame[dataFrame['Code']==code].to_dict(orient='records')[0]
		for col in details:
			if type(details[col]) == str:
				details[col] = details[col].replace('&','అండ్')
			else:
				for i in range(len(details[col])):
					details[col][i] = details[col][i].replace('&','అండ్')
		#title = titles[code]
		title = titles[code].strip()
		print('title',title, code)
		titles_list.append(title)
		wikiText = textTemplate.render(details)
		word_counts.append(len(wikiText.split(' ')))
		pages+=addPage(title, wikiText)
		page_id+=1
	#print(page_id)
	print('Len :',len(set(titles)))
	min_count  = min(word_counts)
	max_count = max(word_counts)
	avg_count = sum(word_counts)/len(word_counts)
	#print('MIN : '+str(min_count))
	#print('MAX : '+str(max_count))
	#print('AVG : '+str(avg_count))
	import numpy as np
	np.save('word_counts.npy',word_counts)
	return pages

def main():
    file_loader = FileSystemLoader('')
    env = Environment(loader=file_loader)
    pages=""
    titlefile = 'new_titles'
    titles = {}
    list_titles = []
    with open(titlefile,'r') as tf:
        lines = tf.readlines()
        for l in lines:
            y = l.split(' ')
            t = ' '.join(y[1:-1])
            titles[y[-1].strip()] = t
            print(y[-1].strip())
            list_titles.append(t)
    print(len(set(list_titles)))
    print('new')
    xmlTextTemplate = env.get_template('asteroid_comet_template.j2')
    subdomainfile = 'asteroids_comets.json'
    data = pd.read_json(subdomainfile)
    pages+=xmlGenerator(titles, xmlTextTemplate, data)
    xmlpage = tewiki+pages+'</mediawiki>'
    f = open('ast_com_tel.xml','w')
    f.write(xmlpage)
    f.close()
main()