var server = {};
InstallFunction(server, 'toggleComplete');
InstallFunction(server, 'getTask');
    
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
        if($('taskname').getValue() != '') {
		    $('newtask').removeClassName('hiding');
	    }
	})
	
	// nudge date show-er
	$('nudge').observe('change', function(e){ 
		var val = $('nudge').getValue();
		if(val == 'daily') {
		    $('nudge_week').addClassName('hiding');
		}
		if(val == 'weekly') { 
			$('nudge_week').removeClassName('hiding');
		}
		if(val == 'monthly') {
		    $('nudge_week').addClassName('hiding');
		}
		if(val == 'never') {
		    $('nudge_week').addClassName('hiding');
		}
	});
	
	// edit 
	$$('#biglist .right a').invoke('observe', 'click', function(event){
       var id = event.element().id.substring(4);
       server.getTask(id, function(task){
          $('newtask').removeClassName('hiding');
          $('mainTable').hide();
          $('taskname').setValue(task.name);
          $('taglist').setValue(task.tags);
          $('nudge').setValue(task.nudge);
       });
       //$('editkey').setValue(id);
       //$('newtask').removeClassName('hiding');
       //$('mainTable').hide();
       //$('taskname').setValue($('name' + id).innerHTML)
       //return false;
	});
	
	
	$('logo').observe('click', function(event){
	    var img = $(event.element().id);
	    if(img.src.match('logo.gif')) { img.src = img.src.replace('logo.gif', 'logo2.gif'); }
	    else if(img.src.match('logo2.gif')) { img.src = img.src.replace('logo2.gif', 'logo3.gif'); }
	    else if(img.src.match('logo3.gif')) { img.src = img.src.replace('logo3.gif', 'logo4.gif'); }
	    else if(img.src.match('logo4.gif')) { img.src = img.src.replace('logo4.gif', 'logo.gif'); }
	});
	
	// complete
	$$('#biglist .left .checkbox').invoke('observe', 'click', function(event){
	    var id = event.element().id.substring(5);
	    //alert(id);
	    server.toggleComplete(id, function(event){
	        if(event){
	            if($('check'+id).checked) {
	                $('name'+id).addClassName('complete'); 
                } else {
                    $('name'+id).removeClassName('complete')
                }
	        }
	        else {
                alert('Oops!  Something went wrong.');
            }
	    })
	});
});

