var canvas;
var gl;

var programId;
var program2dId;
var axisBufferId;
var vertBufferId;
var lineBufferId;
var pointBufferId;
var triangleBufferId;
var numPoints = 100;

var mode = 0;
var numAngles = 8;
var stepsPerCurve = 6;
var vertexCount = [];
var numOfPointsIn3d = 0;

var xpos;
var ypos;
var zpos;

var currCP;
var controlPoints = [];
    controlPoints[0] = vec2(0.1, -1.0);
    controlPoints[1] = vec2(0.3, -0.8);
    controlPoints[2] = vec2(0.4, -0.4);
    controlPoints[3] = vec2(0.45,  0.0);
    controlPoints[4] = vec2(0.5,  0.4);
    controlPoints[5] = vec2(0.7,  0.8);
    controlPoints[6] = vec2(0.9,  1.0);
    
/*
var mousePoints = [
    vec2(290,  449),
    vec2(341,  410),
    vec2(368,  332),
    vec2(380,  250),
    vec2(391,  168),
    vec2(442,  90),
    vec2(495,  52)
    ];*/
var mousePoints = [];
mousePoints[0] = vec2(290,  449);
mousePoints[1] = vec2(341,  410);
mousePoints[2] = vec2(368,  332);
mousePoints[3] = vec2(380,  250);
mousePoints[4] = vec2(391,  168);
mousePoints[5] = vec2(442,  90);
mousePoints[6] = vec2(495,  52);
// Binds "on-change" events for the controls on the web page
function initControlEvents() {
    // Use one event handler for both of the shape controls
    document.getElementById("numAngles").onchange =
    document.getElementById("stepsPerCurve").onchange =
        function(e) {
            numAngles = parseFloat(document.getElementById("numAngles").value);
            stepsPerCurve = parseFloat(document.getElementById("stepsPerCurve").value);
            // Regenerate the vertex data
            vertexCount = buildSurfaceOfRevolution(getControlPoints(), numAngles, stepsPerCurve);
        };
}

//The method that responds to the 'View/Draw' button click to change the mode.
function selectMode() {
    var elem = document.getElementById("myButton1");
    if (elem.value=="View Mode") {
        document.getElementById("demo").innerHTML = "View Mode";
        document.getElementById('anglesDiv').style.visibility = 'visible';
        document.getElementById('stepsDiv').style.visibility = 'visible';
        elem.value = "Draw Mode";    
        mode = 1;

        // Regenerate the vertex data
        vertexCount = buildSurfaceOfRevolution(getControlPoints(), numAngles, stepsPerCurve);
        
    } else {
        document.getElementById("demo").innerHTML = "Draw Mode";
        document.getElementById('anglesDiv').style.visibility = 'hidden';
        document.getElementById('stepsDiv').style.visibility = 'hidden';
	numAngles = parseFloat(document.getElementById("numAngles").value);
        stepsPerCurve = parseFloat(document.getElementById("stepsPerCurve").value);
	elem.value = "View Mode";
        mode = 0;
    }
}

