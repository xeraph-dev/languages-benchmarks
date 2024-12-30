# Copyright 2024 xeraph. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

.PHONY: all clean

CC = cc
LIBS = openssl
OPT = -O3 -march=native -flto

all: $(patsubst %.c, %, $(wildcard *.c))

clean:
	rm -f *.out

%: %.c
	$(CC) `pkg-config --cflags --libs $(LIBS)` -pthread $(OPT) -std=c99 -Wall -Wextra -Werror -pedantic -o $@.out $^
