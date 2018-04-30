CKEDITOR.plugins.add( 'relink', {
	// Require dialog
	requires: 'dialog,widget',

	// Register the icons. They must match command names.
	icons: 'relink',

	// The plugin initialization logic goes inside this method.
	init: function( editor ) {

		// CSS Rules
		editor.addContentsCss( this.path + 'css/global.css' );

		// Define dialog
		CKEDITOR.dialog.add( 'relink', this.path + 'dialogs/relink.js' );

		// Define Widget
		editor.widgets.add( 'relink', {

			button: 'Insert Text Link',

			template:
				'<a class="relink inlinelink" href="" data-id="" data-processed="">' +
				    '<span class="displaytext" aria-hidden="true"></span>' + 
				    '<span class="sr-only readertext"></span>' +
				'</a>',

			allowedContent:
				'a(!relink, inlinelink, active)[href,data-id,data-processed];' + 
				'span(displaytext,sr-only,readertext)[aria-hidden];',

			requiredContent: 'a(inlinelink)',

			dialog: 'relink',

			upcast: function( element ) {
                return element.name == 'a' && element.hasClass( 'inlinelink' );
            },

            init: function() {
            	var displaytext = this.element.findOne('.displaytext');
            	var readertext = this.element.findOne('.readertext');
            	this.setData( 'href', this.element.getAttribute('href') );
            	this.setData( 'displaytext', displaytext.getText() );
            	this.setData( 'readertext', readertext.getText() );
            },

            data: function(){
            	var displaytext = this.element.findOne('.displaytext');
            	var readertext = this.element.findOne('.readertext');
            	this.element.setAttribute( 'href', this.data.href );
            	this.element.setAttribute( 'data-cke-saved-href', this.data.href );
            	// this.element.setAttribute( 'data-id', this.data.href );
            	// this.element.setAttribute( 'data-processed', 'false' );
            	displaytext.setText( this.data.displaytext );
            	readertext.setText( this.data.readertext );
            	if ( this.data.href == '' )
            		this.element.removeClass('active')
            	else
            		this.element.addClass('active')
            },
		});
	}
});
