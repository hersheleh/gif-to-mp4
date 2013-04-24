$(document).ready(function() {

				$('a.frame').click(function() {
								$('a.frame').removeClass("target");
								$(this).addClass("target");
								$('div.set_target').removeClass('disabled');
				});

				$('div.set_target').click(function() {
								if  (!$(this).hasClass('disabled')) {
												var frame = $('.target').data('frame');
												var basename = $('.target').data('basename');
												$.get('/convert', 
																			{ frame : frame,
																					basename : basename
																			}).done(function() {
																							window.location="/home";
																			});
								}
				});
				
				

});
