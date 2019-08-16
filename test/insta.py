from instapy_cli import client

username = 'havasresearch'
password = 'havas-reasearch'
image = 'test.jpg'
text = 'Hello :)' + '\r\n' + '#hash #tag #now'

with client(username, password) as cli:
    cli.upload(image, text)