// ########### Binds events for keyboard and mouse events --- ADD CODE HERE ###########
function initWindowEvents() {
    // Whether or not the mouse button is currently being held down for a drag.
    var mousePressed = false;
    var lastClicked;
    
    canvas.onmousedown = function(e) {
        // A mouse drag started.
        mousePressed = true;
        
        // Log where the mouse drag started.
        // (This is an example of how to get the (x,y) coordinates from a mouse event.)
        console.log('x = ' + e.clientX);
        console.log('y = ' + e.clientY);

	var x = e.clientX;
	var y = e.clientY;
        // Differentiate between view mode and draw mode
        if (mode == 1) { 
            lastClicked = vec2(x,y);
            // Handle mouse down for view mode
            
        } else {
	    
	    for(var i = 0; i < mousePoints.length; i++) {
                if(x > mousePoints[i][0]-5 && x < mousePoints[i][0]+5 && y > mousePoints[i][1]-5 && y < mousePoints[i][1]+5) {
                    currCP = i;
                    break;
                }
            }
            
            // Handle mouse down for draw mode
            
        }
    }

    canvas.onmousemove = function(e) {
        if (mousePressed) {
	    var x = e.clientX;
            var y = e.clientY;
            // Differentiate between view mode and draw mode
            if (mode == 1) { 
            
                // Handle a mouse drag for view mode
                 var lastClickedDiff = vec2(x-lastClicked[0], y-lastClicked[1]);
                ypos += (lastClickedDiff[0]/512) * Math.PI;

                xpos -= (lastClickedDiff[1]/400) * Math.PI;
		
            } else {
                // draw mode

                if(currCP != null) { // check if there is anything currCP

                    var oldPnt = mousePoints[currCP]; //set var oldPoint to the old position of the currCP mouse point

                    mousePoints[currCP] = vec2(x, y); // set the select mouse point to the current x and y pos

                    // get the difference between the x and y of the new point and the old point
                    var dif = vec2(mousePoints[currCP][0] - oldPnt[0], mousePoints[currCP][1] - oldPnt[1]);

                    oldC = controlPoints[currCP]; // save the old control point

                    // set control point to the old controlpoint plus the normalized difference of x and y
                    //(actual x point = 1 / 256px, actual y point = 1 / 200px)
                    controlPoints[currCP] = vec2(controlPoints[currCP][0]+(dif[0]/256), controlPoints[currCP][1]-(dif[1]/200));

                    // this generates the all the bez points. we want to check to make sure that none of the x points in the bez points is less than 0
                    // this will make sure the the curve is locked to the right half of the line
                    BezPoints = makeBez(controlPoints);
                    isValid = true;

                    // check if the x of any of the bez points less than 0. if it is, set goodToGo to false
                    for(var i = 0; i < BezPoints.length; i++) {
                       if(BezPoints[i][0] < 0) {
                          isValid = false;
                          break;
                       }
                    }

                    // if not goodToGo, set the controlPoint back to the old one
                    if(!isValid) {
                        controlPoints[currCP] = oldC;
                    } 
		for(var i = 0; i < 7; i++) {
                        mousePoints[i] = vec2(263+controlPoints[i][0]*256, 250-controlPoints[i][1]*200);
                    }
                    }
                // Handle a mouse drag for draw mode
                
            }
        }
    }

    window.onmouseup = function(e) {
        // A mouse drag ended.
        mousePressed = false;
        currCP = null;
    }
    
    window.onkeydown = function(e) {
        // Log the key code in the console.  Use this to figure out the key codes for the controls you need.
        console.log(e.keyCode);

	if(mode == 1) {
	    // Handle keyboard
            switch(e.keyCode) {
                case 82:
                    xpos = 0;
                    ypos = 0;
                break;
	    }
	}
	    
    }
}

// ########### Function for retrieving control points from "draw" mode --- ADD CODE HERE ###########
function getControlPoints() {
    
    return controlPoints;
}

function getViewMatrix(eye, center, up) {
  var newMatrix = new Float32Array(16);
  var x0, x1, x2, y0, y1, y2, z0, z1, z2, len;
  var eyex = eye[0];
  var eyey = eye[1];
  var eyez = eye[2];
  var upx = up[0];
  var upy = up[1];
  var upz = up[2];
  var centerx = center[0];
  var centery = center[1];
  var centerz = center[2];

  z0 = eyex - centerx;
  z1 = eyey - centery;
  z2 = eyez - centerz;
  len = 1 / Math.sqrt(z0 * z0 + z1 * z1 + z2 * z2);
  z0 *= len;
  z1 *= len;
  z2 *= len;
  x0 = upy * z2 - upz * z1;
  x1 = upz * z0 - upx * z2;
  x2 = upx * z1 - upy * z0;
  len = Math.sqrt(x0 * x0 + x1 * x1 + x2 * x2);

  if (!len) {
    x0 = 0;
    x1 = 0;
    x2 = 0;
  } else {
    len = 1 / len;
    x0 *= len;
    x1 *= len;
    x2 *= len;
  }

  y0 = z1 * x2 - z2 * x1;
  y1 = z2 * x0 - z0 * x2;
  y2 = z0 * x1 - z1 * x0;
  len = Math.sqrt(y0 * y0 + y1 * y1 + y2 * y2);

  if (!len) {
    y0 = 0;
    y1 = 0;
    y2 = 0;
  } else {
    len = 1 / len;
    y0 *= len;
    y1 *= len;
    y2 *= len;
  }

  newMatrix[0] = x0;
  newMatrix[1] = y0;
  newMatrix[2] = z0;
  newMatrix[3] = 0;
  newMatrix[4] = x1;
  newMatrix[5] = y1;
  newMatrix[6] = z1;
  newMatrix[7] = 0;
  newMatrix[8] = x2;
  newMatrix[9] = y2;
  newMatrix[10] = z2;
  newMatrix[11] = 0;
  newMatrix[12] = -(x0 * eyex + x1 * eyey + x2 * eyez);
  newMatrix[13] = -(y0 * eyex + y1 * eyey + y2 * eyez);
  newMatrix[14] = -(z0 * eyex + z1 * eyey + z2 * eyez);
  newMatrix[15] = 1;
  return newMatrix;
}

