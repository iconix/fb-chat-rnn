import argparse
import os
import time

import fb_chat_rnn.arghelper as arghelper
from fb_chat_rnn.message_parser import MessageParser

def main():
    start = time.time()

    # Set up argument parser
    parser = argparse.ArgumentParser()
    arghelper.generate_argparse(parser)
    args = parser.parse_args()

    print("Loading file...")
    filename = args.messages_file
    with open(filename, 'r', encoding='utf8') as f:
        messages_file_data = f.read()

    # Parse the HTML and extract messages (may take a long time)
    print("Building HTML tree...")
    message_parser = MessageParser(messages_file_data)
    print("Parsing messages...")
    thread = message_parser.parse_thread()

    messages = thread.get_messages_contents()

     # If a output file was specified, output to there
    if args.out is not None:
        if args.out.endswith("txt"):
            outFile = args.out
        else:
            outFile = args.out + ".txt"

        with open(outFile, 'w', encoding='utf-8') as f:
            [print(m, file=f) for m in messages]
    else:
        for m in messages:
            try:
                print(m)
            except UnicodeEncodeError as e:
                invalidData = e.object[e.start:e.end]
                encodedData = invalidData.encode('unicode_escape').decode()
                print(e.object.replace(invalidData, encodedData))

    end = time.time()

    print('Elapsed time (s): ' + str(end - start))

if __name__ == '__main__':
    main()
