import argparse
import json
import re
from datetime import datetime

from rich import print

from utils import searcher, mapper, vendorcheck


def banner():
    print("""
   ██████╗ ███████╗ ██████╗   ██╗    ██╗     ███████╗ 
  ██╔════╝ ██╔════╝██╔═══██╗  ██║    ██║ ██╗ ██╔════╝ ██╗
  ██║  ███╗█████╗  ██║   ██║  ██║ █╗ ██║ ██║ █████╗   ██║
  ██║   ██║██╔══╝  ██║   ██║  ██║███╗██║ ██║ ██╔══╝   ██║
  ╚██████╔╝███████╗╚██████╔╝  ╚███╔███╔╝ ██║ ██║      ██║
   ╚═════╝ ╚══════╝ ╚═════╝    ╚══╝╚══╝  ╚═╝ ╚═╝      ╚═╝ :globe_showing_americas: [bold purple italic]by GOΠZO[/bold purple italic]                          
""")


banner()

parser = argparse.ArgumentParser(description='GeoWiFi, search WiFi geolocation data by BSSID and SSID')
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-s', '--ssid', type=str, help='Search by SSID')
group.add_argument('-b', '--bssid', type=str, help='Search by BSSID')
parser.add_argument('-j', '--json', action='store_true', help='Json output')
parser.add_argument('-m', '--map', action='store_true', help='Map output')

args = parser.parse_args()

bssid_json = {'data': {
    'bssid': '',
    'vendor': '',
    'mac_type': '',
    'wigle': {
        'lat': '',
        'lon': ''
    },
    'apple': {
        'lat': '',
        'lon': ''
    },
    'openwifi': {
        'lat': '',
        'lon': ''
    },
    'milnikov': {
        'lat': '',
        'lon': ''
    }
}}


def check_valid_bbsi(bssid):
    macregex = '^[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}$'
    return bool(re.match(macregex, bssid))


def search_bssid(bssid):
    global bssid_json
    bssid_json['data']['bssid'] = bssid
    try:
        if 'no result' in vendorcheck.mac(bssid).text:
            bssid_json['data']['vendor'] = 'not_found'
            bssid_json['data']['mac_type'] = 'not_found'
        else:
            bssid_json['data']['vendor'] = vendorcheck.mac(bssid).json()['result']['company']
            bssid_json['data']['mac_type'] = vendorcheck.mac(bssid).json()['result']['type']
    except:
        print('[bold][red] [!][/red] Error obtaining vendor data[/bold]')
        bssid_json['data']['vendor'] = 'not_found'
        bssid_json['data']['mac_type'] = 'not_found'

    try:
        if r := searcher.milnikov_bssid(bssid):
            bssid_json['data']['milnikov']['lat'] = r['lat']
            bssid_json['data']['milnikov']['lon'] = r['lon']

        else:
            bssid_json['data']['milnikov']['lat'] = 'not_found'
            bssid_json['data']['milnikov']['lon'] = 'not_found'
    except:
        print('[bold][red] [!][/red] Error obtaining Milnikov data[/bold]')
        bssid_json['data']['milnikov']['lat'] = 'not_found'
        bssid_json['data']['milnikov']['lon'] = 'not_found'

    try:
        if r := searcher.apple_bssid(bssid):
            bssid_json['data']['apple']['lat'] = r['lat']
            bssid_json['data']['apple']['lon'] = r['lon']
        else:
            bssid_json['data']['apple']['lat'] = 'not_found'
            bssid_json['data']['apple']['lon'] = 'not_found'
    except:
        print('[bold][red] [!][/red] Error obtaining Apple data[/bold]')
        bssid_json['data']['apple']['lat'] = 'not_found'
        bssid_json['data']['apple']['lon'] = 'not_found'

    try:
        if r := searcher.openwifi_bssid(bssid):
            bssid_json['data']['openwifi']['lat'] = r['lat']
            bssid_json['data']['openwifi']['lon'] = r['lon']
        else:
            bssid_json['data']['openwifi']['lat'] = 'not_found'
            bssid_json['data']['openwifi']['lon'] = 'not_found'
    except:
        print('[bold][red] [!][/red] Error obtaining OpenWifi data[/bold]')
        bssid_json['data']['openwifi']['lat'] = 'not_found'
        bssid_json['data']['openwifi']['lon'] = 'not_found'

    try:
        if r := searcher.wigle_bssid(bssid):
            bssid_json['data']['wigle']['lat'] = r['lat']
            bssid_json['data']['wigle']['lon'] = r['lon']
        else:
            bssid_json['data']['wigle']['lat'] = 'not_found'
            bssid_json['data']['wigle']['lon'] = 'not_found'
    except:
        print('[bold][red] [!][/red] Error obtaining Wigle data[/bold]')
        bssid_json['data']['wigle']['lat'] = 'not_found'
        bssid_json['data']['wigle']['lon'] = 'not_found'

    return bssid_json


