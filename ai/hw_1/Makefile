CC=g++
CFLAGS=-g -Wall

all: puzzle gen_puzzle

puzzle: puzzle.cpp
	$(CC) $(CFLAGS) -o $@ $<

gen_puzzle: gen_puzzle.cpp
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f puzzle gen_puzzle

