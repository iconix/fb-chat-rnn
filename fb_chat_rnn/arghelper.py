"""
    arghelper
    Intended to provide some helper functions for parsing arguments.
"""
import os

# Checks whether an argument is a valid file
# Source: http://codereview.stackexchange.com/questions/28608/checking-if-cli-arguments-are-valid-files-directories-in-python
def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    else:
        # File exists so return the filename
        return arg

def generate_argparse(parser):
    # Required
    parser.add_argument("messages_file",
                        help="path to your Facebook generated messages file",
                        type=lambda x: is_valid_file(parser, x))

    # Optional
    parser.add_argument("-o", "--out",
                        help="desired output file for PNG of word cloud")
