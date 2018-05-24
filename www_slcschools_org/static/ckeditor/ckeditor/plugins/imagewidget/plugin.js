CKEDITOR.plugins.add( 'imagewidget', {
    requires: 'widget',

    icons: 'imagewidget',

    init: function( editor ) {
        editor.addContentsCss( this.path + 'css/global.css' );
        CKEDITOR.dialog.add( 'imagewidget', this.path + 'dialogs/imagewidget.js' );

        editor.widgets.add( 'imagewidget', {

            button: 'Insert Image',

            template:
                '<div class="inlineimage selfclear">' +
                    '<a class="relink" href="" data-id="" data-processed="">' +
                        '<span class="sr-only readertext">#</span>' +
                    '</a>' +
                    '<img class="inlineimage-img responsive-img" src="" alt="" data-id="" data-processed="">' + 
                '</div>',

            allowedContent:
                'div(!inlineimage,!selfclear,linked,fullcenter,fullstretch,left,right,padleft,padright,padtop,padbottom);' +
                'a(!relink, active)[!href,!data-id,!data-processed];' + 
                'span(sr-only,readertext);' +
                'img(!inlineimage-img,!responsive-img)[!src,!alt,data-id,data-processed]{width};',

            requiredContent: 'div(inlineimage)',

            dialog: 'imagewidget',

            upcast: function( element ) {
                return element.name == 'div' && element.hasClass( 'inlineimage' );
            },

            init: function() {
                var img = this.element.findOne('.inlineimage-img');
                var anchor = this.element.findOne('.relink');
                var readertext = this.element.findOne('.readertext');
                var width = img.getStyle( 'width' )
                if ( width )
                    this.setData( 'width', width.replace('px','') );
                if ( this.element.hasClass( 'fullcenter' ) )
                    this.setData( 'style', 'fullcenter' );
                if ( this.element.hasClass( 'fullstretch' ) )
                    this.setData( 'style', 'fullstretch' );
                if ( this.element.hasClass( 'left' ) )
                    this.setData( 'style', 'left' );
                if ( this.element.hasClass( 'right' ) )
                    this.setData( 'style', 'right' );
                this.setData( 'src', img.getAttribute('src') );
                this.setData( 'alttext', img.getAttribute('alt') );
                if ( this.element.hasClass( 'padleft' ) )
                    this.setData( 'padleft', 'checked' );
                else
                    this.setData( 'padleft', '' );
                if ( this.element.hasClass( 'padright' ) )
                    this.setData( 'padright', 'checked' );
                else
                    this.setData( 'padright', '' );
                if ( this.element.hasClass( 'padtop' ) )
                    this.setData( 'padtop', 'checked' );
                else
                    this.setData( 'padtop', '' );
                if ( this.element.hasClass( 'padbottom' ) )
                    this.setData( 'padbottom', 'checked' );
                else
                    this.setData( 'padbottom', '' );
                if ( anchor )
                    this.setData( 'href', anchor.getAttribute('href') );
                if ( readertext )
                    currentvalue = readertext.getText()
                    if (currentvalue == '#')
                        this.setData( 'readertext', '' );
                    else
                        this.setData( 'readertext', readertext.getText() );
            },

            data: function() {
                var img = this.element.findOne('.inlineimage-img');
                var anchor = this.element.findOne('.relink');
                var readertext = this.element.findOne('.readertext');
                this.element.removeClass( 'fullcenter' );
                this.element.removeClass( 'fullstretch' );
                this.element.removeClass( 'left' );
                this.element.removeClass( 'right' );
                this.element.removeClass( 'padleft' );
                this.element.removeClass( 'padright' );
                this.element.removeClass( 'padtop' );
                this.element.removeClass( 'padbottom' );
                this.element.removeClass( 'linked' );
                if ( this.data.style )
                    this.element.addClass( this.data.style );
                img.setAttribute( 'src', this.data.src );
                img.setAttribute( 'data-cke-saved-src', this.data.src );
                img.setAttribute( 'alt', this.data.alttext );
                if ( this.data.width == '' )
                    img.removeStyle( 'width' );
                else
                    img.setStyle( 'width', this.data.width + 'px' );
                if ( this.data.padleft )
                    this.element.addClass( 'padleft' );
                if ( this.data.padright )
                    this.element.addClass( 'padright' );
                if ( this.data.padtop )
                    this.element.addClass( 'padtop' );
                if ( this.data.padbottom )
                    this.element.addClass( 'padbottom' );
                if ( this.data.href )
                    this.element.addClass( 'linked' );
                if ( anchor )
                    anchor.setAttribute( 'href', this.data.href );
                    anchor.setAttribute( 'data-cke-saved-href', this.data.href );
                    if ( this.data.href == '' )
                        anchor.removeClass('active')
                    else
                        anchor.addClass('active')
                if ( readertext )
                    if ( this.data.readertext == '' )
                        readertext.setText( '#' );
                    else
                        readertext.setText( this.data.readertext );
            }
        } );
    }
} );
