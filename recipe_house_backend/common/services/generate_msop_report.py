import os
import tempfile
from datetime import datetime
from pathlib import Path

from django.conf import settings

from blue_agilis_backend.common.services.puppeteer import PuppeteerRenderer
from blue_agilis_backend.common.utils.helper import s3_helper
from blue_agilis_backend.common.utils.logger import get_logger

logger = get_logger()


class MsopReportPdf:

    def generate_pdf(self, params):

        logger.info(params)
        pk = params.get('id', None)
        mission_id = params.get('mission', None)
        pdf_s3_link = ''

        # file name format =>
        dt_string = datetime.now().strftime("%Y-%m-%d_%H:%M")
        filename = 'MSOP_REPORT_%s.pdf' % (dt_string)
        filepath = Path("/".join([tempfile.gettempdir(), filename]))

        try:
            context = dict(id=pk, mission_id=mission_id)
            url = settings.MSOP_REPORT_TEMPLATE_URL.format(**context)
            #url = 'https://www.google.com'

            logger.info('...??? rendering pdf...pls wait')
            renderer = PuppeteerRenderer(host=settings.PUPPETEER_HOST,
                                         port=settings.PUPPETEER_PORT)
            pdf = renderer.render_pdf(url)
            logger.info('...??? rendering finished...')

            filepath.write_bytes(pdf)

            pdf_s3_link = self.save_report_in_s3(str(filepath.absolute()), filename)
            logger.info(pdf_s3_link)

            pass
        except Exception as err:
            logger.exception(err)
            pass

        # remove generated file
        if os.path.exists(filepath.absolute()):
            os.remove(filepath.absolute())

        return pdf_s3_link

    def save_report_in_s3(self, file_path, object_name):
        try:
            bucket = settings.S3_DEFAULT_BUCKET_NAME
            prefix = 'msopreport'
            pdf_s3_link = s3_helper.upload_public_file(file_path, bucket, object_name, prefix)
            return pdf_s3_link
        except Exception as err:
            logger.exception(err)
