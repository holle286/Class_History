var canvas;
var gl;

var programId;
var program2dId;
var axisBufferId;
var vertexBufferId;
var pointsBufferId;
var vertexLineId;
var shapeBufferId;
var STEP_2D = 200;

var rotationX;
var rotationY;
var rotationZ;
var zoom;
var autoRotate = false;

var mode = 0;
var numAngles = 8;
var stepsPerCurve = 6;
var numOfPointsIn3d = 0;
var vertexCount = [];
var controlPoints = [];
controlPoints[0] = vec2(0.5, -0.6); // end
controlPoints[1] = vec2(0.5, -0.4);
controlPoints[2] = vec2(0.5,  -0.2);
controlPoints[3] = vec2(0.5,  0.0); // middle
controlPoints[4] = vec2(0.5,  0.2);
controlPoints[5] = vec2(0.5,  0.4);
controlPoints[6] = vec2(0.5,  0.6); // start

var mousePoints = [];
mousePoints[0] = vec2(391,  370);
mousePoints[1] = vec2(391,  330);
mousePoints[2] = vec2(391,  290);
mousePoints[3] = vec2(391,  250);
mousePoints[4] = vec2(391,  210);
mousePoints[5] = vec2(391,  170);
mousePoints[6] = vec2(391,  130);

var selected;

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

function multiplyMatrix(m1, m2) {

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
        document.getElementById('toggleRotate').style.visibility = 'visible';
        document.getElementById('text').style.visibility = 'visible';
        elem.value = "Draw Mode";
        mode = 1;

        // Regenerate the vertex data
        vertexCount = buildSurfaceOfRevolution(getControlPoints(), numAngles, stepsPerCurve);

    } else {
        document.getElementById("demo").innerHTML = "Draw Mode";
        document.getElementById('anglesDiv').style.visibility = 'hidden';
        document.getElementById('stepsDiv').style.visibility = 'hidden';
        document.getElementById('toggleRotate').style.visibility = 'hidden';
        document.getElementById('text').style.visibility = 'hidden';
        numAngles = parseFloat(document.getElementById("numAngles").value);
        stepsPerCurve = parseFloat(document.getElementById("stepsPerCurve").value);
        elem.value = "View Mode";
        mode = 0;
    }
}

