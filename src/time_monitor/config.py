
import os
from pathlib import Path
import sys

BUFFER_PATH = Path.home() / 'time-monitoring'
DATA_PATH = BUFFER_PATH / 'data'
BUFFER_FILE = BUFFER_PATH / '.activity'
REPORT_FILE = BUFFER_PATH / '.current_report.csv'
LATEX_PATH = Path(sys.prefix) / 'latex' / 'invoice'
INVOICE_DESTINATION = Path.home() / 'Desktop'

DATE_FORMAT = '%Y-%m-%d %H:%M'
