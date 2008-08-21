
document.observe('dom:loaded', function() {
   $$('input.check').invoke('observe', 'click', function(event){
       window.location = '/app/all';
   });
});