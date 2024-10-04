################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
ws2812/%.obj: ../ws2812/%.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP430 Compiler'
	"C:/ti/ccs1260/ccs/tools/compiler/ti-cgt-msp430_21.6.1.LTS/bin/cl430" -vmspx --data_model=restricted -Ooff --opt_for_speed=5 --use_hw_mpy=F5 --include_path="C:/ti/ccs1260/ccs/ccs_base/msp430/include" --include_path="C:/ti/msp430ware_3_80_14_01/iqmathlib/include" --include_path="C:/ti/ccs1230/ccs/ccs_base/msp430/include" --include_path="C:/Users/abdulhamit/Desktop/ledBlink" --include_path="C:/ti/ccs1260/ccs/tools/compiler/ti-cgt-msp430_21.6.1.LTS/include" --advice:power="all" --define=__MSP430F67751__ -g --printf_support=minimal --diag_warning=225 --diag_wrap=off --display_error_number --silicon_errata=CPU21 --silicon_errata=CPU22 --silicon_errata=CPU40 --preproc_with_compile --preproc_dependency="ws2812/$(basename $(<F)).d_raw" --obj_directory="ws2812" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


