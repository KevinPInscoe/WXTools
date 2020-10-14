__author__ = "Kevin P. Inscoe"
__copyright__ = "CC BY-SA 2.5"
__credits__ = ["Kevin P. Inscoe"]
__license__ = "Attribution-ShareAlike Generic"
__version__ = "2.5"
__maintainer__ = "https://kevininscoe.com"
__email__ = "kevin.inscoe@gmail.com"

# Grabs the National Weather Service (NWS) daily
# product "Hazardous Weather Outlook", culls out
# the Spotter Information Statement text from
# the page and displays it. This can be used to
# produce output specific to a daily Skywarn storm
# spotter notification or an email report.
#
# Nod to https://medium.com/@ageitgey/quick-tip-the-easiest-way-to-grab-data-out-of-a-web-page-in-python-7153cecfca58
# for the inspiration to convert from a bash script
# I had been using for sometime to a Python script
#
# To find your WFO - see https://en.wikipedia.org/wiki/List_of_National_Weather_Service_Weather_Forecast_Offices
#
# You will need to know your WFO's warning zone area as well see
#
# https://en.wikipedia.org/wiki/Forecast_region#United_States or
#
# https://www.weather.gov/gis/PublicZones
#

import sys
import os
import requests
from bs4 import BeautifulSoup


def get_wfo():

    wfo_zone = os.environ['NWS_WFO_WZONE']

    return wfo_zone


def get_hwo_page(url):

    p = requests.get(url)
    html = p.content
    soup = BeautifulSoup(html, 'html.parser')
    page_text = soup.find_all(text=True)

    return page_text


def get_spotter_info_stmt(rendered, wfo, warnzone):

    # First grab the warning zone block which ends with a blank line.
    # Then within the zone block look for line containing
    # "SPOTTER INFORMATION STATEMENT" and keep reading until "$$"

    begin = "SPOTTER INFORMATION STATEMENT"
    end = "$$"
    stmt = '\n' + wfo + '-' + warnzone + ': '
    wz = False
    t = False
    lines = rendered.split("\n")
    for line in lines:
        if warnzone in line:
            wz = True
        if wz:
            if begin in line:
                t = True
        if end in line:
            wz = False
            t = False
        if t:
            if begin not in line:
                # Ignore blank lines in text
                if line.strip():
                    stmt = stmt + line

    return stmt


def get_statement(url, wfo, warnzone):

    rendered = ''
    text = get_hwo_page(url)

    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            rendered += '{} '.format(t)

    stmt = get_spotter_info_stmt(rendered, wfo, warnzone)

    return stmt


def main():

    wfo_zone = get_wfo()
    wfox, warnzonex = wfo_zone.split(":")
    wfo = wfox.upper()
    warnzone = warnzonex.upper()

    if wfo == '':
        print("Unable to obtain weather forecast office.")
        print("Make sure you have NWS_WFO_WZONE environment variable set")
        sys.exit(1)

    url = 'https://forecast.weather.gov/product.php?site=NWS&issuedby=' + \
        wfo + \
        '&product=HWO&format=txt&version=1&glossary=0'

    print("\nFor full HWO bulletin for WFO %s click on %s" % (wfo, url))

    stmt = get_statement(url, wfo, warnzone)

    print(stmt)


if __name__ == '__main__':

    main()
