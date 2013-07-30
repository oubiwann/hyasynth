VENV=.venv
ACT=./$(VENV)/bin/activate
REQS=requirements.txt
SUB_REQS=sub_requirements.txt

$(VENV):
	virtualenv $(VENV) \
	--system-site-packages

deps: $(VENV)
	@. $(ACT) && pip install -r $(REQS)
	@. $(ACT) && pip install -r $(SUB_REQS)

shell: deps
	@. $(ACT) && hy

clean-venv:
	rm -rf $(VENV)

clean:
	@echo

clean-all: clean clean-venv