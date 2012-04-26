all: clean src

src:
	python make.py
	mv pysublim.pyc pysublim
	chmod +x pysublim

clean:
	rm -f pysublim

install:
	cp pysublim /usr/bin/