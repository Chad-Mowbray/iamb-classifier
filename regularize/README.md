# regularize: A Python module for early modern spelling

This experimental Python module will modernize English text strings from early modern spelling into modern spellings, e.g. "dogge" will become "dog." It is made possible by the excellent [MorphAdorner](http://morphadorner.northwestern.edu/), which provides many NLP tools for early modern texts, including spelling modernization and regularization. 

The module is for short demonstrations of the importance of spelling regularization or quick tests ONLY---for any serious text-processing tasks, I highly recommend using MorphAdorner directly.

## Installation

Because *regularize* is still a work in progress, I have not yet made it available on the [Python Package Index](https://pypi.python.org/pypi), which means you cannot install with pip. To install manually, download the files or clone this repo, then go to this directory on your command line and type:

`python setup.py install`

This installation should work for both Python 2.7 and 3.x.

## Usage

Once *regularize* is installed, import with `from regularize import regularize as reg`. The module has only one function, *modernize*:

`reg.modernize("Any text string.")`

And that's it!

## License

*regularize* follows the same license and disclaimers as Morphadorner, which can be found [here](http://morphadorner.northwestern.edu/licenses/).
