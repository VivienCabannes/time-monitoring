"""Back-end for invoice generation"""
from datetime import datetime
import glob
import os
import shutil
import subprocess

from .config import INVOICE_DESTINATION, LATEX_PATH
from .report import get_last_report_number, read_report


def invoice_macro(report_nb=None, price=150, activity="work", change=1, invoice_nb=None):
    """Generate tex macro in order to generate invoice with LaTeX"""
    if report_nb is None:
        report_nb = get_last_report_number()
    if invoice_nb is None:
        invoice_nb = report_nb

    activities, outputs, totals, _, dates = read_report(report_nb)

    ind = activities.index(activity)

    total_price = int(totals[ind][0] * price * 100) / 100
    second_price = int(100 * total_price / change) / 100

    [year, month, day] = datetime.now().strftime('%Y %m %d').split()
    month = {
        1: ' janvier ', 2: " f\\'evrier ", 3: ' mars ', 4: ' avril ', 
        5: ' mai ', 6: ' juin ', 7: ' juillet ', 8: ' aout ', 
        9: ' septembre ', 10: ' octobre ', 11: ' novembre ', 12: " d\\'ecembre "
    }[int(month)]
    french_date = day +  month + year

    file_path = LATEX_PATH / "macros.tex"
    with open(file_path, "w", encoding="ascii") as f:
        f.write("\\newcommand{\\fillhours}{" + outputs[ind] + "}\n")
        f.write("\\newcommand{\\totalhours}{" + totals[ind][1] + "}\n")
        f.write("\\newcommand{\\price}{" + str(price) + "}\n")
        f.write("\\newcommand{\\totalprice}{" + str(total_price) + "}\n")
        f.write("\\newcommand{\\invoicenumber}{" + str(invoice_nb) + "}\n")
        f.write("\\newcommand{\\datestart}{" + str(dates[0]) + "}\n")
        f.write("\\newcommand{\\dateend}{" + str(dates[1]) + "}\n")
        f.write("\\newcommand{\\pricechange}{" + str(change) + "}\n")
        f.write("\\newcommand{\\secondprice}{" + str(second_price) + "}\n")
        f.write("\\newcommand{\\frenchdate}{" + french_date + "}\n")


def compile_latex(invoice_nb=None):
    """Compile LaTeX to generate pdf invoice"""
    if invoice_nb is None:
        invoice_nb = get_last_report_number()

    with subprocess.Popen(
        ["pdflatex", "main.tex"], stdout=subprocess.PIPE, universal_newlines=True, cwd=LATEX_PATH
    ) as process:
        while True:
            output = process.stdout.readline()
            print(output.strip(), flush=True)
            # Check for process completion
            return_code = process.poll()
            if return_code is not None:
                print("RETURN CODE", return_code, flush=True)
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    print(output.strip())
                break
    dest = str(INVOICE_DESTINATION / (invoice_nb + ".pdf"))
    process = subprocess.run(["mv", "main.pdf", dest], cwd=LATEX_PATH, check=True)
    clean_latex(LATEX_PATH)


def clean_latex(main_path):
    """Cleat latex auxilliary files"""

    def remove(path_list):
        for path in path_list:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    remove(glob.glob(str(main_path / "*.aux")))
    remove(glob.glob(str(main_path / "auto")))
    remove(glob.glob(str(main_path / "*.fbd_latexmk")))
    remove(glob.glob(str(main_path / "*.fls")))
    remove(glob.glob(str(main_path / "*.out")))
    remove(glob.glob(str(main_path / ".pdf-view-restore")))
