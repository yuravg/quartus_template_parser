#!/usr/bin/env bash

# script to build yasnippets from Quartus Prime Professional(QPP) templates which are located in
# current directory

../quartus_template_parser.py q2_tcl_api.tpl    q2-mode_tcl_api    qpp-
../quartus_template_parser.py systemverilog.tpl systemverilog-mode qpp-
../quartus_template_parser.py sdc.tpl           sdc-mode           qpp-
../quartus_template_parser.py tcl.tpl           tcl-mode           qpp-
../quartus_template_parser.py verilog.tpl       verilog-mode       qpp-
../quartus_template_parser.py vhdl.tpl          vhdl-mode          qpp-

echo "* RENAME directory:"
mv -v q2-mode_tcl_api tcl_api-mode
