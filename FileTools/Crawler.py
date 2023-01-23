import os


class Crawler(object):
    def __init__(self, path: str):
        self.paths = self.crawl(path)

    @classmethod
    def crawl(cls, path: str):
        file_list = []
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                file_list += cls.crawl(os.path.join(root, dir))
            for file in files:
                if os.path.join(root, file) == root:
                    return
                if os.path.isfile(os.path.join(root, file)):
                    file_list.append(os.path.join(root, file))
        return file_list