function getPerspectiveMatrix(fovy, aspect, near, far) {
  var newMatrix = new Float32Array(16);
  var f = 1.0 / Math.tan(fovy / 2),
      nf;
  newMatrix[0] = f / aspect;
  newMatrix[5] = f;
  newMatrix[11] = -1;

  if (far != null && far !== Infinity) {
    nf = 1 / (near - far);
    newMatrix[10] = (far + near) * nf;
    newMatrix[14] = 2 * far * near * nf;
  } else {
    newMatrix[10] = -1;
    newMatrix[14] = -2 * near;
  }

  return newMatrix;
}

// ########### Function for building a surface of revolution from a list of control points ###########
// ########### ADD CODE HERE                                                               ###########

function buildSurfaceOfRevolution(cp, angles, steps) {
    var angle = 360/angles;
    var currBezCurve = get3dBez(steps);
    // ###### Hard-coded list of vertices to support incremental development and testing. ######
    // ###### You should replace this with vertices derived from the control points.      ######
    var bezCurvePoints = currBezCurve.length;

    var results = []; // contains all 3d points
    count = 0;

    for(var i = 0; i < bezCurvePoints; i++) {

        var currentPoint = [];
        var nextPoint = [];
        currentPoint[0] = (vec4(currBezCurve[i],0,1));
        if (i < bezCurvePoints-1) {
            nextPoint[0] = (vec4(currBezCurve[i+1],0,1));
        }

        //generate each step layer
        for(var j = 0; j < angles; j++) {
            results[count] = mm(rotateY(j*angle), currentPoint)[0];
            count++;
        }
        results[count] = mm(rotateY(0*angle), currentPoint)[0];
        count++;

        //generate each step middle
        if(i < bezCurvePoints - 1) {

            for(var j = 0; j < angles; j++) {
                results[count] = mm(rotateY((j+1)*angle), nextPoint)[0];
                count++;
                results[count] = mm(rotateY((j+1)*angle), currentPoint)[0];
                count++;
                results[count] = mm(rotateY((j)*angle), nextPoint)[0];
                count++;
                results[count] = mm(rotateY((j+1)*angle), currentPoint)[0];
                count++;
            }

        }

    }

    numOfPointsIn3d = count;
    return results;
}

// ########### The 3D Mode for Viewing the Surface of Revolution --- ADD CODE HERE ###########

function viewMethod(vertexCount) {
    
    // Ensure OpenGL viewport is resized to match canvas dimensions
    gl.viewportWidth = canvas.width;
    gl.viewportHeight = canvas.height;
    
    // Set screen clear color to R, G, B, alpha; where 0.0 is 0% and 1.0 is 100%
    gl.clearColor(0.9, 1.0, 0.9, 1.0);
    
    // Enable color; required for clearing the screen
    gl.clear(gl.COLOR_BUFFER_BIT);
    
    // Clear out the viewport with solid black color
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    
    // Use 3D program
    gl.useProgram(programId);
    gl.uniform3fv(gl.getUniformLocation(programId, "lineColor"), vec3(.6, .6, .6));
    var matworldx = gl.getUniformLocation(programId, 'worldXMatrix');
    var matworldy = gl.getUniformLocation(programId, 'worldYMatrix');
    var matview = gl.getUniformLocation(programId, 'viewMatrix');
    var matproj = gl.getUniformLocation(programId, 'projMatrix');
    
    var worldXMatrix = new Float32Array(16);
    var worldYMatrix = new Float32Array(16);
    var viewMatrix = new Float32Array(16);
    var projMatrix = new Float32Array(16);
 
    worldXMatrix = flatten(rotateX(xpos));
    worldYMatrix = flatten(rotateY(ypos));
    viewMatrix = getViewMatrix([0,0,-8], [0,0,0], [0,1,0]);
    projMatrix = getPerspectiveMatrix(radians(22.5), canvas.width/canvas.height,0.1,1000.0);
    console.log(worldXMatrix);
    gl.uniformMatrix4fv(matworldx, false, worldXMatrix);
    gl.uniformMatrix4fv(matworldy, false, worldYMatrix);
    gl.uniformMatrix4fv(matview, false, viewMatrix);
    gl.uniformMatrix4fv(matproj, false, projMatrix);
    var vPosition = gl.getAttribLocation(programId, "vPosition");
    //gl.enableVertexAttribArray(vPosition);
    gl.bindBuffer(gl.ARRAY_BUFFER, triangleBufferId);

    gl.bufferData(gl.ARRAY_BUFFER, flatten(buildSurfaceOfRevolution(getControlPoints(), numAngles, stepsPerCurve)), gl.DYNAMIC_DRAW);
    //console.log(flatten(buildSurfaceOfRevolution(numAngles,stepsPerCurve)));
    gl.vertexAttribPointer(
	vPosition,
	4,
	gl.FLOAT,
	false,
    	0,0);
    //console.log(vPosition);
    //gl.bindAttribLocation(programId, vPosition, 0);
    gl.drawArrays(gl.LINE_STRIP, 0, numOfPointsIn3d);
}


