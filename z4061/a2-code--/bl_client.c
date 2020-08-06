#include <pthread.h>
#include "simpio.c"
#include "util.c"

void* to_client(void *c);
void* to_server(void *c);


simpio_t simpio_actual;
simpio_t *simpio = &simpio_actual;
pthread_t client_thread;
pthread_t server_thread;

int main(int argc, char* argv[])
{
  client_t client;
  join_t join;
  memset(&client,0,sizeof(client_t));
  memset(&join,0,sizeof(join_t));
  char *servername = argv[1];
  char *username = argv[2];
  char buffer[50];
  strcpy(buffer,servername);
  strcat(buffer, ".fifo");
  sprintf(client.to_client_fname, "%d.fifo", getpid());
  sprintf(client.to_server_fname, "%d.fifo", getpid()*2);
  mkfifo(client.to_client_fname, DEFAULT_PERMS);
  mkfifo(client.to_server_fname, DEFAULT_PERMS);
  int fd_client = open(client.to_client_fname, O_RDWR);
  int fd_server = open(client.to_server_fname, O_RDWR);
  client.to_client_fd = fd_client;
  client.to_server_fd = fd_server;
  strcpy(client.name,username);
  strcpy(join.name,client.name);
  strcpy(join.to_client_fname,client.to_client_fname);
  strcpy(join.to_server_fname,client.to_server_fname);
  int fd = open(buffer, O_RDWR);
  write(fd, &join, sizeof(join_t));
  char prompt[MAXNAME];
  char input[20] = "";
  strcat(input, client.name);
  strcat(input, ">>");
  snprintf(prompt, MAXNAME, input); // create a prompt string
  simpio_set_prompt(simpio, prompt);         // set the prompt
  simpio_reset(simpio);                      // initialize io
  simpio_noncanonical_terminal_mode();
  //iprintf(simpio, "hello%s\n", username);
  pthread_create(&client_thread, NULL, to_server, &client);
  pthread_create(&server_thread, NULL, to_client, &client);
  pthread_join(client_thread, NULL);
  pthread_join(server_thread, NULL);
  remove(client.to_client_fname);
  remove(client.to_server_fname);
  simpio_reset_terminal_mode();
}

void *to_server(void *c) {
  client_t *client = (client_t *) c;
  while(!simpio->end_of_input) {
    simpio_reset(simpio);
    iprintf(simpio, "");
    while(!simpio->line_ready && !simpio->end_of_input) {
      simpio_get_char(simpio);
    }
    if(simpio->line_ready) {
      mesg_t msg;
      memset(&msg, 0, sizeof(mesg_t));
      msg.kind = BL_MESG;
      strcpy(msg.name,client->name);
      strcpy(msg.body,simpio->buf);
      write(client->to_server_fd, &msg, sizeof(mesg_t));
     }
    //simpio_reset(simpio);
    }
  pthread_cancel(server_thread);
  mesg_t mesg;
  memset(&mesg, 0, sizeof(mesg_t));
  mesg.kind = BL_DEPARTED;
  strcpy(mesg.name,client->name);
  write(client->to_server_fd, &mesg, sizeof(mesg_t));
  
  return NULL;
}

void *to_client(void *c) {
  client_t *client = (client_t *) c;
  struct timeval tv;
  tv.tv_sec = 0;
  tv.tv_usec = 2;
  while(1) {
    mesg_t msg;
    memset(&msg, 0, sizeof(mesg_t));
    //simpio_reset(simpio);
    //iprintf(simpio, "");
    fd_set read_set;
    FD_ZERO(&read_set);
    FD_SET(client->to_client_fd, &read_set);
    select(client->to_client_fd+1, &read_set, NULL, NULL, &tv);
    if(FD_ISSET(client->to_client_fd, &read_set)) {
      //iprintf(simpio, "HERHEHREHRHER");
      fcntl(client->to_client_fd, F_SETFL, O_NONBLOCK);
      read(client->to_client_fd, &msg, sizeof(mesg_t));
      //iprintf(simpio, "%s", client->to_client_fname);
      if (msg.kind == BL_MESG) {
	iprintf(simpio, "[%s] : %s\n", msg.name, msg.body);
	simpio_reset(simpio);
      }
      else if(msg.kind == BL_JOINED) {
	iprintf(simpio, "-- %s JOINED --\n", msg.name);
	simpio_reset(simpio);
      }
      else if(msg.kind == BL_DEPARTED || msg.kind == BL_DISCONNECTED) {
	iprintf(simpio, "-- %s DEPARTED --\n", msg.name);
	simpio_reset(simpio);
      }
      else if(msg.kind == BL_SHUTDOWN) {
	break;
      }
      msg.kind = 0;
      write(client->to_server_fd, &msg, sizeof(mesg_t));
    }
  }
simpio_reset(simpio);
iprintf(simpio, "!!! server is shutting down !!!\n");
pthread_cancel(client_thread);
return NULL;
}


		 
//read name of server and name of user from command line args
//create to-server and to-client FIFOs
//write a join_t request to the server FIFO
//start a user thread to read inpu
//start a server thread to listen to the server
//wait for threads to return
//restore standard terminal output

//user thread{
//  repeat:
//    read input using simpio
//    when a line is ready
//    create a mesg_t with the line and write it to the to-server FIFO
//  until end of input
//  write a DEPARTED mesg_t into to-server
//  cancel the server thread

//server thread{
//  repeat:
//    read a mesg_t from to-client FIFO
//    print appropriate response to terminal with simpio
//  until a SHUTDOWN mesg_t is read
//  cancel the user thread