def terminal_output_bssid(bssid_data):
    print(' [bold]-------------------------- MAC DATA --------------------------[/bold]')
    print(
        f" [bold][-] BSSID: [/bold][italic]{bssid_data['data']['bssid']}[/italic]"
    )

    print(
        f" [bold][-] Vendor: [/bold][italic]{bssid_data['data']['vendor']}[/italic]"
    )

    print(
        f" [bold][-] MAC type: [/bold][italic]{bssid_data['data']['mac_type']}[/italic]"
    )

    print(' [bold]----------------------- LOCATION DATA ------------------------[/bold]')
    if bssid_data['data']['wigle']['lat'] != 'not_found':
        print(
            f" [bold][:pushpin:] Wigle results: [/bold][italic]{str(bssid_data['data']['wigle']['lat'])}, {str(bssid_data['data']['wigle']['lon'])}[/italic]"
        )

    else:
        print(' [bold][:pushpin:] Wigle results: [/bold]not_found')
    if bssid_data['data']['apple']['lat'] != 'not_found':
        print(
            f" [bold][:pushpin:] Apple results: [/bold][italic]{str(bssid_data['data']['apple']['lat'])}, {str(bssid_data['data']['apple']['lon'])}[/italic]"
        )

    else:
        print(' [bold][:pushpin:] Apple results: [/bold]not_found')
    if bssid_data['data']['openwifi']['lat'] != 'not_found':
        print(
            f" [bold][:pushpin:] OpenWiFi results: [/bold][italic]{str(bssid_data['data']['openwifi']['lat'])}, {str(bssid_data['data']['openwifi']['lon'])}[/italic]"
        )

    else:
        print(' [bold][:pushpin:] OpenWiFi results: [/bold]not_found')
    if bssid_data['data']['milnikov']['lat'] != 'not_found':
        print(
            f" [bold][:pushpin:] Milnikov results: [/bold][italic]{str(bssid_data['data']['milnikov']['lat'])}, {str(bssid_data['data']['milnikov']['lon'])}[/italic]"
        )

    else:
        print(' [bold][:pushpin:] Milnikov results: [/bold]not_found')


def terminal_output_ssid(ssid_data):
    print(' [bold]-------------------------- KEYWORD SEARCH --------------------------[/bold]')
    print(f' [bold][-] Keyword: [/bold][italic]{args.ssid}[/italic]')
    print(' [bold]-------------------------- RESULTS --------------------------[/bold]')
    for result in ssid_data['results']:
        print(f" [bold][-] Address: [/bold][italic]{result['address']}[/italic]")
        print(f" [bold][-] Lat: [/bold][italic]{result['lat']}[/italic]")
        print(f" [bold][-] Long: [/bold][italic]{result['lon']}[/italic]")
        print(' [bold]-------------------------------------------------------------[/bold]')


def json_output(json_data):
    try:
        filename = (
            f'results/{str(datetime.timestamp(datetime.now()))}'.replace(
                '.', '_'
            )
            + '.json'
        )

        with open(filename, 'w') as file:
            json.dump(json_data, file)
        file.close()
        print(
            ' [bold white][:floppy_disk:] Json output saved:[/bold white] [italic bright_green]{0}[/italic bright_green]'.format(
                filename))
    except:
        print(' [bold red][:red_circle:] Error saving output[/bold red]')


def map_bssid_output(json_data):
    mapper.create_map()
    if json_data['data']['wigle']['lat'] != 'not_found':
        mapper.add_marker(json_data['data']['wigle']['lat'], json_data['data']['wigle']['lon'],
                          json_data['data']['bssid'])
    if json_data['data']['apple']['lat'] != 'not_found':
        mapper.add_marker(json_data['data']['apple']['lat'], json_data['data']['apple']['lon'],
                          json_data['data']['bssid'])
    if json_data['data']['openwifi']['lat'] != 'not_found':
        mapper.add_marker(json_data['data']['openwifi']['lat'], json_data['data']['openwifi']['lon'],
                          json_data['data']['bssid'])
    if json_data['data']['milnikov']['lat'] != 'not_found':
        mapper.add_marker(json_data['data']['milnikov']['lat'], json_data['data']['milnikov']['lon'],
                          json_data['data']['bssid'])
    filename = (
        f'results/{str(datetime.timestamp(datetime.now()))}'.replace('.', '_')
        + '.html'
    )

    try:
        mapper.save_map(filename)
        print(
            ' [bold white][:world_map: ] Map output saved:[/bold white] [italic bright_green]{0}[/italic bright_green]'.format(
                filename))
    except:
        print(' [bold red][:red_circle:] Error saving output[/bold red]')
        print('')


def map_ssid_output(json_data):
    mapper.create_map()
    for result in json_data['results']:
        mapper.add_marker(result['lat'], result['lon'], args.ssid)
    filename = (
        f'results/{str(datetime.timestamp(datetime.now()))}'.replace('.', '_')
        + '.html'
    )

    try:
        mapper.save_map(filename)
        print(
            ' [bold white][:world_map: ] Map output saved:[/bold white] [italic bright_green]{0}[/italic bright_green]'.format(
                filename))
    except:
        print(' [bold red][:red_circle:] Error saving output[/bold red]')
        print('')


if args.bssid:
    if check_valid_bbsi(args.bssid):
        bssid_data = search_bssid(args.bssid)
        terminal_output_bssid(bssid_data)
        if args.json:
            json_output(bssid_data)
        if args.map:
            map_bssid_output(bssid_data)

    else:
        print(' [bold red][:red_circle:] Invalid BSSID[/bold red]')
        print('')

if args.ssid:
    try:
        ssid_data = searcher.wigle_ssid(args.ssid)
        terminal_output_ssid(ssid_data)
        if args.json:
            json_output(ssid_data)
        if args.map:
            map_ssid_output(ssid_data)
    except:
        print('[bold][red] [!][/red] Error obtaining Wigle data[/bold]')
print('')
