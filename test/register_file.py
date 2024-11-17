# cinco
# procesador de arquitectura RISC-V para el mundo hispano
#
# Licencia Pública Mozilla 2.0 (MPL 2.0)
#
# Este archivo está bajo la Licencia Pública Mozilla 2.0. Puedes usar, modificar 
# y distribuir este código bajo los términos de la MPL 2.0.
#
# Las modificaciones al código fuente deben ser distribuidas bajo los mismos 
# términos de la MPL 2.0. El código modificado debe ser entregado bajo la misma 
# licencia si se distribuye.
#
# Este archivo se distribuye "tal cual", sin garantía alguna, expresa o implícita, 
# incluyendo pero no limitándose a las garantías de comercialización o idoneidad 
# para un propósito específico.
#
# Para más detalles, consulta el archivo LICENSE que acompaña este proyecto.
#
# -----------------------------------------------------------------------------
#
# License: Mozilla Public License 2.0 (MPL 2.0)
#
# This file is under the Mozilla Public License 2.0. You may use, modify, 
# and distribute this code under the terms of the MPL 2.0.
#
# Modifications to the source code must be distributed under the same terms 
# of the MPL 2.0. Modified code must be provided under the same license if 
# distributed.
#
# This file is distributed "as is", without any warranty, express or implied, 
# including but not limited to warranties of merchantability or fitness for a 
# particular purpose.
#
# For more details, please refer to the LICENSE file included with this project.

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
