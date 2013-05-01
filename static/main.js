$(document).ready(function() {

				// select target is the default functionality
				bind_select_target_functionality();

				/* Clears subset progress
							and unsets the active target
							and any highlighted subset of frames
					*/
				$('.clear').click(
								function() {
												clear_all();
												$('.border').removeClass('target-active');
												$('.convert').addClass('disabled');

								});


				/* Rebinds functionality on clicking 
							frames so that user can select a 
							target instead of a subset of frames
					*/
				$('.choose-target').click(function() {
								$('.message').html('Select a Target Frame This will be your first frame');
								$('li').removeClass('active');
								$(this).addClass('active');
								unbind_all();
								bind_select_target_functionality();
				});

				/* On Page load when the user clicks the 
							Choose a subset tab, it sets the tab
							to active and rebinds all functionality 
							related to clicking on frames so that
							the user can select a subset instead of
							a target		
				*/
				$('.choose-subset').click(function() {
								$('li').removeClass('active');
								$(this).addClass('active');
								unbind_all();
								bind_select_subset_functionality();

								if (subset_progress == 1) {
												$('.message').html('Select End Frame');

								}
								else {
												$('.message').html('Select Start Frame')
								}
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
								
								var end_frame = $('.end-frame').data('frame');
								var start_frame = $('.start-frame').data('frame');
								var frame_count = $('.frame-roll').data('frame_count');


								if (subset_progress == 2) {
												if (!is_between(start_frame, end_frame, $(this).data('frame'))) {
																$('.message').html('target must be within subset');
																$('div.convert').addClass('disabled');
												}
												else {
																$(this).addClass("target");
																$(this).parent().addClass('target-active');
																$('div.convert').removeClass('disabled');
												}
												
								}
								else {
												$(this).addClass("target");
												$(this).parent().addClass('target-active');
												$('div.convert').removeClass('disabled');
								}
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

/*This variable tracks the progress	of the subset 
		selection process 		0 is no selection 1 means 
		you've selected the start frame		and 2 means 
		you've selected the end frame              */
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
												if (subset_progress == 0 || subset_progress == 2) {
																clear_all()
																$(this).addClass('subset-active');
																$(this).children('.frame').addClass('start-frame');
																$('.message').html('Select End Frame');
																subset_progress = 1;
												}
												else if (subset_progress == 1) {

																var start_frame = $('.start-frame').data('frame');
																var end_frame = $(this).children('.frame').data('frame');
																var target = $('.target').data('frame');
																
																console.log(is_between(start_frame, end_frame, target));
																
																// If user clicks the same frame. It clears all subset data
																if (start_frame == end_frame) {
																				$('.message').html('Cleared Subset');
																				$('.frame').removeClass('start_frame');
																				$('.border').removeClass('subset-active');
																				subset_progress = 0;
																}

																

																else if ( is_between(start_frame, end_frame, target) || 
																										!$('.target-active')[0])  {
																				
																				$(this).addClass('subset-active');
																				$(this).children('.frame').addClass('end-frame');
																				var frame_count = $('.frame-roll').data('frame_count');
																				selected_frames_visualization(start_frame, end_frame, frame_count);
																				subset_progress = 2
																				$('.message').html('Click again to choose new start frame');
																}
																				
																
												}


								}
				);
}

function selected_frames_visualization(start_frame, end_frame, frame_count) {

				/* Fills all frames between the start and end frame
							with a black background denoting all frames
							included in the subset         */
				if (start_frame != end_frame) {

								for (var frame = 0; frame <= frame_count; frame++) {

												if ( is_between(start_frame, end_frame, frame )) {
																$("[data-frame="+frame+"]").parent().addClass('subset-active');
																$("[data-frame="+frame+"]").children('img').css('opacity',1);
												}
												else {
																$("[data-frame="+frame+"]").children('img').css('opacity',0.3);
												}
								}
				}
}

function clear_all() {
				$('.border').removeClass('subset-active');
				$('.frame').removeClass('start-frame');
				$('.frame').removeClass('end-frame')
				$('img').css('opacity',1);
				subset_progress = 0;
}

function unbind_all() {
				$('.border').unbind();
				$('div.coonvert').unbind();
				$('a.frame').unbind();
}


function is_between(start_frame, end_frame, target) {
				
				if (start_frame < end_frame) {
								if (start_frame <= target && target <= end_frame) {

												return true
								}
								else {
												return false
								}
				}
				else if (start_frame > end_frame) {
								if (target >= start_frame) {
												return true;
								} 
								else if ( target <= end_frame) {
												return true;
								}
								else {
												return false;
								}
				}
				else {
								return false;
				}
}
