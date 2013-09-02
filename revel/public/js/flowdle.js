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

	$('.submit').bind('click', function(){
		$.fn.popTag();
	});

	var selectedTag = $('#selected-tag').val();
	$('.nav-list li a').each(function(i,e){
		if($(e).text() == selectedTag) {
			$(e).parent().addClass('active')
		}
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