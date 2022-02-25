#
# Module to isolate code from Kodi specific stuff
#
# All GUI related functions are named "gui_<something>"
#

import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon

#
# Addon specific stuff
#
def itsme():
    """
    Return current addon object
    """
    return xbmcaddon.Addon()


def id():
    """
    Get localized string for integer code
    """
    return itsme().getAddonInfo("id")


def log(s):
    """
    Log a debug string
    """
    xbmc.log("~~~~~ {} -- {}".format(id(), s), xbmc.LOGINFO)


def debug(s):
    """
    Log a debug string
    """
    xbmc.log("~~~~~ {} -- {}".format(id(), s), xbmc.LOGDEBUG)


def error(s):
    """
    Log an error
    """
    xbmc.log("~~~~~ {} -- {}".format(id(), s), xbmc.LOGERROR)


def fatal(s):
    """
    Log a fatal error
    """
    xbmc.log("~~~~~ {} -- {}".format(id(), s), xbmc.LOGFATAL)


def string(id):
    """
    Get localized string for integer code
    """
    return itsme().getLocalizedString(id)


def setting(id):
    """
    Get value as a string for named setting
    """
    return itsme().getSetting(id)


def set_setting(id, value):
    """
    Set value as a string for named setting
    """
    itsme().setSetting(id, str(value))


def name():
    """
    Get addon name
    """
    return itsme().getAddonInfo("name")


def version():
    """
    Get addon version
    """
    return itsme().getAddonInfo("version")


def icon():
    """
    Get addon icon name
    """
    return itsme().getAddonInfo("icon")


def whereami():
    """
    Get addon path
    """
    return itsme().getAddonInfo("path")


def path(path=""):
    """
    Get addon path
    """
    return xbmcvfs.translatePath("{}{}".format(itsme().getAddonInfo("path"), path))


#
# GUI interaction stuff
#


def gui_notify(hdr, msg, tim=5000, image=""):
    """
    Show briefly a notification message
    """
    xbmc.executebuiltin('Notification({}, "{}", {}, {})'.format(hdr, msg, tim, image))


def gui_ok(hdr, l1, l2="", l3=""):
    """
    Ask user for an acknowledgement before continuing
    """
    xbmcgui.Dialog().ok(hdr, l1, l2, l3)


def gui_select(hdr, the_list):
    """
    Present user a list of choices to choose one.
    """
    return xbmcgui.Dialog().select(hdr, the_list)


def gui_ask_yes_no(hdr, l1, l2="", l3=""):
    """
    Show a Yes/No type of dialog and return result
    """
    return xbmcgui.Dialog().yesno(hdr, l1, l2, l3) == 1


def gui_browse(type, heading, shares="files", mask="", enablemultiple=False):
    """
    Let user select something filesystem related (depends on "type")
    """
    dialog = xbmcgui.Dialog()
    return dialog.browse(type, heading, shares, mask, enablemultiple)


def gui_browse_files(heading, shares="files", mask="", enablemultiple=False):
    """
    Let user select a file
    """
    return gui_browse(1, heading, shares, mask, enablemultiple)


def monitor():
    """
    Return XBMC monitor object
    """
    return xbmc.Monitor()


def sleep(tim):
    """
    No extra credit for guessing what this does...
    """
    xbmc.sleep(tim)
