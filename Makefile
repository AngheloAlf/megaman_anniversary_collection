SPLAT      := 
SPLAT_YAML := SLUS_208.33.yaml

ifeq ($(SPLAT), )
$(error You need to set a path to splat when invoking make like `make SPLAT="path/to/splat/split.py"`)
endif

$(shell mkdir -p asm bin linker_scripts/auto)


extract:
	$(RM) -r asm bin
	$(SPLAT) $(SPLAT_YAML)
