
import glob
import os
from pathlib import Path
import shutil
import subprocess
from .config import (
    INVOICE_DESTINATION,
    LATEX_PATH,
)
from .report import (
    get_last_report_number,
    read_report,
)
from pkg_resources import resource_string


def invoice_macro(report_nb=None, price=150, activity='work', change=1, invoice_nb=None):
    """Generate tex macro in order to generate invoice with LaTeX"""
    if report_nb is None:
        report_nb = get_last_report_number()
    if invoice_nb is None:
        invoice_nb = report_nb

    activities, outputs, totals, messages, dates = read_report(report_nb)

    ind = activities.index(activity)

    total_price = int(totals[ind][0] * price * 100) / 100
    second_price = int(100 * total_price / change) / 100

    file_path = LATEX_PATH / 'macros.tex'
    with open(file_path, 'w') as f:
        f.write('\\newcommand{\\fillhours}{' + outputs[ind] + '}\n')
        f.write('\\newcommand{\\totalhours}{' + totals[ind][1] + '}\n')
        f.write('\\newcommand{\\price}{' + str(price) + '}\n')
        f.write('\\newcommand{\\totalprice}{' + str(total_price) + '}\n')
        f.write('\\newcommand{\\invoicenumber}{' + str(invoice_nb) + '}\n')
        f.write('\\newcommand{\\datestart}{' + str(dates[0]) + '}\n')
        f.write('\\newcommand{\\dateend}{' + str(dates[1]) + '}\n')
        f.write('\\newcommand{\\pricechange}{' + str(change) + '}\n')
        f.write('\\newcommand{\\secondprice}{' + str(second_price) + '}\n')


def compile_latex(invoice_nb=None):
    """Compile LaTeX to generate pdf invoice"""
    if invoice_nb is None:
        invoice_nb = get_last_report_number()

    process = subprocess.Popen(['pdflatex', 'main.tex'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True,
                               cwd=LATEX_PATH,
                              )
    while True:
        output = process.stdout.readline()
        print(output.strip(), flush=True)
        # Check for process completion
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code, flush=True)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break
    dest = str(INVOICE_DESTINATION / (invoice_nb + '.pdf'))
    process = subprocess.run(['mv', 'main.pdf', dest], cwd=LATEX_PATH)
    clean_latex(LATEX_PATH)


def clean_latex(main_path):
    """Cleat latex auxilliary files"""
    def rm(path_list):
        for path in path_list:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    rm(glob.glob(str(main_path / '*.aux')))
    rm(glob.glob(str(main_path / 'auto')))
    rm(glob.glob(str(main_path / '*.fbd_latexmk')))
    rm(glob.glob(str(main_path / '*.fls')))
    rm(glob.glob(str(main_path / '*.out')))
    rm(glob.glob(str(main_path / '.pdf-view-restore')))
