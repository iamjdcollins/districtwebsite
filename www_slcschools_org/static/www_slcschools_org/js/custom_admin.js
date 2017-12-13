django.jQuery(document).ready(function(){
  nextURL = btoa(window.location)

  var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
  };
  while( django.jQuery(".change-related").length > django.jQuery(".change-related.initialized").length ){
    console.log('waiting to initialize')
  }
  django.jQuery(".change-related").off()
  django.jQuery(".change-related").each(function(index,element){
    if( django.jQuery(this).attr('href') != undefined ){
      django.jQuery(this).attr('href',django.jQuery(this).attr('href').split('?')[0])
      django.jQuery(this).attr('href', django.jQuery(this).attr('href') + '?next=' + nextURL)
      var clone = this.cloneNode();
      while (this.firstChild) {
        clone.appendChild(this.lastChild);
      }
      this.parentNode.replaceChild(clone, this);
    }
  })
  while( django.jQuery(".add-related").length > django.jQuery(".add-related.initialized").length ){
    console.log('waiting to initialize')
  }
  django.jQuery(".add-related").off()
  django.jQuery(".add-related").each(function(index,element){
    if( django.jQuery(this).attr('href') != undefined ){
      django.jQuery(element).attr('href',django.jQuery(element).attr('href').split('?')[0])
      django.jQuery(element).attr('href', django.jQuery(element).attr('href') + '?next=' + nextURL)
      var clone = this.cloneNode();
      while (element.firstChild) {
        clone.appendChild(element.lastChild);
      }
      element.parentNode.replaceChild(clone, element);
    }
  })
  django.jQuery('.editlink').each(function(index,element){
    django.jQuery(element).attr('href', django.jQuery(element).attr('href') + '?next=' + nextURL)
  });
  console.log(atob(nextURL))
});
