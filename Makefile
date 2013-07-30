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

hy-shell: deps
	@. $(ACT) && hy

keys: deps
	@. $(ACT) && twistd hyasynth keygen

start:
	@. $(ACT) && twistd hyasynth

start-dev: deps
	@. $(ACT) && twistd -n hyasynth

stop:
	@. $(ACT) && twistd hyasynth stop

shell: deps
	@. $(ACT) && twistd hyasynth shell

clean-venv:
	rm -rf $(VENV)

clean:
	@echo

clean-all: clean clean-venv