/*
 * cinco
 * procesador de arquitectura RISC-V para el mundo hispano
 *
 * Mozilla Public License 2.0 (MPL 2.0)
 *
 * Este archivo está bajo la Licencia Pública Mozilla 2.0. Puedes usar, modificar 
 * y distribuir este código bajo los términos de la MPL 2.0.
 *
 * Las modificaciones al código fuente deben ser distribuidas bajo los mismos 
 * términos de la MPL 2.0. El código modificado debe ser entregado bajo la misma 
 * licencia si se distribuye.
 *
 * Este archivo se distribuye "tal cual", sin garantía alguna, expresa o implícita, 
 * incluyendo pero no limitándose a las garantías de comercialización o idoneidad 
 * para un propósito específico.
 *
 * Para más detalles, consulta el archivo LICENSE que acompaña este proyecto.
 *
 * -----------------------------------------------------------------------------
 *
 * License: Mozilla Public License 2.0 (MPL 2.0)
 *
 * This file is under the Mozilla Public License 2.0. You may use, modify, 
 * and distribute this code under the terms of the MPL 2.0.
 *
 * Modifications to the source code must be distributed under the same terms 
 * of the MPL 2.0. Modified code must be provided under the same license if 
 * distributed.
 *
 * This file is distributed "as is", without any warranty, express or implied, 
 * including but not limited to warranties of merchantability or fitness for a 
 * particular purpose.
 *
 * For more details, please refer to the LICENSE file included with this project.
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