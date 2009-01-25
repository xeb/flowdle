function setValue(type, val, nudgeVal) {
    	if(val == 'daily') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
		    $('#' + type + '_year').addClass('hiding');
		    $('#' + type + '_frequently').addClass('hiding');
            $('#nudge_label').show();
		}
		if(val == 'frequently') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
		    $('#' + type + '_year').addClass('hiding');
		    $('#' + type + '_frequently').removeClass('hiding');
            $('#nudge_label').show();		    
		}
		if(val == 'weekly') { 
			$('#' + type + '_week').removeClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
		    $('#' + type + '_year').addClass('hiding');
		    $('#' + type + '_frequently').addClass('hiding');
		    if(nudgeVal && nudgeVal != ''){
		        $('#' + type + '_' + nudgeVal).attr('checked',true);
		    }
            $('#nudge_label').show();
		}
		if(val == 'monthly') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').removeClass('hiding');
		    $('#' + type + '_year').addClass('hiding');
		    $('#' + type + '_frequently').addClass('hiding');
		    if(nudgeVal && nudgeVal != '') {
		        $('#' + type + '_month_value').val(nudgeVal); }
            $('#nudge_label').show();		    
		}
		if(val == 'yearly') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
		    $('#' + type + '_year').removeClass('hiding');
		    $('#' + type + '_frequently').addClass('hiding');
		    if(nudgeVal && nudgeVal != '') {
		        $('#' + type + '_year_value').val(nudgeVal); }
            $('#nudge_label').show();		    
		}
		if(val == 'never') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
		    $('#' + type + '_year').addClass('hiding');
            $('#nudge_label').hide();		    
		}
}

