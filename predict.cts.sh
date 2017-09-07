#! /bin/bash
############################################
#
# Author: 
# E-Mail:@sogou-inc.com
# Create time: 2016 12ÔÂ 20 17Ê±44·Ö29Ãë
# version 1.0
#
############################################
nvidia-smi |fgrep Default|awk 'BEGIN{srand()}{
print (NR-1)"\t"substr($13,1,length($13)-1)"\t"rand()
}'|sort -t$'\t' -k 2,2n -k 3,3n|awk -F"\t" 'NR==1{
print "export CUDA_VISIBLE_DEVICES="$1
print "echo $CUDA_VISIBLE_DEVICES"
}' > setdevicesubp.sh
. setdevicesubp.sh
rm -f setdevicesubp.sh

python predict.cts.py --save_dir=save


