/**
 * Script file to execute all dynamic page actions
 *
 * @author D. Tiems (dennis-at-bigbase-dot-nl)
 * @version 1.0.0 - September 22nd 2012
 */

$( document ).ready( function(){

	// Show a message
	// console.log( 'All script will be executed now' );

	// Run the slideshows on the page
	if( $( '.nivoslider' ).length ) $( '.nivoslider' ).nivoSlider();

	// Hover images with their lowsrc attr
	$( 'img[data-hover]' ).on( 'hover' , function(){
		var tmp = $(this).attr( 'src' );
		$(this).attr( 'src' , $(this).attr( 'data-hover' ) );
		$(this).attr( 'data-hover' , tmp );
	})

	// Apply the lightbox feature on images
	if( $( '.colorbox' ).length ) $( '.colorbox' ).colorbox();

});