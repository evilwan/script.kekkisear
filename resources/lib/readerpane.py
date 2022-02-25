#
# Stuff related to actual reader pane
#
# Looks like we need a subclass of xbmcgui.WindowXMLDialog to be able to have
# a scrollbar and to have access to various components (such as the textfield holding
# the actual book text)
#

import xbmcgui
import resources.lib.kodiutils as kodi

# Some useful defintions for interaction with Kodi for
# handling the XML window
#
# XNL file defining the panel layout
WINDOW_XML = "reading_pane.xml"
#
# Various control ID values: these are found in the "id=..." attributes
# of the controls in the XML
#
# Control-ID for title
ID_TITLE = 201
# Control-ID for chapter body text
ID_BODY = 200
# Control-ID for scrollbar
ID_SCROLLBAR = 300
# Control-ID for previous chapter button
ID_PRV_CHP = 301
# Control-ID for next chapter button
ID_NXT_CHP = 302
# Control-ID for options button
ID_TOC = 303
# Control-ID for quit button
ID_QUIT = 304
# Control-ID for "-" button
ID_MIN = 305
# Control-ID for "+" button
ID_PLUS = 306
# Control-ID for library button
ID_LIBRARY = 307


class ReaderPane(xbmcgui.WindowXMLDialog):
    """
    Pane for viewing chapter text (body)
    """

    def __init__(self, *args, **kwargs):
        """
        Add some specialized code here and then call the parent class constructor
        """
        self.title = kwargs.get("title", "")
        self.body = kwargs.get("body", "")
        self.delay = 3000  # params taken from XML
        self.ttime = 1000  # this one can be changed with -/+ buttons
        self.repeat = 10000  # should be sufficiently large
        self.prv_chapter = False
        self.nxt_chapter = False
        self.toc = False
        self.croak = False
        self.closed = False
        self.library = False
        super().__init__()

    @staticmethod
    def createReaderPane(title, body):
        """
        Helper class method for creating a new reader pane with everything on it.
        """
        return ReaderPane(
            WINDOW_XML,
            kodi.whereami(),
            title=title,
            body=body,
        )

    # until now we have a blank window, the onInit function will parse the xml file
    def onInit(self):
        """
        Called when form is actually shown: set appropriate field values
        """
        self.update_fields()
        super().onInit()
        # self.getControl(ID_BODY).setEnabled(True)

    def onAction(self, action):
        """
        Handle all activity on screen (except for button clicks)

        Scrollbar interaction does not result in a call to this method, though.
        """
        if (action == xbmcgui.ACTION_PREVIOUS_MENU) or (
            action == xbmcgui.ACTION_NAV_BACK
        ):
            self.close()
            self.closed = True

    def onClick(self, id):
        """
        Where the action is: something got clicked
        """
        if id == ID_QUIT:
            self.croak = True
            self.close()
            self.closed = True
        elif id == ID_TOC:
            self.toc = True
            self.close()
            self.closed = True
        elif id == ID_LIBRARY:
            self.library = True
            self.close()
            self.closed = True
        elif id == ID_PRV_CHP:
            self.prv_chapter = True
        elif id == ID_NXT_CHP:
            self.nxt_chapter = True
        elif id == ID_MIN:
            self.ttime = int(self.ttime / 2)
            txtfld = self.getControl(ID_BODY)
            txtfld.autoScroll(self.delay, self.ttime, self.repeat)
        elif id == ID_PLUS:
            if self.ttime == 0:
                self.ttime = 1
            else:
                self.ttime = int(self.ttime * 2)
            txtfld = self.getControl(ID_BODY)
            txtfld.autoScroll(self.delay, self.ttime, self.repeat)

    def update_fields(self):
        """
        Set correct values for screen fields
        """
        self.set_title(self.title)
        self.set_body(self.body)

    def set_title(self, title):
        """
        Set title text as a bolded label
        """
        self.title = title
        lbl = self.getControl(ID_TITLE)
        lbl.setLabel("[B]{}[/B]".format(title))  # set label text in bold

    def set_body(self, body):
        """
        Set the actual text in the main reading component
        """
        self.body = body
        txt = self.getControl(ID_BODY)
        txt.setText(body)

    def want_previous_chapter(self):
        """
        Return true if previous chapter button was clicked
        """
        return self.prv_chapter

    def want_next_chapter(self):
        """
        Return true if next chapter button was clicked
        """
        return self.nxt_chapter

    def want_toc(self):
        """
        Return true if previous TOC button was clicked
        """
        return self.toc

    def want_library(self):
        """
        Return true if library button was clicked
        """
        return self.library

    def want_quit(self):
        """
        Return true if quit button was clicked
        """
        return self.croak

    def isClosed(self):
        """
        Return true if window close was clicked
        """
        return self.closed

    def clearFlags(self):
        """
        Rest flags for various button clicks
        """
        self.prv_chapter = False
        self.nxt_chapter = False
        self.toc = False
        self.croak = False
        self.closed = False
        self.library = False
