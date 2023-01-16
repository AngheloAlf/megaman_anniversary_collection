SPLAT      := tools/splat/split.py
SPLAT_YAML := SLUS_208.33.yaml

$(shell mkdir -p asm bin linker_scripts/auto)


extract:
	$(RM) -r asm bin
	$(SPLAT) $(SPLAT_YAML)
