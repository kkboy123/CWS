#!/usr/bin/env python
#-*- coding: UTF-8 -*-

def getString(f, offset):
    offset = offset- 4*2
    f.seek(offset)
    return f.read(4*5).decode('utf32')

    
if __name__ == '__main__':
    index_path = '/data/experiments/termextract/autoSys/indexes/fahua_te/'
    fn = index_path + 'Text_f'
    f = open(fn, 'rb')
    
    predict_path = '/home/master/kkboy/feature/testdata.table.scale.predict'
    fr = open(predict_path,'r')
    
    result_path = 'result'
    fo = open(result_path,'wb')
    
    i=3
    for predict in fr:
        if (len(predict))==2:
            offset = i*4
            f.seek(offset)            
            #print (f.read(4).decode('utf32').encode("UTF-8"),offset)
            fo.write("%s,%s\n"%(f.read(4).decode('utf32').encode("UTF-8"),offset))        
        i = i+1
    
    
