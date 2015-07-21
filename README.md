splash
======

Speedreading program similar to spritz.


Built with:

* python3
* gtk3 & glade
* pango
* cairo


## Usage

### Console mode

run `cat file | python3 -m splash.splash`

further invocation help can be seen via
`python3 -m splash.splash --help`


### GUI mode

run `python3 -m splash`


## File conversion

Currently, splash supports plain text only.
To read other formats, convert them to text first.


### Ebooks

You can convert `.epub` ebooks with [callibre](http://calibre-ebook.com/):

```
ebook-convert input.epub output.txt
```


### PDF files

Use [poppler](http://poppler.freedesktop.org/):

```
pdftotext input.pdf output.txt
```


## Contributing

If you're bored and want to add new stuff to the project,
just go for it and submit pull requests.

Please adhere to the PEP8 coding style.


## Contact

You can reach us in IRC:

`#sfttech` on `freenode.net`


License
-------

GNU GPLv3 or any later version. See COPYING for further info.
