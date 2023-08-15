# Kodi addon for reading books in EPUB format

## Notice

Moved to [Codeberg]([https://codeberg.org/evilwan/script.kekkisear) because of policy changes at Github (see
[Github notice](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13) )

## Introduction
Reading ebooks on Kodi looked like a logical thing to do ... but strangely enough no readily available addons exist to make this possible. Googling around shows that, at one time, there was in fact an addon for doing just that, but the addon is no longer maintained and does not even work on recent Kodi versions.

That is where this addon comes in: it is intended to allow reading DRM free books in EPUB format in Kodi. The main focus here is on **reading** meaning that showing text is the primary goal, not so much how the text is supposed to be rendered according formatting instructions in the EPUB file. This addon will extract all text from the book and will show it without any special character formatting at all: no bold, no italics, no whatever, just the bare text.

The EPUB specification is quite extensive. However, this addon will happily ignore most of that.

The Kodi API does not offer the same rich formatting options that are available in web browsers. So, any chance of building an EPUB reader that adheres to the full specification is doomed from the start. E.g. the API allows to show a long text in a scrollable area. However, that same API does not offer the possibility to ask that text component which part of a large text is currently visible. The API allows to specify which line has to be shown on the top of the textbox, but that is not all that practical if there is no way to find out how much text is being shown (the text is wrapped around, but the textbox does not tell you how many characters are on one line...)

Finally, the DRM free part. This addon will in no way help bypass any restriction placed on EPUB files. If there are limitations (DRM) then this addon is not for you.

There are currently no plans for support of other ebook formats as the author prefers ebooks in EPUB format. PDF is, almost by definition, not suitable for this addon. PDF **draws** information on pages. Given the Kodi addon API restrictions mentioned above, rendering PDF seems impossible from the start.

## Usage
The first time that the addon starts it will prompt for an EPUB file to start reading. All subsequent starts will resume the last book that was open in the addon. There is no fancy interface that will show book covers or even book titles: you will have to pick a file.

Whenever a new book is opened, the reader will start with the first chapter. Wnen the addon is restarted, the chapter that was shown during the last run will be shown again.

The chapter text will start scrolling automatically shortly after being shown on screen. On the right hand side is a scrollbar that can be used to control the scrolling.

On the bottom are a number of buttons:

- "<" and ">" buttons will go to the previous/next chapter
- "Table of Contents" will show the list of chapters and let you select to which chapter you want to jump
- "-" and "+" buttons control the speed of autoscroll ("-" will speed up, "+" will slow down)
- "Library" will let you select a different book to read
- "Quit" will leave the addon

## Open issues
As indicated above, the author has not been able to find a way in the Kodi addon API to:

- have fine-tuned control over the scrollable textbox (such as querying what part of the text is currently visible)
- do extensive text formatting (mixed fonts, CSS-like formatting...)

If you have a solution for the above questions, please feel free to contact the author.

## License
This addon is distributed under the 3 clause MIT license (see LICENSE.txt)

Two images have been downloaded from the internet: on both sites the images were marked as "free":

- [Addon icon: https://www.flaticon.com/authors/smashicons](https://www.flaticon.com/authors/smashicons)
- [Fanart: https://unsplash.com/s/photos/bookshelf](https://unsplash.com/s/photos/bookshelf)

