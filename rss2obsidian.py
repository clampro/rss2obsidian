# Simple script to read RSS feeds from urls stored in a text file

# Imports
import feedparser
import configparser
from datetime import datetime


def main():
    # Global Lists
    rssList = []
    feeds = []
    output = []

    # Read ini file and get RSS feeds
    config = configparser.ConfigParser()
    config.read('rss2obsidian.ini')

    rss_file = config.get('DEFAULT', 'rss_list')
    output_file_path = config.get('DEFAULT', 'output_file')
    number_of_posts = config.get('DEFAULT', 'number_of_posts')

    posts_to_read = int(number_of_posts) - 1.

    # Open RSS List and get Feeds
    with open(rss_file) as readFile:
        fileLines = readFile.readlines()

    # strip is used to remove /n from lines
    for i in fileLines:
        rssList.append(i.rstrip())

    for url in rssList:
        singleFeed = feedparser.parse(url)
        if singleFeed.bozo is False:
            feeds.append(singleFeed)
        else:
            print(singleFeed.bozo_exception)

    for feed in feeds:
        line = '## ' + feed.feed.title + '\n'
        output.append(line)
        line = '\n'
        output.append(line)
        for index, post in enumerate(feed.entries):
            line = '- ' + post.published[0:16] + ': ' + '[' + post.title + '](' + post.link + ')' + '\n'
            output.append(line)
            if index == posts_to_read:
                break
        line = '\n'
        output.append(line)

    line = '\n'
    output.append(line)
    line = '---\n'
    output.append(line)
    line = 'RSS File Generated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output.append(line)

    with open(output_file_path, "w") as output_file:
        for line in output:
            output_file.write(line)

if __name__ == "__main__":
    main()
