import requests
import schedule
import time
from datetime import datetime
from llama_index import Document 

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
    global LAST_TIMESTAMP, index  # Ensure you're using the global index
    if index is None:
        index = set()  # Initialize the set if it's the first run

    documents = []  # This will store new Document objects
    posts = get_facebook_posts()

    for post in posts:
        post_id = post["id"]
        # Skip the post if it's already been processed
        if post_id in index:
            continue

        created_time_str = post.get("created_time", "")
        created_time = datetime.strptime(created_time_str, '%Y-%m-%dT%H:%M:%S+0000')

        if LAST_TIMESTAMP is None or created_time > LAST_TIMESTAMP:
            post_message = post.get("message", "").strip()
            created_time_iso = created_time.isoformat()
            document = Document(text=post_message, doc_id=post_id, extra_info={'date': created_time_iso})
            documents.append(document)
            index.add(post_id)  # Add the ID to the set of processed documents

    # Update LAST_TIMESTAMP with the timestamp of the latest post processed
    if documents:
        LAST_TIMESTAMP = documents[0].extra_info['date']

    # Print each new post in a beautified output
    for doc in documents:
        print(f"Document ID: {doc.doc_id}")
        print(f"Date: {doc.extra_info['date']}")
        print("Text:")
        print(doc.text)
        print("\n" + "="*80 + "\n")  # Separator for readability

                        
    if __name__ == '__main__':
        job()
        schedule.every(1).minutes.do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)