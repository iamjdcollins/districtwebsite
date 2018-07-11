class SiteType():
    title = (
        '<span>Enter a name for this site type. The name should be a'
        ' short descriptive name for the purpose of the site (e.g. ',
        ' School Website, District Website, or Teacher Website).</span>'
    )


class SiteTypeRequiredPage():
    title = (
        '<span>Enter a name for this required page. The name should be a'
        ' short descriptive name for the purpose of the page. (e.g. ',
        ' Home, About Our School, or School Community Council (SCC)).</span>'
    )


class PageLayout():
    title = (
        '<span>Enter a name for this page layout. The name should be a'
        ' short descriptive name for the purpose of the page (e.g. Home Page,'
        ' Contact Us Page, or School Communinity Council Page).</span>'
    )
    namespace = (
        '<span>Enter the name of the html file that is used to render this'
        ' page layout (i.e.the home page layout may have a file called'
        ' home.html).</span>'
    )


class Templates():
    title = ()
    namespace = ()


class GeneralSettings():
    title = (
        '<span>Enter the title of the site.<br>It is recommended this '
        'be the official name of the entity this site represents.</span>'
    )
    primary_domain = (
        '<span>Enter the primary domain name for this site. All sites '
        'must have one primary domain that is used to access information. '
        'It is possible to have other domains used to redirect to this domain '
        'or also a development and test enviroment that does not redirect.'
        '</span>'
    )
    namespace = (
        '<span>Enter a lower case a-z identifier for this site. Will be used '
        'to allow custom css/js files provided by the webmaster.</span>'
    )
    gatrackingid = (
        '<span>Enter the Google Analytics Tracking ID for this property '
        'which can be found in the admin interface of Google Analytics.</span>'
    )
    monsido_domaintoken = (
        '<span>Enter the Monsido Domain Token for this site '
        'which can be found in the admin interface of Monsido.</span>'
    )
    main_phone = (
        '<span>Enter the main phone number for the entity this site '
        'represents. The number should be in the 11 number format. '
        ' (i.e.: 18015788599)</span>'
    )
    main_fax = (
        '<span>Enter the main fax number for the entity this site '
        'represents. The number should be in the 11 number format. '
        ' (i.e.: 18015788599)</span>'
    )
    global_facebook = (
        '<span>Enter the URL for the Facebook page for this site '
        ' (i.e.: https://www.facebook.com/slcschools)</span>'
    )
    global_twitter = (
        '<span>Enter the URL for the Twitter page for this site '
        ' (i.e.: https://twitter.com/slcschools)</span>'
    )
    global_instagram = (
        '<span>Enter the URL for the Instagram page for this site '
        ' (i.e.: https://www.instagram.com/slcschools/)</span>'
    )
    global_youtube = (
        '<span>Enter the URL for the YouTube page for this site '
        ' (i.e.: https://www.youtube.com/user/slcschools)</span>'
    )
    location = (
        '<span>Select the primary location for the entity this site '
        'represents. This list is managed by the webmaster.</span>'
    )
    template = (
        '<span>Select the template used on this site. '
        'A value must be selected.</span>'
    )
    nd_statement = (
        '<span>Non-Discrimination Statement is set globally for all sites and may'
        ' not be editable on this page. Contact Jordan Collins if a correction'
        ' may be needed.</span>'
    )
    ada_statement = (
        '<span>Americans with Disabilities Act (ADA) Statement is set globally for all sites and may'
        ' not be editable on this page. Contact Jordan Collins if a correction'
        ' may be needed.</span>'
    )
