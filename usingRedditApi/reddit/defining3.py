import praw

class Reddit:
    def __init__(self, client_id, client_secret, redirect_uri, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.user_agent = user_agent
        self.reddit = None

    def __enter__(self):
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            user_agent=self.user_agent,
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Add cleanup logic here if needed
        pass

    def get_authorization_url(self):
        print(self.reddit.auth.url(scopes=['identity', 'submit', 'read'], state='web', duration='permanent'))
        #return self.reddit.auth.url(scopes=['identity', 'submit', 'read'], state='web', duration='permanent')
        return self
    def authorize_application(self, code):
        # print(f'Visit the following URL to authorize the application:\n{self.reddit.auth.authorize(code)}')
        return self.reddit.auth.authorize(code)

    def create_reddit_instance_with_token(self, refresh_token):
        return praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            user_agent=self.user_agent,
            refresh_token=refresh_token,
        )

    def comment_on_post(self, reddit_instance, post_url, comment_text):
        post = reddit_instance.submission(url=post_url)
        post.reply(comment_text)
        print('Comment posted successfully!')

    def create_post(self, subreddit_name, title, content):
        subreddit = self.reddit.subreddit(subreddit_name)
        subreddit.submit(title, selftext=content)
        print('Post created successfully!')

    def read_top_comments(self, subreddit_name, post_limit=5, comment_limit=3):
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.top(limit=post_limit):
            print(f"\nPost Title: {submission.title}")
            print("Top Comments:")
            for comment in submission.comments[:comment_limit]:
                print(f"\t- {comment.body}")

    def read_popular_comments(self, subreddit_name, post_limit=5, comment_limit=3):
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=post_limit):
            print(f"\nPost Title: {submission.title}")
            print("Popular Comments:")
            for comment in submission.comments[:comment_limit]:
                print(f"\t- {comment.body}")

    def read_new_comments(self, subreddit_name, post_limit=5, comment_limit=3):
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit=post_limit):
            print(f"\nPost Title: {submission.title}")
            print("New Comments:")
            for comment in submission.comments[:comment_limit]:
                print(f"\t- {comment.body}")

if __name__ == "__main__":
    CLIENT_ID = '.'
    CLIENT_SECRET = '.'
    REDIRECT_URI = '.'
    USER_AGENT = '.'

    with Reddit(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USER_AGENT) as reddit_bot:
        authorization_url = reddit_bot.get_authorization_url()
        print(f'Visit the following URL to authorize the application:\n{authorization_url}')

        # Ask the user to enter the code obtained after authorization
        code = input('Enter the code: ')

        # Exchange the code for an access token
        token_info = reddit_bot.authorize_application(code)

        # Create a new Reddit instance with the access token
        reddit_with_token = reddit_bot.create_reddit_instance_with_token(token_info)

        # Example: Commenting on a post
        post_url = 'https://www.reddit.com/r/VALORANT/comments/1b7mg85/life_hack_to_get_gun_dropped_for_you_in_low_elo/'
        reddit_bot.comment_on_post(reddit_with_token, post_url, 'nah i am saving')

        # subreddit_name = 'test'
        # title = 'New Post Title'
        # content = 'This is the content of the new post.'
        # reddit_bot.create_post(subreddit_name, title, content)
        #
        # # Example: Reading top comments
        # reddit_bot.read_top_comments(subreddit_name)
        #
        # # Example: Reading popular comments
        # reddit_bot.read_popular_comments(subreddit_name)
        #
        # # Example: Reading new comments
        # reddit_bot.read_new_comments(subreddit_name)
