# -*- coding: utf-8 -*-
import cnlstk
import codecs
path = '/data/experiments/termextract/autoSys/indexes/fahua_te/'
obj = cnlstk.SearchCBETA(path)
my_map = {u'諸':2101,u'於':1722,u'法':1585,u'者':1476,u'是':1420,u'佛':1350,u'為':1239,
u'不':1230,u'說':1193,u'以':1106,u'得':1065,u'故':1044,u'無':958,u'而':926,u'若':894,u'心':794,
u'有':717,u'我':717,u'如':657,u'行':650,}
f = codecs.open('filename', 'w', 'utf32')
for key1,value in sorted(my_map.items(), key=lambda (k,v):v ,reverse=True): 
    f.write( key1)
    temp_freq = obj.getFreq(key1)
    f.write(':%s,%s,%.2f\n' %(my_map[key1],temp_freq,(float(my_map[key1]))/(float(temp_freq))))

for key1,value in sorted(my_map.items(), key=lambda (k,v):v ,reverse=True):
    f.write(key1)
    f.write('\n')
    rst = obj.getConcordance(key1)
    for k in rst:
	f.write(k[0].replace('\n', u"\u204B "))
	f.write('\n')


#strg = (u'諸', u'漢')
#term = strg[0]
#print obj.binarySch(term, 'f')
#print obj.getFreq(strg[0])
#print 'con_f'
#rst = obj.getConcordance(strg[0])
#for k in rst[:10]:
#    f.write(k[0].replace('\n', u"\u204B "))
#    f.write('\n')
#    print k[0].replace('\n', u"\u204B "), k[1]
