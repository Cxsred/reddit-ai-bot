import praw
import openai

# Set up Reddit API credentials
reddit_client_id = 'REDDIT_CLIENT_ID'
reddit_client_secret = 'REDDIT_CLIENT_SECRET'
reddit_user_agent = 'REDDIT_USER_AGENT'
reddit_username = 'REDDIT_USERNAME'
reddit_password = 'REDDIT_PASSWORD'

# Set up OpenAI API credentials
openai_api_key = 'OPENAI_API_KEY'

# Create the PRAW (Reddit API) client
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent=reddit_user_agent,
                     username=reddit_username,
                     password=reddit_password)

# Configure the OpenAI API client
openai.api_key = openai_api_key

# Function to check new posts in a specific subreddit on Reddit
def check_subreddit_posts(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    for post in subreddit.stream.submissions():
        # Send the post text to OpenAI for analysis
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=post.title,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7
        )
        generated_text = response.choices[0].text.strip()

        # Generate a comment using the analysis result
        comment = f"ChatGPT analysis: {generated_text}"

        # Reply with the comment
        post.reply(comment)

# Main loop
def main():
    subreddit_file = 'subreddits.txt'  # File containing the list of subreddits
    with open(subreddit_file, 'r') as file:
        subreddit_names = [line.strip() for line in file if line.strip()]
    for subreddit_name in subreddit_names:
        check_subreddit_posts(subreddit_name)

if __name__ == '__main__':
    main()
