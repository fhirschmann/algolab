#-*- mode: makefile -*-
MAIN = proposal

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	pdflatex --shell-escape $<
	pdflatex --shell-escape $<

LOGS = $(wildcard *.log)
AUXS = $(wildcard *.aux)
PREVIEW = $(wildcard *.prv)

clean:
	-rm -f $(LOGS)
	-rm -f $(AUXS)
	-rm -rf $(PREVIEW)

clean-all: clean
	-rm -f $(MAIN).pdf
