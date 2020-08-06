// File name of currently loaded example (rendered on the bottom of the
// screen for your convenience).
String var; //final string of axiom with rules applied total times
String currentFile; 
int stepsize =2; //how big the image is, adjustable
float x1 = 200; //starting coordinates, adjustable
float y1 = 300;
float ang = 270;
import java.util.*;


/*****************************************************
 * Place variables for describing the L-System here. *
 * These might include the final expansion of turtle *
 * commands, the step size d, etc.                   *
 *****************************************************/
String[] spec;
 
/*
 * This method is automatically called when ever a new L-System is
 * loaded (either by pressing 1 - 6, or 'o' to open a file dialog).
 *
 * The lines array will contain every line from the selected 
 * description file. You can assume it's a valid description file,
 * so it will have a length of 6:
 *
 *   lines[0] = number of production rule applications
 *   lines[1] = angle increment in degrees
 *   lines[2] = initial axiom
 *   lines[3] = production rule for F (or the string 'nil')
 *   lines[4] = production rule for X (or the string 'nil')
 *   lines[5] = production rule for Y (or the string 'nil')
 */
void processLSystem(String[] lines) {
  spec = lines;
  int cycles = Integer.parseInt(spec[0]); //make cycles the int of whatever line 1 is
  String axiom = spec[2];
  String fprod = spec[3];
  String xprod = spec[4];
  String yprod = spec[5];
  var = ""; //set var to empty string in prep for new lsystem
  String temp = axiom;
  for(int i = 0; i < cycles; i++) { //run through process for how many cycles there are
    for(int j = 0; j < temp.length(); j++) {  //parse thru lsystem and add rules
  	  char val = temp.charAt(j);
	    if(val == 'F') {
	  	 var += fprod;
		   }
	    else if(val == 'X') {
	       var += xprod;
	     }
	    else if(val == 'Y') {
	       var += yprod;
	     }
	    else {
	     var += val;
	     }
     }
     temp = var;
     var = "";
  }
  var = temp;
}

/*
 * This method is called every frame after the background has been
 * cleared to white, but before the current file name is written to
 * the screen.
 *
 * It is not called if there is no loaded file.
 */
void drawLSystem() {
  float temp1 = x1;
  float temp2 = y1;
  // Implement your LSystem rendering here
  //ang = 270; //set angle to "up"
  float tang = 270;
  tang = ang;
  float angle = Float.parseFloat(spec[1]); //set angle to float at line 2
  Deque<Float> deque = new ArrayDeque<Float>(); //using arraydeque lib to push/pop
  float x2,y2; //coord for end of each line
  for(int j = 0; j < var.length(); j++) {
    char val = var.charAt(j);//parse thru lsystem
    if(val == 'F') {
       x2 = temp1 + stepsize*cos(radians(tang)); //calc end of line
       y2 = temp2 + stepsize*sin(radians(tang));
       line(temp1,temp2,x2,y2);
       temp1 = x2;
       temp2 = y2;
    }
      else if(val == '+') {
      tang += angle; //increase angle
      }
      else if(val == '-') {
      tang -= angle; //decrease angle
      }
      else if(val == '[') {
        deque.push(temp1); //push coord on stack
        deque.push(temp2);
        deque.push(tang);
      }
      else if(val == ']') { //pop coords off and set equal
        tang = deque.pop();
        temp2 = deque.pop();
        temp1 = deque.pop();
      }
  }
  for(int i = 0; i < 6; i++) {
    text(spec[i], 10, 20 + 15 * i); //display file on screen
  }
   // x1 = temp1;
  //y1 = temp2;
}

void setup() {
  size(500, 500);
}

void draw() {
  background(255);

  if (currentFile != null) {
    drawLSystem();
  }

  fill(0);
  stroke(0);
  textSize(15);
  if (currentFile == null) {
    text("Press [1-6] to load an example, or 'o' to open a dialog", 5, 495);
  } else {
    text("Current l-system: " + currentFile, 5, 495);
  }
  text("WASD control location, Z/X control size, and E/Q to rotate",  5, 475);
}

void keyReleased() {
  /*********************************************************
   * The examples loaded by pressing 1 - 6 must be placed  *
   * in the data folder within your sketch directory.      *
   * The same goes for any of your own files you'd like to *
   * load with relative paths.                             *
   *********************************************************/
   
  if (key == 'o' || key == 'O') {
    // NOTE: This option will not work if you're running the
    // Processing sketch with JavaScript and your browser.
    selectInput("Select a file to load:", "fileSelected");
  } else if (key == '1') {
    loadLSystem("example1.txt");
  } else if (key == '2') {
    loadLSystem("example2.txt");
  } else if (key == '3') {
    loadLSystem("example3.txt");
  } else if (key == '4') {
    loadLSystem("example4.txt");
  } else if (key == '5') {
    loadLSystem("example5.txt");
  } else if (key == '6') {
    loadLSystem("example6.txt");
  } else if (key == '7') {
    loadLSystem("example7.txt");
  } else if (key == 'z') { //control size of image w 'z'/'x'
    stepsize++;
  } else if (key == 'x') {
    if(stepsize > 1) {    // stepsize shouldnt be below zero
      stepsize--;
    }
  } else if (key == 'a') { //control location of image w 'wasd'
    x1 -= 10;
  } else if (key == 's') {
    y1 += 10;
  } else if (key == 'd') {
    x1 += 10;
  } else if (key == 'w') {
    y1 -= 10;
  } else if (key == 'e') {
    ang += 45;
  } else if (key == 'q') {
    ang -= 45;
  }
  // else modify the above code to include
  // keyboard shortcuts for your own examples
}

import java.io.File;
void fileSelected(File selection) {
  if (selection == null) {
    println("File selection cancelled."); 
  } else {
    loadLSystem(selection.getAbsolutePath()); 
  }
}

void loadLSystem(String filename) {
  String[] contents = loadStrings(filename);
  processLSystem(contents);
  currentFile = filename;
}
