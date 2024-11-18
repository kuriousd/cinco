/*
 * cinco
 * procesador de arquitectura RISC-V para el mundo hispano
 *
 * Copyright 2024 by Fernando Domínguez (kurious_d@proton.me)
 *
 * This source describes Open Hardware and is licensed under the CERN-OHL-W v2
 *
 * You may redistribute and modify this documentation and make products using it
 * under the terms of the CERN-OHL-W v2 (https:/cern.ch/cern-ohl).This
 * documentation is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY,
 * INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A
 * PARTICULAR PURPOSE. Please see the CERN-OHL-W v2 for applicable conditions.
 *
 * Source location: hhttps://github.com/kuriousd/cinco
 *
 * As per CERN-OHL-W v2 section 4.1, should You produce hardware based on these
 * sources, You must maintain the Source Location visible on the external case
 * of the FPGA Cores or other product you make using this documentation.
 */

module alu (
    input logic [31:0] a,
    input logic [31:0] b,
    input logic [2:0] alu_control,
    output logic [31:0] result,
    output logic v,
    output logic c,
    output logic n,
    output logic z
    );

  // b negado para selección de resta en función
  // del primer bit del control
  logic [31:0] b_op;
  assign b_op = alu_control[0] ? ~b : b;

  logic c_out; //desborde de suma
  logic [31:0] sum;
  assign {c_out, sum} = a + b_op + alu_control[0];

  logic is_sum;
  assign is_sum = ~alu_control[1];

  /*
  desborde (overflow) es nivel alto cuando ocurren
  las tres condiciones:
  - A y B suman o restan (alu_control[1]=0)
  - A y sum tienen signos opuestos
  - A y B tienen mismo signo y se hace suma
    (alu_control[0]=0) el overflow es posible
  */
  assign v = (is_sum) & (sum[31] ^ a[31]) & ~(alu_control[0] ^ a[31] ^ b[31]);

  /*
  carry es a nivel alto cuando el sumador se activa cuando
  hay carry desde la suma y se ordena operación que implique suma
  alu_control[1]=0
  */
  assign c = c_out & is_sum;

  /*
  negativo (negative) es a nivel alto si result[31] es alto
  */
  assign n = result[31];

  /*
  cero (zero) si result es igual a cero
  */
  assign z = ~|result;

  /*
  resultado desde multiplexor en función del control
  */
  always @*
  begin
    case (alu_control)
      3'b001:
        result = sum;
      3'b010:
        result = a & b;
      3'b011:
        result = a | b;
      3'b101:
        result = v ^ sum[31];
      default:
        result=sum;
    endcase

  end


endmodule
