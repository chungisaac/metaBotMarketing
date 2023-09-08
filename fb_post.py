import os
import requests

from constants import FB_PAGE_ID
from llm import ClarifaiPrompter
from upload import ClarifaiUploader

page_access_token = os.environ.get("PAGE_ACCESS_TOKEN")

def clean_llm_output(raw_text: str) -> str:
    try:
        cleaned = raw_text.split('\"')
        if len(cleaned) <= 1:
            cleaned = raw_text.lstrip("\n\n")
        else:
            cleaned = cleaned[1]
        cleaned = cleaned.replace("Sure! Here's a possible Facebook post:\n\n","")
        cleaned = cleaned.replace("Example Facebook Post:\n\n","")
        cleaned = cleaned.replace(" Clarifai's"," @clarifai's")
        cleaned = cleaned.replace(" Clarifai "," @clarifai ")
        cleaned = cleaned.replace("#Clarifai's","@clarifai's")
        cleaned = cleaned.replace("#Clarifai", "@clarifai")
        cleaned = cleaned.replace(">","").replace("<","")
    except:
        raise Exception("Raw output: %s, cleaned:%s" % (raw_text, str(cleaned)))
    return cleaned


def build_fb_post_url(post_id:str) -> str:
    return "https://www.facebook.com/%s" %(post_id)


def main():
    prompter = ClarifaiPrompter()

    while True:
        output = prompter.predict()
        post_msg = clean_llm_output(output)
        if "https" in post_msg:
            break

    post_url = 'https://graph.facebook.com/{}/feed'.format(FB_PAGE_ID)
    payload = {
        'message': post_msg,
        'access_token': page_access_token
    }

    r = requests.post(post_url, data=payload)
    post_id = r.json()['id']
    
    post_url = build_fb_post_url(post_id)    
    print(post_url)
    ClarifaiUploader().upload(post_url)


if __name__ == "__main__":
    main()