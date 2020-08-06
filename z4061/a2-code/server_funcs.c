#include "blather.h"

client_t *server_get_client(server_t *server, int idx) {
  if(idx > MAXCLIENTS) {
    exit(1);
  }
  //client_t* client = server->client[idx];
  return &server->client[idx];
}
// Gets a pointer to the client_t struct at the given index. If the
// index is beyond n_clients, the behavior of the function is
// unspecified and may cause a program crash.

void server_start(server_t *server, char *server_name, int perms) {
  strcpy(server->server_name,server_name);
  remove("server_name.fifo");
  mkfifo("server_name.fifo", DEFAULT_PERMS);
  int fd_join = open("server_name.fifo", O_RDWR);
  server->join_fd = fd_join;
}
// Initializes and starts the server with the given name. A join fifo
// called "server_name.fifo" should be created. Removes any existing
// file of that name prior to creation. Opens the FIFO and stores its
// file descriptor in join_fd._
//
// ADVANCED: create the log file "server_name.log" and write the
// initial empty who_t contents to its beginning. Ensure that the
// log_fd is position for appending to the end of the file. Create the
// POSIX semaphore "/server_name.sem" and initialize it to 1 to
// control access to the who_t portion of the log.

void server_shutdown(server_t *server) {
  mesg_t msg;
  msg.kind = BL_SHUTDOWN;
  strcpy(msg.name,"SHUTDOWN");
  for(int i = server->n_clients-1; i >= 0; i--)
    {
    int fd = server->client[i].to_client_fd;
    write(fd, &msg, sizeof(mesg_t));
    remove(server->client[i].name);
    }
  close(server->join_fd);
  remove("server_name.fifo");
}
// Shut down the server. Close the join FIFO and unlink (remove) it so
// that no further clients can join. Send a BL_SHUTDOWN message to all
// clients and proceed to remove all clients in any order.
//
// ADVANCED: Close the log file. Close the log semaphore and unlink
// it.

int server_add_client(server_t *server, join_t *join) {
  if(server->n_clients >= MAXCLIENTS) {
    return 1;
  }
  client_t client;
  memset(&client, 0, sizeof(client_t));
  memcpy(client.name,join->name,sizeof(*join->name));
  memcpy(client.to_client_fname,join->to_client_fname, sizeof(*join->to_client_fname));
  memcpy(client.to_server_fname,join->to_server_fname, sizeof(*join->to_server_fname));
  client.data_ready = 0;
  client.to_client_fname[sizeof(client.to_client_fname)] = 0;
  client.to_server_fname[sizeof(client.to_server_fname)] = 0;
  client.to_client_fd = open(client.to_client_fname, O_RDWR);
  client.to_server_fd = open(client.to_server_fname, O_RDWR);
  server->client[server->n_clients] = client;
  server->n_clients += 1;
  return 0;
}
// Adds a client to the server according to the parameter join which
// should have fileds such as name filed in.  The client data is
// copied into the client[] array and file descriptors are opened for
// its to-server and to-client FIFOs. Initializes the data_ready field
// for the client to 0. Returns 0 on success and non-zero if the
// server as no space for clients (n_clients == MAXCLIENTS).

int server_remove_client(server_t *server, int idx) {
  if(idx > server->n_clients || idx < 0) {
    exit(1);
  }
  close(server->client[idx].to_client_fd);
  close(server->client[idx].to_server_fd);
  remove(server->client[idx].to_client_fname);
  remove(server->client[idx].to_server_fname);
  for(int i = idx -1; i < server->n_clients-1; i++) {
    server->client[i] = server->client[i+1];
  }
  server->n_clients -= 1;
  return 0;
  
}
// Remove the given client likely due to its having departed or
// disconnected. Close fifos associated with the client and remove
// them.  Shift the remaining clients to lower indices of the client[]
// preserving their order in the array; decreases n_clients.

