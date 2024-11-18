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

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly, Timer

import random

@cocotb.test()
async def test_zero(dut):
    # escribir en el registro x0 no debe tener efecto
    # x0 tiene que devolver siempre 0
    cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())
    dut.we.value = 0
    dut.a1.value = 0
    dut.a2.value = 0
    dut.a3.value = 0
    await RisingEdge(dut.clk)
    dut.we.value = 1
    dut.wd3.value = random.randint(0,2**32-1)
    await RisingEdge(dut.clk)
    assert dut.rd1.value==0
    assert dut.rd2.value==0
    
@cocotb.test()
async def test_lectura_escritura(dut):
    # las lecturas son combinacionales
    # la escritura secuencial
    cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())
    dut.we.value = 1
    dut.a1.value = 0
    dut.a2.value = 0
    await RisingEdge(dut.clk)
    # escribe todos los registros
    for i in range(0,32):
        dut.we.value = 1
        dut.a3.value = i
        dut.wd3.value = i
        await RisingEdge(dut.clk)
        
    # comprueba lectura combinacional de todos los registros
    for i in range(0,32):
        await Timer(1, units='ns')
        dut.a1.value = i
        dut.a2.value = 31-i
        await ReadOnly()
        assert dut.rd1.value==i
        assert dut.rd2.value==31-i
        
@cocotb.test()
async def test_lectura_no_escritura(dut):
    # bajando we y escribiendo distintos valores
    # se deben leer los valores anteriores
    cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())
    dut.we.value = 1
    dut.a1.value = 0
    dut.a2.value = 0
    await RisingEdge(dut.clk)
    # escribe todos los registros
    for i in range(0,32):
        dut.we.value = 0
        dut.a3.value = i
        dut.wd3.value = 31-i
        await RisingEdge(dut.clk)
        
    # comprueba lectura combinacional de todos los registros
    for i in range(0,32):
        await Timer(1, units='ns')
        dut.a1.value = i
        dut.a2.value = 31-i
        await ReadOnly()
        assert dut.rd1.value==i
        assert dut.rd2.value==31-i
