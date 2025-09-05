import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from api.googleApis.memeForm import *
from api.googleApis.getWinner import get_winner
from jsonMethods import read_from_json

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
app = App(token = bot_token)
client = WebClient(token = bot_token)

@app.command("/memereview!")
def review_memes(ack, respond, command):
    try:
        ack()

        respond(
            text=f"Generating form...",
            response_type="in_channel"
        )

        memes = get_memes(respond, command)
        
        memeForm = create_form(memes)

        respond(
            text=f"Time for a new round of Meme Review! Go to {memeForm} and vote!",
            response_type="in_channel"
        )

    except Exception as e:
        respond(
            text=f'Something happened: {e}. Please try again!',
            response_type="in_channel"
        )


@app.command("/getwinner")
def get_winner_meme(ack, respond, command):
    ack()

    respond(
        text=f'🥁 Drumroll please... 🥁',
        response_type="in_channel"
    )
    
    winner_memes = get_winner(read_from_json('last_formID', './lastExecution.json'))
    if len(winner_memes) < 1:
        respond(
            text=f'It seems like there was no winner meme this time, hmmmm...',
            response_type="in_channel"
        )
    else:
        for x in winner_memes:
            respond(
                text=f'The winner of this round of Orbit Meme review is {x}',
                response_type="in_channel"
            )


def get_memes(respond, command):
    channel_id = command['channel_id']
    mime_types = ['image/gif', 'image/png', 'image/jpeg', 'video/mp4']

    try:
        response = client.conversations_history(channel=channel_id, oldest=getMondayOfLastWeek())
        messages = response['messages']
        memes = [x for x in messages 
                 if 'files' in x and x['files'][0]['mimetype'] 
                 in mime_types]
        
        if len(memes) < 1:
            respond(
                text=f"Oh, no memes sent since last Big Workshop!",
                response_type="in_channel"
            )
            print("no memes since last time..")
        else:
            return memes

    except Exception as e:
        print(e)

def getMondayOfLastWeek():
    weekdayRightNow = datetime.now()
    start_of_last_week = (weekdayRightNow - timedelta(days=weekdayRightNow.weekday() + 7)).replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_last_week_timestamp = int(start_of_last_week.timestamp())
    return start_of_last_week_timestamp


if __name__ == "__main__":
    handler = SocketModeHandler(app, 
                                os.getenv('APP_TOKEN'),
                                )
    handler.start()

