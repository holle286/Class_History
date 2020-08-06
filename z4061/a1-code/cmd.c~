#include "commando.h"
#include <stdio.h>
#include <string.h>

// cmd.c: functions related the cmd_t struct abstracting a
// command. Most functions maninpulate cmd_t structs.

cmd_t *cmd_new(char *argv[]) {
  cmd_t *cmd = malloc(sizeof(cmd_t));
  int i = 0;
  while(argv[i] != NULL) {
    cmd->argv[i] = strdup(argv[i]);
    i++;
   }
  strcpy(cmd->name,cmd->argv[0]);
  cmd->argv[i] = NULL;
  snprintf(cmd->str_status, STATUS_LEN, "INIT");
  cmd->finished = 0;
  cmd->status = -1;
  cmd->pid = -1;
  cmd->output = NULL;
  cmd->output_size = -1;
  return cmd;
// Allocates a new cmd_t with the given argv[] array. Makes string
// copies of each of the strings contained within argv[] using
// strdup() as they likely come from a source that will be
// altered. Ensures that cmd->argv[] is ended with NULL. Sets the name
// field to be the argv[0]. Sets finished to 0 (not finished yet). Set
// str_status to be "INIT" using snprintf(). Initializes the remaining
// fields to obvious default values such as -1s, and NULLs.
}

void cmd_free(cmd_t *cmd) {
  int i = 0;
  while(cmd->argv[i] != NULL) {
    free(cmd->argv[i]);
    i += 1;
  }
  if(cmd->output != NULL) {
    free(cmd->output);
  }
  free(cmd);
// Deallocates a cmd structure. Deallocates the strings in the argv[]
// array. Also deallocats the output buffer if it is not
// NULL. Finally, deallocates cmd itself.
}

void cmd_start(cmd_t *cmd) {
  pipe(cmd->out_pipe);
  pid_t child = fork();
  snprintf(cmd->str_status, STATUS_LEN, "RUN");
  if(child > 0) {
    cmd->pid = child;
    close(cmd->out_pipe[PWRITE]);
  }
  else {
    dup2(cmd->out_pipe[PWRITE],1);
    execvp(cmd->name,cmd->argv);
    close(cmd->out_pipe[PREAD]);
  }
      
// Forks a process and starts executes command in cmd in the process.
// Changes the str_status field to "RUN" using snprintf().  Creates a
// pipe for out_pipe to capture standard output.  In the parent
// process, ensures that the pid field is set to the child PID. In the
// child process, directs standard output to the pipe using the dup2()
// command. For both parent and child, ensures that unused file
// descriptors for the pipe are closed (write in the parent, read in
// the child).
}

void cmd_update_state(cmd_t *cmd, int block) {
  if(cmd->finished == 1) {
    return;
  }
  int status;
  int pid = waitpid(cmd->pid, &status, block);
  if(pid == -1) {
    exit(0);
  }
  else if(pid == 0) {
    return;
  }
  if(WIFEXITED(status) != 0) {
      cmd->status = WEXITSTATUS(status);
      snprintf(cmd->str_status, STATUS_LEN, "EXIT(%d)", cmd->status);
      cmd->finished = 1;
      cmd_fetch_output(cmd);
      printf("@!!! %s[#%d]: EXIT(%d)\n",cmd->name,cmd->pid,cmd->status);
  }
// If the finished flag is 1, does nothing. Otherwise, updates the
// state of cmd.  Uses waitpid() and the pid field of command to wait
// selectively for the given process. Passes block (one of DOBLOCK or
// NOBLOCK) to waitpid() to cause either non-blocking or blocking
// waits.  Uses the macro WIFEXITED to check the returned status for
// whether the command has exited. If so, sets the finished field to 1
// and sets the cmd->status field to the exit status of the cmd using
// the WEXITSTATUS macro. Calls cmd_fetch_output() to fill up the
// output buffer for later printing.
//
// When a command finishes (the first time), prints a status update
// message of the form
//
// @!!! ls[#17331]: EXIT(0)
//
// which includes the command name, PID, and exit status.
}

char *read_all(int fd, int *nread) {
  ssize_t ret_val;
  char buffer[BUFSIZE];
  char *msg = malloc(BUFSIZE);
  size_t msgbuff = BUFSIZE;
  size_t msgsz = 0;
  while ((ret_val = read(fd, buffer, BUFSIZE)) > 0) {
      memcpy(msg + msgsz, buffer, ret_val);
      msgsz += ret_val;
      if (msgsz == msgbuff) {
          msgbuff += BUFSIZE;

          char *tmp = realloc(msg, msgbuff);

          if (tmp == NULL) {
              perror("Buffer reallocation error");
              exit(EXIT_FAILURE);
          }
          msg = tmp;
      }
  }
  *nread = msgsz;
  msg[msgsz] = '\0';
  return msg;
// Reads all input from the open file descriptor fd. Stores the
// results in a dynamically allocated buffer which may need to grow as
// more data is read.  Uses an efficient growth scheme such as
// doubling the size of the buffer when additional space is
// needed. Uses realloc() for resizing.  When no data is left in fd,
// sets the integer pointed to by nread to the number of bytes read
// and return a pointer to the allocated buffer. Ensures the return
// string is null-terminated. Does not call close() on the fd as this
// is done elsewhere.
}

void cmd_fetch_output(cmd_t *cmd) {
  if(cmd->finished == 0) {
    printf("%s[#%d]not yet finished",cmd->name,cmd->pid);
    return;
  }
  int read = 0;
  int *nread = &read;
  cmd->output = read_all(cmd->out_pipe[PREAD],nread);
  cmd->output_size = read;
  close(cmd->out_pipe[PREAD]);
// If cmd->finished is zero, prints an error message with the format
// 
// ls[#12341] not finished yet
// 
// Otherwise retrieves output from the cmd->out_pipe and fills
// cmd->output setting cmd->output_size to number of bytes in
// output. Makes use of read_all() to efficiently capture
// output. Closes the pipe associated with the command after reading
// all input.
}

void cmd_print_output(cmd_t *cmd) {
  if(cmd->output == NULL) {
    printf("%s[#%d] : output not ready",cmd->name,cmd->pid);
    return;
  }
  //printf("@<<< Output for %s[#%d] (%d bytes):\n",cmd->name, cmd->pid,cmd->output_size);
  write(STDOUT_FILENO,cmd->output,cmd->output_size);
// Prints the output of the cmd contained in the output field if it is
// non-null. Prints the error message
// 
// ls[#17251] : output not ready
//
// if output is NULL. The message includes the command name and PID.
}
