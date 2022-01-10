
from pathlib import Path


CODE_PATH = Path(__file__).resolve().parents[1]
LATEX_PATH = CODE_PATH / 'latex'
BUFFER_FILE = CODE_PATH / '.activity'
REPORT_FILE = CODE_PATH / '.current_report.csv'

DATE_FORMAT = '%Y-%m-%d %H:%M'
