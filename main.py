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
        postContent = post.select('.postContent p')[3].text.strip()

        print(color.BOLD + postTitle + color.END)
        print(postContent)


main()
