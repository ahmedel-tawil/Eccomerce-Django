import json

import requests
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Sum


#
# def get_ip():
#     response = requests.get('https://api64.ipify.org?format=json').json()
#     return response["ip"]
#
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_currency_code():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return 'AED'


def get_location(request):
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "currency": response.get("currency"),
        "currency_name": response.get("currency_name"),
    }
    return {}
    # return location_data


def location_IP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = request.META.get('REMOTE_ADDR')
    else:
        ip = request.META.get('REMOTE_ADDR')
    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""
    # if request.user_agent.is_mobile:
    #     device_type = "Mobile"
    # if request.user_agent.is_tablet:
    #     device_type = "Tablet"
    # if request.user_agent.is_pc:
    #     device_type = "PC"
    #
    # browser_type = request.user_agent.browser.family
    # browser_version = request.user_agent.browser.version_string
    # os_type = request.user_agent.os.family
    # os_version = request.user_agent.os.version_string
    g = GeoIP2()
    # location = g.city(ip)
    location = g.city('2.50.37.142')
    location_country = location["country_name"]
    location_city = location["city"]

    context = {
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type": os_type,
        "os_version": os_version,
        "location_country": location_country,
        "location_city": location_city
    }
    return context
