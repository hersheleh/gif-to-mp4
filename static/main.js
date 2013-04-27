$(document).ready(function() {

				// select target is the default functionality
				bind_select_target_functionality();

				// When user clicks Choose a target
				$('.choose-target').click(function() {
								$('li').removeClass('active');
								$(this).addClass('active');
								unbind_all();
								bind_select_target_functionality();
				});

				// When user clicks Choose a Subset
				$('.choose-subset').click(function() {
								$('li').removeClass('active');
								$(this).addClass('active');
								unbind_all();
								bind_select_subset_functionality();
								$('.message').html('Select Start Frame')
				});

});

function bind_select_target_functionality() {
				
				// Sets the background color to green on hover
				$('.border').hover(
								function() {
												$(this).addClass('target-hover');
								},
								function() {
												$(this).removeClass('target-hover');
								}
				);
				// Sets the target on click
				$('a.frame').bind('click',function() {
								$('a.frame').removeClass("target");
								$('.border').removeClass('target-active');
								
								$(this).addClass("target");
								$(this).parent().addClass('target-active');
								$('div.convert').removeClass('disabled');
								
				});
				
				// Binds functionality to the convert function
				$('div.convert').click(function() {
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
				
}

/*This variable tracks the progress
		of the subset selection process */
var subset_progress = 0

function bind_select_subset_functionality() {

				$('.border').hover(
								function() {
												$(this).addClass('subset-hover');
								},
								function() {
												$(this).removeClass('subset-hover');
								}
				);
				
				$('.border').click(
								function() {
												if (subset_progress == 0) {
																clear_all()
																$(this).addClass('subset-active');
																$(this).children('.frame').addClass('start-frame');
																$('.message').html('Select End Frame');
																subset_progress = 1;
												}
												else if (subset_progress == 1) {
																$(this).addClass('subset-active');
																$(this).children('.frame').addClass('end-frame');
																
																var end_frame = $('.end-frame').data('frame');
																var start_frame = $('.start-frame').data('frame');
																
																if (start_frame < end_frame) {
																				for (i = start_frame; i < end_frame; i++) {
																								$("[data-frame="+i+"]").parent().addClass('subset-active');
																				}
																}
																
																else if (start_frame > end_frame) {
																				
																}

																
															$('.message').html('Click again to choose new start frame');
																subset_progress = 0
												}
								}
				);

				

}

function clear_all() {
				$('.border').removeClass('subset-active');
				$('.border').removeClass('start-frame');
				$('.border').removeClass('end-frame')
}

function unbind_all() {
				$('.border').unbind();
				$('div.coonvert').unbind();
				$('a.frame').unbind();
				
}
