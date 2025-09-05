import os
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient import discovery
from jsonMethods import write_to_json


root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
dotenv_path = os.path.join(root_folder, '.env')
load_dotenv(dotenv_path)

def upload_memes(memes):
    try:
        files_list = []
        files = [(x['files'][0]['url_private_download'], x['files'][0]['filetype'], x['files'][0]['id'], x['files'][0]['user']) for x in memes]
        print(f'all files: {files}')
        
        for x in files:
                file_name = "{creator}_{file_id}.{file_type}".format(creator=x[3], file_id=x[2], file_type=x[1])
                files_list.append(file_name)
                reqs = requests.get(x[0], stream=True, headers={'Authorization': f'Bearer {os.getenv('BOT_TOKEN')}'})
                if reqs.ok:
                    post_url = 'http://host.docker.internal:8000/post-candidate-meme'
                    content_type = reqs.headers.get('Content-Type', 'application/octet-stream')
                    files_data = {
                        'file': (file_name, reqs.raw, content_type)
                    }
                    response = requests.post(post_url, files=files_data)
                    print(f'Upload successful, status code: {reqs.status_code, response.status_code}')
                else:
                    print(f'Upload failed, status code: {reqs.status_code, response.status_code}')
        return files_list
    except Exception as e:
        print(f'An error occured: {e}.')


def create_form(memes):
    if memes:
        upload_memes(memes)
        urls = ['https://cdn.orbitntnu.com/43.jpg', 'https://cdn.orbitntnu.com/42.jpg', 'https://cdn.orbitntnu.com/41.jpg', 'https://cdn.orbitntnu.com/40.jpg']
        options = [{'value' : x, 
                    'image' : {
                        'sourceUri': x,
                        'altText': x
                        }} for x in urls]

        credentials = service_account.Credentials.from_service_account_file(
        os.getenv('SERVICE_ACCOUNT_FILE'), scopes=os.getenv('SCOPES').split(','))

        forms_service = discovery.build('forms', 'v1', credentials=credentials, discoveryServiceUrl=os.getenv('DISCOVERY_DOC'), static_discovery=False)

        form = {
            'info': {
                'title': 'Orbit Meme Review 🚀🌠'
            }
        }

        new_form = forms_service.forms().create(body=form).execute()
        form_id = new_form['formId']

        question = {
            'requests': [
                {
                    'createItem': {
                        'item': {
                            'title': ('Vote for the funniest meme!'),
                            'questionItem': {
                                'question': {
                                    'required': True,
                                    'choiceQuestion': {
                                        'type': 'RADIO',
                                        'options': options,
                                        'shuffle': False
                                    },
                                }
                            },
                        },
                        'location': {'index': 0},
                    }
                },

            ]
        }


        forms_service.forms().batchUpdate(formId=form_id, body=question).execute()
        form_url = f'https://docs.google.com/forms/d/{form_id}/viewform'
        write_to_json('last_formID', form_id, './lastExecution.json')

        return form_url
    else:
        print("No memes to create a form out of.")

