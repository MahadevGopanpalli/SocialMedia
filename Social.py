
import facebook
import requests
import json

def FBMessage(token,message):
    v = facebook.GraphAPI(token)
    if v.put_object(parent_object='me', connection_name='feed',message=message):
        return True 
    return False 

def FBPhotoPost(token,message,img):
    v = facebook.GraphAPI(token)
    if v.put_photo(open(img,'rb'),message=message):
        return True 
    return False


def FBVideoPost(token,page_id,message,videopath):
    fburl = 'https://graph-video.facebook.com/v2.0/'+ str(page_id)+'/videos?access_token='+str(token)
    
    files = {'source': (videopath, open(videopath, 'rb'), 'video/mp4')}

    m = {'description': message,
      }
    if requests.post(fburl, data=m, files=files):
        return True 
    return False 


import tweepy 
from requests_oauthlib import OAuth1


def Tweet(consumer_key,consumer_secret,access_token,access_token_secret, MESSAGE):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 
    
    if api.update_status(status=MESSAGE):
        return True 
    return False

def TweetPhoto(consumer_key,consumer_secret,access_token,access_token_secret, PHOTOPATH,MESSAGE):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 
    
    if api.update_with_media(PHOTOPATH, MESSAGE)  :
        return True 
    return False   

from requests_oauthlib import OAuth1
import os
import sys
import time
def TweetVideo(consumer_key,consumer_secret,access_token,access_token_secret, video,MESSAGE):
    auth = OAuth1(consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

    total_bytes = os.path.getsize(video)
    request_data = {
      'command': 'INIT',
      'media_type': 'video/mp4',
      'total_bytes': total_bytes,
      'media_category': 'tweet_video'
    }


    req = requests.post('https://upload.twitter.com/1.1/media/upload.json', data=request_data, auth=auth)
    media_id = req.json()['media_id']

    print('Media ID: %s' % str(media_id))

    s = 0
    file = open(video, 'rb')
    bytes_sent=0
    while bytes_sent < total_bytes:
        chunk=file.read(4096)
        request_data = {
            'command': 'APPEND',
            'media_id': media_id,
            'segment_index': s
        }
        

        files = {
            'media':chunk
        }
        req = requests.post('https://upload.twitter.com/1.1/media/upload.json', data=request_data, files=files, auth=auth)

        s=s+1        
        print(req.status_code)
        print (req.text)
        bytes_sent = file.tell()

        print ('%s of %s bytes uploaded' % (str(bytes_sent), str(total_bytes)))
    print ("Done...")

    request_data = {
         'command': 'FINALIZE',
         'media_id': media_id
         }

    req = requests.post('https://upload.twitter.com/1.1/media/upload.json', data=request_data, auth=auth)
    print(req.json())
    processing_info = req.json().get('processing_info', None)
    if processing_info is None:
        print ("Not Processed")
        sys.exit(0)

    state = processing_info['state']

    print('Media processing status is %s ' % state)

    if state == u'succeeded':
        print ("Successfully Uploaded")
        sys.exit(0)

    if state == u'failed':
        sys.exit(0)

    check = processing_info['check_after_secs']
    
    print('Checking after %s seconds' % str(check))
    time.sleep(check)

    print('-------STATUS-------')

    request_params = {
      'command': 'STATUS',
      'media_id': media_id
    }

    req = requests.get('https://upload.twitter.com/1.1/media/upload.json', params=request_params, auth=auth)
    
    p = req.json().get('processing_info', None)

    print(p)

    request_data = {
      'status': MESSAGE,
      'media_ids': media_id
    }

    req = requests.post('https://api.twitter.com/1.1/statuses/update.json', data=request_data, auth=auth)
