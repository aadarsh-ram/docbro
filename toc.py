import os
from urllib import request

class TreeGenerate():
    """
    Class to generate a TOC for a given directory.
    """
    def __init__(self, root):
        self.root = root

    def sort_files(a, b):
        """Sorts files by their name. Directories come first."""
        if a == b:
            return 0
        if a == None or b == None:
            return -1 if a == None else 1
        left, right = os.path.isdir(a), os.path.isdir(b)
        if left == right:
            return -1 if a < b else 1
        return -1 if left else 1

    def directory_line(self, file_name, level):
        """Creates a line of text for a directory entry."""
        return ('\t' * level) + '- ' + ('### 📁 %s' % (file_name))

    def file_line(self, file_name, full_path, level):
        """Creates a line of text for a file entry."""
        file_root = os.path.splitext(file_name)[0]
        file_link = (full_path.replace(self.root, ''))
        if file_link.startswith('/'):
            file_link = file_link[1:]
        if file_link.endswith('/'):
            file_link = file_link[:-1]
        return ('\t' * level) + '- [%s](%s)' % (file_root, request.pathname2url(file_link))

    def generate_toc(self, path = '.', level = 0):
        """Walks a given directory to create a TOC out of it."""
        dirlist = sorted([x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))])
        filelist = sorted([x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))])

        result = []
        # Make sure files are listed before directories (personal preference)
        for file_name in filelist + dirlist:
            full_path = os.path.join(path, file_name)
            if os.path.isdir(full_path):
                result.append(self.directory_line(file_name, level))
                result.extend(self.generate_toc(full_path, level + 1))
            elif file_name.endswith('.html'):
                result.append(self.file_line(file_name, full_path, level))
        return result