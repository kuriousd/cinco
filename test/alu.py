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
from cocotb.regression import TestFactory
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_alu(dut):

    # Prueba con varios valores de a y b para enteros de 4-bit con signo
    for control in range(0, 4):
        for a in range(-7, 8):
            for b in range(-7, 8):
                
                dut.alu_control.value = control
                dut.a.value = a
                dut.b.value = b

                await Timer(2, units='ns')

                if control == 0:
                    esperado = a + b
                elif control == 1:
                    esperado = a - b
                elif control == 2:
                     esperado = a & b
                else:
                     esperado = a | b

                if esperado < 0:
                    n_flag = 1
                else:
                    n_flag = 0

                if esperado == 0:
                    z_flag = 1
                else:
                    z_flag = 0
                
                signed_dut = int(dut.result.value) - 2**32 if int(dut.result.value) >= 2**31 else int(dut.result.value)
                assert signed_dut == esperado, f"Error: CTRL={control}, A={a}, B={b}, dut={dut.result.value}, esperado={esperado}"
                assert dut.n.value == n_flag, f"Error: CTRL={control}, A={a}, B={b}, dut={dut.n.value}, esperado={n_flag}"
                assert dut.z.value == z_flag, f"Error: CTRL={control}, A={a}, B={b}, dut={dut.n.value}, esperado={z_flag}"

@cocotb.test()
async def test_alu_carry(dut):

        dut.a.value = -1
        dut.b.value = 1
        dut.alu_control.value = 0
        await Timer(2, units="ns")
        assert dut.c.value == 1, f"Carry Suma: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

        dut.a.value = -2
        dut.b.value = 1
        dut.alu_control.value = 0
        await Timer(2, units="ns")
        assert dut.c.value == 0, f"SIN Carry Suma: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

        dut.a.value = -1
        dut.b.value = 2
        dut.alu_control.value = 1
        await Timer(2, units="ns")
        assert dut.c.value == 1, f"Carry Resta: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

        dut.b.value = 3
        dut.a.value = 1
        dut.alu_control.value = 1
        await Timer(2, units="ns")
        assert dut.c.value == 0, f"SIN Carry Resta: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

@cocotb.test()
async def test_alu_overflow(dut):
        # Suma de dos valores de mismo signo
        dut.a.value = 0x7fffffff
        dut.b.value = 0x7fffffff
        dut.alu_control.value = 0
        await Timer(2, units="ns")
        assert dut.v.value == 1, f"Overflow Suma: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

        # Suma de dos valores de mismo signo
        dut.a.value = 0x80000000
        dut.b.value = 0x7fffffff
        dut.alu_control.value = 1
        await Timer(2, units="ns")
        assert dut.v.value == 1, f"Overflow Resta: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

        # Operación no provoca overflow (AND)
        dut.a.value = 2**31
        dut.b.value = 2**31
        dut.alu_control.value = 2
        await Timer(2, units="ns")
        assert dut.v.value == 0, f"Overflow AND: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

        # Operación no provoca overflow (OR)
        dut.a.value = 2**31
        dut.b.value = 2**31
        dut.alu_control.value = 3
        await Timer(2, units="ns")
        assert dut.v.value == 0, f"Overflow OR: a={hex(dut.a.value)}, b={hex(dut.b.value)}, resultado={hex(dut.result.value)}"

# Slt (set if less than): Nivel alto si a < b
@cocotb.test()
async def test_alu_slt(dut):
    dut.alu_control.value = 5
    for a in range(-7, 7):
        for b in range(-7, 7):
            dut.a.value = a
            dut.b.value = b

            await Timer(2, units='ns')

            lt_esperado = 1 if a < b else 0
            assert dut.result.value == lt_esperado, f"SLT Error: A={a}, B={b}, lt_dut={dut.result.value}, lt_esperado={lt_esperado}"

    dut.a.value = 0x80000000
    dut.b.value = 0x7fffffff

    await Timer(2, units='ns')

    assert dut.result.value == 1, f"SLT Error: A={a}, B={b}, lt_dut={dut.result.value}, lt_esperado={lt_esperado}"