// ########### The 2D Mode to draw the Bezier Curver --- ADD CODE HERE ###########

function makeBez(pts) {
    const points = [];
    var count = 0;
    var halfnum = numPoints/2;
    for (let i = 0; i < halfnum; ++i) {
        const t = i / (halfnum - 1);
        var newpoint = (getPointOnBezierCurve(pts, 0, t));

	points[count] = vec2(newpoint[0], newpoint[1]);
	count++;
    }
    for (let i = 0; i < halfnum; ++i) {
        const t = i / (halfnum - 1);
        var newpoints = (getPointOnBezierCurve(pts, 3, t));

	points[count] = vec2(newpoints[0], newpoints[1]);
	count++;
    }
    points[count] = controlPoints[6];
    count++;
    return points;   
}

function get3dBez(steps) {
    const points = [];
    var count = 0;
    var halfnum = steps/2;

    points[count] = vec2(0, controlPoints[0][1]);
    count++;
    for (let i = 0; i < halfnum; ++i) {
        const t = i / (halfnum - 1);
        var newpoint = (getPointOnBezierCurve(controlPoints, 0, t));

	points[count] = vec2(newpoint[0], newpoint[1]);
	count++;
    }
    for (let i = 0; i < halfnum; ++i) {
        const t = i / (halfnum - 1);
        var newpoints = (getPointOnBezierCurve(controlPoints, 3, t));

	points[count] = vec2(newpoints[0], newpoints[1]);
	count++;
    }
    points[count] = controlPoints[6];
    count++;

    points[count] = vec2(0, controlPoints[6][1]);
    count++;
    return points;   
}


function getPointOnBezierCurve(points, offset, t) {
    bezierM = [
	vec4(-1,3,-3,1),
	vec4(3,-6,3,0),
	vec4(-3,3,0,0),
	vec4(1,0,0,0)
    ];
    matr = [
	points[0+offset],
	points[1+offset],
	points[2+offset],
	points[3+offset]
    ];

    tM = [
	vec4(t*t*t,t*t,t,1)
    ];
    var givenBex = mm(matr, bezierM);
    var result = mm(givenBex, tM);

    return result;
    }

function tranposeMatrix(m) {
    var newMat = [];
    for(var i = 0; i < m.length; i++) {
        for(var j = 0; j < m[0].length; j++) {
            newMat[j][i] = m[i][j];
        }
    }
    return newMat;
}

function myTranspose(a) {

  // Calculate the width and height of the Array
  var w = a.length;
  // var h = a[0] instanceof Array ? a[0].length : 0;
  var h = a[0].length;

  // In case it is a zero matrix, no transpose routine needed.
  if(h === 0 || w === 0) { return []; }

  var i, j, t = [];

  // Loop through every item in the outer array (height)
  for(i=0; i<h; i++) {

    // Insert a new row (array)
    t[i] = [];

    // Loop through every item per item in outer array (width)
    for(j=0; j<w; j++) {

      // Save transposed data.
      t[i][j] = a[j][i];
    }
  }
  return t;
}

function mm(m1, m2) {

    var result = [];

    if(m1[0].length == m2.length) {
        console.log('error multipling two incompatibile matrices');
        return result;
    }

    for (var i = 0; i < m1[0].length; i++) {
          var row = [];
          for (var j = 0; j < m2.length; j++) {
              var newVal = 0;
              for (var k = 0; k < m2[0].length; k++) {
                  oldVal = newVal; // testing

                  newVal += m1[k][i] * m2[j][k];
              }
              row[j] = newVal;
              // console.log("final value: " + row[j] );
          }
          result[i] = row;
    }
    // console.log(result);
    return myTranspose(result);
    // return result;
}
	
