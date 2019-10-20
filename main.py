from bs4 import BeautifulSoup
import requests
import cli_helper
import re
import urllib.parse

color = cli_helper.color()


def main():
    domain = r'http://audiobookbay.nl'
    search_prefix = r'/?s='
    user_search = input("Enter search term: ") # TODO: Error if no results (DISABLED FOR FASTER TESTING)
    # user_search = "ready+player+one"

    # Create BeautifulSoup of the main page to get number of pages
    main_url = domain + search_prefix + user_search
    r = requests.get(main_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    navigation = soup.select('.wp-pagenavi a')
    navigation_last = str(navigation[len(navigation) - 1])
    navigation_secondLast = navigation[len(navigation) - 2].text.strip()
    # NOTE: navigation_last is the whole HTML element, and navigation_secondLast is only the text from the element
    # (number of pages as string)

    if "»»" in navigation_last:
        # Finds all the integers in given String
        maxPages = re.findall(r'\d+', navigation_last)[0]
        maxPages = int(maxPages)
        print(f"Number of pages found: {maxPages}")
    else:
        maxPages = int(navigation_secondLast)
        print(f"Number of pages found: {maxPages}")

    pages = [main_url]
    for i in range(2, maxPages + 1):
        pages.append(domain + r'/page/' + str(i) + search_prefix + user_search)

    nth = 1
    post_link_list = []

    for page in pages:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html.parser')
        contents = soup.select('.post')

        for post in contents:
            # TODO: Breaks at second page of "ready player one" search for unknown reason (post re-ab class?)
            postTitle = post.select_one('.postTitle h2 a').text.strip()
            # TODO: Parse book language for postInfo
            # Named "raw" because the String at this point is not very readable
            rawPostContent = post.select('.postContent p')[3].text.strip()
            # TODO: rawPostContent doesn't acguire the file size if it's in Bytes instead of GBs
            postContent = formatContent(rawPostContent)
            postLink = domain + post.select_one('.postTitle h2 a')['href']

            print(color.BOLD + color.UNDERLINE +
                  str(nth) + ". " + postTitle + color.END)
            print(postContent)
            print("")  # Puts empty line between books

            # Puts post link to list so user can later retrieve it)
            # TODO: Doesn't work, first variable is put on slot 0 etc... see 'choice' variable below
            post_link_list.insert(nth, postLink)
            nth += 1

        choice = input("Type 'y' to show next page, or select audiobook by its number: ") #  DISABLED FOR FASTER TESTING
        # choice = "0"
        print("")  # Empty line for better formatting

        if choice is not "y":  # TODO: Better choice checking;, continue if choice is anything but integer?
            break
        # TODO: Crashes if you go to unexisting page

    # ### PARSING THE BOOK PAGE FROM HERE BELOW ### #

    post_url = post_link_list[int(choice) - 1]
    r = requests.get(post_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.select_one('.postTitle h1').text.strip()

    data = []  # The table from book's page
    base_table = soup.select_one('.torrent_info')
    rows = base_table.find_all('tr')
    for row in rows:  # Goes through the table and creates simpler list
        cols = []
        cols_raw = row.find_all('td')
        for col in cols_raw:
            cols.append(col.get_text())
        data.append(cols)

    trackers = []  # TODO: Find out which trackers abb uses
    # Go throught the table to extract all needed information
    for row in data:
        if row[0] == "Tracker:":
            trackers.append(row[1])
        if row[0] == "Info Hash:":
            hash = row[1]

    print(color.BOLD + color.UNDERLINE + name + color.END)
    print("")

    magnet_link = generateMagnet(name, hash, trackers)
    print(magnet_link)


def formatContent(s):
    formatted = s.replace("Format:", " / Format:")
    formatted = formatted.replace("  /", " /")
    formatted = formatted.replace("File ", "/ File ")
    formatted = formatted.replace("Kbps/", "Kbps /")
    formatted = formatted.replace("?/", "? /")
    formatted = formatted.replace("?", color.RED + "?" + color.END)
    return formatted


def generateMagnet(name, hash, trackers):
    prefix = 'magnet:?xt=urn:btih:'
    beforeTitle = '&dn='
    title = urllib.parse.quote(name)
    encoded_trackers = []
    final = prefix + hash + beforeTitle + title
    for tracker in trackers:
        tracker = urllib.parse.quote(tracker)
        tracker = tracker.replace("/", "%2F")
        tracker = "&tr=" + tracker
        # encoded_trackers.append(tracker)
        final = final + tracker
    return final


main()
