testdata.table => all features in this corpus (51XXXX)
top1.table => "於"的feature (837)
top1.all => "於"的index

sed '/^$/d' top1.table > top1.table.noblank
bash -x my_NuVarynew.sh