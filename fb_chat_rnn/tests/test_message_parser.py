import os
import datetime
from lxml import html
from unittest import TestCase

from fb_chat_rnn.message_parser import *

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "messages_sample.htm")

class TestMessageParser(TestCase):
    def setUp(self):
        with open(TESTDATA_FILENAME, 'r') as f:
            self.testdata = f.read()

    def test_testdata(self):
        # Should be a string right now
        self.assertTrue(isinstance(self.testdata, str))

        # Should be able to convert to HTML. If this fails, the test fails.
        html_tree = html.fromstring(self.testdata)

    # Test whether messages are handled with dates sent as strings or date objects
    def test_message(self):
        # The following should be passing
        date = datetime.datetime(2016, 1, 2, 12, 15, 37)
        msg = Message("John Smith", date, "You are super fly")
        self.assertTrue(str(msg) == "John Smith (Sat Jan 02, 2016 12:15 PM): You are super fly")

        sample_date = "Saturday, 02 January 2016 at 12:15:00 EDT"
        msg = Message("John Smith", sample_date, "You are super fly")
        self.assertTrue(str(msg) == "John Smith (Sat Jan 02, 2016 12:15 PM): You are super fly")

        # The following should fail
        self.assertRaises(Exception, Message, "John Smith", [15, 15, 15], "Test")


    # Test message comparisons using dates
    def test_message_comparison(self):
        date1 = datetime.datetime(2016, 1, 2)
        date2 = datetime.datetime(2016, 1, 3)

        msg1 = Message("Test", date1, "Test")
        msg2 = Message("Test", date2, "Test")

        self.assertTrue(msg1 < msg2)
        self.assertTrue(msg2 > msg1)
        self.assertTrue(msg1 == msg1)
        self.assertTrue(msg2 == msg2)
        self.assertFalse(msg1 == msg2)

    # Test conversation thread handling
    def test_thread(self):
        thread = Thread()
        thread.add_user("User 1")
        thread.add_user("User 2")

        # Create and add good messages
        msg1 = Message("User 1", datetime.datetime(2016, 1, 1), "Test")
        msg2 = Message("User 2", datetime.datetime(2016, 1, 3), "Test")
        msg3 = Message("User 1", datetime.datetime(2016, 1, 2), "Test")
        thread.add_message(msg1)
        thread.add_message(msg2)
        thread.add_message(msg3)

        # Verify messages are sorted
        self.assertEqual(msg1, thread.messages[2])
        self.assertEqual(msg3, thread.messages[0])
        self.assertEqual(msg2, thread.messages[1])

        # Add a message with the same date
        msg4 = Message("User 2", datetime.datetime(2016, 1, 2), "Test")
        thread.add_message(msg4)
        self.assertEqual(msg1, thread.messages[3])
        self.assertEqual(msg3, thread.messages[1])
        self.assertEqual(msg4, thread.messages[0])
        self.assertEqual(msg2, thread.messages[2])

        # Add a user that doesn't exist
        msg5 = Message("User 3", datetime.datetime(2016, 1, 3), "Test")
        thread.add_message(msg5)
        self.assertEqual(msg5, thread.messages[0])

        # Test creating a thread with arrays
        thread2 = Thread(["User 1", "User 2"])
        thread2.add_message(msg1)
        thread2.add_message(msg2)
        self.assertEqual(msg1, thread2.messages[1])
        self.assertEqual(msg2, thread2.messages[0])
        msg5 = Message("User 3", datetime.datetime(2016, 1, 3), "Test")
        thread.add_message(msg5)
        self.assertEqual(msg5, thread.messages[0])

        thread3 = Thread(["User 1", "User 2", "User 1"], [msg1, msg2, msg3])
        self.assertEqual(len(thread3.users), 2)
        self.assertEqual(msg1, thread3.messages[0])
        self.assertEqual(msg3, thread3.messages[1])
        self.assertEqual(msg2, thread3.messages[2])
        msg5 = Message("User 3", datetime.datetime(2016, 1, 3), "Test")
        thread.add_message(msg5)
        self.assertEqual(msg5, thread.messages[0])

        thread4 = Thread()
        thread4.add_users(["User 1", "User 2"])
        thread4.add_message(msg1)
        thread4.add_message(msg2)
        self.assertEqual(msg1, thread4.messages[1])
        self.assertEqual(msg2, thread4.messages[0])
        msg5 = Message("User 3", datetime.datetime(2016, 1, 3), "Test")
        thread.add_message(msg5)
        self.assertEqual(msg5, thread.messages[0])

    # Test message parser constructor with good and bad HTML inputs
    def test_constructor(self):
        # Try our constructor with a good inputs
        MessageParser(self.testdata)
        MessageParser("get schwifty")

        # Now try with bad inputs
        self.assertRaises(ValueError, MessageParser, [1, 2, 3])
        self.assertRaises(ValueError, MessageParser, html.fromstring(self.testdata))

    # Test get_users_facebookaddress functionality
    def test_get_users_facebookaddress(self):
        parser = MessageParser(self.testdata)
        self.assertEqual(["The Driver", "Party Girl", "Social Butterfly", "Eager Beaver", "Gif Goddess", "Mediator"], parser.get_participants())

    def test_parser(self):
        parser = MessageParser(self.testdata)
        thread = parser.parse_thread()

        # Verify thread
        self.assertTrue("The Driver" in thread.users)
        self.assertTrue("Party Girl" in thread.users)
        self.assertTrue("Social Butterfly" in thread.users)
        self.assertTrue("Eager Beaver" in thread.users)
        self.assertTrue("Gif Goddess" in thread.users)
        self.assertTrue("Mediator" in thread.users)
        self.assertTrue("John Smith" not in thread.users)
        self.assertTrue("Linus Torvalds" not in thread.users)

        # Verify messages
        messages = thread.messages
        self.assertEqual(len(messages), 14)
