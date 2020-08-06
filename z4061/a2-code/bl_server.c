//#include "blather.h"
#include "util.c"

int signaled = 0;

server_t server;

int handle_signals(int signo) {
  server_shutdown(&server);
  signaled = 1;
  return 0;
}

int main() {
  memset(&server, 0,sizeof(server_t));
  //DEBUG = 1;
  struct sigaction my_sa = {};
  my_sa.sa_handler = handle_signals;
  sigemptyset(&my_sa.sa_mask);
  my_sa.sa_flags = SA_RESTART;
  sigaction(SIGTERM, &my_sa, NULL);
  sigaction(SIGINT, &my_sa, NULL);
  while(!signaled) {
    server_check_sources(&server);
    //dbg_printf("GOTTEEM");
    if(server_join_ready(&server)) {
      server_handle_join(&server);
    }
    for(int i = 0; i < server.n_clients; i++) {
      if(server_client_ready(&server, i)) {
	server_handle_client(&server,i);
      }
    }
  }
  return 0;
}
