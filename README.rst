facebook-message-rnn
=======================

Parser is based on `facebook-chat-word-cloud <https://github.com/mjmeli/facebook-chat-word-cloud/>`_:
"A Python tool for generating a word cloud for a Facebook chat conversation."

Get Facebook messages archive
-----------------------------
1. Go to Facebook Settings: https://www.facebook.com/settings
2. Click the link at the bottom ("Download a copy of your Facebook data")
3. Click "Start My Archive" and wait for the download to be ready
4. Download and extract
5. Pull out or remember the location of the **messages.htm** file

The messages file downloaded from Facebook will probably be quite large (mine was 60 MB). It may take a while to parse, which can get annoying when you are making small changes to get a nice looking word cloud. I highly recommend using the sample conversation I provide as this will parse in seconds and has very high word density. You can either directly reference this file (examples/messages_sample.htm with user "Foo Bar") or just use the "-sample" option with the command

Parsing requirements
------------
This uses `lxml` to parse the messages file provided by Facebook. This requires `libxml2` and `libxslt` to be installed.

For Debian/Ubuntu:

    sudo apt-get install libxml2-dev libxslt-dev python-dev python-tk

This also uses `Pillow` to handle image manipulation. This requires `libjpeg`, `zlib`, and `libfreetype`:

    sudo apt-get install libjpeg-dev zlib1g-dev libfreetype6-dev

Parsing issues
------
**ImportError: The _imagingft C module is not installed**
This means you don't have `libfreetype` installed. See the Requirements section. If installing it does not work, you may have to uninstall and reinstall `Pillow` via `pip`.

**IOError: Couldn't locate mask file...did you make sure to specify the URL relative to where you are running the script?**
This error is self-explanatory. In `masked/config.json`, the mask file is specified with a relative URL. This URL is *relative to where you are running the script*. I wrote the config file assuming that you were running the `facebook_wordcloud` in the `/examples` directory. If this is not the case, then either `cd` into that directory, or adjust the path in `masked/config.json`.

**The mask doesn't seem to be working?**
I ran into this issue a few times. Make sure the mask is either in RGB or grayscale. Note that only parts that are pure white (#FFFFFF) will be removed.
