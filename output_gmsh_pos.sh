#!/bin/sh

# OUTPUT_GMS_POS=/home/86933/work/Etcetra/Programs/Python/OutputGmshPos/output_gmsh_pos.py
OUTPUT_GMS_POS=/home/86933/work/Etcetra/Programs/Python/OutputGmshPos/output_gmsh_pos_20220908.py
NLAP2GMSH=/home/86933/work/Etcetra/Programs/awk/nlap2gmsh/nlap2gmsh.awk

nmsh=case001-02.nmsh


nodes="
  429  430  431  432  433  967  434  968  435  436
  437  438  439  440  441  442  443  444  445  446
  447  448  449  450  451  969  452  970  453  454
  455  456  457
"


for i in $nodes; do
    printf "NODE%5d\n" $i
done > out_node_elem.in

# cat <<EOF > out_node_elem.in
# NODE  10
# NODE  11
# NODE  12
# ELEM  10
# ELEM  11
# ELEM  12
# EOF


$nums
VERBOSE=1
if [ $VERBOSE = 1 ]; then
    cat out_node_elem.in
fi


$OUTPUT_GMS_POS $nmsh out_node_elem.in

awk -f $NLAP2GMSH $nmsh
