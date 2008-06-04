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
	}
	
	$('cancel').observe('click', hideNewTask);
	//$('save').observe('click', hideNewTask);
	
	// When TaskName gets focus
	$('taskname').observe('keydown', function(e){
        if(validKey(e, letters + numbers + signs + mathsigns + custom)) {
		    $('newtask').removeClassName('hiding');
	    }
	})
	
	// nudge dte show-er
	$('nudgelist').observe('change', function(e){
		if($('nudgelist').getValue() == 'Specific Date...') { 
			$('nudge_date').removeClassName('hiding');
		} else {
			$('nudge_date').addClassName('hiding');
		}
	});
});

function validKey(e, allow) {
 var k;
 k=document.all?parseInt(e.keyCode): parseInt(e.which);
 return (allow.indexOf(String.fromCharCode(k))!=-1);
}
