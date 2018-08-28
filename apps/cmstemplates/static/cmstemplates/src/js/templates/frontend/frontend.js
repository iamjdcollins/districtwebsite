/* Zenscroll 4.0.2 https://zengabor.github.io/zenscroll/ */
!function(t,e){"function"==typeof define&&define.amd?define([],e()):"object"==typeof module&&module.exports?module.exports=e():function n(){document&&document.body?t.zenscroll=e():setTimeout(n,9)}()}(this,function(){"use strict";var t=function(t){return t&&"getComputedStyle"in window&&"smooth"===window.getComputedStyle(t)["scroll-behavior"]};if("undefined"==typeof window||!("document"in window))return{};var e=function(e,n,o){n=n||999,o||0===o||(o=9);var i,r=function(t){i=t},u=function(){clearTimeout(i),r(0)},c=function(t){return Math.max(0,e.getTopOf(t)-o)},a=function(o,i,c){if(u(),0===i||i&&i<0||t(e.body))e.toY(o),c&&c();else{var a=e.getY(),f=Math.max(0,o)-a,s=(new Date).getTime();i=i||Math.min(Math.abs(f),n),function t(){r(setTimeout(function(){var n=Math.min(1,((new Date).getTime()-s)/i),o=Math.max(0,Math.floor(a+f*(n<.5?2*n*n:n*(4-2*n)-1)));e.toY(o),n<1&&e.getHeight()+o<e.body.scrollHeight?t():(setTimeout(u,99),c&&c())},9))}()}},f=function(t,e,n){a(c(t),e,n)},s=function(t,n,i){var r=t.getBoundingClientRect().height,u=e.getTopOf(t)+r,s=e.getHeight(),l=e.getY(),d=l+s;c(t)<l||r+o>s?f(t,n,i):u+o>d?a(u-s+o,n,i):i&&i()},l=function(t,n,o,i){a(Math.max(0,e.getTopOf(t)-e.getHeight()/2+(o||t.getBoundingClientRect().height/2)),n,i)};return{setup:function(t,e){return(0===t||t)&&(n=t),(0===e||e)&&(o=e),{defaultDuration:n,edgeOffset:o}},to:f,toY:a,intoView:s,center:l,stop:u,moving:function(){return!!i},getY:e.getY,getTopOf:e.getTopOf}},n=document.documentElement,o=function(){return window.scrollY||n.scrollTop},i=e({body:document.scrollingElement||document.body,toY:function(t){window.scrollTo(0,t)},getY:o,getHeight:function(){return window.innerHeight||n.clientHeight},getTopOf:function(t){return t.getBoundingClientRect().top+o()-n.offsetTop}});if(i.createScroller=function(t,o,i){return e({body:t,toY:function(e){t.scrollTop=e},getY:function(){return t.scrollTop},getHeight:function(){return Math.min(t.clientHeight,window.innerHeight||n.clientHeight)},getTopOf:function(t){return t.offsetTop}},o,i)},"addEventListener"in window&&!window.noZensmooth&&!t(document.body)){var r="history"in window&&"pushState"in history,u=r&&"scrollRestoration"in history;u&&(history.scrollRestoration="auto"),window.addEventListener("load",function(){u&&(setTimeout(function(){history.scrollRestoration="manual"},9),window.addEventListener("popstate",function(t){t.state&&"zenscrollY"in t.state&&i.toY(t.state.zenscrollY)},!1)),window.location.hash&&setTimeout(function(){var t=i.setup().edgeOffset;if(t){var e=document.getElementById(window.location.href.split("#")[1]);if(e){var n=Math.max(0,i.getTopOf(e)-t),o=i.getY()-n;0<=o&&o<9&&window.scrollTo(0,n)}}},9)},!1);var c=new RegExp("(^|\\s)noZensmooth(\\s|$)");window.addEventListener("click",function(t){for(var e=t.target;e&&"A"!==e.tagName;)e=e.parentNode;if(!(!e||1!==t.which||t.shiftKey||t.metaKey||t.ctrlKey||t.altKey)){if(u){var n=history.state&&"object"==typeof history.state?history.state:{};n.zenscrollY=i.getY();try{history.replaceState(n,"")}catch(t){}}var o=e.getAttribute("href")||"";if(0===o.indexOf("#")&&!c.test(e.className)){var a=0,f=document.getElementById(o.substring(1));if("#"!==o){if(!f)return;a=i.getTopOf(f)}t.preventDefault();var s=function(){window.location=o},l=i.setup().edgeOffset;l&&(a=Math.max(0,a-l),r&&(s=function(){history.pushState({},"",o)})),i.toY(a,null,s)}}},!1)}return i});
/* GTranslate */
function googleTranslateElementInit2() {new google.translate.TranslateElement({pageLanguage: 'en',autoDisplay: false}, 'google_translate_element2');}
/**
 * Simulate a click event.
 * @public
 * @param {Element} elem  the element to simulate a click on
 */
var simulateClick = function (elem) {
  // Create our event (with options)
  var evt = new MouseEvent('click', {
    bubbles: true,
    cancelable: true,
    view: window
  });
  // If cancelled, don't dispatch our event
  var canceled = !elem.dispatchEvent(evt);
};


// Open external links in new window
$("a").each( function( index, item){ if ( window.location.hostname !== item.hostname) { $(item).attr('target', '_blank') }});

