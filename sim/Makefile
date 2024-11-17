
# Basado en iverilog
SIM = icarus
TOPLEVEL_LANG = verilog

# Todos los fuentes de system verilog
VERILOG_SOURCES = ../src/register_file.sv

register_file:
	$(MAKE) sim MODULE=$@ TOPLEVEL=$@ WAVES=1

include $(shell cocotb-config --makefiles)/Makefile.sim