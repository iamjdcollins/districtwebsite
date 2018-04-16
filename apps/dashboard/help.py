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
