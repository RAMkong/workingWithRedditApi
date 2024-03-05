import requests
import os

class Reddit:
    def __init__(self, client_id, client_secret, redirect_uri, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.user_agent = user_agent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Add cleanup logic here if needed
        pass

    def reddit_auth(self):
        auth_url = f'https://www.reddit.com/api/v1/authorize?client_id={self.client_id}&response_type=code&state=RANDOM&redirect_uri={self.redirect_uri}&duration=permanent&scope=vote'
        print(f'Please visit the following URL to authorize the application:\n{auth_url}')

    def reddit_callback(self, code):
        options = {
            'method': 'POST',
            'url': 'https://www.reddit.com/api/v1/access_token',
            'auth': (self.client_id, self.client_secret),
            'data': {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri
            },
            'headers': {
                'User-Agent': self.user_agent
            }
        }

        try:
            response = requests.request(**options).json()
            print(response)

            with open('reddit_token.txt', 'w') as file:
                file.write(response['access_token'])

            print('Logged in!')
        except Exception as error:
            print('Error', error)

    def reddit_list(self):
        token = open('reddit_token.txt', 'r').read()

        options = {
            'method': 'GET',
            'url': 'https://oauth.reddit.com/hot',
            'headers': {
                'Authorization': f'Bearer {token}',
                'User-Agent': self.user_agent
            }
        }

        try:
            response = requests.request(**options).json()
            print(response)
        except Exception as error:
            print('Error', error)

    def create_post(self):
        token = open('reddit_token.txt', 'r').read()

        options = {
            'method': 'POST',
            'url': 'https://oauth.reddit.com/api/submit',
            'headers': {
                'Authorization': f'Bearer {token}',
                'User-Agent': self.user_agent
            },
            'data': {
                'api_type': 'json',
                'kind': 'self',
                'sr': 'self',
                'title': 'CodingWithAdo is the best youtube channel',
                'text': 'You should go and check: https://www.youtube.com/@codingwithado'
            }
        }

        try:
            response = requests.request(**options).json()
            print(response)
        except Exception as error:
            print('Error', error)


    def upvote_post(self, post_id):
        token = open('reddit_token.txt', 'r').read()

        options = {
            'method': 'POST',
            'url': f'https://oauth.reddit.com/api/vote',
            'headers': {
                'Authorization': f'Bearer {token}',
                'User-Agent': self.user_agent
            },
            'data': {
                'dir': 1,  # 1 for upvote, -1 for downvote
                'id': post_id
            }
        }

        try:
            response = requests.request(**options).json()
            print(response)
        except Exception as error:
            print('Error', error)

    def downvote_post(self, post_id):
        token = open('reddit_token.txt', 'r').read()

        options = {
            'method': 'POST',
            'url': f'https://oauth.reddit.com/api/vote',
            'headers': {
                'Authorization': f'Bearer {token}',
                'User-Agent': self.user_agent
            },
            'data': {
                'dir': -1,  # 1 for upvote, -1 for downvote
                'id': post_id
            }
        }

        try:
            response = requests.request(**options).json()
            print(response)
        except Exception as error:
            print('Error', error)

    def comment_on_post(self, post_id, text):
        token = open('reddit_token.txt', 'r').read()

        options = {
            'method': 'POST',
            'url': f'https://oauth.reddit.com/api/comment',
            'headers': {
                'Authorization': f'Bearer {token}',
                'User-Agent': self.user_agent
            },
            'data': {
                'thing_id': post_id,
                'text': text
            }
        }

        try:
            response = requests.request(**options).json()
            print(response)
        except Exception as error:
            print('Error', error)
