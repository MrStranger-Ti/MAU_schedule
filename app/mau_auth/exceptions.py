class TagNotFound(BaseException):
    def __str__(self):
        return 'Method BeautifulSoup.find did not find any tag'
