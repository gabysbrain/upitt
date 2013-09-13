CC=g++
CFLAGS=-g -Wall

#all: player
all: player playero

player: player.cpp
	$(CC) $(CFLAGS) -o $@ $<

playero: player.cpp
	$(CC) $(CFLAGS) -DME=O -o $@ $<
    

clean:
	rm -f player

