from bs4 import BeautifulSoup
import requests
import cli_helper
import re

color = cli_helper.color()

def main():
    searchpage_url = r'http://audiobookbay.nl/?s='
    # TODO: Use input() so you can decide what to search
    # TODO: string converter (html encrypt), e.g. "Harry Potter" -> "harry+potter"
    user_search = "harry+potter+collection"

    # Create BeautifulSoup of the main page to get number of pages
    main_url = searchpage_url + user_search
    r = requests.get(main_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    navigation = soup.select('.wp-pagenavi a')
    navigation_last = str(navigation[len(navigation) - 1])
    navigation_secondLast = navigation[len(navigation) - 2].text.strip()
    # NOTE: navigation_last is the whole HTML element, and navigation_secondLast is only the text from the element
    # (number of pages as string)

    if "»»" in navigation_last:
        maxPages = re.findall(r'\d+', navigation_last)[0] # Finds all the integers in given String
        print(f"Number of pages found: {maxPages}")
    else:
        maxPages = int(navigation_secondLast)
        print(f"Number of pages found: {maxPages}")

    contents = soup.select('.post')

    print("Found " + str(len(contents)) + " books")

    for post in contents:
        postTitle = post.select_one('.postTitle h2 a').text.strip()
        # TODO: Parse book language for postInfo
        rawPostContent = post.select('.postContent p')[3].text.strip() # Named "raw" because the String at this point is not very readable
        # TODO: rawPostContent doesn't acguire the file size if it's in Bytes instead of GBs
        postContent = formatContent(rawPostContent)

        print(color.BOLD + color.UNDERLINE + postTitle + color.END)
        print(postContent)
        break


def formatContent(s):
    formatted = s.replace("Format:", " / Format:")
    formatted = formatted.replace("  /", " /")
    formatted = formatted.replace("File ", "/ File ")
    formatted = formatted.replace("?/", "? /")
    formatted = formatted.replace("?", color.RED + "?" + color.END)
    return formatted


main()
