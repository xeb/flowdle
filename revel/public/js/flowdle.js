$(function(){
	$('.newTask')
		.keydown(function(){$(this).removeClass('hiding');})
		.blur(function(){ 
			if($(this).val().length == 0) {
				$(this).addClass('hiding');
			}
		})
		.focus()
		;



});