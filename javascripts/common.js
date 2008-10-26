function setValue(type, val, nudgeVal) {
    	if(val == 'daily') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
            $('#nudge_label').show();
		}
		if(val == 'weekly') { 
			$('#' + type + '_week').removeClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
		    if(nudgeVal && nudgeVal != ''){
		        $('#' + type + '_' + nudgeVal).attr('checked',true);
		    }
            $('#nudge_label').show();
		}
		if(val == 'monthly') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').removeClass('hiding');
		    if(nudgeVal && nudgeVal != '') {
		        $('#' + type + '_month_value').val(nudgeVal); }
            $('#nudge_label').show();		    
		}
		if(val == 'never') {
		    $('#' + type + '_week').addClass('hiding');
		    $('#' + type + '_month').addClass('hiding');
            $('#nudge_label').hide();		    
		}
}

