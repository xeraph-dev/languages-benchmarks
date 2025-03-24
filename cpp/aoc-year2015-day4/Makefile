LIBS=openssl
LDFLAGS=`pkg-config --libs $(LIBS)`
CPPFLAGS=`pkg-config --cflags $(LIBS)`
STD=-std=gnu++23
FLAGS=-O2 -DNDEBUG

SECRET=yzbqklnj

all:
	clang++ $(CPPFLAGS) $(LDFLAGS) $(STD) $(FLAGS) -o main main.cpp
	strip ./main

five: all
	./main $(SECRET) 5

six: all
	./main $(SECRET) 6

seven: all
	./main $(SECRET) 7