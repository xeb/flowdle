var server = {};
InstallFunction(server, 'getTask');
InstallFunction(server, 'getTaskCompleteDate')
InstallFunction(server, 'deleteTask')
InstallFunction(server, 'toggleComplete');
InstallFunction(server, 'isRepeat')

$(document).ready(function() {
    
    $('body').keypress(function(){
        
    });
    
	$('#taskname').val('');
	$('#taskname').focus();
	
	if($('#taskname').val() != '') {
		$('#newtask').removeClass('hiding');
	}
	
	hideNewTask = function() {
		$('#newtask').addClass('hiding');
		$('#taskname').val('');
		$('#taskname').focus();
		$('#taskkey').val('');
		$('#mainTable').show();
	}
	
	$('#cancel').click(hideNewTask);
	
	// home
	$('#logo').click(function(e){ 
	    window.location = '/';  
	});
	
	// new task
	$('#taskname').keyup(function(e){
        if($('#taskname').val() != '') {
		    $('#newtask').removeClass('hiding');
		    $('#newtask').show("slow");
	    }
	})
	
	// nudge date show-er
	$('#nudge, #repeat').change(function(e){ 
        setValue('nudge', $(this).val())
	}).change();
	
	// edit 
	$('#biglist .right a.editlink').click(function(){
       var id = $(this).attr('id').substring(4);
       server.getTask(id, function(task){
          if(task) {
              $('#newtask').removeClass('hiding');
              $('#mainTable').hide();
              $('#taskname').val(task.name);
              $('#taglist').val(task.tags);
              $('#nudge').val(task.nudge);
              $('#taskkey').val(task.key);
              if(task.repeat && task.repeat == 'True') {
                  $('#repeat').attr('checked', true);
              } else {
                  $('#repeat').attr('checked', false);
              }
              setValue('nudge', task.nudge, task.nudge_value);
           }
       });
	});
	
	$('#biglist .right a.deletelink').click(function(){
       var id = $(this).attr('id').substring(6);
       if(confirm('Are you sure you want to delete this task?')) {
           server.deleteTask(id, function(result) {
              if(result) {
                  $('#tr'+id).hide()
              } else {
                  alert('Could not delete')
              }
           });
       }
    });    
	
	// complete
	$('#biglist .left .checkbox').click(function(){
	    var id = $(this).attr('id').substring(5);
	    $('#name'+id).addClass('complete'); 
	    server.toggleComplete(id, function(event){
            if(event){
                if($('#check'+id).attr('checked')) {
	                $('#edit'+id).hide();
	                $('#delete'+id).hide();
	                
	                var repeat = false
	                server.isRepeat(id, function(result) {
	                    if(result) {
	                        $('check'+id).disable();
	                        repeat = true
	                    }
	                    
    	                server.getTaskCompleteDate(id, function(date) {
	                        if(date) {
	                            if(repeat) {
                                    $('#nudge'+id).html('Done on ' + date + ' <br /> (repeat created)')
	                            } else {
	                                $('#nudge'+id).html('Done on ' + date)
	                            }
	                            $('#nudge'+id).addClass('complete')
	                        }
	                    });

	                });
                } else {
                    $('#name'+id).removeClass('complete')
                    $('#edit'+id).show();
                    $('#delete'+id).show();
                    server.getTask(id, function(task){
                        if(task) {
                            if(task.repeat == 'True') {
                              $('#nudge'+id).html('Nudge me '+ task.nudge +  ' (repeats)')
                            } else {
                                $('#nudge'+id).html('Nudge me '+ task.nudge)
                            }
                            $('#nudge'+id).removeClass('complete')
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
