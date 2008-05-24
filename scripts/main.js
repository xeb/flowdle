document.observe('dom:loaded', function() {

	$('email').observe('click', function(e){
		$('email').value = '';
	})

	$('submit').observe('click', function(e){
		new Ajax.Request('/index.html', {
			method: 'post',
			parameters: { email: $('email').value },
			onSuccess: function(response) {
				$$('#body .coming-soon img').each(function(img) {
					img.src = '/images/thankyou.gif';
				});
				$$('#body .form').each(function(div){
					div.setStyle({'display':'none'});
				});
			},
			onFailure: function(response) {
				window.location = 'errors/500.html'
			}
		});
		Event.stop(e);
	}, false);

});