###############################################################################
# Created by write_sdc
###############################################################################
current_design lstm16x_top
###############################################################################
# Timing Constraints
###############################################################################
create_clock -name core_clk -period 100.0000 [get_ports {clk}]
set_propagated_clock [get_clocks {core_clk}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[0]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[1]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[2]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[3]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[4]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[5]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[6]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_data[7]}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {cmd_valid}]
set_input_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rst_n}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[0]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[1]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[2]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[3]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[4]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[5]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[6]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_data[7]}]
set_output_delay 5.0000 -clock [get_clocks {core_clk}] -add_delay [get_ports {rsp_valid}]
set_false_path\
    -from [get_ports {rst_n}]
###############################################################################
# Environment
###############################################################################
###############################################################################
# Design Rules
###############################################################################
