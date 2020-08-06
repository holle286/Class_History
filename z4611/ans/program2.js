//Left basic math functions like multiply, transpose, calculating the view matrix
//and the perspective matrix down below all other code (mm is matrix multiplaction)
var canvas;
var gl;

attribute vec3 vNormal;
var programId;
var program2dId;
var axisBufferId;
var vertBufferId;
var pointBufferId;
var triangleBufferId;
var numPoints = 100;

var mode = 0;
var numAngles = 8;
var stepsPerCurve = 6;
var points3d = 0;
var zoom;

var xpos;
var ypos;

var currCP;
var controlPoints = [];
    controlPoints[0] = vec2(0.1, -1.0);
    controlPoints[1] = vec2(0.3, -0.8);
    controlPoints[2] = vec2(0.4, -0.4);
    controlPoints[3] = vec2(0.45,  0.0);
    controlPoints[4] = vec2(0.5,  0.4);
    controlPoints[5] = vec2(0.7,  0.8);
    controlPoints[6] = vec2(0.9,  1.0);
    

var mousePoints = [
    vec2(290,  449),
    vec2(341,  410),
    vec2(368,  332),
    vec2(380,  250),
    vec2(391,  168),
    vec2(442,  90),
    vec2(495,  52)
    ];

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

function initWindowEvents() {
    // Whether or not the mouse button is currently being held down for a drag.
    var mousePressed = false;
    var last;
    
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
            last = vec2(x,y);
            // Handle mouse down for view mode
            
        } else {
	    
	    for(var i = 0; i < mousePoints.length; i++) {
                if(y < mousePoints[i][1]+10) {
		    if(x < mousePoints[i][0]+10) {
			if(x > mousePoints[i][0]-10) {
			    if(y > mousePoints[i][1]-10) {
				currCP = i;
				break;
			    }
			}
		    }
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
                 var lastDiff = vec2(x-last[0], y-last[1]);
                ypos += (lastDiff[0]/512) * Math.PI;

                xpos -= (lastDiff[1]/400) * Math.PI;
		
            } else {
                // draw mode

                if(currCP != null) { // check if there is anything currCP
                    var oldPnt = mousePoints[currCP];
                    mousePoints[currCP] = vec2(x, y);
                    var dif = vec2(mousePoints[currCP][0] - oldPnt[0], mousePoints[currCP][1] - oldPnt[1]);
                    oldC = controlPoints[currCP];
                    controlPoints[currCP] = vec2(controlPoints[currCP][0]+(dif[0]/256), controlPoints[currCP][1]-(dif[1]/200));
                    BezPoints = makeBez(controlPoints);
                    isValid = true;
                    for(var i = 0; i < BezPoints.length; i++) {
                       if(BezPoints[i][0] < 0) {
                          isValid = false;
                          break;
                       }
                    }
                    if(!isValid) {
                        controlPoints[currCP] = oldC;
                    } 
                    }
                // Handle a mouse drag for draw mode
                
            }
        }
    }

    window.onmouseup = function(e) {
        // A mouse drag ended.
        mousePressed = false;
    }
    
    window.onkeydown = function(e) {
        // Log the key code in the console.  Use this to figure out the key codes for the controls you need.
        console.log(e.keyCode);

	if(mode == 1) {
	    // Handle keyboard
            switch(e.keyCode) {
                case 83:
                    if(zoom - 0.2 > -16) {
                        zoom -= 0.3;
                    }
                    break;
                case 87:
                    if(zoom + 0.2 < -2) {
                        zoom += 0.3;
                    }
                    break;
		case 81:
                    xpos -= .4;
                    break;
		case 65:
                    ypos += .4;
                    break;
	    }
	    //CONTROLS:
	    // a rotate horizontal
	    // d rotate vertical
	    // w zoom in
	    // s zoom out
	}
	    
    }
}

// ########### Function for retrieving control points from "draw" mode

//control points is global var that updates regularly, so just return global var
function getControlPoints() {
    return controlPoints;
}

// ########### Function for building a surface of revolution from a list of control points ###########

