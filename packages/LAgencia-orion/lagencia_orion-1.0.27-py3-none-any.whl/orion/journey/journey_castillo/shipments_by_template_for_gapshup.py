import json

import requests
from loguru import logger

from orion.journey.journey_castillo.models import RequestToSendNotifications


def sends_nuevos_ingresos(record: RequestToSendNotifications):
    url = "https://arrcastilloback.bonett.chat/gupshup-send-templates"

    headers = {"Content-Type": "application/json"}

    if record.add_data:
        print(f"{record=}")
        print([record.add_data.customer_name, record.token])
        print(record.add_data.customer_phone)
        if record.add_data.customer_name and record.add_data.customer_phone and record.token:
            payload_customer = {
                "app": "arrcastillo",
                "securekey": "sk_e6de090b1f89457698ff81a01b7b9e9e",
                "template": [{"id": "425811df-40ea-4167-beb6-f084e10ede49", "params": [record.add_data.customer_name, record.token]}],
                "localid": "suscription",
                "IntegratorUser": "0",
                "message": [],
                "number": record.add_data.customer_phone,
            }


            response_customer = requests.post(url=url, headers=headers, json=payload_customer)
            print(response_customer.text)
            response_customer.raise_for_status()
            logger.info("Notificacion enviada al cliente")


        if record.add_data.adviser_name and record.add_data.adviser_phone and record.token:
            payload_adviser = {
                "app": "arrcastillo",
                "securekey": "sk_e6de090b1f89457698ff81a01b7b9e9e",
                "template": [{"id": "4ee5b7ae-6793-4a0d-ac64-9c38b7038cf6", "params": [record.add_data.adviser_name, record.add_data.customer_name, record.add_data.customer_phone, record.token]}],
                "localid": "suscription_asesor",
                "IntegratorUser": "0",
                "message": [],
                "number": record.add_data.adviser_phone,
            }

            response = requests.post(url=url, headers=headers, json=payload_adviser)
            response.raise_for_status()
            logger.info("Notificacion enviada al asesor")
        return True if response_customer.ok else False

    logger.info("No se enviaron notificaciones nuevos ingresos castillo")

    print(response.text)



def art1():
    url = "https://api.gupshup.io/wa/api/v1/template/msg"

    payload = 'channel=whatsapp&source=573175865413&destination=%7B%7Bdestination_phone_number%7D%7D&src.name=arrcastillo&template=%7B%22id%22%3A%2226e2a78e-89ff-429b-ae40-96ec14ac4337%22%2C%22params%22%3A%5B%5D%7D&message=%7B%22image%22%3A%7B%22link%22%3A%22https%3A%2F%2Ffss.gupshup.io%2F0%2Fpublic%2F0%2F0%2Fgupshup%2F573175865413%2Fda27201d-5314-470a-afae-12ebc1e04772%2F1760104970564_busq_inm_cast.jpg%22%7D%2C%22type%22%3A%22image%22%7D'
    headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'apikey': 'uyq2hoyskt96dfz0khlcmdzse7hae6pu',
    'cache-control': 'no-cache'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def art2():
    url = "https://api.gupshup.io/wa/api/v1/template/msg"

    payload = 'channel=whatsapp&source=573175865413&destination=%7B%7Bdestination_phone_number%7D%7D&src.name=arrcastillo&template=%7B%22id%22%3A%22c93b09bc-185c-46eb-8e62-d396f36f61cb%22%2C%22params%22%3A%5B%5D%7D&message=%7B%22image%22%3A%7B%22link%22%3A%22https%3A%2F%2Ffss.gupshup.io%2F0%2Fpublic%2F0%2F0%2Fgupshup%2F573175865413%2F4564c8a1-c74d-48c6-958d-e37bd842b747%2F1760104553083_est_lib_cast.jpg%22%7D%2C%22type%22%3A%22image%22%7D'
    headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'apikey': 'uyq2hoyskt96dfz0khlcmdzse7hae6pu',
    'cache-control': 'no-cache'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def art3():
    url = "https://api.gupshup.io/wa/api/v1/template/msg"

    payload = 'channel=whatsapp&source=573175865413&destination=%7B%7Bdestination_phone_number%7D%7D&src.name=arrcastillo&template=%7B%22id%22%3A%227d5af6c1-0210-4ea1-a3cb-0d6d9d9d2c44%22%2C%22params%22%3A%5B%5D%7D&message=%7B%22image%22%3A%7B%22link%22%3A%22https%3A%2F%2Ffss.gupshup.io%2F0%2Fpublic%2F0%2F0%2Fgupshup%2F573175865413%2F0aa6987c-c0be-49ed-b17a-c1903c4ebbb3%2F1760104754563_import_cont_cast.jpg%22%7D%2C%22type%22%3A%22image%22%7D'
    headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'apikey': 'uyq2hoyskt96dfz0khlcmdzse7hae6pu',
    'cache-control': 'no-cache'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response
