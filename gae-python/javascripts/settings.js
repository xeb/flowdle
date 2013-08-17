$(document).ready(function(){
    hideMsg = function(){ $('h6').hide("slow") }           
    if($('h6').html() != '') {
        setTimeout('hideMsg()', 2000);  }
        
    $('#nudge').change(function(e){ 
        setValue('nudge', $(this).val()) }).change();
});