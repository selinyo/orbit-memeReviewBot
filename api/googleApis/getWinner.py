import os
import mysql.connector
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient import discovery
from pathlib import Path


root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
dotenv_path = os.path.join(root_folder, '.env')
load_dotenv(dotenv_path)

def get_winner(form_id):
    """Gets the winning memes from the Google Form given by the formID.

    Args:
        formID (_string_): The ID of the form

    Returns:
        winners _(array)_: An array containing all the choices that had the most votes.
    """

    credentials = service_account.Credentials.from_service_account_file(
    os.getenv('SERVICE_ACCOUNT_FILE'), scopes=os.getenv('SCOPES').split(','))

    forms_service = discovery.build('forms', 'v1', credentials=credentials, discoveryServiceUrl=os.getenv('DISCOVERY_DOC'), static_discovery=False)
    responses = forms_service.forms().responses().list(formId=form_id).execute()

    answers = [
        answer_data['textAnswers']['answers'][0]['value']
        for response in responses['responses']
        for answer_data in response['answers'].values()
    ]
    counted_answers = [(answers.count(x), x) for x in set(answers)]

    max_count = max(counted_answers, key=lambda x: x[0])[0]

    winners = [answer[1] for answer in counted_answers if answer[0] == max_count] 
    # for winner in winners:
    #   saveWinnerToCDN(winner)
    #   saveWinnerMeme(winner)
    # removeAllFilesFromFolder(cdnpath)

    return winners

def save_winner_meme(meme):
    """_summary_

    Args:
        meme (_string_): _description_
    """
    db = mysql.connector.connect(
            host=os.getenv('host'),
            port=int(os.getenv('port')),
            user=os.getenv('user'),
            password=os.getenv('password'),
            database=os.getenv('database')
        )
    
    file_name = meme.replace('https://cdn.orbitntnu.com', '')
    meme_creator = file_name.partition('_')[0]
    
    if db and db.is_connected():
        with db.cursor() as cursor:
            try:
                if True:
                    cursor.execute(
                        f''' 
                        INSERT INTO Meme (memeUri, memberID)
                        VALUES ('{meme}', '{meme_creator}');
                    '''
                    )
                cursor.execute("SELECT * FROM Meme;")
                    
            except Exception as e:
                db.rollback()

            finally:
                db.commit()
                db.close()
    else:
        print('SQL connection failed.')

def remove_all_files_from_folder(folder_path):
    """Removes everything that's inside the provided folder. 
    """
    try:
        folder_content = os.listdir(folder_path)
        if not folder_content:
            print('The folder is empty.')
        else:
            for file in folder_content:
                os.remove(os.path.join(folder_path, file))
    except Exception as e:
        print(f'No directory found in {folder_path}, error: {e}')

def save_winner_to_CDN(meme, origin_folder, dest_folder):
    """Moves the specified file (meme) from one folder to another.

    Args:
        meme (_string_): The filename of the file to be moved.
        originFolder (_string_): The folder the file is originally stored in.
        destFolder (_string_): The folder the file will be stored in.
    """
    try:
        origin = Path(origin_folder) / meme
        destination = Path(dest_folder) / meme
        origin.rename(destination)
    except Exception as e:
        print(e)




