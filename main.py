import logging
from typing import Optional

from reportlab.pdfgen import canvas

from zcp_py_plugin.meta import Meta
from zcp_py_plugin.phi import Phi
from zcp_py_plugin.report_plugin import ReportPlugin
from zcp_py_plugin.plugin_result_type import PluginResultType
from zcp_py_plugin.plugin_client import PluginClient

class MyFirstPlugin(ReportPlugin):
    def process(self, meta: Meta, phi: Optional[Phi]) -> None:
        logging.info(f"Process started with meta: {meta} and phi: {phi}")

        report_file_name = 'report-' + meta.capture_id + '.pdf'
        c = canvas.Canvas(report_file_name)
        c.drawString(100, 120, 'Subject name: ' + phi.name)
        c.drawString(100, 100, 'Study recorded: ' + meta.capture_start_time_display)
        c.save()
    
        self.progress(80, 'Uploading report')
        self.emit(PluginResultType.PDF, file_name=report_file_name)

        self.progress(100, 'All done')
        logging.info(f"Emit succeeded")

def main():
    logging.basicConfig(level=logging.INFO)
    auth_string = "YOUR_AUTH_STRING"

    PluginClient.of()
        .server('apidev.zetoserver.com')
        .vendor('Zeto Inc.')
        .name('Automated GHT testing plugin')
        .version('1.0.0')
        .operation_pdf()
        .plugin(MyReportPlugin)
        .auth_string(auth_string)
        .server_region('eu-central-1')
        .description('GHT-testing plugin')
        .icon('report')
        .build()

if __name__ == '__main__':
    main()