// Show/Hide dropdown
function toggleDropdown(event){
  element = document.getElementById(this.getAttribute('data-activates'))
  if (element.classList) { 
    element.classList.toggle("open");
  } else {
    // For IE9
    var classes = element.className.split(" ");
    var i =  classes.indexOf("open");
    if (i >= 0){
      classes.splice(i, 1);
    } else {
      classes.push("open");
      element.className = classes.join(" "); 
    }
  }
  event.preventDefault ? event.preventDefault() : event.returnValue = false;
}
// Show/Hide slideleft
function toggleSlideleft(event){
  element = document.getElementById(this.getAttribute('data-activates'))
  if (element.classList) { 
    element.classList.toggle("open");
  } else {
    // For IE9
    var classes = element.className.split(" ");
    var i =  classes.indexOf("open");
    if (i >= 0){
      classes.splice(i, 1);
    } else {
      classes.push("open");
      element.className = classes.join(" "); 
    }
  }
  event.preventDefault ? event.preventDefault() : event.returnValue = false;
}
function closeSlideleft(event){
  if(this == event.target){
    element = document.getElementById(this.getAttribute('id'))
    if (element.classList) { 
      element.classList.toggle("open");
    } else {
      // For IE9
      var classes = element.className.split(" ");
      var i =  classes.indexOf("open");
      if (i >= 0){
        classes.splice(i, 1);
      } else {
        classes.push("open");
        element.className = classes.join(" "); 
      }
    }
  }
  event.preventDefault ? event.preventDefault() : event.returnValue = false;
}
// Initialize dropdown-button
function initDropdown(){
  var buttons = document.querySelectorAll(".dropdown-button");
  buttons.forEach(function(item){
    if (item.addEventListener) {                    // For all major browsers, except IE 8 and earlier
      item.addEventListener("click", toggleDropdown);
    } else if (item.attachEvent) {                  // For IE 8 and earlier versions
      item.attachEvent("onclick", toggleDropdown);
    }
  });
}
// Initialize slideleft-button
function initSlideleft(){
  var buttons = document.querySelectorAll(".slideleft-button");
  buttons.forEach(function(item){
    if (item.addEventListener) {                    // For all major browsers, except IE 8 and earlier
      item.addEventListener("click", toggleSlideleft);
    } else if (item.attachEvent) {                  // For IE 8 and earlier versions
      item.attachEvent("onclick", toggleSlideleft);
    }
  });
  var contents = document.querySelectorAll(".slideleft-content");
  contents.forEach(function(item){
    if (item.addEventListener) {                    // For all major browsers, except IE 8 and earlier
      item.addEventListener("click", closeSlideleft);
    } else if (item.attachEvent) {                  // For IE 8 and earlier versions
      item.attachEvent("onclick", closeSlideleft);
    }
  });
}
function initKeyDown(){
  document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode == 27) {
        var boxes = document.querySelectorAll(".nav-trigger");
        boxes.forEach(function(item){
          item.checked = false
        });
    }
  };
}

function toggleBodyOverflow(){
	var element = document.getElementById('top')
	if (element.classList) {
        element.classList.toggle("nooverflow");
	} else {
	    // For IE9
	    var classes = element.className.split(" ");
	    var i = classes.indexOf("nooverflow");

	    if (i >= 0)
	        classes.splice(i, 1);
	    else
	        classes.push("nooverflow");
	        element.className = classes.join(" ");
	} 
}

function mobileMenuVisibleScrollLock(){
	var  triggers = document.querySelectorAll(".nav-trigger-label");
	triggers.forEach(function(item){
        item.addEventListener("click", toggleBodyOverflow)
	});
}

function closeMobileMenus(){
	var  triggers = document.querySelectorAll(".nav-trigger-label");
	triggers.forEach(function(item){
        input = document.getElementById(item.htmlFor)
        if (input.checked){
          simulateClick(item);
        }
	});
}

function closeMobileMenusEvent(){
  var  triggers = document.querySelectorAll(".sidenav .nav-item");
  triggers.forEach(function(item){
        item.addEventListener("click", closeMobileMenus)
  });
}

initKeyDown();
initDropdown();
mobileMenuVisibleScrollLock();
closeMobileMenusEvent();
$(".editlink").each(function(index, element){
  $(element).attr('href', $(element).attr('href') + '?next=' + btoa(window.location));
});

$(".modal-ajax").modaal({
    type: 'ajax',
    custom_class: 'modaal-ajax',
    after_callback_delay: 300,
    after_open: function(modal){
      $(modal).find('.modaal-focus').each(function(index,element){
        if(index === 0){
          $(element).removeAttr('aria-label')
          $(element).attr('aria-labelledby','pagefeedbacktitle')
          $(element).attr('aria-describedby','pagefeedbackdesc')
          $(element).focus()
        }
      });
    },
  });

// GTranslate Init
/*! gtranslate !*/
function GTranslateFireEvent(a,b)
	{
	try
		{
		if(document.createEvent)
			{
			var c=document.createEvent("HTMLEvents");
			c.initEvent(b,true,true);
			a.dispatchEvent(c)
		}
		else
			{
			var c=document.createEventObject();
			a.fireEvent('on'+b,c)
		}
	}
	catch(e)
		{
	}
}
function doGTranslate(a)
	{
	if(a.value)a=a.value;
	if(a=='')return;
	var b=a.split('|')[1];
	var c;
	var d=document.getElementsByTagName('select');
	for(var i=0;
	i<d.length;
	i++)if(d[i].className=='goog-te-combo')c=d[i];
	if(document.getElementById('google_translate_element2')==null||document.getElementById('google_translate_element2').innerHTML.length==0||c.length==0||c.innerHTML.length==0)
		{
		setTimeout(function()
			{
			doGTranslate(a)
		}
		,500)
	}
	else
		{
		c.value=b;
		GTranslateFireEvent(c,'change');
		GTranslateFireEvent(c,'change')
	}
}
