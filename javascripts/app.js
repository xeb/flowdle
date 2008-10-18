var server = {};
InstallFunction(server, 'getTask');
InstallFunction(server, 'getTaskCompleteDate')
InstallFunction(server, 'deleteTask')
InstallFunction(server, 'toggleComplete');
InstallFunction(server, 'isRepeat')

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
	
	// home
	$('logo').observe('click',function(e){ 
	    window.location = '/';  
	});
	
	// new task
	$('taskname').observe('keyup', function(e){
        if($('taskname').getValue() != '') {
		    $('newtask').removeClassName('hiding');
	    }
	})
	
	// nudge date show-er
	$('nudge').observe('change', function(e){ 
		var val = $('nudge').getValue();
        setValue('nudge', val)
	});
	
	// repeat date show-er
	$('repeat').observe('change', function(e){ 
		var val = $('repeat').getValue();
        setValue('repeat', val)
	});
	
	// edit 
	$$('#biglist .right a.editlink').invoke('observe', 'click', function(event){
       var id = event.element().id.substring(4);
       server.getTask(id, function(task){
          if(task) {
              $('newtask').removeClassName('hiding');
              $('mainTable').hide();
              $('taskname').setValue(task.name);
              $('taglist').setValue(task.tags);
              $('nudge').setValue(task.nudge);
              $('taskkey').setValue(task.key);
              if(task.repeat && task.repeat == 'True') {
                  $('repeat').checked = true;
              } else {
                  $('repeat').checked == false;
              }
              setValue('nudge', task.nudge, task.nudge_value);
           }
       });
	});
	
	$$('#biglist .right a.deletelink').invoke('observe', 'click', function(event){
       var id = event.element().id.substring(6);
       if(confirm('Are you sure you want to delete this task?')) {
           server.deleteTask(id, function(result) {
              if(result) {
                  $('tr'+id).hide()
              } 
           });
       }
    });    
	
	// complete
	$$('#biglist .left .checkbox').invoke('observe', 'click', function(event){
	    var id = event.element().id.substring(5);
	    server.toggleComplete(id, function(event){
            if(event){
	            if($('check'+id).checked) {
	                $('name'+id).addClassName('complete'); 
	                $('edit'+id).hide();
	                $('delete'+id).hide();
	                
	                var repeat = false
	                server.isRepeat(id, function(result) {
	                    if(result) {
	                        $('check'+id).disable();
	                        repeat = true
	                    }
	                    
    	                server.getTaskCompleteDate(id, function(date) {
	                        if(date) {
	                            if(repeat) {
                                    $('nudge'+id).update('Done on ' + date + ' <br /> (repeat created)')
	                            } else {
	                                $('nudge'+id).update('Done on ' + date)
	                            }
	                            $('nudge'+id).addClassName('complete')
	                        }
	                    });

	                });
	                
                } else {
                    $('name'+id).removeClassName('complete')
                    $('edit'+id).show();
                    $('delete'+id).show();
                    server.getTask(id, function(task){
                        if(task) {
                            if(task.repeat == 'True') {
                              $('nudge'+id).update('Nudge me '+ task.nudge +  ' (repeats)')
                            } else {
                                $('nudge'+id).update('Nudge me '+ task.nudge)
                            }
                            $('nudge'+id).removeClassName('complete')
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

function setValue(type, val, nudgeVal) {
    	if(val == 'daily') {
		    $(type + '_week').addClassName('hiding');
		    $(type + '_month').addClassName('hiding');
            $('nudge_label').show();
		}
		if(val == 'weekly') { 
			$(type + '_week').removeClassName('hiding');
		    $(type + '_month').addClassName('hiding');
		    if(nudgeVal){
		        $(type + '_' + nudgeVal).checked = true;
		    }
            $('nudge_label').show();
		}
		if(val == 'monthly') {
		    $(type + '_week').addClassName('hiding');
		    $(type + '_month').removeClassName('hiding');
		    $(type + '_month_value').setValue(nudgeVal);
            $('nudge_label').show();		    
		}
		if(val == 'never') {
		    $(type + '_week').addClassName('hiding');
		    $(type + '_month').addClassName('hiding');
            $('nudge_label').hide();		    
		}
}

