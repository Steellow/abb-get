import urllib.parse

str = "The Oldest Living Vampire on the Prowl The Oldest Living Vampire Saga, Book 2 - Joseph Duncan"
str2 = "The Oldest Living Vampire on the Prowl The Oldest Living Vampire Saga, Book 2 - Joseph Duncan"

str = str.replace(" ", "%20")
str = str.replace(",", "%2C")
str2 = urllib.parse.quote(str2)

print(str)
print(str2)

#Convert this shit to method