$(document).ready(function() {

				$('a.frame').click(function() {
								$('a.frame').removeClass("target");
								$('.border').removeClass('blue-background');

								$(this).addClass("target");
								$(this).parent().addClass('blue-background');
								$('div.set_target').removeClass('disabled');
				});

				$('div.set_target').click(function() {
								if  (!$(this).hasClass('disabled')) {
												var frame = $('.target').data('frame');
												var basename = $('.target').data('basename');
												$.get('/convert', 
																			{ frame : frame,
																					basename : basename
																			}).done(function(data) {
																							window.location = data;
																			});
								}
				});
				
				

});
