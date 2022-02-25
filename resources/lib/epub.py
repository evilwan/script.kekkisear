#
# All stuff EPUB book related
#
# Note that an EPUB file is basically a ZIP file.
#


import zipfile
import sys
import os

#
# Note: lxml requires native components and is therefore not available on all
# Kodi supported platforms. Therefore, use beatifulsoup as a hack for parsing
# the various epub XML files.
#
# import lxml.etree as ET
from bs4 import BeautifulSoup
import resources.lib.kodiutils as kodi


class EpubChapter:
    """
    Encapsulation of one single chapter in an Epub book.

    The raw XHTML from the Epub file is used in the constructor, but for now only
    the chapter title and text body are available as chapter properties.
    """

    def __init__(self, raw):
        """
        Constructor: raw is the raw data fetched from the Epub zip entry.
        """
        self.raw = raw
        self.soup = BeautifulSoup(raw, "html.parser")

    def get_body(self):
        """
        Extract body text from XHTML body.

        Note that this effectively removes all formatting from the text, but given that
        Kodi has only primitive formatting support, we don't care and focus on the pure
        text. This is a book reader after all.
        """
        return self.soup.get_text()

    def get_title(self):
        """
        Return the chapter title.
        """
        head = self.soup.find("title")
        if head:
            return head.text
        else:
            return "No title"


class Epub:
    """
    Encapsulation of am Epub book file.
    """

    def __init__(self, filnam):
        """
        Constructor: filnam is the name of the EPUB book file.
        """
        self.filnam = filnam
        self.book = zipfile.ZipFile(filnam)
        self.title = ""
        self.author = ""
        self.prefix = ""
        self.items = {}
        self.chapters = []

    def getentry(self, nam):
        """
        Get content of named entry in Epub book.
        """
        buf = ""
        with self.book.open(nam) as f:
            buf = f.read()
        return buf

    def gettocfilnam(self):
        """
        Get name of the TOC entry
        """
        manifest = self.getentry("META-INF/container.xml")
        root = BeautifulSoup(manifest, "html.parser")
        toc = ""
        #
        # Note: manifest file uses namespaces so use manual method to search
        # for all elements in the XML document and check eaach and every local
        # (that is: without namespaces) tag name
        #
        ll = root.find_all("rootfile")
        for c in root.find_all("rootfile"):
            if c.name == "rootfile":
                toc = c["full-path"]
        return toc

    def gettoc(self):
        """
        Get TOC for book
        """
        tocfil = self.gettocfilnam()
        d = os.path.dirname(tocfil)
        if d != "":
            self.prefix = d + "/"
        buf = ""
        with self.book.open(tocfil) as f:
            buf = f.read()
        return buf

    def parsetoc(self):
        """
        Parse TOC into python objects

        Note that the logic in this module is rather primitive in the sense that
        much of the Epub standard is simply ignored. Use the <spine> element as the list
        of chapters to present and in that order.
        """
        toc = self.gettoc().decode()
        root = BeautifulSoup(toc, "html.parser")
        c = root.find("metadata")
        if c:
            for k in c.findChildren():
                if k.name.endswith("title"):
                    self.title = k.text
                elif k.name.endswith("creator"):
                    self.author = k.text
        c = root.find("manifest")
        if c:
            for itm in c.findChildren():
                self.items[itm["id"]] = itm["href"]
        c = root.find("spine")
        if c:
            for itm in c.findChildren():
                self.chapters.append(
                    EpubChapter(self.getentry(self.prefix + self.items[itm["idref"]]))
                )

    def getchaptertext(self, idx):
        """
        Get plain text for specified chapter
        """
        return self.chapters[idx].get_body()

    def gettitle(self, idx):
        """
        Get plain text for specified chapter
        """
        return self.chapters[idx].get_title()
