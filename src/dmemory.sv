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

module dmemory #(parameter BYTES = 1024)
  (
    input logic clk,
    input logic we,
    input logic [31:0] a,
    input logic [31:0] wd,
    output logic [31:0] rd
  );

  parameter DEPTH = BYTES / 32;
  logic [31:0] ram [DEPTH-1:0];

  // acceso a ram alineado a palabra, los dos primeros bits no tienen efecto
  // las direcciones se expresan en bytes pero la memoria trabaja a nivel de palabra
  assign rd = ram[a[31:2]];

  always_ff @(posedge clk) begin
    if (we) begin
        ram[a[31:2]] <= wd;
    end
  end

endmodule
