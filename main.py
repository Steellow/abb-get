from bs4 import BeautifulSoup
import requests
import cli_helper
import re

color = cli_helper.color()

def main():
    domain = r'http://audiobookbay.nl'
    search_prefix = r'/?s='
    user_search = input("Enter search term: ")

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
        maxPages = re.findall(r'\d+', navigation_last)[0] # Finds all the integers in given String
        maxPages = int(maxPages)
        print(f"Number of pages found: {maxPages}")
    else:
        maxPages = int(navigation_secondLast)
        print(f"Number of pages found: {maxPages}")

    pages = [main_url]
    for i in range(2, maxPages + 1):
        pages.append(domain + r'/page/' + str(i) + search_prefix + user_search)

    nth = 1 # Keeps track of how many books

    for page in pages:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html.parser')
        contents = soup.select('.post')

        for post in contents:
            postTitle = post.select_one('.postTitle h2 a').text.strip()
            # TODO: Parse book language for postInfo
            rawPostContent = post.select('.postContent p')[3].text.strip() # Named "raw" because the String at this point is not very readable
            # TODO: rawPostContent doesn't acguire the file size if it's in Bytes instead of GBs
            postContent = formatContent(rawPostContent)

            print(color.BOLD + color.UNDERLINE + str(nth) + ". " + postTitle + color.END)
            print(postContent)
            print("") # Puts empty line between books
            nth += 1 # TODO: Stop and ask before going to next page?


def formatContent(s):
    formatted = s.replace("Format:", " / Format:")
    formatted = formatted.replace("  /", " /")
    formatted = formatted.replace("File ", "/ File ")
    formatted = formatted.replace("Kbps/", "Kbps /")
    formatted = formatted.replace("?/", "? /")
    formatted = formatted.replace("?", color.RED + "?" + color.END)
    return formatted


main()
