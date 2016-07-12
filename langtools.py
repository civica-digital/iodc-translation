import os
import requests
import urllib
import json
from xml.etree import ElementTree
from langdetect import detect
import pickle

MS_ID = os.environ["ms_id"]
MS_SECRET = os.environ["ms_secret"]

KEYWORDS =  pickle.load( open("data/expression_translations.pickle","rb"))
LANGUAGES =  pickle.load( open("data/expression_translations.pickle","rb"))
COUNTRIES = pickle.load( open("data/country_list.pickle","rb"))


def GetTextAndTranslate(textToTranslate, to, original="en"):

    token = GetToken(MS_ID, MS_SECRET)

    #Call to Microsoft Translator Service
    headers = {"Authorization": token}
    translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to={}&from={}".format(textToTranslate, to, original)

    try:
        translationData = requests.get(translateUrl, headers = headers) #make request
        translation = ElementTree.fromstring(translationData.text.encode('utf-8')) # parse xml return values
    except OSError:
        pass

    return(translation.text)


def GetToken(client_id, client_secret): #Get the access token from ADM, token is good for 10 minutes
    urlArgs = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'http://api.microsofttranslator.com',
        'grant_type': 'client_credentials'
    }

    oauthUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'

    try:
        oauthToken = json.loads(requests.post(oauthUrl, data = urllib.parse.urlencode(urlArgs)).content.decode("utf-8")) #make call to get ADM token and parse json
        finalToken = "Bearer " + oauthToken['access_token'] #prepare the token
    except OSError:
        pass

    return finalToken
#End GetToken

def DetectLanguage(text):
    fromLang = detect(text)
    return fromLang
