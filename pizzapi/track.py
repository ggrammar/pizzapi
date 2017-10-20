from .urls import Urls, COUNTRY_USA
from .utils import request_xml, request_json


def track_by_phone(phone, country=COUNTRY_USA):
    phone = str(phone).strip()
    data = request_xml(Urls(country).track_by_phone(), phone=phone)['soap:Envelope']['soap:Body']
    response = data['GetTrackerDataResponse']['OrderStatuses']['OrderStatus']
    return response


def track_by_order(store_id, order_key, country=COUNTRY_USA):
    return request_json(Urls(country).track_by_order(), store_id=store_id, order_key=order_key)
