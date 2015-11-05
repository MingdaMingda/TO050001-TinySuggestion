. bin/sugg_conf.py

python bin/index.py build_item_set 1> ${FileOutputItemSet}
python bin/index.py gen_tag2tid 1> ${FileTag2tid}
python bin/index.py gen_prefix2tid 1> ${FilePrefix2tid}
sort -t$'\t' -k1,1 -k3,3nr ${FilePrefix2tid} > ${FilePrefix2tid}.sort
awk -f bin/select_top.awk -v N=${topN} ${FilePrefix2tid}.sort > ${FileOutput}.prefix

