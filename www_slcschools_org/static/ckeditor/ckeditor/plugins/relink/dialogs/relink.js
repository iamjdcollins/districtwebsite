CKEDITOR.dialog.add( 'relink', function( editor ) {
    return {
        title: 'Link Properties',
        minWidth: 200,
        minHeight: 100,
        contents: [
            {
                id: 'info',
                elements: [
                    {
                        type: 'html',
                        html: '<p>Use the Link input to enter a URL. If the URL entered matches content found on a<br> district website it will make the link dynamic and dynamically determine the URL even if the<br> content moves in the future. If the link points to an external location the content will link to the<br> URL given and will not be dynamic.</p>'
                    },
                    {
                        type: 'text',
                        label: 'Link (Required: Must enter full URL)',
                        id: 'href',
                        validate: CKEDITOR.dialog.validate.notEmpty( 'Link is required' ),
                        setup: function( widget ) {
                            this.setValue( widget.data.href );
                        },
                        commit: function( widget ) {
                            widget.setData( 'href', this.getValue() );
                        }
                    },
                    {
                        type: 'text',
                        label: 'Display Text (Required)',
                        id: 'displaytext',
                        validate: CKEDITOR.dialog.validate.notEmpty( 'Display Text is required' ),
                        setup: function( widget ) {
                            this.setValue( widget.data.displaytext );
                        },
                        commit: function( widget ) {
                            widget.setData( 'displaytext', this.getValue() );
                        }
                    },
                    {
                        type: 'text',
                        label: 'Accessible Link Text (Required :Should describe what the link will open or do if clicked. For example<br> if the display text is "click here" this field should better describe what happens when click<br> such as "click here to visit xyz page.").',
                        id: 'readertext',
                        validate: CKEDITOR.dialog.validate.notEmpty( 'Accessible Link Text is required' ),
                        setup: function( widget ) {
                            this.setValue( widget.data.readertext );
                        },
                        commit: function( widget ) {
                            widget.setData( 'readertext', this.getValue() );
                        }
                    },
                ]
            }
        ]
    };
} );