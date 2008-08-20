var server = {};
InstallFunction(server, 'toggleComplete');
InstallFunction(server, 'getTask');
InstallFunction(server, 'getTaskCompleteDate')

document.observe('dom:loaded', function() {
    
	$('taskname').setValue('');
	$('taskname').focus();
	
	if($('taskname').getValue() != '') {
		$('newtask').removeClassName('hiding');
	}
	
	hideNewTask = function() {
		$('newtask').addClassName('hiding');
		$('taskname').setValue('');
		$('taskname').focus();
		$('taskkey').setValue('');
		$('mainTable').show();
	}
	
	$('cancel').observe('click', hideNewTask);
	
	// new task
	$('taskname').observe('keydown', function(e){
        if($('taskname').getValue() != '') {
		    $('newtask').removeClassName('hiding');
	    }
	})
	
	// nudge date show-er
	$('nudge').observe('change', function(e){ 
		var val = $('nudge').getValue();
        setNudgeValue(val)
	});
	
	// edit 
	$$('#biglist .right a').invoke('observe', 'click', function(event){
       var id = event.element().id.substring(4);
       server.getTask(id, function(task){
          if(task) {
              $('newtask').removeClassName('hiding');
              $('mainTable').hide();
              $('taskname').setValue(task.name);
              $('taglist').setValue(task.tags);
              $('nudge').setValue(task.nudge);
              $('taskkey').setValue(task.key);
              setNudgeValue(task.nudge, task.nudge_value);
           }
       });
	});
	
	// complete
	$$('#biglist .left .checkbox').invoke('observe', 'click', function(event){
	    var id = event.element().id.substring(5);
	    server.toggleComplete(id, function(event){
	        if(event){
	            if($('check'+id).checked) {
	                $('name'+id).addClassName('complete'); 
	                $('edit'+id).hide();
	                
	                server.getTaskCompleteDate(id, function(date) {
	                    if(date) {
	                        $('nudge'+id).update('Done on ' + date)
	                    }
	                });
	                
                } else {
                    $('name'+id).removeClassName('complete')
                    $('edit'+id).show();
                    server.getTask(id, function(task){
                        if(task) {
                            $('nudge'+id).update('Nudge me '+ task.nudge)
                        }
                    });
                }
	        }
	        else {
                alert('Oops!  Something went wrong.');
            }
	    })
	});
});

function setNudgeValue(val, nudgeVal) {
    	if(val == 'daily') {
		    $('nudge_week').addClassName('hiding');
		    $('nudge_month').addClassName('hiding');
		}
		if(val == 'weekly') { 
			$('nudge_week').removeClassName('hiding');
		    $('nudge_month').addClassName('hiding');
		    if(nudgeVal){
		        $('nudge_' + nudgeVal).checked = true;
		    }
		}
		if(val == 'monthly') {
		    $('nudge_week').addClassName('hiding');
		    $('nudge_month').removeClassName('hiding');
		    $('nudge_month_value').setValue(nudgeVal);
		}
		if(val == 'never') {
		    $('nudge_week').addClassName('hiding');
		    $('nudge_month').addClassName('hiding');
		}
}

