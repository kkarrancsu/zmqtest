# Makefile to build the worker
SRC_DIR = .

CC = g++
CFLAGS = -O3 -Wall -I./ -I/usr/local/include 
LIBS = -L/usr/local/lib/ -lzmq


all:
	$(CC) $(CFLAGS) -o test $(SRC_DIR)/test.cpp $(LIBS)
	
clean:
	rm -f test