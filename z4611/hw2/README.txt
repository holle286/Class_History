This download is a template that is intended to help you get started on Program 2 in CSCI 4611.  It consists of several files.

Three of the files are libraries provided by the textbook author, which are used by the template and will also be useful for developing your solution.  You will often see them used in examples from the textbook.
    initShaders.js
    MV.js
    webgl-utils.js

One of the files simply consists of some hard-coded vertex data that you can use to test your rendering code before you get the surface-of-revolution generation part working.  The template is set up to use this data by default.  
    hardcodedVertices.js
    
The remaining files are where you should implement your solution:
    program2.html
    program2.js
    
The only thing you need to do in program2.html is create a 3D vertex shader.  As described in the program writeup, it works better when hosting the files locally to include the shader as a script in the HTML file, rather than as a seprate file.  You will find a simple 2D vertex shader has already been implemented which will be useful for draw mode; however, this vertex shader will be insufficient for the 3D view mode.  A simple fragment shader has also been provided for you on this project, so all you need to do is write the 3D vertex shader.

The remainder of the program will be completed in program2.js.  The outline of this program is as follows:
    - The user interacts with the draw mode of the program to set the control points.  This interaction is handled using Javascript events that are registered in a function called initWindowEvents().
    - When the user enters the view mode of the program, a function called getControlPoints() is called to retrieve the control points that were specified in draw mode.  Then, these control points are passed to another function called buildSurfaceOfRevolution() which uses these control points to generate the vertices of a surface of revolution and pass them to a vertex buffer object on the graphics card.
    - While in the view mode of the program, the user can interact with the 3D object using the mouse and keyboard.  As with the draw mode, these interactions are handled using Javascript events that are registered in initWindowEvents().
    - A rendering loop runs constantly in the background, either calling a function called drawMethod() to render the control points and the Bezier curve if the program is in draw mode, or calling a function called viewMethod() to render the 3D wireframe if the program is in view mode.

While this framework is entirely in place, much of the details are left out in the template to be filled in by you.  There are several specific tasks that you need to complete to have a complete solution:
    - Much of the OpenGL state initialization has been done for you, but not all of it.  In particular, you will need to create all of the vertex buffer objects that you need for both the draw and view modes of the program.  This is to be done in the designated place in the window.onload function.
    - You must complete the function called getControlPoints() for retrieving the current set of control points as specified by the user in draw mode.  This should be specified as an array of arrays, where each inner array has two components corresponding to x and y.  The inner arrays can be created using the vec2() convenience function, which comes from the MV.js file provided by the textbook author.  An example of how to do this with hard-coded control points is provided in the template.
    - You must complete the function called buildSurfaceOfRevolution().  This function takes a list of control points and is responsible for deriving the vertices of the surface of revolution.  It should then pass these vertices to the vertex buffer object that you created for the wireframe.
    - You must complete the function called viewMethod() so that it renders the wireframe of the surface of revolution as described in the project wrietup.
    - You must complete the function called drawMethod() so that it renders the current set of control points and the derived Bezier curve as described in the project wrietup.
    - You must implement the keyboard and mouse controls for both draw mode and view mode as described in the project writeup.  This is to be done by expanding the initWindowEvents() function.  Stubs have been set up for all of the events that you should need to use.

You may complete the tasks described above in whatever order you find easiest.  Since the template has been designed with a modular structure as described above, it is recommended that you take advantage of this by completing these tasks one at a time, and testing each one after you complete it before moving on to the next.  You may also create any other functions or global variables that you find neccessary or useful for completing the above tasks.
    
That should be everything that you need to know about the template in order to finish Program 2.  However, please don't hesitate to post on the class forum if you have any questions or concerns about using this template.
