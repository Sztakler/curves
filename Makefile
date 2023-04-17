CC=g++
CFLAGS=-lsfml-graphics -lsfml-window -lsfml-system

curves-editor: main.o
	$(CC) -o curves-editor main.o $(CFLAGS)
