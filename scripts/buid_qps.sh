#!/usr/bin/env bash

# script to build yasnippets from Quartus Prime Standard(QPS) templates which are located in
# current directory

../quartus_template_parser.py ahdl.tpl          ahdl-mode          qps-
../quartus_template_parser.py q2_tcl_api.tpl    q2-mode_tcl_api    qps-
../quartus_template_parser.py systemverilog.tpl systemverilog-mode qps-
../quartus_template_parser.py sdc.tpl           sdc-mode           qps-
../quartus_template_parser.py tcl.tpl           tcl-mode           qps-
../quartus_template_parser.py verilog.tpl       verilog-mode       qps-
../quartus_template_parser.py vhdl.tpl          vhdl-mode          qps-

echo "* RENAME directory:"
mv -v q2-mode_tcl_api tcl_api-mode
