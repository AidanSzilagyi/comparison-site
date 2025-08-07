
// ripped straight from the docs: https://docs.djangoproject.com/en/5.2/howto/csrf/
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// big-text.js

/*
Bruno Orlandi - 2017

Copyright (C) 2013 Daniel Hoffmann Bernardes, Ícaro Technologies
Copyright (C) 2016 Jet Holt

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

function _calculateInnerDimensions(computedStyle){
	//Calculate the inner width and height
	var innerWidth;
	var innerHeight;

	var width = parseInt(computedStyle.getPropertyValue("width"));
	var height = parseInt(computedStyle.getPropertyValue("height"));
	var paddingLeft = parseInt(computedStyle.getPropertyValue("padding-left"));
	var paddingRight = parseInt(computedStyle.getPropertyValue("padding-right"));
	var paddingTop = parseInt(computedStyle.getPropertyValue("padding-top"));
	var paddingBottom = parseInt(computedStyle.getPropertyValue("padding-bottom"));
	var borderLeft = parseInt(computedStyle.getPropertyValue("border-left-width"));
	var borderRight = parseInt(computedStyle.getPropertyValue("border-right-width"));
	var borderTop = parseInt(computedStyle.getPropertyValue("border-top-width"));
	var borderBottom = parseInt(computedStyle.getPropertyValue("border-bottom-width"));

	//If box-sizing is border-box, we need to subtract padding and border.
	var parentBoxSizing = computedStyle.getPropertyValue("box-sizing");
	if(parentBoxSizing == "border-box"){
		innerWidth = width - (paddingLeft + paddingRight + borderLeft + borderRight);
		innerHeight = height - (paddingTop + paddingBottom + borderTop + borderBottom);
	}else{
		innerWidth = width;
		innerHeight = height;
	}
	var obj = {};
	obj["width"] = innerWidth;
	obj["height"] = innerHeight;
	return obj;
}

export function BigText(element, options) {

	if (typeof element === 'string') {
		element = document.querySelector(element);
	} else if (element.length) {
		// Support for array based queries (such as jQuery)
		element = element[0];
	}

	var defaultOptions = {
		rotateText: null,
		fontSizeFactor: 0.8,
		maximumFontSize: null,
		limitingDimension: "both",
		horizontalAlign: "center",
		verticalAlign: "center",
		textAlign: "center",
		whiteSpace: "nowrap"
	};
	
	//Merge provided options and default options
	options = options || {};
	for (var opt in defaultOptions)
		if (defaultOptions.hasOwnProperty(opt) && !options.hasOwnProperty(opt))
			options[opt] = defaultOptions[opt];
	
	//Get variables which we will reference frequently
	var style = element.style;
	var computedStyle = document.defaultView.getComputedStyle(element);
	var parent = element.parentNode;
	var parentStyle = parent.style;
	var parentComputedStyle = document.defaultView.getComputedStyle(parent);
	
	//hides the element to prevent "flashing"
	style.visibility = "hidden";
	
	//Set some properties
	style.display = "inline-block";
	style.clear = "both";
	style.float = "left";
	style.fontSize = (1000 * options.fontSizeFactor) + "px";
	style.lineHeight = "1000px";
	style.whiteSpace = options.whiteSpace;
	style.textAlign = options.textAlign;
	style.position = "relative";
	style.padding = 0;
	style.margin = 0;
	style.left = "50%";
	style.top = "50%";

	//Get properties of parent to allow easier referencing later.
	var parentPadding = {
		top: parseInt(parentComputedStyle.getPropertyValue("padding-top")),
		right: parseInt(parentComputedStyle.getPropertyValue("padding-right")),
		bottom: parseInt(parentComputedStyle.getPropertyValue("padding-bottom")),
		left: parseInt(parentComputedStyle.getPropertyValue("padding-left")),
	};
	var parentBorder = {
		top: parseInt(parentComputedStyle.getPropertyValue("border-top")),
		right: parseInt(parentComputedStyle.getPropertyValue("border-right")),
		bottom: parseInt(parentComputedStyle.getPropertyValue("border-bottom")),
		left: parseInt(parentComputedStyle.getPropertyValue("border-left")),
	};

	//Calculate the parent inner width and height
	var parentInnerDimensions = _calculateInnerDimensions(parentComputedStyle);
	var parentInnerWidth = parentInnerDimensions["width"];
	var parentInnerHeight = parentInnerDimensions["height"];
	
	var box = {
		width: element.offsetWidth, //Note: This is slightly larger than the jQuery version
		height: element.offsetHeight,
	};

	
	if (options.rotateText !== null) {
		if (typeof options.rotateText !== "number")
			throw "bigText error: rotateText value must be a number";
		var rotate= "rotate(" + options.rotateText + "deg)";
		style.webkitTransform = rotate;
		style.msTransform = rotate;
		style.MozTransform = rotate;
		style.OTransform = rotate;
		style.transform = rotate;
		//calculating bounding box of the rotated element
		var sine = Math.abs(Math.sin(options.rotateText * Math.PI / 180));
		var cosine = Math.abs(Math.cos(options.rotateText * Math.PI / 180));
		box.width = element.offsetWidth * cosine + element.offsetHeight * sine;
		box.height = element.offsetWidth * sine + element.offsetHeight * cosine;
	}
	
	var widthFactor = (parentInnerWidth - parentPadding.left - parentPadding.right) / box.width;
	var heightFactor = (parentInnerHeight - parentPadding.top - parentPadding.bottom) / box.height;
	var lineHeight;

	if (options.limitingDimension.toLowerCase() === "width") {
		lineHeight= Math.floor(widthFactor * 1000);
		parentStyle.height = lineHeight + "px";
	} else if (options.limitingDimension.toLowerCase() === "height") {
		lineHeight= Math.floor(heightFactor * 1000);
	} else if (widthFactor < heightFactor)
		lineHeight= Math.floor(widthFactor * 1000);
	else if (widthFactor >= heightFactor)
		lineHeight= Math.floor(heightFactor * 1000);

	var fontSize = lineHeight * options.fontSizeFactor;
	if (options.maximumFontSize !== null && fontSize > options.maximumFontSize) {
		fontSize = options.maximumFontSize;
		lineHeight = fontSize / options.fontSizeFactor;
	}

	style.fontSize = Math.floor(fontSize) + "px";
	style.lineHeight = Math.ceil(lineHeight)  + "px";
	style.marginBottom = "0px";
	style.marginRight = "0px";

	if (options.limitingDimension.toLowerCase() === "height") {
		//this option needs the font-size to be set already so computedStyle.getPropertyValue("width") returns the right size
		//this +4 is to compensate the rounding erros that can occur due to the calls to Math.floor in the centering code
		parentStyle.width = (parseInt(computedStyle.getPropertyValue("width")) + 4) + "px";
	}

	//Calculate the inner width and height
	var innerDimensions = _calculateInnerDimensions(computedStyle);
	var innerWidth = innerDimensions["width"];
	var innerHeight = innerDimensions["height"];

	switch(options.verticalAlign.toLowerCase()) {
		case "top":
			style.top = "0%";
		break;
		case "bottom":
			style.top = "100%";
			style.marginTop = Math.floor(-innerHeight) + "px";
		break;
		default:
			style.marginTop = Math.floor((-innerHeight / 2)) + "px";
		break;
	}

	switch(options.horizontalAlign.toLowerCase()) {
		case "left":
			style.left = "0%";
		break;
		case "right":
			style.left = "100%";
			style.marginLeft = Math.floor(-innerWidth) + "px";
		break;
		default:
			style.marginLeft = Math.floor((-innerWidth / 2)) + "px";
		break;
	}

	//shows the element after the work is done
	style.visibility = "visible";

	return element;
}

//module.exports = BigText;