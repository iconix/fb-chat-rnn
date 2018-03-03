from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='fb-chat-rnn',
      version='0.1',
      description='A Python tool for generating Facebook Messenger conversations.',
      long_description=readme(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      keywords='facebook chat parser',
      license='MIT',
      packages=['fb_chat_rnn'],
      install_requires=[
          'python-dateutil',
          'lxml'
      ],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['fb_chat_rnn=fb_chat_rnn.command_line:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose', 'mock'],
      include_package_data=True
)
