# See Makefile-commented for explanation
CFLAGS = -Wall -g 
CC     = gcc $(CFLAGS)

PROGRAMS = bl_server bl_client

all : $(PROGRAMS)

server_funcs.o : server_funcs.c blather.h
	     $(CC) -c $<

bl_server.o : bl_server.c blather.h
	     $(CC) -c $< bl_server.c server_funcs.c

bl_client.o : bl_client.c blather.h
	$(CC) -c $< -pthread

bl_server : server_funcs.o bl_server.o
	     $(CC) -o bl_server bl_server.o server_funcs.o

bl_client : bl_client.o
	    $(CC) -o bl_client bl_client.o -pthread

clean:
	rm -f *.o bl_client bl_server test-data/*.fifo test-data/*.out test-data/*.valgrindout test-data/*.expect test-data/*.diff


## TEST TARGETS
TEST_PROGRAMS = test_blather.sh test_blather_data.sh normalize.awk cat_sig.sh filter-semopen-bug.awk 

test : test-blather

make test-blather : bl_client bl_server $(TEST_PROGRAMS)
	chmod u+rx $(TEST_PROGRAMS)
	./test_blather.sh

clean-tests :
	cd test-data && \
	rm -f *.* 


