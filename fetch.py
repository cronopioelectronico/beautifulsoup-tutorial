from b4 import BeautifulSoup


def get_site_name(link, url):
    """Attempt to get the site's base name."""
    sitename = None
    if link.find("meta", property="og:site_name") is not None:
        sitename = link.find("meta", property="og:site_name").get('content')
    else:
        sitename = url.split('//')[1]
        name = sitename.split('/')[0]
        name = sitename.rsplit('.')[1]
        return name.capitalize()
    return sitename


def get_domain(url):
    """Get site root domain name."""
    domain = url.split('//')[1]
    name = domain.split('/')[0]
    return name


def get_title(link):
    """Attempt to get a title."""
    title = None
    if link.title.string is not None:
        title = link.title.string
    elif link.find("h1") is not None:
        title = link.find("h1").string
    elif link.find_all("h1") is not None:
        title = link.find_all("h1")[0].string
    if title:
        title = title.split('|')[0]
    return title


def get_description(link):
    """Attempt to get description."""
    description = None
    if link.find("meta", property="og:description") is not None:
        description = link.find("meta", property="og:description").get('content')
    elif link.find("p") is not None:
        description = link.find("p").contents
    elif link.find_all("p") is not None:
        description = link.find_all("p")[0].contents
    return description


def get_image(link):
    """Attempt to get image."""
    image = None
    if link.find("meta", property="og:image") is not None:
        image = link.find("meta", property="og:image").get('content')
    elif link.find_all("img", src=True) is not None:
        image = link.find_all("img")
        if image:
            image = link.find_all("img")[0].get('src')
    if str(image)[0] == '/':
        image = str(get_domain(link)) + image
    return image


def site_exceptions(link, url):
    """Check to see if site is in list of exceptions."""
    domain = get_site_name(link, url)
    exception_domains = ['Youtube', 'Medium' 'Github']
    if domain in exception_domains:
        print('WARNING:', domain)


def get_meta(url):
    """Generate preview obj per link."""
    embedded_url = BeautifulSoup(url, 'html.parser')
    preview_dict = {
        'title': get_title(embedded_url),
        'description': get_description(embedded_url),
        'image': get_image(embedded_url),
        'sitename': get_site_name(embedded_url, url),
        'url': url
        }
    return preview_dict