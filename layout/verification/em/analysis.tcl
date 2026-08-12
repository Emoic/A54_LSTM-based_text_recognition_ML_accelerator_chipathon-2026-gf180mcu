# Post-route PDNSim electromigration/current-density analysis.
#
# The shell wrapper sets EM_BASE_ENV to the LibreLane IR-drop step environment
# from the signed-off run and EM_RUN_DIR to an independent output directory.

if {![info exists ::env(EM_BASE_ENV)]} {
    error "EM_BASE_ENV is not set"
}
if {![info exists ::env(EM_RUN_DIR)]} {
    error "EM_RUN_DIR is not set"
}

source $::env(EM_BASE_ENV)

set ::env(STEP_ID) OpenROAD.EMCurrentDensity
set ::env(STEP_DIR) $::env(EM_RUN_DIR)
set ::env(SCRIPTS_DIR) /usr/local/lib/python3.12/dist-packages/librelane/scripts

# LibreLane normally supplies these derived variables through a temporary Tcl
# environment file.  This standalone post-route run recreates the small subset
# needed by read_current_odb for the default power-analysis corner.
set ::env(_TCL_ENV_IN) /dev/null
set default_lib /foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/lib/gf180mcu_fd_sc_mcu7t5v0__tt_025C_5v00.lib
set ::env(_LIB_CORNER_0) [list $::env(DEFAULT_CORNER) $default_lib]
set ::env(_SDC_IN) $::env(PNR_SDC_FILE)
set ::env(_PNR_EXCLUDED_CELLS) [list \
    gf180mcu_fd_sc_mcu7t5v0__mux2_1 \
    gf180mcu_fd_sc_mcu7t5v0__oai33_2 \
    gf180mcu_fd_sc_mcu7t5v0__nor2_1 \
    gf180mcu_fd_sc_mcu7t5v0__nor3_1]

file mkdir $::env(STEP_DIR)

source $::env(SCRIPTS_DIR)/openroad/common/io.tcl
read_current_odb

source $::env(SCRIPTS_DIR)/openroad/common/set_power_nets.tcl
source $::env(SCRIPTS_DIR)/openroad/common/set_rc.tcl
read_spef $::env(CURRENT_SPEF_DEFAULT_CORNER)

puts "=== OpenROAD PDNSim EM/current-density analysis ==="
puts "Base ODB: $::env(CURRENT_ODB)"
puts "Base SPEF: $::env(CURRENT_SPEF_DEFAULT_CORNER)"

foreach net $::env(VDD_NETS) {
    set_pdnsim_net_voltage -net $net -voltage $::env(LIB_VOLTAGE)
    set args [list \
        -net $net \
        -voltage_file $::env(STEP_DIR)/voltage-$net.csv \
        -error_file $::env(STEP_DIR)/grid-errors-$net.rpt \
        -enable_em \
        -em_outfile $::env(STEP_DIR)/em-$net.csv]
    log_cmd analyze_power_grid {*}$args
}

foreach net $::env(GND_NETS) {
    set_pdnsim_net_voltage -net $net -voltage 0
    set args [list \
        -net $net \
        -voltage_file $::env(STEP_DIR)/voltage-$net.csv \
        -error_file $::env(STEP_DIR)/grid-errors-$net.rpt \
        -enable_em \
        -em_outfile $::env(STEP_DIR)/em-$net.csv]
    log_cmd analyze_power_grid {*}$args
}

puts "=== EM/current-density analysis completed ==="
