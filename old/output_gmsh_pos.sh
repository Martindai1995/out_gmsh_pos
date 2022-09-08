#!/bin/sh

OUTPUT_GMS_POS=/home/86933/work/Etcetra/Programs/Python/OutputGmshPos/output_gmsh_pos.py

nmsh=ini2d.nmsh


cat <<EOF > out_node_elem.in
NODE  10
NODE  11
NODE  12
ELEM  10
ELEM  11
ELEM  12
EOF

$OUTPUT_GMS_POS $nmsh out_node_elem.in

