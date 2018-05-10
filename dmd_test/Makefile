CC=gcc
CFLAGS=-lwiringPi

helloworld: main.o 
	$(CC) -o helloworld main.o oppa_display.o $(CFLAGS)

main.o : main.c oppa_display.o
	gcc -c main.c 

oppa_display.o: oppa_display.c oppa_display.h
	$(CC) -c oppa_display.c

clean:
	rm *.o helloworld
