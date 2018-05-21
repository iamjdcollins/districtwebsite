// Gets the position of an element top left corner relative to viewport
function getPageTopLeft(el) {
    var rect = el.getBoundingClientRect();
    var docEl = document.documentElement;
    return {
        left: rect.left + (window.pageXOffset || docEl.scrollLeft || 0),
        top: rect.top + (window.pageYOffset || docEl.scrollTop || 0)
    };
}

// Aligns the sites list menu to the left and ends at the right edge of the trigger button.
function alignSiteList(){
  el = document.getElementById('siteslist')
  getPageTopLeft(el);
  el.style['width'] = (parseInt(el.style['width']) + parseInt(el.style['left'])).toString() + 'px';
  el.style['left'] = '0px';
  el.style['visibility'] = 'visible';
}

// Removes the visibility attribute when the sites list is close to avoid jumping in place on future opens.
function closedSiteList(){
  el = document.getElementById('siteslist')
  el.style.removeProperty('visibility')
}

// Initializes the sites list menu.
function initSitesList(){
  var elem = document.getElementById('siteslist-trigger');
  var instance = M.Dropdown.init(elem, {
      alignment: 'right',
      constrainWidth: false,
      coverTrigger: false,
      closeOnClick: true,
      hover: false,
      inDuration: 100,
      outDuration: 100,
      onOpenEnd: alignSiteList,
      onCloseEnd: closedSiteList,
  });
}
// Initialize select lists.
function initSelect(){
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems);
}

// Runs on document loaded
(function(){
  initSitesList();
  initSelect();
})();
