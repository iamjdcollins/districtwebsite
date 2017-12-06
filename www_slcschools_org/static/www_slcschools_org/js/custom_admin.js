django.jQuery(document).ready(function(){
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
  nextURL = btoa(window.location)
  django.jQuery('.editlink').each(function(index,element){
    django.jQuery(element).attr('href', django.jQuery(element).attr('href') + '?next=' + nextURL)
  });
  console.log(atob(nextURL))
});
