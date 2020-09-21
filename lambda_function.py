import base64
import json
import logging
import re
import requests

from urllib.parse import parse_qs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_config():
    with open("config.json") as f:
        return json.loads(f.read())


def decode_base64(content):
    return base64.urlsafe_b64decode(bytearray(content, "utf-8")).decode("utf-8")


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    config = get_config()
    if not event.get("isBase64Encoded", False):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "unknown request body"}),
        }

    body = event["body"]
    parsed_body = parse_qs(decode_base64(body))
    logger.info(f"Weibo content: {parsed_body}")
    if config["token"] != parsed_body.get("token", [None])[0]:
        return {
            "statusCode": 401,
        }

    if "image" in parsed_body:
        # tweet with image
        url = config["image_text_endpoint"]
        r = requests.post(
            url,
            data={"value1": parsed_body["text"][0], "value2": parsed_body["image"][0]},
        )
        if r.status_code != 200:
            logger.warn(f"Calling {url} seems abnormal")
    else:
        # tweet text only
        text_content = parsed_body["text"][0]
        if re.search(r"(Repost)|(转发微博)|(\/\/\@)|(轉發微博)", text_content) is None:
            url = config["only_text_endpoint"]
            r = requests.post(
                url,
                data={
                    "value1": parsed_body["text"][0],
                },
            )
            if r.status_code != 200:
                logger.warn(f"Calling {url} seems abnormal")
    return {"statusCode": 200, "body": json.dumps("Success")}
