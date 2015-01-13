#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from sampling import FeatureMaker


def getString(f, offset):
	offset = offset- 4*2
	f.seek(offset)
	return f.read(4*5).decode('utf32')

	
if __name__ == '__main__':
	index_path = '/data/experiments/termextract/autoSys/indexes/fahua_te/'
	fn = index_path + 'Text_f'
	f = open(fn, 'rb')
	obj = FeatureMaker(index_path, 'cbeta')
	
	my_offsets=[160,2088,5052,5196,17132,17260,18380,22092,35144,35312,35456,35648,41288,46416,46728,47256,49232,50128,52528,53708,59392,75756,80128,82328,82492,90096,90208,91176,97612,97740,100328,100448,102188,107676,111060,111940,114096,118060,120108,120312,121052,121412,122040,122764,127188,132284,133240,137980,138696,141092,142708,144488,145484,145824,147784,147892,147948,148020,148760,148836,150324,151200,154184,155344,157712,157880,162640,163008,167744,169076,172784,173188,177348,177884,186844,187468,187624,188224,188592,189072,189612,190428,190824,197492,200712,202292,202544,203600,204120,204196,204564,207800,212524,219608,219972,221160,223384,223648,226376,231136,241564,249060,249944,251276,253392,253716,254556,255404,255700,257752,258668,261424,261912,262696,262936,265296,266668,266892,267412,267528,270180,270944,274572,276296,277832,277968,284256,290688,298244,298720,300396,301100,302072,302724,304860,304984,305192,305912,308000,308792,310276,314712,330640,331440,332672,383312,383584,404020,404076,408772,410588,422460,423796,453520,453772,455340,462432,465144,484780,485116,494800,502668,513680,516452,518636,518728,530332,530548,530856,531168,533452,534676,541444,544024,565244,565640,570540,571732,580996,596940,600180,601860,603224,603420,635976,645456,645912,648528,655088,672600,674680,681452,681492,693516,694952,695096,698908,707024,707152,708284,711996,725028,725196,725340,725532,731172,736300,736612,737140,739112,740004,742392,743564,749232,765592,769940,772148,772312,779920,780032,780992,789512,791448,792024,795836,796964,797420,797548,800136,800256,802000,807480,810860,811728,813876,817828,819880,820084,820808,821160,821788,822500,826920,832016,832968,837708,838424,840808,842420,844196,845192,845532,847492,847596,847652,847724,848452,848524,850008,850884,853832,854992,857372,857536,862272,862640,867320,868636,870648,872332,872732,877440,886392,887016,887172,887772,888140,888624,889164,889972,890364,897036,900260,901824,902076,903132,903648,903724,904092,912040,919132,919468,920656,922872,923136,925848,930572,939940,940944,948416,949288,950592,952712,953036,953876,954736,955032,957084,957628,966232,966700,967484,970040,971408,971632,972152,972268,974908,975668,982364,984108,985616,985752,990416,997776,998260,999948,1000648,1001628,1002280,1004420,1004544,1004752,1007612,1008396,1009860,1011592,1026884,1027732,1031528,1036768,1040940,1050144,1055576,1056672,1057464,1057752,1058280,1058568,1065700,1067188,1069600,1070228,1070876,1071836,1073516,1074096,1074692,1079808,1079880,1081344,1096912,1101716,1103628,1104504,1112400,1112788,1115560,1118776,1119592,1119712,1120048,1125828,1136392,1137144,1138604,1147804,1149176,1149528,1159412,1161844,1164860,1164972,1165844,1167500,1168228,1169132,1170184,1173068,1174100,1174968,1182592,1183412,1183452,1187504,1187528,1188392,1190056,1190296,1193872,1195552,1198652,1199156,1199492,1202792,1203312,1203560,1203664,1204444,1205404,1207324,1207524,1207576,1211312,1212676,1213316,1214448,1214512,1215012,1221088,1224856,1225144,1225528,1225672,1227168,1234436,1235020,1236368,1238140,1238208,1240232,1240644,1241516,1242040,1244996,1246988,1247264,1249932,1250304,1251096,1251320,1252256,1252340,1252448,1252656,1253280,1255344,1255656,1255760,1255808,1255860,1255964,1256092,1257920,1258328,1260032,1263176,1263244,1263404,1266212,1266276,1268328,1269000,1269840,1270248,1270848,1271136,1271184,1271496,1273244,1273748,1275232,1275472,1277428,1277524,1277696,1277836,1277964,1278144,1278316,1278408,1278492,1278660,1278828,1279776,1280476,1281460,1284220,1284772,1285528,1287580,1287988,1294520,1294676,1294772,1296908,1296980,1300916,1302112,1303520,1304008,1304056,1305332,1305400,1306828,1310816,1311868,1316844,1317916,1318836,1319480,1319640,1325312,1332424,1333144,1334764,1339252,1340736,1341144,1342192,1345224,1346448,1346756,1347556,1347652,1349164,1349332,1350856,1352804,1353044,1355428,1358884,1364212,1364860,1364980,1365044,1365404,1367220,1367252,1367288,1367324,1372712,1372784,1379276,1379352,1386864,1387120,1388484,1391716,1395456,1395584,1395712,1396040,1396332,1396400,1396448,1399372,1399884,1400288,1402724,1403860,1404888,1405148,1406400,1406704,1406828,1408568,1409800,1410436,1411280,1412424,1413076,1413740,1415180,1425588,1430536,1434528,1436000,1448020,1450464,1450568,1450972,1451612,1452660,1452952,1457388,1457508,1460036,1460248,1460312,1461976,1462316,1479848,1486560,1487668,1488264,1490848,1493760,1493804,1497048,1509952,1510032,1513196,1525072,1525200,1528788,1530812,1531324,1532264,1533160,1533340,1533848,1533924,1534296,1536632,1538344,1539384,1545648,1546208,1551920,1555532,1556416,1556764,1556932,1557624,1559036,1559312,1559452,1564620,1564860,1565148,1565480,1565920,1567060,1567256,1567288,1568568,1572528,1576012,1577064,1577488,1578476,1578568,1578696,1579488,1586036,1587124,1591708,1591796,1591896,1591996,1593884,1595376,1595732,1596624,1597412,1598196,1598228,1600400,1606988,1607808,1607840,1608224,1608644,1609024,1609156,1609188,1609240,1609336,1609744,1610040,1612384,1612488,1613940,1618892,1619364,1619772,1625160,1625316,1625380,1632776,1645568,1646348,1647504,1652372,1653668,1660168,1663048,1667908,1671348,1673056,1675488,1675840,1677048,1679912,1680608,1683088,1696996,1711544,1712840,1713184,1715168,1715236,1715652,1717148,1717300,1741232,1745628,1745788,1746204,1746596,1746752,1746916,1747344,1747472,1753176,1754156,1754592,1764600,1768088,1790996,1796248,1798088,1798280,1802200,1803016,1805196,1806764,1813552,1814956,1818120,1818928,1824708,1824844,1827148,1827260,1829776,1832808,1835012,1837540,1843612,1851184,1860528,1867764,1868244,1869456,1875676,1877336,1883384,1885392,1889432,1890400,1890504,1891520,1892432,1893380,1894516,1895460,1900988,1902696,1902720,1902972,1903020,1903052,1907244,1908672,1909228,1917012,1917884,1926468,1927568,1931948,1933404,1937588,1939020,1939632,1939664,1942588,1948388,1949760,1951544,1951656,1955916,1958584,1961284,1969888,1972964,1973728,1974968,1975160,1975756,1976252,1978544,1978772,1978844,1979392,1981464,1982732,1986172,1986188,1986228,1986272,1986312,1986352,1986392,1986684,1986820,1987036,1987880,1990028,1991796,1992368,1993936,1993972,1994364,1994780,1995516,1995692,2003308,2007992,2010128,2019708,2020916,2024952,2027172,2027876,2029660,2029892,2030380,2042852,2043136,2043184,2047960,2054000,2056196,2056656,2058540]
	for my_offset in my_offsets:
		gram = 1				# uni-gram
		fs = '2'				# feature set
		string = getString(f,my_offset)	# extend string
		label = 'P'				# class label
		print obj.getFeatures(gram, string, label, fs)
		
		
	# gram = 1				# uni-gram
	# fs = '2'				# feature set
	# string = u'妙法蓮華經'	# extend string
	# label = 'P'				# class label
	# print obj.getFeatures(gram, string, label, fs)
