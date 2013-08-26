$(function(){
	$('.newTask')
		.keydown(function(){$(this).parent().parent().removeClass('hiding');})
		.blur(function(){ 
			if($(this).val().length == 0) {
				$(this).parent().parent().addClass('hiding');
			}
		})
		.focus()
		;

	$("#tagentry").tagsManager({
		prefilled: $('#tags').val().split(',')
	});

});