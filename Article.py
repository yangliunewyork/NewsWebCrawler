#!/usr/bin/python
import json

class Article:
    """
    Store website articles.
    """
    def __init__(self):
        self.m_title = None
        self.m_text = None
        self.m_author = None
        self.m_publish_date = None
        self.m_url = None
                        
    def to_json(self):
        """
        Serilization.
        """
        jsonObject = {}
        jsonObject['title'] = self.m_title
        jsonObject['text'] = self.m_text
        jsonObject['author'] = self.m_author
        jsonObject['publish_date'] = self.m_publish_date
        jsonObject['m_url'] = self.m_url
        return json.dumps(jsonObject,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)
