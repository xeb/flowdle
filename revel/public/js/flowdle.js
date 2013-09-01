$(function(){
	$('.newTask')
		.keyup(function(){
			if($(this).val() != '') {
				$(this).parent().parent().removeClass('hiding');
			}
		})
		.blur(function(){ 
			if($(this).val() == '') {
				$(this).parent().parent().addClass('hiding');
			}
		})
		.focus()
		;

	$("#tagentry").tagsManager({
		prefilled: $('#tags').val().split(',')
	});

	$('.tasks input:checkbox').bind('click', function(){
		var chkd = $(this).is(':checked');
		var parent = $(this).parent();
		var menu = parent.find('.btn-group .btn.dropdown-toggle');
		if(chkd) {
			parent.addClass('complete');
			// menu.removeData('toggle');
			// $(this).prop('disabled', true);
		} else {
			parent.removeClass('complete');
			// menu.data('toggle', 'dropdown');
			// $(this).prop('disabled', false);
		}
	})
});