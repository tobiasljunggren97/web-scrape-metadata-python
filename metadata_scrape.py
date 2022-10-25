from bs4 import BeautifulSoup
import requests

def get_metadata(url):
    #Default requests headers doesn't work on some sites, TODO find the headers that work best
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    title = None
    author = None
    description = None
    date_published = None
    date_modified = None
    language = None
    content_type = None
    meta_url = None

    #Metadata properties to check
    properties = ["property","name","itemprop","content"]

    #Names of tags to check as backups if it doesn't find by regex, add more to increase range (but may lower accuracy if not generally relevant)
    titles = ["og:title", "title", "vr:title", "article:title", "twitter:title", "dc:title", "sailthru.title", "sailthru.fulltitle", "name", "TITLE", "headline", "og:headline", "fullTitle"]
    authors = ["og:author", "author", "vr:author", "article:author", "byline", "by-line", "by-author", "dc:creator", "dc:creator", "creator", "AUTHOR", "writer", "byLine"]
    descriptions = ["og:description", "description", "vr:description", "article:description", "twitter:description", "dc:description", "sailthru.description", "sailthru.fulldescription", "description", "DESCRIPTION", "dscrptn", "descr"]
    publish_dates = ["article:published_time", "date", "og:date", "og:pubdate", "vr:published_time", "vr:published-time", "published", "pubdate", "datePublished", "dc:date", "dc:date.created", "dc:date.issued", "DATE", "pubd", "publishdate"]
    modified_dates = ["article:modified_time", "modified", "og:updated_time", "og:moddate", "og:modified_time", "updated", "updated_time", "dc:modified", "dc:date.modified", "dateModified", "date_modified", "lastmod", "LASTMOD"]
    meta_languages = ["inLanguage", "language", "lang", "langauge", "LANGUAGE", "language-code", "language-code", "lng", "og:locale"]
    content_types = ["og:type", "vr:type","type", "article:type", "TYPE"]
    urls = ["og:url", "url", "URL"]

    #Find all metatags
    for tag in soup.find_all("meta"):
        #Check property, name, itemprop, content in that order.
        for metaproperty in properties:
            current_tag = tag.get(metaproperty, None)
            if current_tag != None:
                str = tag.get("content", None)

                #Booleans to check if a tag has [not] been found 
                title_not_found = title is None or title == ""
                author_not_found = author is None or author == ""
                description_not_found = description is None or description == ""
                date_published_not_found = date_published is None or date_published == ""
                date_modified_not_found = date_modified is None or date_modified == ""
                language_not_found = language is None or language == ""
                content_type_not_found = content_type is None or content_type == ""
                meta_url_not_found = meta_url is None or meta_url == ""

                #Main part of the code, checks if the tag is a title, author, description, date published, date modified, language, content type, or url
                #Match either by regex or by the list of exact tags
                if title_not_found and ('title' in current_tag or current_tag in titles):
                    title = str

                if author_not_found and ('author' in current_tag or current_tag in authors):
                    author = str

                if description_not_found and ('description' in current_tag or current_tag in descriptions):
                    description = str.replace("\n", " ")

                if date_published_not_found and ('published' in current_tag or current_tag in publish_dates):
                    date_published = str

                if date_modified_not_found and ('modified' in current_tag or current_tag in modified_dates):
                    date_modified = str

                if language_not_found and ('language' in current_tag or current_tag in meta_languages):
                    language = str

                if content_type_not_found and ('type' in current_tag or current_tag in content_types):
                    content_type = str

                if meta_url_not_found and current_tag in urls:
                    meta_url = str

    #If no url is found in the metadata, use the url of the input
    if meta_url == None:
        meta_url = url

    return {
        "title": title,
        "author": author,
        "description": description,
        "date_published": date_published,
        "date_modified": date_modified,
        "language": language,
        "content_type": content_type,
        "url": meta_url
    }
