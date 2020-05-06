import json
import os
import subprocess
from urllib.parse import urlparse

import requests

DEFAULT_LIGHTHOUSE_ARGS = " ".join([
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-breakpad',
    '--disable-browser-side-navigation',
    '--disable-client-side-phishing-detection',
    '--disable-default-apps',
    '--disable-dev-shm-usage',
    '--disable-extensions',
    '--disable-features=site-per-process',
    '--disable-hang-monitor',
    '--disable-popup-blocking',
    '--disable-prompt-on-repost',
    '--disable-sync',
    '--disable-translate',
    '--metrics-recording-only',
    '--no-first-run',
    '--safebrowsing-disable-auto-update',
    '--enable-automation',
    '--password-store=basic',
    '--use-mock-keychain',
    '--headless',
    '--hide-scrollbars',
    '--mute-audio',
])


class Report:
    def __init__(self, url, desktop=True):
        self._url = url
        self.reports_folder_path = f'/home/chrome/reports/${urlparse(url).netloc}'
        self.lighthouse_file_path = f'${self.reports_folder_path}/lighthouse.json'
        self._device = 'desktop' if desktop else 'mobile'
        self.browser = None

    def __enter__(self):
        self._create_file()
        self._call_lighthouse()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._delete_report_file()

    def _build_pagespeed_query(self):
        try:
            key = os.environ['PAGESPEED_KEY']
        except KeyError:
            raise KeyError('You need to set the environment variable PAGESPEED_KEY')

        query_params = {
            'url': self._url,
            'strategy': self._device,
            'locale': 'pt_BR',
            'key': key
        }
        return 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed', query_params

    def _create_file(self):
        if not os.path.exists(self.reports_folder_path):
            os.makedirs(self.reports_folder_path)
        # delete file if exists
        self._delete_report_file()
        os.mknod(self.lighthouse_file_path)

    def _delete_report_file(self):
        if os.path.exists(self.lighthouse_file_path):
            os.remove(self.lighthouse_file_path)

    def _call_lighthouse(self):
        try:
            command = [
                'lighthouse',
                self._url,
                '--quiet',
                f'--chrome-flags="${DEFAULT_LIGHTHOUSE_ARGS}"',
                '--preset=full',
                f'--emulated-form-factor=${self._device}',
                '--output=json',
                f'--output-path=${self.lighthouse_file_path}',
            ]
            subprocess.check_call(' '.join(command), shell=True)
        except subprocess.CalledProcessError as exc:
            msg = f'''
                Command "${exc.cmd}"
                returned an error code: ${exc.returncode},
                output: ${exc.output}
                '''
            raise RuntimeError(msg)

    def lighthouse_results(self):
        with open(self.lighthouse_file_path, 'r') as f:
            return json.load(f)

    def pagespeed_results(self):
        url, params = self._build_pagespeed_query()
        req = requests.get(url, params)
        req.raise_for_status()
        return req.json()

    def generate_report(self):
        pass


if __name__ == '__main__':
    with Report('http://www.example.com') as lh:
        print(lh.read_report_file())
