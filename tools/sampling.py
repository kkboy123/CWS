#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
Coded by TRuEmInG (2011 Summer) at NTU ESOE for TE autoSys
"""

import os, sys, codecs, random, math
import cnlstk
from struct import *
from time import time, strftime, gmtime

class FeatureMaker:
	
	def __init__( self, path, opt='' ):
		'''
		path: path of indexes
		opt: 'cbeta' or ''
		'''
		if opt == 'cbeta': self.Scher = cnlstk.SearchCBETA( path )
		else: self.Scher = cnlstk.Search( path )

			
	def getStrOffsetList(self, string):
		return self.Scher.getOffsetList(string, 'f')


	def getStrOffsetList2(self, fn, gram):
		'''
		取得 [大正藏索引] 內所有詞條的 offset list
		'''
		cp = []			#check distinct
		L = []			#offset list
		i = ii = 0		#i: 總共符合 gram 的詞條數； ii: 在索引中找不到的詞條數
		f = codecs.open(fn, 'r', 'utf8')
		for l in f:
			tmp = l.split(',')[-1].strip()
			if cnlstk.countStrLen(tmp) == gram and tmp not in cp:
				cp.append(tmp)
				i += 1
				tp = self.getStrOffsetList(tmp)
				if tp != []: L.extend( tp )
				else: ii += 1
		f.close()
		L.sort()
		return L, i, ii


	def getStrStatisticsUni(self, string): pass


	def getMI(self, string):
		'''
		Mutual Information
		fahua_te:
			bi-gram: total No. 142295, distinct No. 22614
			uni-gram:total No. 477901, distinct No. 2992
		** 目前只可進行 fahua_te index 的 bi-gram 的計算，三字以上 p(AB) OK，但 p(A), p(B) 取樣方式要討論。
		'''
		n = self.Scher.getFreq(string)
		if n == 0: return -1					#### 有問題的資料回傳 0 以便檢查 ####
		strg = self.Scher.convertStr2List(string)
		fx = float(n)
		fy = self.Scher.getFreq( ''.join(strg[:-1]) )
		fz = self.Scher.getFreq( ''.join(strg[1:]) )
		if fy == 0 or fz == 0: return -1		#### 有問題的資料回傳 0 以便檢查 ####
		MI = math.log(fx/142295.0, 2) - math.log(fy/477901.0, 2) - math.log(fz/477901.0, 2)
		return MI
	
	
	def getStrStatistics(self, string):
		'''
		frequency, l_unique,l_max,l_break, r_unique,r_max,r_break, AEc,Max_l,Max_r
		** 若輸入小於 bi-gram 長度的字串會回傳錯誤。（計算內聚會出問題）
		** 抽詞用的索引若不包含換行符號，則 self.getFreq(strg) 有可能查無資料。
		** 任何元素查無資料其結果均回傳 0
		'''
		#不可輸入單字
		if self.Scher.countStrLen(string) < 2: return 'err: string length must more than 2'
		
		n = self.Scher.getFreq(string)

		if n == 0:						#### 有問題的資料回傳 0 以便檢查 ####
			return -1, 0,0,0, 0,0,0, 0,0,0
			
		strg = self.Scher.convertStr2List(string)

		fx = float(n)
		fy = self.Scher.getFreq( ''.join(strg[:-1]) )
		fz = self.Scher.getFreq( ''.join(strg[1:]) )
		
		right = self.Scher.getNextWordInf(string)
		if right == (0,0,0,0,0):
			print 'right', cnlstk.convertStr2List(string)
			return -11, 0,0,0, 0,0,0, 0,0,0
		left = self.Scher.getPreWordInf(string)
		if left == (0,0,0,0,0):
			print 'left', cnlstk.convertStr2List(string)
			return -12, 0,0,0, 0,0,0, 0,0,0
		
#		1. No. of next distinct characters
#		2. Highest frequency of the next distinct character (Chinses)
#		3. Highest frequency of the next distinct character (non-Chinses)
#		4. No. of next distinct break points (non-Chinese characters) 
#		5. Total No. of break points
#		因加上 break points 資訊，因此 next distinct 及 maximum 均不排除非中文字。

		r_unique = right[0]
		l_unique = left[0]

# break point 的兩種取法擇一
# 1. 有斷點為 1 無斷點為 0
#		if right[4] > 0: r_break = 1
#		else: r_break = 0
#		if left[4] > 0: l_break = 1
#		else: l_break = 0
# 2. 用原斷點頻率
		r_break = right[4]
		l_break = left[4]

		if right[1] >= right[2]: r_max = right[1]
		else: r_max = right[2]
		if left[1] >= left[2]: l_max = left[1]
		else: l_max = left[2]
		
		#避免因未建索引的字碼而算不出資訊
		if fy+fz-fx <= 0: AEc = 0.0			#不應該出現
		else: AEc = fx/(fy+fz-fx)			#呼叫此 def 時應先過濾，盡量避免 fx 為 0
		
		#有段點的 boundary (degree of freedom) 趨近於(=) 0, 否則用 Max/fx
		if r_break > 0: Max_r = 0
		else: Max_r = r_max/fx
		if l_break > 0: Max_l = 0
		else: Max_l = l_max/fx

		return fx, l_unique,l_max,l_break, r_unique,r_max,r_break, AEc,Max_l,Max_r
				

	def getBiFeatures(self, string):
		'''
		將 line 分成 bi-grams 送出
		取得 Features
		'''
		strg = self.Scher.convertStr2List(string)
		L = []
		i = 0
		while i+2 <= len(strg):
#			print ''.join( strg[i:i+2] )
#			raw_input()
			n = self.getStrStatistics( ''.join( strg[i:i+2] ) )
			
##			if n[0] == -1 or n[0] == -11 or n[0] == -12:		#檢查錯誤用 -1: getFreq()=0, -11: getNextWordInf()=(0,0,0,0,0), -12: getPreWordInf()=(0,0,0,0,0)
##				print n[0], string, ''.join( strg[i:i+2] )
##				raw_input()

			L.extend(n)
			i += 1
		return L
		
				
	def getBiFeaturesMI(self, string):
		'''
		將 line 分成 bi-grams 送出
		取得 Features
		getBiFeatures() 的內容再加上 MI
		'''
		strg = self.Scher.convertStr2List(string)
		L = []
		i = 0
		while i+2 <= len(strg):
#			print ''.join( strg[i:i+2] )
#			raw_input()
			n = self.getStrStatistics( ''.join( strg[i:i+2] ) )
##			if n[0] == -1 or n[0] == -11 or n[0] == -12:		#檢查錯誤用 -1: getFreq()=0, -11: getNextWordInf()=(0,0,0,0,0), -12: getPreWordInf()=(0,0,0,0,0)
##				print n[0], string, ''.join( strg[i:i+2] )
##				raw_input()
			L.extend(n)
			
			mi = self.getMI( ''.join( strg[i:i+2] ) )				#增加 Mutual Information feature
			L.append(mi)
			
			i += 1
		return L


	def getCentralFeatures(self, line, no):
		'''
		只取該 n-gram 的 features 如果有 ext 去掉左右
		中心字串有非中文字碼者，不應送進來。（理論上應該不會抽出有非中文字碼的字串）
		'''
		L = []
		if self.Scher.countStrLen(line) == no: ln = line		#左右沒有 ext 直接取得資料
		else:
			strg = self.Scher.convertStr2List(line)
			while len(strg) > no: strg = strg[1:-1]
			ln = ''.join(strg)
		return self.getStrStatistics( ln )


	def getUniFrquences(self, string):
		'''
		傳入字串，回傳字串中每個單字字頻的陣列。
		'''
		strg = self.Scher.convertStr2List(string)
		L = []
		for k in strg: L.append( self.Scher.getFreq(k) )
		return L


	def getFeatures(self, gram, string, opt, choice):
		'''
		choice == '1': features = bi-gram(fx, l_unique,l_max,l_break, r_unique,r_max,r_break, AEc,Max_l,Max_r)
		choice == '2': features = uni-gram(freq) + bi-gram(fx, l_unique,l_max,l_break, r_unique,r_max,r_break, AEc,Max_l,Max_r)
		** check l_break, r_break 的說明
		** check Max_l, Max_r 的說明
		'''
		features = []
		
# ** 字串每個字元的頻率（uni-gram freq.）feature selection f-score 的值不高所以關掉
		if choice == '2':
			features.extend( self.getUniFrquences(string) )						#字串中每個單字的字頻
#			print '+uni:', len(features)
		if choice == 'idf1':													#原始 sample string 的 tfidf
			features.extend( tfidf.sampletfidf(string, gram) )
		if choice == 'idf2':													#延伸後字串的 bi-grams' tfidf
			features.extend( tfidf.everybigram_tfidf(string, gram) )
		if choice == '3': features.extend( self.getBiFeaturesMI(string) )		#多了 MI 的 vector
		
		features.extend( self.getBiFeatures(string) )							#字串中每個雙字的資訊

#		print '+bi:', len(features)
		if gram > 2: features.extend( self.getCentralFeatures(string, gram) )	#非 bi-gram 的該字串資訊
#		print '+ >bi:', len(features)
#		raw_input()		
		if opt == 'p' or opt == 'P': output = '0'
		else: output = '1'
		i = 0
		for uni in features:
			i += 1
			output += '\t%d:%s' % (i, str(uni))
		output += '\n'
		return output
		

	# # # # # # # # #
	# P & N samples #
	# # # # # # # # #
	
	def getTEsamples(self, ofsets, sv_pth, gram, ext, choice):
		'''
		產生未知字串 SVM imput data
		建 label 為 N, ofsets 範圍內 gram, ext 樣本的特徵參數資料
		作為預測（抽詞）用
		ex:N	1:1.0	2:3.4	3:...
		'''
		fw = open(sv_pth+'.t', 'w')
		fwo = open(sv_pth+'.t.ofsts', 'w')
		tmp = ofsets.split('-')			#ex: 0-1234
		ofst = int(tmp[0])				#開始 offset
		ei = int(tmp[1])				#結束 offset
		
		i = 0
		while ofst < ei:
			if ofst+gram > ei: break
			
			line = cnlstk.convertStr2List( self.Scher.getSequence(ofst, 0, gram, 'f') )
			flag = 'on'
			for k in line:
				if cnlstk.chkChineseCB(k) == 1:
					flag = 'off'
					break
			if flag == 'off':
				ofst += 4
				continue
			
			line = self.Scher.getSequence(ofst, ext, gram+ext, 'f')
			sp = self.getFeatures(gram, line, 'N', choice)	# 'N' 表示 testing data label 為 1
															# 如果有先標好的就有 'P' or 'N' (0 or 1)
			fwo.write(str(ofst)+'\n')
			i += 1
			fw.write( sp )
			ofst += 4
		fw.close()
		fwo.close()
		print i, 'samples'
		return sv_pth+'.t.ofsts', sv_pth+'.t'
		
		
	def saveSampleFiles(self, ofstlist, sv_pth, gram, ext, choice):
		'''
		fw: offsets
		fwp: positive samples
		fwn: negative samples
			** fwp, fwn using SVM input data standard
		fwa: training data
		fwt: testing data
		fwr: random numbers of getting testing data
		
		** fw 中的 offset 與 fwp 中的 data(label & features) 是一對一關係
		** fwp 與 fwn 中的資料是一對二關係
		** 以上三個檔案的 offset, positive, negatives 都可以追回去（ chkSamples() ）
		'''
		if sv_pth[-1] != '/': sv_pth += '/'
		fw = open(sv_pth+'offsets', 'w')
		for k in ofstlist: fw.write( str(k)+'\n' )
		fw.close()
		
		fwp = open(sv_pth+'positive', 'w')
		fwn = open(sv_pth+'negative', 'w')
		fwa = open(sv_pth+'ala', 'w')
		fwt = open(sv_pth+'ala.t', 'w')
		fwr = open(sv_pth+'random_no', 'w')
		
		rL = []
		for k in range(len(ofstlist)): rL.append(k)		#建與 ofstlist 長度相同的連續數字陣列
		if len(ofstlist) < 10: ctem = 1					#設定 1/10 的數量
		else: ctem = len(ofstlist)/10
		rL = random.sample(rL, ctem)					#將 rL 縮小成 1/10 的大小（隨機取）
		rL.sort()
		for k in rL: fwr.write(str(k)+'\n')
		fwr.close()
		
		overwrite = 0
		n = ''
		
		i = 0
		for ofst in ofstlist:
			
			if i%100 == 0: print i, '/', len(ofstlist)
			sys.stdout.flush()
#			n = str(i)
#			sys.stdout.write("%s%s\r" % (n, " "*overwrite ))
#			sys.stdout.flush()
#			overwrite = len(n)
			
			line = self.Scher.getSequence(ofst, ext+1, gram+ext+1, 'f')	#比欲延伸的長度前後多讀一個字元（才能 shift）

#			line = line.replace('\n', u'〇')			#CBETA 2010 年版本無 u'〇'，所以替換掉。
													#但本版的抽詞程式不能替換，換了會找不到。須保留所有符號。
			line = self.Scher.convertStr2List(line)	#把 line 字串轉成陣列
			
			pt = ''.join( line[1:-1] )
			ntf = ''.join( line[:-2] )				#line 前後多一個字元這裡才能前後 shift
			ntb = ''.join( line[2:] )
#			print pt.replace('\n',u'〇'),ntf.replace('\n',u'〇'),ntb.replace('\n',u'〇')
#			raw_input()
			
			pp = self.getFeatures(gram, pt, 'P', choice)
			n1 = self.getFeatures(gram, ntf, 'N', choice)
			n2 = self.getFeatures(gram, ntb, 'N', choice)
			
			fwp.write( pp )
			fwn.write( n1 )
			fwn.write( n2 )
			
			fwa.write( pp+n1+n2 )		#全部放進 training data
			if i in rL:					#隨機取得 1/10 量的 testing data
				fwt.write( pp+n1+n2 )
				del rL[ rL.index(i) ]
			i += 1
		print n
		print 'random list:', rL
		fwp.close()
		fwn.close()
		fwa.close()
		fwt.close()
		return 'offsets', 'positive', 'negative', 'ala', 'ala.t', 'random_no'


	def saveSampleFiles_point(self, ofstlist, sv_pth, gram, ext, choice):
		'''
		[ make point samples ]
		fw: offsets
		fwp: positive samples
		fwn: negative samples
			** fwp, fwn using SVM input data standard
		fwa: training data
		fwt: testing data
		fwr: random numbers of getting testing data
		
		** fw 中的 offset 與 fwp 中的 data(label & features) 是一對一關係
		** fwp 與 fwn 中的資料是一對二關係
		** 以上三個檔案的 offset, positive, negatives 都可以追回去（ chkSamples() ）
		'''
		if sv_pth[-1] != '/': sv_pth += '/'
		fw = open(sv_pth+'offsets', 'w')
		for k in ofstlist: fw.write( str(k)+'\n' )
		fw.close()
		
		fwp = open(sv_pth+'positive', 'w')
		fwn = open(sv_pth+'negative', 'w')
		fwa = open(sv_pth+'ala', 'w')
		fwt = open(sv_pth+'ala.t', 'w')
		fwr = open(sv_pth+'random_no', 'w')
		
		rL = []
		for k in range(len(ofstlist)): rL.append(k)		#建與 ofstlist 長度相同的連續數字陣列
		if len(ofstlist) < 10: ctem = 1					#設定 1/10 的數量
		else: ctem = len(ofstlist)/10
		rL = random.sample(rL, ctem)					#將 rL 縮小成 1/10 的大小（隨機取）
		rL.sort()
		for k in rL: fwr.write(str(k)+'\n')
		fwr.close()
		
		overwrite = 0
		n = ''
		
		i = 0
		for ofst in ofstlist:
			
			if i%100 == 0: print i, '/', len(ofstlist)
			sys.stdout.flush()
#			n = str(i)
#			sys.stdout.write("%s%s\r" % (n, " "*overwrite ))
#			sys.stdout.flush()
#			overwrite = len(n)
			
			line = self.Scher.getSequence(ofst, ext+1, gram+ext+1, 'f')	#比欲延伸的長度前後多讀一個字元（才能 shift）

#			line = line.replace('\n', u'〇')			#CBETA 2010 年版本無 u'〇'，所以替換掉。
													#但本版的抽詞程式不能替換，換了會找不到。須保留所有符號。
			line = self.Scher.convertStr2List(line)	#把 line 字串轉成陣列
			
			pt = ''.join( line[1:-1] )
			ntf = ''.join( line[:-2] )				#line 前後多一個字元這裡才能前後 shift
			ntb = ''.join( line[2:] )
#			print pt.replace('\n',u'〇'),ntf.replace('\n',u'〇'),ntb.replace('\n',u'〇')
#			raw_input()
			
			pp = self.getFeatures(gram, pt, 'P', choice)
			n1 = self.getFeatures(gram, ntf, 'N', choice)
			n2 = self.getFeatures(gram, ntb, 'N', choice)
			
			fwp.write( pp )
			fwn.write( n1 )
			fwn.write( n2 )
			
			fwa.write( pp+n1+n2 )		#全部放進 training data
			if i in rL:					#隨機取得 1/10 量的 testing data
				fwt.write( pp+n1+n2 )
				del rL[ rL.index(i) ]
			i += 1
		print n
		print 'random list:', rL
		fwp.close()
		fwn.close()
		fwa.close()
		fwt.close()
		return 'offsets', 'positive', 'negative', 'ala', 'ala.t', 'random_no'


	def chkSamples(self, path):
		'''
		追 samples 源頭用（ offset, positive, negatives ）
		'''
		pass
	
	
	# # # # # # # # # # # # # #
	# training & testing data #
	# # # # # # # # # # # # # #
		
	
	def saveTestFileEvaluated(self, file_name, sv_pth, gram, ext):
		'''
		處理已經人工判斷對錯的檔案
		人工判斷的檔案須從索引輸出（以避免有誤差），人工作業後再來使用。
		testing data 的 label 是正確的 label，預測結果與人工判斷的 label 直接比對的正確率即所求之正確率。
		** 要比 saveTestFileBlind() 多一個 parse file 的流程。
		'''
#		sv_pth = os.path.split(sv_file)[0]
#		if not os.path.exists(sv_pth): os.mkdir(sv_pth)
		pass
			
	def saveTestFileBlind(self, ranges, sv_file, gram, ext):
		'''
		直接從索引輸出全文，label 都先指定為 0，預測結果與 0 比對後的正確率不重要。
		預測的結果再以人工辨識對錯後，其正確率才是所求的正確率。
		'''
		fw = open(sv_file, 'w')
		
		texts = self.Scher.getFullTexts(ranges)
		lines = self.Scher.convertStr2List(texts)
		
		for c in range( len(lines) ):
			#檔首跳過延伸的字數 與 檔尾跳過（gram 數 + 延伸的字數），如此取樣才不會有少數例外。
			if c < ext: continue
			if c > len(lines)-ext-gram: break

			pt = ''.join( lines[c-ext:c+gram+ext] )
#			print c, lines[c], pt
#			raw_input()
			fw.write( self.getFeatures(gram, pt, 'P') )

		fw.close()
		return


def checkString(file, ofstL, gram, ecode='utf32'):
	'''
	輸入 main file, offset list file, n-gram
	顯示字串
	'''
	L = []
	f = open(ofstL, 'r')
	for l in f: L.append(int(l))
	f.close()
	
	f = open(file, 'rb')
	i = 0
	for k in L:
		i += 1
		f.seek(k)
		print i, f.read(gram*4).decode('utf32')
		raw_input()
	f.close()
	

if __name__ == "__main__":

	Ts = time()
	
#	ofst = '../results/fahua_org/bigram/ext2/SVM/tSamples/offsets'
#	mfile = '../indexes/fahua_te/Text_f'
#	gram = 2
#	checkString(mfile, ofst, gram)
	
	obj = FeatureMaker('../indexes/fahua_te', 'cbeta')
#	print obj.getStrStatistics(u'十一')
#	print obj.getCentralFeatures(u'\U00020000先人一十一一大\U000FA000跑', 4)
#	print obj.getBiFeatures(u'一十一一')
#	print obj.getUniFrquences(u'一十一一')
#	print obj.getFeatures(2, u'一十一一', 'P')

#	obj.saveTestFileBlind('T01n0001_p0001a09', './test', 2, 3)

	Te = time()
	print strftime('%H:%M:%S', gmtime(Te-Ts))