function toggleRotate() {
    var elem = document.getElementById("toggleRotate");

    if (elem.value == "Auto-Rotate On") {
        elem.value = "Auto-Rotate Off";
        autoRotate = false;
    } else {
        elem.value = "Auto-Rotate On";
        autoRotate = true;
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

            lastClicked = vec2(x, y);
            // Handle mouse down for view mode

        } else {

            for(var i = 0; i < mousePoints.length; i++) {
                if(x > mousePoints[i][0]-5 && x < mousePoints[i][0]+5 && y > mousePoints[i][1]-5 && y < mousePoints[i][1]+5) {
                    selected = i;
                    console.log("selected point " + i);
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
                rotationY += (lastClickedDiff[0]/512) * Math.PI;

                rotationX -= (lastClickedDiff[1]/400) * Math.PI;
                // console.log(rotationX);

            } else {

                if(selected != null) {

                    var oldPoint = mousePoints[selected];

                    mousePoints[selected] = vec2(x, y);

                    var newDif = vec2(mousePoints[selected][0] - oldPoint[0], mousePoints[selected][1] - oldPoint[1]);

                    oldControl = controlPoints[selected];

                    controlPoints[selected] = vec2(controlPoints[selected][0]+(newDif[0]/256), controlPoints[selected][1]-(newDif[1]/200));

                    checkBez = generateBezPoints(STEP_2D);
                    goodToGo = true;

                    for(var i = 0; i < checkBez.length; i++) {
                       if(checkBez[i][0] < 0) {
                          goodToGo = false;
                          break;
                       }
                    }

                    if(!goodToGo) {
                        controlPoints[selected] = oldControl;
                    } else {
                        if(selected == 3 ) {
                            controlPoints[2] = vec2(controlPoints[2][0]+(newDif[0]/256), controlPoints[2][1]-(newDif[1]/200));
                            controlPoints[4] = vec2(controlPoints[4][0]+(newDif[0]/256), controlPoints[4][1]-(newDif[1]/200));
                        }

                        if(selected == 2 || selected == 4) {

                            var p2;
                            var p4;
                            var oppLength;
                            var opp;

                            var p3 = controlPoints[3];
                            var p2o = vec2(p3[0] + 1, p3[1])

                            if (selected == 2) {
                                p2 = controlPoints[2];
                                p4 = controlPoints[4];
                                opp = 4;
                            } else {
                                p2 = controlPoints[4];
                                p4 = controlPoints[2];
                                opp = 2;
                            }
                            oppLength = Math.sqrt(((p4[1] - p3[1])*(p4[1] - p3[1])) + ((p4[0] - p3[0])*(p4[0] - p3[0])));
                            angle = findAngle(p2,p2o,p3);

                            if(p3[1] > p2[1]) {
                                controlPoints[opp] = vec2(p3[0]-(oppLength * Math.cos(angle)), p3[1]+(oppLength * Math.sin(angle)));
                            } else {
                                controlPoints[opp] = vec2(p3[0]-(oppLength * Math.cos(angle)), p3[1]-(oppLength * Math.sin(angle)));
                            }

                        }
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
        selected = null;

        // Differentiate between view mode and draw mode
        if (mode == 1) {

            // Handle mouse up for view mode

        } else {

            // Handle mouse up for draw mode

        }
    }

    window.onkeydown = function(e) {
        // Log the key code in the console.  Use this to figure out the key codes for the controls you need.
        console.log(e.keyCode);

        if (mode == 1) {
            // Handle keyboard
            switch(e.keyCode) {
                case 88:
                    if(zoom - 0.2 > -16) {
                        zoom -= 0.2;
                    }
                    break;
                case 90:
                    if(zoom + 0.2 < -2) {
                        zoom += 0.2;
                    }
                    break;
                case 82:
                    rotationX = 0;
                    rotationY = 0;
                    zoom = -8;
                    break;
            }

        }
    }
}

function findAngle(p0, p1, c) {
    var p0c = Math.sqrt(Math.pow(c[0]-p0[0],2) + Math.pow(c[1]-p0[1],2));
    var p1c = Math.sqrt(Math.pow(c[0]-p1[0],2) + Math.pow(c[1]-p1[1],2));
    var p0p1 = Math.sqrt(Math.pow(p1[0]-p0[0],2) + Math.pow(p1[1]-p0[1],2));

    return Math.acos((p1c*p1c+p0c*p0c-p0p1*p0p1)/(2*p1c*p0c));
}

// ########### Function for retrieving control points from "draw" mode --- ADD CODE HERE ###########
function getControlPoints() {

    return controlPoints;
}

function getControlLines() {

    var controlLines = [];

    controlLines[0] = vec2(controlPoints[0][0], controlPoints[0][1]);
    controlLines[1] = vec2(controlPoints[1][0], controlPoints[1][1]);
    controlLines[2] = vec2(controlPoints[2][0], controlPoints[2][1]);
    controlLines[3] = vec2(controlPoints[3][0], controlPoints[3][1]);
    controlLines[4] = vec2(controlPoints[3][0], controlPoints[3][1]);
    controlLines[5] = vec2(controlPoints[4][0], controlPoints[4][1]);
    controlLines[6] = vec2(controlPoints[5][0], controlPoints[5][1]);
    controlLines[7] = vec2(controlPoints[6][0], controlPoints[6][1]);

    return controlLines;
}

function printMatrix(m)
{
    if(m && m[0]) {
      for(var i = 0; i < m[0].length; i++) {
          var string = i + "      ";
          for(var j = 0; j < m.length; j++) {
              string += m[j][i] + " ";
          }
          console.log(string);
      }
    }
}

function bezCurve(p1, p2, p3, p4, t) {
    bezMatrix = [];
    bezMatrix[0] = vec4(-1, 3, -3, 1);
    bezMatrix[1] = vec4(3, -6, 3, 0);
    bezMatrix[2] = vec4(-3, 3, 0, 0);
    bezMatrix[3] = vec4(1, 0, 0, 0);

    given = [];
    given[0] = vec2(p1[0], p1[1]);
    given[1] = vec2(p2[0], p2[1]);
    given[2] = vec2(p3[0], p3[1]);
    given[3] = vec2(p4[0], p4[1]);

    tMatrix = [];
    tMatrix[0] = vec4(t*t*t, t*t, t, 1);

    var givenBez = multiplyMatrix(given, bezMatrix);

    var result = multiplyMatrix(givenBez, tMatrix);

    return result;
}

function generateBezPoints(numPoints) {

    p = getControlPoints();

    step = 1/(numPoints/2);

    var points = [];
    var count = 0;

    for(var i = 0; i < 1; i += step) {

        var newPoint = bezCurve(p[0], p[1], p[2], p[3], i);

        points[count] = vec2(newPoint[0], newPoint[1]);
        count++;
    }
    for(var i = 0; i < 1; i += step) {
        var newPoint = bezCurve(p[3], p[4], p[5], p[6], i);

        points[count] = vec2(newPoint[0], newPoint[1]);
        count++;
    }

    points[count] = p[6];
    count++;
    return points;
}

function generate3DBezPoints(numPoints) {

    p = getControlPoints();

    step = 1/(numPoints/2);

    var points = [];
    var count = 0;

    points[count] = vec2(0, p[0][1]);
    count++;

    for(var i = 0; i < 1; i += step) {

        var newPoint = bezCurve(p[0], p[1], p[2], p[3], i);

        points[count] = vec2(newPoint[0], newPoint[1]);
        count++;
    }
    for(var i = 0; i < 1; i += step) {
        var newPoint = bezCurve(p[3], p[4], p[5], p[6], i);

        points[count] = vec2(newPoint[0], newPoint[1]);
        count++;
    }

    points[count] = p[6];
    count++;

    points[count] = vec2(0, p[6][1]);
    count++;

    return points;
}

function convertToVec4(vec2) {
    return vec4(vec2, 0, 1);
}

function buildSurfaceOfRevolution(controlPoints, angles, steps) {

    var angle = 360/angles;
    var currBezCurve = generate3DBezPoints(steps);
    var bezCurvePoints = currBezCurve.length;

    var results = []; // contains all 3d points
    count = 0;

    for(var i = 0; i < bezCurvePoints; i++) {

        var currentPoint = [];
        var nextPoint = [];
        currentPoint[0] = convertToVec4(currBezCurve[i]);
        if (i < bezCurvePoints-1) {
            nextPoint[0] = convertToVec4(currBezCurve[i+1]);
        }

        //generate each step layer
        for(var j = 0; j < angles; j++) {
            results[count] = multiplyMatrix(rotateY(j*angle), currentPoint)[0];
            count++;
        }
        results[count] = multiplyMatrix(rotateY(0*angle), currentPoint)[0];
        count++;

        //generate each step middle
        if(i < bezCurvePoints - 1) {

            for(var j = 0; j < angles; j++) {
                results[count] = multiplyMatrix(rotateY((j+1)*angle), nextPoint)[0];
                count++;
                results[count] = multiplyMatrix(rotateY((j+1)*angle), currentPoint)[0];
                count++;
                results[count] = multiplyMatrix(rotateY((j)*angle), nextPoint)[0];
                count++;
                results[count] = multiplyMatrix(rotateY((j+1)*angle), currentPoint)[0];
                count++;
            }

        }

    }

    numOfPointsIn3d = count;
    return results;
}

// returns an identity matrix (used for testing)
function identity() {

    var newMatrix = new Float32Array(16);

    for (var i = 0; i < newMatrix.length; i++) {
        if(i % 5 == 0) {
            newMatrix[i] = 1;
        } else {
            newMatrix[i] = 0;
        }
    }
    return newMatrix;
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
    gl.uniform3fv(gl.getUniformLocation(programId, "lineColor"), vec3(0.6, 0.6, 0.6));

    var worldXMatrix = new Float32Array(16);
    var worldYMatrix = new Float32Array(16);
    var viewMatrix = new Float32Array(16);
    var projMatrix = new Float32Array(16);

    if (autoRotate) {
        rotationX -= 0.2;
        rotationY += 0.2;
    }

    worldXMatrix = flatten(rotateX(rotationX));
    worldYMatrix = flatten(rotateY(rotationY));
    viewMatrix = getViewMatrix([0, 0, zoom], [0, 0, 0], [0, 1, 0]);
    projMatrix = getPerspectiveMatrix(radians(22.5), canvas.width/canvas.height, 0.1, 1000.0);

    gl.uniformMatrix4fv(gl.getUniformLocation(programId, "worldXMatrix"), false, worldXMatrix);
    gl.uniformMatrix4fv(gl.getUniformLocation(programId, "worldYMatrix"), false, worldYMatrix);
    gl.uniformMatrix4fv(gl.getUniformLocation(programId, "viewMatrix"), false, viewMatrix);
    gl.uniformMatrix4fv(gl.getUniformLocation(programId, "projectionMatrix"), false, projMatrix);

    var vPosition = gl.getAttribLocation(programId, "vPosition");

    gl.bindBuffer(gl.ARRAY_BUFFER, shapeBufferId);


    gl.bufferData(gl.ARRAY_BUFFER, flatten(buildSurfaceOfRevolution(getControlPoints(), numAngles, stepsPerCurve)), gl.DYNAMIC_DRAW);
    gl.vertexAttribPointer(vPosition, 4, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.LINE_STRIP, 0, numOfPointsIn3d);

}


// ########### The 2D Mode to draw the Bezier Curver --- ADD CODE HERE ###########

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

    gl.bindBuffer(gl.ARRAY_BUFFER, pointsBufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(controlPoints), gl.DYNAMIC_DRAW);
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.POINTS, 0, 7);

    // console.log(controlPoints);
    // console.log(getControlLines());

    gl.bindBuffer(gl.ARRAY_BUFFER, vertexLineId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(getControlLines()), gl.DYNAMIC_DRAW);
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.LINES, 0, 8);


    gl.uniform3fv(gl.getUniformLocation(program2dId, "lineColor"), vec3(1, 0.7, 0.7));

    // draw bez curve
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBufferId); //generateBezPoints()
    gl.bufferData(gl.ARRAY_BUFFER, flatten(generateBezPoints(STEP_2D)), gl.DYNAMIC_DRAW);
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.LINE_STRIP, 0, STEP_2D+1);

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

    rotationX = 0;
    rotationY = 0;
    rotationZ = 0;
    zoom = -8;

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

    // Get the hardcoded control points
    var controlPoints = getControlPoints();

    // ###### Create vertex buffer objects --- ADD CODE HERE ######

    vertexBufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(controlPoints), gl.DYNAMIC_DRAW);

    vertexLineId = gl.createBuffer();

    pointsBufferId = gl.createBuffer();

    shapeBufferId = gl.createBuffer();

    // Create the surface of revolution
    // (this should load the initial shape into one of the vertex buffer objects you just created)
    vertexCount = buildSurfaceOfRevolution(controlPoints, numAngles, stepsPerCurve);

    // Set up events for the HTML controls
    initControlEvents();

    // Setup mouse and keyboard input
    initWindowEvents();

    // Start continuous rendering
    window.setInterval(render, 33);
};