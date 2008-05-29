document.observe('dom:loaded', function() {
	$('taskname').value = '';
	
	hideNewTask = function() {
		$('newtask').addClassName('hiding');
		$('taskname').value = '';
	}
	
	$('cancel').observe('click', hideNewTask);
	$('save').observe('click', hideNewTask);
	
	// When TaskName gets focus
	$('taskname').observe('click', function(e){
		$('newtask').removeClassName('hiding');
		$('nudgelist').observe('change', function(e){
			if($('nudgelist').value == 'Specific Date...') {
				$('nudge_date').removeClassName('hiding');
			} else {
				$('nudge_date').addClassName('hiding');
			}
		});
	})
});
