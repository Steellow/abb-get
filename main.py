from bs4 import BeautifulSoup
import requests
import cli_helper

color = cli_helper.color()

def main():
    searchpage_url = r'http://audiobookbay.nl/?s='
    # TODO: Use input() so you can decide what to search
    # TODO: string converter (html encrypt), e.g. "Harry Potter" -> "harry+potter"
    user_search = "harry+potter+collection"

    url = searchpage_url + user_search
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    contents = soup.select('.post')

    print("Found " + str(len(contents)) + " books")


    for post in contents:
        postTitle = post.select_one('.postTitle h2 a').text.strip()
        # TODO: Parse book language for postInfo
        rawPostContent = post.select('.postContent p')[3].text.strip() # Named "raw" becayse the String at this point is not very readable
        postContent = formatContent(rawPostContent)

        print(color.BOLD + color.UNDERLINE + postTitle + color.END)
        print(postContent)
        #break


def formatContent(s):
    formatted = s.replace("Format:", " / Format:")
    formatted = formatted.replace("  /", " /")
    formatted = formatted.replace("File ", "/ File ")
    return formatted


main()
