var WAIT_PERIOD = 1500;
var letter_pts = new Array();
var last_drawn_time = new Date().getTime()

var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;
var canvas;
var context;
var canvasWidth = $(window).width();
var canvasHeight = $(window).height();

$(document).ready(function() {
	prepareSimpleCanvas();
});

/**
* Creates a canvas element.
*/
function prepareSimpleCanvas()
{
	// Create the canvas (Neccessary for IE because it doesn't know what a canvas element is)
	var canvasDiv = document.getElementById('canvasDiv');
	canvas = document.createElement('canvas');
	canvas.setAttribute('width', canvasWidth);
	canvas.setAttribute('height', canvasHeight);
	canvas.setAttribute('id', 'canvasSimple');
	canvasDiv.appendChild(canvas);
	if(typeof G_vmlCanvasManager != 'undefined') {
		canvas = G_vmlCanvasManager.initElement(canvas);
	}
	context = canvas.getContext("2d");

	// setup stroke properties
	context.strokeStyle = "#000000";
	context.lineJoin = "round";
	context.lineWidth = 10; // radius of circles drawn
	
	// Add mouse events
	$('#canvasSimple').mousedown(function(e) {
		// Mouse down location
		var mouseX = e.pageX - this.offsetLeft;
		var mouseY = e.pageY - this.offsetTop;
		
		paint = true;
		addClickSimple(mouseX, mouseY, false);
		redraw();
	});
	
	$('#canvasSimple').mousemove(function(e) {
		if(paint){
			addClickSimple(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
			redraw();
		}
	});
	
	$('#canvasSimple').mouseup(function(e) {
		paint = false;
	  	redraw();
	});
	
	$('#canvasSimple').mouseleave(function(e) {
		paint = false;
	});
	
	$('#clearCanvasSimple').mousedown(function(e) {
		clickX = new Array();
		clickY = new Array();
		clickDrag = new Array();
		clearcanvas(); 
	});
	
	// Add touch event listeners to canvas element
	canvas.addEventListener("touchstart", function(e) {
		// Mouse down location
		var mouseX = (e.changedTouches ? e.changedTouches[0].pageX : e.pageX) - this.offsetLeft,
			mouseY = (e.changedTouches ? e.changedTouches[0].pageY : e.pageY) - this.offsetTop;
		
		paint = true;
		addClickSimple(mouseX, mouseY, false);
		redraw();
	}, false);
	canvas.addEventListener("touchmove", function(e) {
		var mouseX = (e.changedTouches ? e.changedTouches[0].pageX : e.pageX) - this.offsetLeft,
			mouseY = (e.changedTouches ? e.changedTouches[0].pageY : e.pageY) - this.offsetTop;
					
		if(paint){
			addClickSimple(mouseX, mouseY, true);
			redraw();
		}
		e.preventDefault()
	}, false);
	canvas.addEventListener("touchend", function(e) {
		paint = false;
	  	redraw();
	}, false);
	canvas.addEventListener("touchcancel", function(e) {
		paint = false;
	}, false);
}

function addClickSimple(x, y, dragging) {
	letter_pts.push([x, y]);
	clickX.push(x);
	clickY.push(y);
	clickDrag.push(dragging);

	// wait for drawing to stop, then process
	last_drawn_time = new Date().getTime()
	setTimeout(function() {
		if (new Date().getTime() - last_drawn_time >= WAIT_PERIOD) {
			console.log(JSON.stringify(letter_pts));

			clearcanvas()
			letter_pts = new Array()
		}
	}, WAIT_PERIOD)
}

function clearcanvas() {
	context.clearRect(0, 0, canvasWidth, canvasHeight);
	clickX = new Array()
	clickY = new Array()
	clickDraw = new Array()
}

function redraw() {			
	for(var i=0; i < clickX.length; i++) {		
		context.beginPath();
		if(clickDrag[i] && i) {
			context.moveTo(clickX[i-1], clickY[i-1]);
		} else {
			context.moveTo(clickX[i]-1, clickY[i]);
		}
		context.lineTo(clickX[i], clickY[i]);
		context.closePath();
		context.stroke();
	}
}

// Converts canvas to an image
function convertCanvasToImage(canvas) {
	var image = new Image();
	image.src = canvas.toDataURL("image/png");
	return image;
}
