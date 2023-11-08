import requests
import schedule
import time
from datetime import datetime
from llama_index import Document, GPTVectorStoreIndex  

# Configuration for Facebook
PAGE_ID = '106180925472561'  # Replace with your page's ID
ACCESS_TOKEN = 'EAAI8xeOsCMoBO4mCkwBZAxjogkZBaGa5ZCiLuC2hqbzeE4AvBR1fZB7kjTL5zfAiRPdlIL8lmjAwd2xHIHEKY2hkEYqR6pZBZA6wUKqud440nxSS08AF4fKdykqLh85cg3dAMC7xK53XjEGRHEZAhtRgzVQRfdTQByZB7rLDVeVJE3rgVH7RhRjZBvBA81OXmXG6Qd2l09QHjvfVGNGAZD'  # Replace with your long-lived page access token
BASE_URL = f'https://graph.facebook.com/v12.0/{106180925472561}/posts'

LAST_TIMESTAMP = None

def get_facebook_posts():
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'message,created_time,id,attachments',
        'limit': 100
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []
    
index = None  # Declare index here to ensure it's in the global scope

def job():
    global LAST_TIMESTAMP
    global index  # Refer to the index declared outside of the function
    posts = get_facebook_posts()
    documents = []  # This will store Document objects

    for post in posts:
        created_time_str = post.get("created_time", "")
        created_time = datetime.strptime(created_time_str, '%Y-%m-%dT%H:%M:%S+0000')

        if LAST_TIMESTAMP is None or created_time > LAST_TIMESTAMP:
            post_id = post["id"]
            post_message = post.get("message", "").strip()

            # Create a Document object for each post
            # Assuming the Document class requires keyword arguments for initialization
            document = Document(text=post_message, doc_id=post_id, extra_info={'date': created_time})
            documents.append(document)

        # Initialize the index if it's the first run
        if index is None and documents:
            index = GPTVectorStoreIndex(documents)
        else:
            # Update the existing index with the new documents
            for document in documents:
                index.add_document(document)
                
        # Update LAST_TIMESTAMP with the timestamp of the latest post processed
        if posts:
            latest_time_str = posts[0].get("created_time", "")
            LAST_TIMESTAMP = datetime.strptime(latest_time_str, '%Y-%m-%dT%H:%M:%S+0000')
                        
    if __name__ == '__main__':
        job()
        schedule.every(1).minutes.do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)