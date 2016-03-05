#!/bin/python

"""
A layer\interface to Microsoft Translator API
"""

import urllib
import urllib.request
import codecs
import json
from xml.dom import minidom
from os.path import exists as fexist
from pickle import dump as pdump, load as pload
from datetime import datetime, timedelta

api_url  = "http://api.microsofttranslator.com/V2/Http.svc/Translate" 
tok_url  = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
appid = '' 
clientid = ''
clientse = ''

def _unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode.
    Borrowed from pyfacebook :: http://github.com/sciyoshi/pyfacebook/
    """
    if isinstance(params, dict):
        params = params.items()
    enc =  urllib.parse.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])
    return enc

def _run_query(args):
    """
    takes arguments and optional language argument and runs query on server
    """
    data = _unicode_urlencode(args)
    sock = urllib.urlopen(api_url + '?' + data)
    result = sock.read()
    if result.startswith(codecs.BOM_UTF8):
        result = result.lstrip(codecs.BOM_UTF8).decode('utf-8')
    elif result.startswith(codecs.BOM_UTF16_LE):
        result = result.lstrip(codecs.BOM_UTF16_LE).decode('utf-16-le')
    elif result.startswith(codecs.BOM_UTF16_BE):
        result = result.lstrip(codecs.BOM_UTF16_BE).decode('utf-16-be')
    # return json.loads(result) -> Couldn't find how to request a JSON response
    xmldoc = minidom.parseString(result)
    string = xmldoc.getElementsByTagName("string")[0].firstChild.nodeValue.encode('utf-8')
    return string


def set_credentials(app_id,client_id,client_secret):
    global appid, clientid, clientse
    appid = app_id
    clientid = client_id
    clientse = client_secret

def get_access_token(path_to_tok='./translate.tok'):
    if fexist(path_to_tok):
        ftok = open(path_to_tok, 'rb+')
        tokdata = pload(ftok)
        expiretime = tokdata['expires_in'] 
        if (datetime.now() - expiretime) > timedelta(10,0):
            return tokdata['token']
    else:
        ftok = open(path_to_tok, 'w')
    args = {'client_id':clientid,'client_secret':clientse,'scope':'http://api.microsofttranslator.com/','grant_type':'client_credentials'}
    enc_args = urllib.parse.urlencode(args)
    req = urllib.Request(tok_url,enc_args)
    response = urllib.urlopen(req)
    data = json.load(response)
    timeandten = datetime.now() + timedelta(minutes = 10)
    pdump({'token':data['access_token'],'expires_in':timeandten}, ftok)
    return data['access_token']

def translate(text, source, target, html=False):
    """
    action=opensearch
    """
    if not appid:
        raise ValueError("AppId needs to be set by set_appid")
    tok = 'Bearer %s' % get_access_token()
    query_args = {
        'appId': tok, # appid,
        'text': text,
        'from': source,
        'to': target,
        'contentType': 'text/plain' if not html else 'text/html',
        'category': 'general',
        'Authorization': tok
    }
    return _run_query(query_args)
