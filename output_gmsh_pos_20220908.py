#!/usr/bin/env python3

# Nlapの要素データ(ft17), 節点データ(ft16)を読み込んで、gmshのpost viewを用いて

# View "To Next Node" {
# VP(   1,   1,  0){    0.1, 0.1,  0};
# };
# last updated: Wed Sep 21 08:58:31     2016

import sys, os
import re
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'site-packages'))
from  nlap import Nlap

################
# Main
################
if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("{0:s} [nlap.nmsh] [output_elem_or_node]\n".format(sys.argv[0]))
        sys.stderr.write("Statement of output_elem_or_node file.\n")
        sys.stderr.write("keyword number\n")
        sys.stderr.write("NODE element_number\n")
        sys.stderr.write("ELEM element_number\n")
        exit(1)

    inp_nlap = sys.argv[1]
    inp_out_elem_node = sys.argv[2]

    # print(inp_nlap)
    nlap = Nlap(inp_nlap)

    try:
        fin = open(inp_out_elem_node, 'r', encoding='utf-8')
    except IOError:
        sys.stderr.write('read_node_data: Can not find out {0:s}\n'.format(nlap_file))
        sys.exit(1)

    out_node = []
    out_elem = []

    for line in fin:
        line = line.rstrip("\n")

        rows = line.split()
        keyword = rows[0]
        value  = rows[1]

        if keyword == 'NODE' or keyword == 'node':
            out_node.append(int(value))
        elif keyword == 'ELEM' or keyword == 'elem':
            out_elem.append(int(value))

    fin.close()


    # output pos file
    # print(out_node)
    # print(out_elem)

    output = 'elnum_physical_num.pos'
    fout = open(output, "w", encoding="utf=8")

    # header
    fout.write('View "Element Number(Physical Tag) or Nodal Number" {\n')

    # nodal number
    command = "T3"
    alignment = 0

    # 節点番号を描画するために読み込まれた節点番号の連番
    seq = 0

    for i in out_node:
        coord_x = nlap._node[i]['x']
        coord_y = nlap._node[i]['y']
        coord_z = 0.0

        # position
        fout.write("{0:s}".format(command))
        fout.write("({0:f},{1:f},{2:f},{3:d})".format(coord_x, coord_y, coord_z, alignment))

        # text
        fout.write('{"')
        fout.write("({0:d}) {1:d}".format(seq, i))
        fout.write('"};\n')

        seq += 1


    # element number
    command = "T3"
    alignment = 0

    # 要素番号を描画するために読み込まれた要素番号の連番
    seq = 0

    for i in out_elem:
        # print(nlap._element[i])
        coord_x = nlap._element[i]['mean_x']
        coord_y = nlap._element[i]['mean_y']
        coord_z = 0.0

        # material number
        mat = nlap._element[i]['mat']

        # position
        fout.write("{0:s}".format(command))
        fout.write("({0:f},{1:f},{2:f},{3:d})".format(coord_x, coord_y, coord_z, alignment))

        # text
        fout.write('{"')
        fout.write("({0:d}) {1:d} ({2:d})".format(seq, i, mat))
        fout.write('"};\n')

        seq += 1


    # End of View
    fout.write('};\n')

    fout.close()
