# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-05-06 14:55
# modified : 2015-05-06 14:55
"""
Create a web-app with additional information and quick access to the database.
"""

__author__="Johann-Mattis List"
__date__="2015-05-06"


#import os
#os.system('mv sinotibetan.sqlite3 ~/projects/websites/dighl/triples/')
from lingpyd import *
from lingpyd.plugins.lpserver.lexibase import LexiBase,load_sqlite
import json

# in later steps:
# re-link the data
db = LexiBase('sinotibetan', dbase='../sqlite/sinotibetan.sqlite3')


# we expand on the meta-data template
with open('../metadata/metadata.json') as f:
    meta = json.loads(f.read())

mcon = [w[1] for w in csv2list('../concepts/stdb.concepts.csv')]
txt1 = ''
concepts = sorted(set([db[k,'concept'] for k in db]))
for c in concepts:
    
    # determine coverage
    cov = len([db[k,'concept'] for k in db if db[k,'concept'] == c])
    if c in mcon:
        txt1 += '<option value="'+c+'" selected>'+c+' ('+str(cov)+' entries)</option>'
    else:
        txt1 += '<option value="'+c+'">'+c+' ('+str(cov)+' entries)</option>'

txt2 = ''

langs = db.taxa 
conv = dict([(k,v['subgroup']) for k,v in meta.items()])


for k in langs:
    etr = len(db.get_list(doculect=k,flat=True))
    txt2 += '<option value="'+k+'">'+k+' ('+conv[k]+', '+str(etr)+' entries)</option>'

txt3 = ''
for col in sorted(db.header, key=lambda x: db.header[x]):
    txt3 += '<option value="'+col.upper()+'" selected>'+col.upper()+'</option>'

# we expand on the meta-data template
with open('../metadata/metadata.json') as f:
    meta = 'META = '+json.dumps(json.loads(f.read()))+';'

with open('templates/index.template.html') as f:
    d = f.read()
    d = d.format(JS=open('templates/stb.js').read(), 
            DOCULECTS = txt2,
            CONCEPTS  = txt1,
            CONTENT = txt3,
            META = meta
            )
with open('index.html', 'w') as f:
    f.write(d)        
