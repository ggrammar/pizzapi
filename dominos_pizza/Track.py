from utils import request_xml, request_json
import requests
import xmltodict

TRACK_BY_ID = ('https://trkweb.dominos.com/orderstorage/GetTrackerData?'
               'StoreID={storeId}&OrderKey={orderKey}')
TRACK_BY_PHONE = ('https://trkweb.dominos.com/orderstorage/GetTrackerData?'
                  'Phone={phone}')

def track_by_phone(phone):
    data = request_xml(TRACK_BY_PHONE, phone=str(phone).strip())
    response = data['soap:Envelope']['soap:Body']['GetTrackerDataResponse']
    return response['OrderStatuses']['OrderStatus']

def track_by_id(store_id, order_key):
    return request_json(TRACK_BY_ID, storeID=store_id, orderKey=order_key)
