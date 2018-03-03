fb-chat-rnn
=======================

Message parsing is based on `facebook-chat-word-cloud <https://github.com/mjmeli/facebook-chat-word-cloud/>`_:
"A Python tool for generating a word cloud for a Facebook chat conversation."

Get Facebook messages archive
-----------------------------
1. Go to Facebook Settings: https://www.facebook.com/settings
2. Click the link at the bottom ("Download a copy of your Facebook data")
3. Click "Start My Archive" and wait for the download to be ready
4. Download and extract
5. Open up the **messages.htm** file in a browser
6. Click on the conversation you would like to use
7. Remember the location of the **messages/<#>.html** file of the conversation (<#> should be Facebook's conversation number)

Development
-----------

    git clone https://github.com/iconix/fb-chat-rnn.git

    pip install -e .

Quick Example Usage
-------------------
Request your Facebook data archive and get the conversation html file.

    fb_chat_rnn examples/messages_sample.htm

Output the results to a text file:

    fb_chat_rnn messages_sample.htm -o out.txt

Testing
-------
    python setup.py test
