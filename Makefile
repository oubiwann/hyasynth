VENV=.venv
ACT=./$(VENV)/bin/activate

$(VENV):
	virtualenv $(VENV) \
	--python=`which python2.7` \
	--system-site-packages

deps: $(VENV)
	@. $(ACT) && pip install -r requirements.txt

clean-venv:
	rm -rf $(VENV)

clean:
	@echo

shell: deps
	@. $(ACT) && hy

clean-all: clean clean-venv