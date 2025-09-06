# orbit-memeReviewBot
A Slackbot for OrbitNTNU!

Members post memes in the channel, and the memebot will collect all recent memes into a Google Form.
How to use it in Slack using slash commands:
- /memereview! : the bot creates a Google Form with all recent memes, where people can vote for their favorite meme.
- /getwinner : the bot announces the winner meme.

How to run it:
make sure to be in "orbit-memeReviewBot" folder and run docker container+image:
```
docker compose up --build
```

Note: This requires a Slack Bot and a Google Service Account.
This Bot is meant to be run on OrbitNTNU's server.