//build the surface of revolution given the control points, the value of the angles, and the increment to step by
function buildSurfaceOfRevolution(cp, anglesval, incr)
{
    var angle = 360/anglesval;
    var currentBezier = get3dBez(incr);
    var bezierPoints = currentBezier.length;
    var ans = []; // contains all 3d points
    var curr = []; //create empty list for current, and new points
    var next = [];
    count = 0;
    var i = 0;
    while(i < bezierPoints) //loop thru number of bezier points
    {
        curr[0] = (vec4(currentBezier[i], 0, 1)); //current point is the current bezier in vector 4 form
	for(var j = 0; j < anglesval; j += 1)
	{
            ans[count] = mm(rotateY(j*angle), curr)[0]; //create the ans matrix by multiplying the current by the set angle
            count += 1;
        }
        next[0] = buildhelper2(bezierPoints, currentBezier, i, next)
        ans[count] = mm(rotateY(0*angle), curr)[0];
        count += 1;

        if(i < bezierPoints - 1)
	{
	    var h = 0;
            while(h < anglesval)
	    {//increment thru ansers with count and add in the solution from buildhelper function
                ans[count] = buildhelper(angle, next, 1, h);
		
                count += 1;
		
                ans[count] = buildhelper(angle, curr, 1, h);
		
                count += 1;
		
                ans[count] = buildhelper(angle, next, 0, h);
		
                count += 1;
		
                ans[count] = buildhelper(angle, curr, 1, h);

		count += 1;
		h += 1;
            }
        }
	 i += 1
    }
    points3d = count; //set num of points to the amount counted in the function
    return ans; // return
}
function buildhelper2 (pts, bez, num, next) {
    if (num < pts - 1)
	{
            return (vec4(bez[num+1],0,1)); //next point is the next one in the bezier
        }
    else {
	return next[0];
    }
}
//helper to keep some math separate
function buildhelper (angle, point, offset, counter) {
    return mm(rotateY((counter + offset) * angle), point)[0];
}

// ########### The 3D Mode for Viewing the Surface of Revolution --- ADD CODE HERE ###########
//view method, pretty self explanotory, use triangleBufferId even though I used linesplit
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
    gl.uniform3fv(gl.getUniformLocation(programId, "lineColor"), vec3(.1, .1, .1));
    var matworldx = gl.getUniformLocation(programId, 'worldXMatrix');
    var matworldy = gl.getUniformLocation(programId, 'worldYMatrix');
    var matview = gl.getUniformLocation(programId, 'viewMatrix');
    var matproj = gl.getUniformLocation(programId, 'projectionMatrix');
    
    var worldXMatrix = new Float32Array(16);
    var worldYMatrix = new Float32Array(16);
    var viewMatrix = new Float32Array(16);
    var projMatrix = new Float32Array(16);
 
    worldXMatrix = flatten(rotateX(xpos));
    worldYMatrix = flatten(rotateY(ypos));
    viewMatrix = getViewMatrix([0,0,zoom], [0,0,0], [0,1,0]);
    projMatrix = getPerspectiveMatrix(radians(22.5), canvas.width/canvas.height,0.1,1000.0);
    gl.uniformMatrix4fv(matworldx, false, worldXMatrix);
    gl.uniformMatrix4fv(matworldy, false, worldYMatrix);
    gl.uniformMatrix4fv(matview, false, viewMatrix);
    gl.uniformMatrix4fv(matproj, false, projMatrix);
    var vPosition = gl.getAttribLocation(programId, "vPosition");
    gl.bindBuffer(gl.ARRAY_BUFFER, triangleBufferId);

    gl.bufferData(gl.ARRAY_BUFFER, flatten(buildSurfaceOfRevolution(getControlPoints(), numAngles, stepsPerCurve)), gl.DYNAMIC_DRAW);
    gl.vertexAttribPointer(
	vPosition,
	4,
	gl.FLOAT,
	false,
    	0,0);
    //gl.bindAttribLocation(programId, vPosition, 0);
    gl.drawArrays(gl.LINE_STRIP, 0, points3d);
}
//getting the bezier curve
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
//getting the bezier curve in 3d form
function get3dBez(steps) {
    const points = [];
    var count = 0;
    var step = 1/(steps/2);

    pts = getControlPoints();
    points[count] = vec2(0, pts[0][1]);
    count++;
    for (let i = 0; i < 1; i += step) {
        var newpoint = (getPointOnBezierCurve(pts, 0, i));

	points[count] = vec2(newpoint[0], newpoint[1]);
	count++;
    }
    for (let i = 0; i < 1; i += step) {
        var newpoint = (getPointOnBezierCurve(pts, 3, i));

	points[count] = vec2(newpoint[0], newpoint[1]);
	count++;
    }
    points[count] = pts[6];
    count++;

    points[count] = vec2(0, pts[6][1]);
    count++;
    return points;   
}

