function showDeletedActions(){
  django.jQuery('#showdeleted').click(function(){
    window.location = django.jQuery('#changelist-filter h3:contains("deleted") + ul li a:contains("Yes")').attr('href')
    return false;
  });
  django.jQuery('#hidedeleted').click(function(){
    window.location = django.jQuery('#changelist-filter h3:contains("deleted") + ul li a:contains("No")').attr('href')
    return false;
  });
}
