VENV=.venv
ACT=./$(VENV)/bin/activate
REQS=requirements.txt

$(VENV):
	virtualenv $(VENV)

deps: $(VENV)
	@for LINE in $(shell cat $(REQS)); do \
		. $(ACT) && pip install $$LINE ; \
	done

hy-shell: deps
	@. $(ACT) && hy

keys: deps
	@. $(ACT) && twistd hyasynth keygen

start: clean
	@. $(ACT) && twistd hyasynth

start-dev: deps clean
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
	@find . -name "*.pyc" -exec rm {} \;

clean-all: clean clean-venv