int server_broadcast(server_t *server, mesg_t *mesg) {
  for(int i = server->n_clients-1; i >= 0; i--)
    {
    int fd = server->client[i].to_client_fd;
    write(fd, &mesg, sizeof(mesg_t));
    }
  return 0;
}
// Send the given message to all clients connected to the server by
// writing it to the file descriptors associated with them.
//
// ADVANCED: Log the broadcast message unless it is a PING which
// should not be written to the log.

void server_check_sources(server_t *server) {
  fd_set read_set;
  FD_ZERO(&read_set);
  server->join_ready = 1;
  if(server->n_clients == 0) {
    return;
  }
  int maxfd = server->client[0].to_server_fd;
  for(int i = 0; i < server->n_clients; i++) {
    int fd = server->client[i].to_server_fd;
    FD_SET(fd, &read_set);
    server->client[i].data_ready = 1;
    maxfd = (maxfd < fd) ? fd : maxfd;
  }
  select(maxfd+1, &read_set, NULL, NULL, NULL);
}
// Checks all sources of data for the server to determine if any are
// ready for reading. Sets the servers join_ready flag and the
// data_ready flags of each of client if data is ready for them.
// Makes use of the select() system call to efficiently determine
// which sources are ready.

int server_join_ready(server_t *server) {
  return server->join_ready;
}
// Return the join_ready flag from the server which indicates whether
// a call to server_handle_join() is safe.

int server_handle_join(server_t *server) {
  //dbg_printf("GOT HERE SOMEHOW");
  join_t join;
  memset(&join, 0, sizeof(join_t));
  read(server->join_fd, &join, sizeof(join_t));
  server_add_client(server, &join);
  server->join_ready = 0;
  return 0;
}
// Call this function only if server_join_ready() returns true. Read a
// join request and add the new client to the server. After finishing,
// set the servers join_ready flag to 0.

int server_client_ready(server_t *server, int idx) {
  return server->client[idx].data_ready;
}
// Return the data_ready field of the given client which indicates
// whether the client has data ready to be read from it.

int server_handle_client(server_t *server, int idx) {
  mesg_t msg;
  memset(&msg,0,sizeof(mesg_t));
  read(server->client[idx].to_server_fd, &msg, sizeof(mesg_t));
  if(msg.kind == BL_MESG || msg.kind == BL_DEPARTED || BL_JOINED) {
    server_broadcast(server, &msg);
  }
  server->client[idx].data_ready = 0;
  return 0;
}
// Process a message from the specified client. This function should
// only be called if server_client_ready() returns true. Read a
// message from to_server_fd and analyze the message kind. Departure
// and Message types should be broadcast to all other clients.  Ping
// responses should only change the last_contact_time below. Behavior
// for other message types is not specified. Clear the client's
// data_ready flag so it has value 0.
//
// ADVANCED: Update the last_contact_time of the client to the current
// server time_sec.

void server_tick(server_t *server);
// ADVANCED: Increment the time for the server

void server_ping_clients(server_t *server);
// ADVANCED: Ping all clients in the server by broadcasting a ping.

void server_remove_disconnected(server_t *server, int disconnect_secs);
// ADVANCED: Check all clients to see if they have contacted the
// server recently. Any client with a last_contact_time field equal to
// or greater than the parameter disconnect_secs should be
// removed. Broadcast that the client was disconnected to remaining
// clients.  Process clients from lowest to highest and take care of
// loop indexing as clients may be removed during the loop
// necessitating index adjustments.

void server_write_who(server_t *server);
// ADVANCED: Write the current set of clients logged into the server
// to the BEGINNING the log_fd. Ensure that the write is protected by
// locking the semaphore associated with the log file. Since it may
// take some time to complete this operation (acquire semaphore then
// write) it should likely be done in its own thread to preven the
// main server operations from stalling.  For threaded I/O, consider
// using the pwrite() function to write to a specific location in an
// open file descriptor which will not alter the position of log_fd so
// that appends continue to write to the end of the file.

void server_log_message(server_t *server, mesg_t *mesg);
// ADVANCED: Write the given message to the end of log file associated
// with the server.