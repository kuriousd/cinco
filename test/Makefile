#
# cinco
# procesador de arquitectura RISC-V para el mundo hispano
#
# Copyright 2024 by Fernando Domínguez (kurious_d@proton.me)
#
# This source describes Open Hardware and is licensed under the CERN-OHL-W v2
#
# You may redistribute and modify this documentation and make products using it
# under the terms of the CERN-OHL-W v2 (https:/cern.ch/cern-ohl).This
# documentation is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY,
# INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A
# PARTICULAR PURPOSE. Please see the CERN-OHL-W v2 for applicable conditions.
#
# Source location: hhttps://github.com/kuriousd/cinco
#
# As per CERN-OHL-W v2 section 4.1, should You produce hardware based on these
# sources, You must maintain the Source Location visible on the external case
# of the FPGA Cores or other product you make using this documentation.
#
 
# Basado en iverilog
SIM = icarus
TOPLEVEL_LANG = verilog

# Todos los fuentes de system verilog
VERILOG_SOURCES += ../src/alu.sv
VERILOG_SOURCES += ../src/register_file.sv

alu:
	$(MAKE) sim MODULE=$@ TOPLEVEL=$@ WAVES=1

register_file:
	$(MAKE) sim MODULE=$@ TOPLEVEL=$@ WAVES=1

include $(shell cocotb-config --makefiles)/Makefile.sim