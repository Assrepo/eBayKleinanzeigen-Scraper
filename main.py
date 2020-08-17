from EbayScraper import EbayScraper
from gmail_util import send_email
from string import Template
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import config

VERSION = "1.0.3 (RELEASE)"


def send_offers():
    """
    Called by main thread.
    Looks for new items and send them to the client via email
    :return: None
    """
    for job in config.JOBS:
        scraper = EbayScraper(config.LOCATION, job)
        data = scraper.get_items()
        if data:
            html_template = Template(open('html_template.txt').read())
            item_template = Template(open('item_template.txt').read())
            html_content = {'items': ''}
            for item in data:
                html_content['items'] += item_template.substitute(item)
            if job['Mode'] == 'Everything':
                subject = 'Found {} new offers in the category {}!'.format(len(data), job['Category'])
            else:
                subject = 'Found {} new offers for "{}"!'.format(len(data), job['Search_for'])
            send_email(subject, html_template.substitute(html_content), config.YOUR_EMAIL)
            print("[+] " + time.strftime("%H:%M") + " - " + subject)
        else:
            print("[-] " + time.strftime("%H:%M") + " - No new offers found..")


if __name__ == "__main__":

    print("Running EbayKleinanzeigenScraper version {} by Varsius".format(VERSION))

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_offers, 'interval', hours=config.INTERVAL)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # Execute immediately, further executions are handled by the scheduler
    send_offers()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        print("Exiting...")
        scheduler.shutdown()
