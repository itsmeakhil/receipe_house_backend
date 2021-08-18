import requests

from blue_agilis_backend.common.utils.logger import get_logger

logger = get_logger()


class PuppeteerRenderer:

    """
    Puppeteer (Chrome headless node API) based web page renderer.
    Useful server side rendering through proxy.
    Outputs HTML, PDF and screenshots as PNG.

    https://github.com/zenato/puppeteer-renderer
    """

    def __init__(self, host='localhost', port='3000'):
        self._url = 'http://%s:%s/render' % (host, port)

    def render_pdf(self, url):
        return self.__render_pdf(url)

    def __render_pdf(self, url):
        params = {
            "url": url,
            "type": "pdf",
            "fullpage": "true",
            "timeout": 1000 * 1000
        }
        response = requests.get(self._url, params=params)
        logger.info('PuppeteerRequest=> ' + response.url)
        return response.content

    def __str__(self):
        return '<PuppeteerRenderer Object>'
