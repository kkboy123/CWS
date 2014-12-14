import json
path_seg = "/data/experiments/termextract/autoSys/results/point_ext3_SVM/fahua_te/Features2/iterativeSeed_fahua_2-3-4/3/extract/fahua_te_P_offsets_0.6"
path_index = "/data/experiments/termextract/autoSys/indexes/fahua_te/Text_f"
file_seg = open(path_seg,"r")
file_index = open(path_index,'rb')
my_unigram={}
i1=0
i2=(int)(file_seg.readline())
for line in file_seg.readlines()[10:]:
    # if i1> 200:
    # break
    i1 = i2
    i2 = (int)(line)
    if (i2-i1)==4:
        file_index.seek(i1-8)
        c = file_index.read(4*5).decode('utf32')
        #print c[2]
        if my_unigram.has_key(c[2]):
            my_unigram[c[2]].append({i1:c})
        else:
            my_unigram[c[2]]=[{i1:c}]
with open('my_uni_sort','wb') as f:
    f.write('{')
    counter_uni=0
    for key, value in sorted(my_unigram.items(), key=lambda (k,v): len(v),reverse=True):
    #for key in my_unigram:
	if counter_uni>20:
	    break
        counter_uni = counter_uni +1
        if key == chr(10):
            continue
        f.write("u'%s':%s" % (key.encode("UTF-8"),len(value)))
        if counter_uni < len(my_unigram.keys()):
            f.write(',')
        f.write('\n')
    f.write('}')
    #.write(json.dumps(my_unigram))
f.close()
#print my_unigram
