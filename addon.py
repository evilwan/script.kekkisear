# Main entryoint for addon
#
# Simple Epub reader Kodi addon.
#
# The primary goal is to read DRM free Epub files in Kodi, so the main focus
# is on showing the text content, not so much on possible formatting of said text.
#
# Kodi does not offer rich formatting options that are commonly found in web browsers,
# so no effort was made at all to keep any of the formatting information in the Epub.
#


import resources.lib.kodiutils as kodi
import resources.lib.epub as epub
from resources.lib.readerpane import ReaderPane

#
# Find out who we are ;-)
#
addon_name = kodi.name()
kodi.log("~~~~~ {}: started up".format(addon_name))
#
# Get info on last book opened and which chapter was shown.
# If no book was previously opened, prompt for one to continue.
#
epubfil = kodi.setting("bookfile")
if epubfil in [None, ""]:
    epubfil = kodi.gui_browse_files(kodi.string(32001), mask=".epub")
    kodi.log("~~~~~ {}: selected epub file: {}".format(addon_name, epubfil))
    kodi.set_setting("bookfile", epubfil)
#
# Slurp and parse the selected/saved file
#
book = epub.Epub(epubfil)
book.parsetoc()
#
# Reposition on chapter being read in previous session (if available, if not, start with first chapter)
#
chapter_nr = kodi.setting("chapter_nr")
if chapter_nr in [None, ""]:
    chapter_nr = 0
    kodi.set_setting("chapter_nr", chapter_nr)
else:
    chapter_nr = int(chapter_nr)
#
# Create book reader pane from XML specification
#
body = ReaderPane.createReaderPane(
    title=book.gettitle(chapter_nr), body=book.getchaptertext(chapter_nr)
)
body.show()
#
# This might take a while ...
#
monitor = kodi.monitor()
while (not body.isClosed()) and (not monitor.abortRequested()):
    #
    # This parameter defines how responsive the addon will react to user input
    #
    kodi.sleep(100)
    if body.want_quit():
        kodi.log("~~~~~ {}: bailing out...".format(addon_name))
        break
    elif body.want_previous_chapter():
        if chapter_nr > 0:
            chapter_nr = chapter_nr - 1
            body.set_title(book.gettitle(chapter_nr))
            body.set_body(book.getchaptertext(chapter_nr))
            kodi.set_setting("chapter_nr", chapter_nr)
        body.clearFlags()
    elif body.want_next_chapter():
        if chapter_nr < len(book.chapters) - 1:
            chapter_nr = chapter_nr + 1
            body.set_title(book.gettitle(chapter_nr))
            body.set_body(book.getchaptertext(chapter_nr))
            kodi.set_setting("chapter_nr", chapter_nr)
        body.clearFlags()
    elif body.want_toc():
        chaps = []
        for c in book.chapters:
            chaps.append(c.get_title())
        idx = kodi.gui_select(kodi.string(32004), chaps)
        chapter_nr = idx
        body.set_title(book.gettitle(chapter_nr))
        body.set_body(book.getchaptertext(chapter_nr))
        body.clearFlags()
        kodi.set_setting("chapter_nr", chapter_nr)
        body.show()
    elif body.want_library():
        epubfil = kodi.gui_browse_files(kodi.string(32001), mask=".epub")
        kodi.set_setting("bookfile", epubfil)
        book = epub.Epub(epubfil)
        book.parsetoc()
        chapter_nr = 0
        kodi.set_setting("chapter_nr", chapter_nr)
        body.set_title(book.gettitle(chapter_nr))
        body.set_body(book.getchaptertext(chapter_nr))
        body.clearFlags()
        body.show()

kodi.log("~~~~~ {}: done: bailing out.".format(addon_name))
del monitor
