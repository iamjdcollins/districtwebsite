CKEDITOR.dialog.add( 'imagewidget', function( editor ) {
    return {
        title: 'Image Properties',
        minWidth: 200,
        minHeight: 100,
        contents: [
            {
                id: 'info',
                label: 'Image',
                elements: [
                    {
                        id: 'src',
                        type: 'text',
                        label: 'Image URL (Required)',
                        validate: CKEDITOR.dialog.validate.notEmpty( 'Image URL is required' ),
                        setup: function( widget ) {
                            this.setValue( widget.data.src );
                        },
                        commit: function( widget ) {
                            widget.setData( 'src', this.getValue() );
                        }

                    },
                    {
                        id: 'alttext',
                        type: 'text',
                        label: 'Alternative Text (Required)',
                        validate: CKEDITOR.dialog.validate.notEmpty( 'Alternative Text is required' ),
                        setup: function( widget ) {
                            this.setValue( widget.data.alttext );
                        },
                        commit: function( widget ) {
                            widget.setData( 'alttext', this.getValue() );
                        }
                    },
                    {
                        id: 'style',
                        type: 'select',
                        label: 'Image Style (Required)',
                        items: [
                            [ '---', '' ],
                            [ 'Full Width Centered Image', 'fullcenter' ],
                            [ 'Full Width Stretched Image', 'fullstretch' ],
                            [ 'Image Left Text Wrap', 'left' ],
                            [ 'Image Right Text Wrap', 'right' ]
                        ],
                        validate: CKEDITOR.dialog.validate.notEmpty( 'Image Style is required' ),
                        setup: function( widget ) {
                            this.setValue( widget.data.style );
                        },
                        commit: function( widget ) {
                            widget.setData( 'style', this.getValue() );
                        }
                    },
                    {
                        id: 'width',
                        type: 'text',
                        label: 'Width (Ignored on Full Width Stretched Image)',
                        validate: CKEDITOR.dialog.validate.number( 'Width must be a number.' ),
                        setup: function( widget ) {
                            this.setValue( widget.data.width );
                        },
                        commit: function( widget ) {
                            widget.setData( 'width', this.getValue() );
                        }
                    },
                    {
                        id: 'padleft',
                        type: 'checkbox',
                        label: 'Padding Left (Adds padding to the left side of the image)',
                        default: '',
                        setup: function( widget ) {
                            this.setValue( widget.data.padleft );
                        },
                        commit: function( widget ) {
                            widget.setData( 'padleft', this.getValue() );
                        }
                    },
                    {
                        id: 'padright',
                        type: 'checkbox',
                        label: 'Padding Right (Adds padding to the right side of the image)',
                        default: '',
                        setup: function( widget ) {
                            this.setValue( widget.data.padright );
                        },
                        commit: function( widget ) {
                            widget.setData( 'padright', this.getValue() );
                        }
                    },
                    {
                        id: 'padtop',
                        type: 'checkbox',
                        label: 'Padding Top (Adds padding to the top side of the image)',
                        default: '',
                        setup: function( widget ) {
                            this.setValue( widget.data.padtop );
                        },
                        commit: function( widget ) {
                            widget.setData( 'padtop', this.getValue() );
                        }
                    },
                    {
                        id: 'padbottom',
                        type: 'checkbox',
                        label: 'Padding Bottom (Adds padding to the bottom side of the image)',
                        default: '',
                        setup: function( widget ) {
                            this.setValue( widget.data.padbottom );
                        },
                        commit: function( widget ) {
                            widget.setData( 'padbottom', this.getValue() );
                        }
                    },
                ]
            },
            {
                id: 'link',
                label: 'Link',
                elements: [
                    {
                        type: 'html',
                        html: '<p>Use the Link input to enter a URL. If the URL entered matches content found on a<br> district website it will make the link dynamic and dynamically determine the URL even if the<br> content moves in the future. If the link points to an external location the content will link to the<br> URL given and will not be dynamic.</p>'
                    },
                    {
                        type: 'text',
                        label: 'Link (Must enter full URL)',
                        id: 'href',
                        setup: function( widget ) {
                            this.setValue( widget.data.href );
                        },
                        commit: function( widget ) {
                            widget.setData( 'href', this.getValue() );
                        }
                    },
                    {
                        type: 'text',
                        label: 'Accessible Link Text (Should describe what the link will open or do if clicked. For example<br> if the display text is "click here" this field should better describe what happens when click<br> such as "click here to visit xyz page.").',
                        id: 'readertext',
                        // validate: CKEDITOR.dialog.validate.notEmpty( 'Accessible Link Text is required' ),
                        validate: function(){
                            var dialog = this._.dialog;
                            var href = dialog.getValueOf( 'link', 'href' )
                            var readertext = dialog.getValueOf( 'link', 'readertext' )
                            if (href != '' && readertext == '') {
                                alert( 'Accessible Link Text is required when providing a link.' );
                                return false;
                            }
                            return true;
                        },
                        setup: function( widget ) {
                            this.setValue( widget.data.readertext );
                        },
                        commit: function( widget ) {
                            widget.setData( 'readertext', this.getValue() );
                        }
                    },
                ],
            },
        ]
    };
} );