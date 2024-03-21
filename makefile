
LINE_LENGTH = 160
PY_DIR = .
STRICT = --strict
STRICT =
FILES = t1.py procFunc.py makefile

all: reformat test

reformat: $(FILES)
	black --line-length $(LINE_LENGTH) $(PY_DIR)
	pylama --max-line-length $(LINE_LENGTH) $(PY_DIR)
	mypy $(STRICT) --no-incremental $(PY_DIR)

test: $(FILES)
	./t1.py
