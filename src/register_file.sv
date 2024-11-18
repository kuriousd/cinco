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

 module register_file (
    input logic clk,
    input logic we,
    input logic [4:0] a1,
    input logic [4:0] a2,
    input logic [4:0] a3,
    output logic [31:0] rd1,
    output logic [31:0] rd2,
    output logic [31:0] wd3
 );
    // 32 registros de 32 bits, por definición de la isa riscv
    logic [31:0] reg_file[31:0];
    logic [31:0] debug;

    // dos puertos de lectura combinacionales
    // por definición de isa, el registro x0 (zero) devuelve ceros a su lectura 
    assign rd1 = (a1 != 0) ? reg_file[a1] : 32'b0;
    assign rd2 = (a2 != 0) ? reg_file[a2] : 32'b0;
    
    // un puerto de escritura secuencial
    always_ff @(posedge clk) begin
        if (we) begin
            reg_file[a3] <= wd3;
            debug <= wd3;
        end
    end
 endmodule