import asyncio
import json
import os
import subprocess
import tempfile


class LightHouse:
    def __init__(self, url, desktop=True):
        self._url = url
        self._device = 'desktop' if desktop else 'mobile'
        self._file_descriptor, self._file_name = tempfile.mkstemp(suffix='.json')
        self.browser = None

    def __enter__(self):
        self.async_loop = asyncio.get_event_loop()
        self._call_lighthouse()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self._file_name)
        self.async_loop.close()

    def _call_lighthouse(self):
        try:
            command = [
                'lighthouse',
                self._url,
                '--quiet',
                # TODO: Add all chrome flags from pyppeteer
                '--chrome-flags="--headless"',
                '--preset=full',
                '--emulated-form-factor={0}'.format(self._device),
                '--output=json',
                '--output-path={0}'.format(self._file_name),
            ]
            subprocess.check_call(' '.join(command), shell=True)
        except subprocess.CalledProcessError as exc:
            msg = '''
                Command "{0}"
                returned an error code: {1},
                output: {2}
            '''.format(exc.cmd, exc.returncode, exc.output)
            raise RuntimeError(msg)

    def read_report_file(self):
        with os.fdopen(self._file_descriptor, 'r') as f:
            return json.load(f)



if __name__ == '__main__':
    with LightHouse('http://www.example.com') as lh:
        print(lh.read_report_file())

