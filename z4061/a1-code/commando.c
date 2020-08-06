// util.c: provided functions to ease parsing and pausing.

#include "commando.h"
#define COMMANDO_ECHO 0


int main(int argc, const char* argv[]) {
  // setvbuf(stdout, NULL, _IONBF, 0); // Turn off output buffering
  cmd_t *cmd = NULL;
  cmdcol_t cmdcol = {};
  cmdcol_t *col = &cmdcol;
  _Bool isecho = 0;
  col->size = 0;
  if(argc > 1 && strncmp(argv[1], "--echo",6) == 0) {
    isecho = 1;
  }
  while(1) {
    printf("%s", "@>");
    if(COMMANDO_ECHO != 0) {
      isecho = 1;
    }
    char buf[MAX_LINE];
    char *str = fgets(buf,MAX_LINE,stdin);
    if(str == NULL) {
      printf("\nEnd of input");
      exit(0);
    }
    char * tokens[MAX_LINE];
    int tok = 0;
    int *ntok = &tok;
    parse_into_tokens(buf,tokens,ntok);
    if(*ntok != 0) {
    if((strncmp(tokens[0],"help",4)) == 0) {
      if(isecho) {
	printf(" %s\n", tokens[0]);
      }
	  printf("COMMANDO COMMANDS\n");
	  printf("help               : show this message\n");
	  printf("exit               : exit the program\n");
	  printf("list               : list all jobs that have been started giving information on each\n");
	  printf("pause nanos secs   : pause for the given number of nanseconds and seconds\n");
	  printf("output-for int     : print the output for given job number\n");
	  printf("output-all         : print output for all jobs\n");
	  printf("wait-for int       : wait until the given job number finishes\n");
	  printf("wait-all           : wait for all jobs to finish\n");
printf("command arg1 ...   : non-built-in is run as a job\n");
	}
    else if((strncmp(tokens[0],"exit",4)) == 0) {
      if(isecho) {
	printf(" %s\n", tokens[0]);
      }
	    exit(0);
      }
      else if((strncmp(tokens[0],"list",4)) == 0) {
	if(isecho) {
	printf(" %s\n", tokens[0]);
      }
	cmdcol_print(col);
      }
      else if((strncmp(tokens[0],"pause",5)) == 0) {
	if(isecho) {
	  printf(" %s %s %s\n", tokens[0],tokens[1],tokens[2]);
      }
	if(tokens[1] && tokens[2] != NULL){
	  int sec = atoi(tokens[2]);
	  long pars = atol(tokens[1]);
	  pause_for(pars,sec);
	}
	else {
	  printf("Incorrect Input");
	}
      }
      else if((strncmp(tokens[0],"output-for",10)) == 0) {
	if(tokens[1] != NULL) {
	if(isecho) {
	  printf(" %s %s\n", tokens[0],tokens[1]);
      }
	  int num = atoi(tokens[1]);
	  printf("@<<< Output for %s[#%d] (%d bytes):\n----------------------------------------\n",col->cmd[num]->name, col->cmd[num]->pid,col->cmd[num]->output_size);
	  cmd_print_output(col->cmd[num]);
	  printf("----------------------------------------");
	}
	else {
	  printf("Incorrect input");
	}
      }
      else if((strncmp(tokens[0],"output-all",10)) == 0) {
	if(isecho) {
	printf(" %s\n", tokens[0]);
      }
	int count = 0;
	while(col->cmd[count] != NULL) {
	  cmd_print_output(col->cmd[count]);
	  count +=1;
	}
      }
      else if((strncmp(tokens[0],"wait-for",8)) == 0) {
	if(isecho) {
	  printf(" %s %s\n", tokens[0],tokens[1]);
      }
	if(tokens[1] != NULL) {
	  int num = atoi(tokens[1]);
	  cmd_update_state(col->cmd[num],DOBLOCK);
	  free(col->cmd[num]);
	}
	else {
	  printf("Incorrect input");
	}
      }
      else if((strncmp(tokens[0],"wait-all",8)) == 0) {
	if(isecho) {
	printf(" %s\n", tokens[0]);
      }
	for(int i = 0; i < col->size -1; i++) {
	  cmd_update_state(col->cmd[i],DOBLOCK);
	}
      }
      else {
	cmd = cmd_new(tokens);
	if(isecho) {
	  int count = 0;
	  while(cmd->argv[count] != NULL) {
	    printf(" %s", cmd->argv[count]);
	    count += 1;
	  }
	  printf("\n");
	}
	cmd_start(cmd);
	cmdcol_add(col,cmd);
      }
    }
    else{
      printf("\n");
    }
    cmdcol_update_state(col,NOBLOCK);
  }
 cmdcol_freeall(col);	  
 return 0;
}
