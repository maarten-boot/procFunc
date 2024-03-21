
FILES = t1.py procFunc.py

all: reformat test

reformat: $(FILES)
	black .
	mypy .

test: $(FILES)
	./t1.py
