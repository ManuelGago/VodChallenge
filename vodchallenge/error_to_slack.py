import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SLACK_CHANNEL = '#general'
HOOK_URL = 'https://hooks.slack.com/services/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'
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    #alarm_name = message['AlarmName']
    #old_state = message['OldStateValue']
    #new_state = message['NewStateValue']
    #reason = message['NewStateReason']

    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': "New error message: %s" % (str(message))
    }

    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

