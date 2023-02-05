# VerilogTestBenchGenerator
python program that reads a file containing a verilog design then generates a complete testbench 
for the design.

* Instantiation of the design is generated.

* If the design contains a sequential element a clock signal is generated.

* Directed and random stimulus both are generated (random stimulus is generated using $random
verilog function).

* Conditional statements are taken into account when generating stimulus ensuring full 
branch coverage.

* monitoring statements (ex. $monitor) are generated for inputs and outputs.






