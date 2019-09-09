from setuptools import setup, find_packages
import sys
from codecs import open
from os import path

try:
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    message = "Unable to locate 'semantic_release', releasing won't work"
    print(message, file=sys.stderr)


version = '1.0.0'


package_root = path.abspath(path.dirname(__file__))

with open(path.join(package_root, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='schedule_tweet',
    version=version,
    description='Schedules tweets using TweetDeck',
    long_description=long_description,
    url='https://github.com/honzajavorek/schedule-tweet',
    author='Honza Javorek',
    author_email='mail@honzajavorek.cz',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tweet tweets twitter tweetdeck scheduling scheduler',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'selenium>=3.5,<3.142'
    ],
    extras_require={
        'tests': [
            'requests>=2.18.4,<2.23.0',
            'lxml>=4.1.1,<4.5.0',
            'cssselect>=1.0.1,<1.2.0',
            'pytz>=2017.3',
            'pylama>=7.4.3,<7.8.0',
        ],
        'release': [
            'python-semantic-release>=3.10.2,<4.4.0'
        ],
    }
)
