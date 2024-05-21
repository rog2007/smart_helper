import requests

IAM_TOKEN = 't1.9euelZqekpebic-amImLjpmVycyZl-3rnpWak46SzJKOlM2Yl5CYxpTHjo_l8_dlJzFO-e9_cB5-_t3z9yVWLk75739wHn7-zef1656VmomVzc6YzoqYjZiRkcmUnY6b7_zF656VmomVzc6YzoqYjZiRkcmUnY6b.aVagASw3CaFrBIxseMA0GL2YHROHgV-iXXUu-97fTAo_T329N6SzyqQLq2tnj2uU1b-fRtOJ1TD3DvGstJGmBg'
folder_id = 'b1gv0sm3kfenkogmonrc'
target_language = 'ru'
texts = ["Hello", "World"]

body = {
    "targetLanguageCode": target_language,
    "texts": texts,
    "folderId": folder_id,
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {0}".format(IAM_TOKEN)
}

response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
    json = body,
    headers = headers
)

print(response.text)