function drawMethod(controlPoints) {
    
    // Ensure OpenGL viewport is resized to match canvas dimensions
    gl.viewportWidth = canvas.width;
    gl.viewportHeight = canvas.height;
    
    // Set screen clear color to R, G, B, alpha; where 0.0 is 0% and 1.0 is 100%
    gl.clearColor(0.9, 1.0, 1.0, 1.0);
    
    // Enable color; required for clearing the screen
    gl.clear(gl.COLOR_BUFFER_BIT);
    
    // Clear out the viewport with solid black color
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    
    // Use 2D program
    gl.useProgram(program2dId);
    
    // Set line color for "axis of revolution"
    gl.uniform3fv(gl.getUniformLocation(program2dId, "lineColor"), vec3(0.5, 0.5, 0.5));
    
    // Draw the "axis of revolution"
    var vPosition = gl.getAttribLocation(program2dId, "vPosition");
    gl.bindBuffer(gl.ARRAY_BUFFER, axisBufferId);
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.LINES, 0, 20);


    gl.bindBuffer(gl.ARRAY_BUFFER, pointBufferId);

    gl.bufferData(gl.ARRAY_BUFFER, flatten(getControlPoints()), gl.DYNAMIC_DRAW);

    gl.vertexAttribPointer(
	vPosition,
	2,
	gl.FLOAT,
	gl.FALSE,
	0,0);

    gl.drawArrays(gl.POINTS,0,7);
    gl.drawArrays(gl.LINE_STRIP,0, 7)

    gl.uniform3fv(gl.getUniformLocation(program2dId, "lineColor"), vec3(1, 0, 0));
    gl.bindBuffer(gl.ARRAY_BUFFER, vertBufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(makeBez(getControlPoints())), gl.DYNAMIC_DRAW);
    gl.vertexAttribPointer(
	vPosition,
	2,
	gl.FLOAT,
	gl.FALSE,
	0,0);
    console.log(vPosition);
    gl.drawArrays(gl.LINE_STRIP,0,numPoints+1)
    
}

// Called automatically every 33 milliseconds to render the scene
function render() {
    if (mode == 1) {
        viewMethod(vertexCount);
    } else {
        drawMethod(getControlPoints());
    }
}

// Initializations
window.onload = function() {
    
    // Get initial angles and steps
    numAngles = parseFloat(document.getElementById("numAngles").value);
    stepsPerCurve = parseFloat(document.getElementById("stepsPerCurve").value);

    xpos = 0;
    ypos = 0;
    zpos = 0;
    // Find the canvas on the page
    canvas = document.getElementById("gl-canvas");
    
    // Initialize a WebGL context
    gl = WebGLUtils.setupWebGL(canvas);
    if (!gl) { 
        alert("WebGL isn't available"); 
    }
    
    gl.enable(gl.DEPTH_TEST);
    
    // Load shaders
    programId = initShaders(gl, "vertex-shader", "fragment-shader");
    program2dId = initShaders(gl, "vertex-shader-2d", "fragment-shader");
    
    // Setup axis of revolution to be rendered in draw mode
    var revolutionAxis = [];
    for (var i = 0; i < 20; i++) {
        revolutionAxis[i] = vec2(0.0, 2 * i / 19.0 - 1);
    }
    
    axisBufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, axisBufferId );
    gl.bufferData(gl.ARRAY_BUFFER, flatten(revolutionAxis), gl.DYNAMIC_DRAW);
    
    // Enable the position attribute for our 2D shader program.
    gl.useProgram(program2dId);
    var vPosition = gl.getAttribLocation(program2dId, "vPosition");
    gl.enableVertexAttribArray(vPosition);

   // gl.useProgram(programId);
   // var vPosition = gl.getAttribLocation(programId, "vPosition");
   // gl.enableVertexAttribArray(vPosition);
    
    // Get the hardcoded control points
    var controlPoints = getControlPoints();
    
    // ###### Create vertex buffer objects --- ADD CODE HERE ######
    vertBufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertBufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(controlPoints), gl.DYNAMIC_DRAW);

    lineBufferId = gl.createBuffer();
    pointBufferId = gl.createBuffer();
    triangleBufferId = gl.createBuffer();

    vertexCount = buildSurfaceOfRevolution(controlPoints, numAngles, stepsPerCurve);
    // Set up events for the HTML controls
    initControlEvents();

    // Setup mouse and keyboard input
    initWindowEvents();
    
    // Start continuous rendering
    window.setInterval(render, 33);
};
