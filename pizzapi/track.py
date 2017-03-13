from urls import TRACK_BY_PHONE, TRACK_BY_ORDER
from utils import request_xml, request_json


def track_by_phone(phone):
    phone = str(phone).strip()
    data = request_xml(TRACK_BY_PHONE, phone=phone)['soap:Envelope']['soap:Body']
    response = data['GetTrackerDataResponse']['OrderStatuses']['OrderStatus']
    return response


def track_by_order(store_id, order_key):
    return request_json(TRACK_BY_ORDER, store_id=store_id, order_key=order_key)