//helper function to compute math in the bezier curve
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

//draw method for 2d mode, built one buffer and used points and linesplit on it
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
    vertBufferId = gl.createBuffer();
    pointBufferId = gl.createBuffer();
    triangleBufferId = gl.createBuffer();

    vertexCount = buildSurfaceOfRevolution(controlPoints, numAngles, stepsPerCurve);
    // Set up events for the HTML controls
    initControlEvents();

    // Setup mouse and keyboard input
    initWindowEvents();
    
    // Start continuous rendering
    window.setInterval(render, 33);
}
//MATH FUNCTIONS FOR BASIC MATRIX CALCULATIONS
//View and perspective matrix calculations
function getViewMatrix(cam, mid, top) {
  var x0;
  var x1;
  var x2;
  var y0;
  var y1;
  var y2;
  var z0;
  var z1;
  var z2;
  var length;
  var camx = cam[0];
  var camy = cam[1];
  var camz = cam[2];
  var topx = top[0];
  var topy = top[1];
  var topz = top[2];
  var midx = mid[0];
  var midy = mid[1];
  var midz = mid[2];
  var ans = new Float32Array(16);

    //Math section
  z0 = camx - midx; z1 = camy - midy; z2 = camz - midz; length = 1 / Math.sqrt(z0 * z0 + z1 * z1 + z2 * z2);

  z0 *= length; z1 *= length; z2 *= length;

  x0 = topy * z2 - topz * z1; x1 = topz * z0 - topx * z2; x2 = topx * z1 - topy * z0;

    
  length = Math.sqrt(x0 * x0 + x1 * x1 + x2 * x2);
  if (!length)
    {
	x2 = 0;	x1 = 0; x0 = 0;
    }
  else
    {
	length = 1 / length; x0 *= length; x1 *= length; x2 *= length;
    }
  y0 = z1 * x2 - z2 * x1; y1 = z2 * x0 - z0 * x2; y2 = z0 * x1 - z1 * x0;
  length = Math.sqrt(y0 * y0 + y1 * y1 + y2 * y2);
  if (!length) {
    y2 = 0; y1 = 0; y0 = 0;
  }
    else
    {
	length = 1 / length; y0 *= length; y1 *= length; y2 *= length;
  }

    
  ans[0] = x0; ans[1] = y0; ans[2] = z0; ans[3] = 0; ans[4] = x1; ans[5] = y1;
  ans[6] = z1; ans[7] = 0; ans[8] = x2; ans[9] = y2; ans[10] = z2; ans[11] = 0;
  ans[12] = -(x0 * camx + x1 * camy + x2 * camz); ans[13] = -(y0 * camx + y1 * camy + y2 * camz);
  ans[14] = -(z0 * camx + z1 * camy + z2 * camz); ans[15] = 1;
  return ans;
}

function getPerspectiveMatrix(a, b, c, d) {
  var matrix = new Float32Array(16);
  var f = 1.0 / Math.tan(a / 2), nf;
  matrix[0] = f / b;
  matrix[5] = f;
  matrix[11] = -1;
    if (d != null && d !== Infinity)
    {
	nf = 1 / (c - d); matrix[10] = (d + c) * nf; matrix[14] = 2 * d * c * nf;
    }
    else
    {
	matrix[10] = -1; matrix[14] = -2 * c;
    }
  return matrix;
}

//calculate transpose (used in matrix multplication only)
function calc_transpose(original) {
  var height = original[0].length;
  var width = original.length;
    var i = []; var j = []; var t = [];
    i = 0;
    while( i<height)
    {
	t[i] = [];
	j = 0;
	while(j<width)
	{
	    t[i][j] = original[j][i];
	    j+=1;
	}
	i+=1;
    }
  return t;
}

function mm(a, b) { //matrix multiplication
    var ans = [];
    for (var count1 = 0; count1 < a[0].length; count1++) {
          var row = [];
          for (var count2 = 0; count2 < b.length; count2++) {
              var num = 0;
              for (var count3 = 0; count3 < b[0].length; count3++) {
                  num+= a[count3][count1]*b[count2][count3];
              }
              row[count2] = num;
          }
          ans[count1] = row;
    }
    return calc_transpose(ans);
};
