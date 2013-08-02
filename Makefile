VENV=.venv
ACT=./$(VENV)/bin/activate
REQS=requirements.txt

$(VENV):
	virtualenv $(VENV) \
	--system-site-packages

deps: $(VENV)
	@. $(ACT) && pip install -r $(REQS)

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
	make start &
	@sleep 3
	@. $(ACT) && twistd hyasynth shell
	make stop

clean-venv:
	rm -rf $(VENV)

clean:
	@echo

clean-all: clean clean-venv