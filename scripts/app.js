var letters=' ABCÇDEFGHIJKLMNÑOPQRSTUVWXYZabcçdefghijklmnñopqrstuvwxyzàáÀÁéèÈÉíìÍÌïÏóòÓÒúùÚÙüÜ'
var numbers='1234567890'
var signs=',.:;@-\''
var mathsigns='+-=()*/'
var custom='<>#$%&?¿'

document.observe('dom:loaded', function() {
	$('taskname').value = '';
	$('taskname').focus();
	
	if($('taskname').getValue() != '') {
		$('newtask').removeClassName('hiding');
	}
	
	hideNewTask = function() {
		$('newtask').addClassName('hiding');
		$('taskname').value = '';
		$('mainTable').show();
	}
	
	$('cancel').observe('click', hideNewTask);
	
	// When TaskName gets focus
	$('taskname').observe('keydown', function(e){
        if(validKey(e, letters + numbers + signs + mathsigns + custom)) {
		    $('newtask').removeClassName('hiding');
	    }
	})
	
	// nudge date show-er
	$('nudge').observe('change', function(e){ 
		if($('nudge').getValue() == 'specific') { 
			$('nudge_date').removeClassName('hiding');
		} else {
			$('nudge_date').addClassName('hiding');
		}
	});
	
	// edit 
	$$('#biglist .right a').invoke('observe', 'click', function(event){
       var id = event.element().id;
       var nudge = $$('#' + id + ' span.nudge_date')
       alert(nudge);
       $('editkey').setValue(id);
       $('newtask').removeClassName('hiding');
       $('mainTable').hide();
       $('taskname').setValue($('name' + id).innerHTML)
       return false;
	});
});

function validKey(e, allow) {
 var k;
 k=document.all?parseInt(e.keyCode): parseInt(e.which);
 return (allow.indexOf(String.fromCharCode(k))!=-1);
}
