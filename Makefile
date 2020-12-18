DAYS := $(find . -type d -name "day-*")

.PHONY: run
run:
	$(MAKE) run -C day-one
	$(MAKE) run -C day-two
	$(MAKE) run -C day-three
	$(MAKE) run -C day-four
	$(MAKE) run -C day-five
	$(MAKE) run -C day-six
	$(MAKE) run -C day-seven
	$(MAKE) run -C day-eight
	$(MAKE) run -C day-nine
	$(MAKE) run -C day-ten
	$(MAKE) run -C day-eleven
	$(MAKE) run -C day-twelve
	$(MAKE) run -C day-thirteen
	$(MAKE) run -C day-fourteen
	$(MAKE) run -C day-fifteen
	$(MAKE) run -C day-sixteen
	$(MAKE) run -C day-seventeen

.PHONY: partone
partone:
	$(MAKE) partone -C day-one
	$(MAKE) partone -C day-two
	$(MAKE) partone -C day-three
	$(MAKE) partone -C day-four
	$(MAKE) partone -C day-five
	$(MAKE) partone -C day-six
	$(MAKE) partone -C day-seven
	$(MAKE) partone -C day-eight
	$(MAKE) partone -C day-nine
	$(MAKE) partone -C day-ten
	$(MAKE) partone -C day-eleven
	$(MAKE) partone -C day-twelve
	$(MAKE) partone -C day-thirteen
	$(MAKE) partone -C day-fourteen
	$(MAKE) partone -C day-fifteen
	$(MAKE) partone -C day-sixteen
	$(MAKE) partone -C day-seventeen

.PHONY: parttwo
parttwo:
	$(MAKE) parttwo -C day-one
	$(MAKE) parttwo -C day-fifteen
	$(MAKE) parttwo -C day-seventeen

