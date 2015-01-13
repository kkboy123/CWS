#!/usr/bin/bash
<<COMMENT
if [[ "$1" == ""  ]]
	then echo 'Warning:沒有給予參數Nu值!'
	echo '退出程式'
	kill -2 $$
	fi
COMMENT

egrep='egrep --color=auto'
fgrep='fgrep --color=auto'
getMmatch='python /home/stayhigh/bin2TwoFile/getM-match.py'
getPosByRange='python /home/stayhigh/bin2TwoFile/getPosByRange.py'
getmatch='python /home/stayhigh/bin2TwoFile/getmatch.py'
gettablebyoffset='python /home/stayhigh/bin2TwoFile/gettablebyoffset.py'
getwordByPos='python /home/stayhigh/bin2TwoFile/getwordByPos.py'
gotofahua='cd /data/experiments/termextract/autoSys/HE/fahua_te'
grep='grep --color=auto'
l='ls -CF'
la='ls -A'
ll='ls -alF'
ls='ls --color=auto'
runsvm='python /data/libsvm/tools/easy.py '
runsvm2514fold='python /data/libsvm/tools/easy2514fold.py '
runsvm3660fold='python /data/libsvm/tools/easy3660fold.py '
runsvmOneclass='python /data/libsvm/tools/easyone.py '
runsvmfold='python /data/libsvm/tools/easyfold.py '
svmpredict='/data/libsvm/svm-predict'
svmscale='/data/libsvm/svm-scale'
svmtrain='/data/libsvm/svm-train'

echo '-- 訓練資料和測試資料正在scaling --';
$svmscale -s scale human.table > human.table.scale 2> /dev/null;
$svmscale -r scale testdata.table > testdata.table.scale 2> /dev/null;
echo '--scaling 完成--'
echo '--one-class機器學習--';
$svmtrain -n $1 -s 2 human.table.scale;
echo 'one-class機器學習訓練完成';
echo '開始進行predict';
$svmpredict testdata.table.scale human.table.scale.model testdata.table.scale.predict;
wc -l testdata.table.scale.predict testdata.pos >> run.log;
echo '製作machine.sl 檔案中..';
paste testdata.table.scale.predict testdata.pos |awk '{if($1==1)print $2}' > machine.sl ;
wc -l machine.sl human.all >> run.log;
echo '製作match.sl　檔案中..';
$getmatch machine.sl human.all > match.sl;
wc -l match.sl >> run.log;
echo '製作diff.sl　檔案中..';
$getMmatch machine.sl match.sl > diff.sl;
wc -l diff.sl >> run.log;
echo 利用程式gettablebyoffset將檔案diff.sl轉成下一回合binary classification用的negative example;
$gettablebyoffset diff.sl -1  negative.table;
echo 將訓練資料合併;
cat human.table negative.table  > forBinarytraindata.table;
echo 實行binary classification;
$runsvmfold forBinarytraindata.table testdata.table 2514;
echo 生成文件machine.2.sl;
paste  testdata.table.predict testdata.pos |awk '{if ($1==1) print $4}' > machine.2.sl;
wc -l machine.2.sl >> run.log;
echo 取出文件machine.2.sl和match.2.sl的交集項目;
$getmatch machine.2.sl human.all > match.2.sl;
wc -l match.2.sl >> run.log;
echo 取出文件machine.2.sl 和 match.2.sl的差集diff.2.sl;
$getMmatch machine.2.sl  match.2.sl > diff.2.sl ;
wc -l diff.2.sl >> run.log;
echo '請觀看run.log檔案';
echo 程式執行結束...;
