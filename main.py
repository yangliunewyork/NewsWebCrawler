#!/usr/bin/python
import os
import errno
import newspaper
import logging
import logging.config

from Article import Article


logger = logging.getLogger(__name__)

# load config from file
# logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
# or, for dictConfig
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                    },
            },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.StreamHandler',
                    },
            },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
                    }
            }
})


def download_articles_from_website(website_url):
    """
    This particular strategy looks for companies whose total number of outstanding 
    shares are in excess of the market average (632 million shares).
    """
    website_source = newspaper.build(website_url, memoize_articles=False)
    logging.info("There are %s articles at %s.",
                website_source.size(),
                website_url)
    article_list = []
    for article in website_source.articles:
        article.download()
        article.parse()
        articleObject = Article()
        articleObject.m_title = article.title
        articleObject.m_text = article.text
        articleObject.m_author = article.authors
        articleObject.m_publish_date = "null" if article.publish_date is None else article.publish_date.strftime('%Y-%m-%d')
        articleObject.m_url = article.url
        article_list.append(articleObject)
        if len(article_list) > 10 :
            break
    return article_list

def create_required_directory_if_not_exists(source, date):
    """
    We store articles to directory ./source/date
    This function will create the required directory if not exists.
    It's return value is the path of the directory.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    required_dir = current_dir + "/" + source + "/" + date
    if not os.path.exists(required_dir):
        try:
            os.makedirs(required_dir, exist_ok=True)
        except OSError as error: # Guard against race condition
            logging.error(error);
            if error.errno != errno.EEXIST:
                raise
    logging.info('The required directory %s is ready.', required_dir)
    return required_dir
        
def save_articles_to_file(source, article_list):
    """
    Save the download articles to a file as JSON format.
    """
    for article in article_list:
        required_dir = create_required_directory_if_not_exists(source, article.m_publish_date)
        filename =  required_dir + "/" + article.m_title +".txt"
        
        if os.path.exists(filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not

        file_writer = open(filename, append_write)
        file_writer.write(article.to_json())
        file_writer.close()
    logging.info('%s articles has been written to %s.', len(article_list), filename) 

if __name__ == "__main__":
    article_list = download_articles_from_website("http://cnn.com")
    save_articles_to_file("cnn", article_list)
    
