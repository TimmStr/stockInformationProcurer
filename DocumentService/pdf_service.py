"""
File is responsible for obtaining the data from the StockAnalysis Service.
The creation of the PDF document also takes place here.
"""
# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
import requests
from datetime import date
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from Utils.paths import *
import json


def deleteFiles(filename):
    """
    This function ensures that the data is deleted again after the PDF has been published.
    :param filename: str
    :return:
        str with message
    """
    try:
        os.remove(filename)
        return "Successful deleted"
    except:
        return "File deletion failed"


def create_pdf(file_names, avg_value, max_value, min_value, kpis):
    """
    Creating PDF with the parameters:
    :param file_names: List of str
    :param avg_value: float
    :param max_value: float
    :param min_value: float
    :param kpis: {
                    Ticker: str,
                    EPS: str,
                    PE: str,
                    High52: str,
                    Low52: str,
                    Marketcap: str}
    :return:
        str filename - represents the path, where the pdf has been stored.
    """

    # Check whether the PDF folder exists in the current path
    if not os.path.exists('PDF'):
        os.mkdir('PDF')

    # Extracting name for the pdf file. Graphs/NASDAQ_NVDA_2023-09-22.png -> NVDA
    name = file_names[0].split('_')
    name = ''.join(name[1:2])

    # Creating pdf filename with todays date. -> PDF/NVDA_2023-09-25.pdf
    filename = 'PDF/' + str(name) + '_' + str(date.today()) + '.pdf'

    # Creating template with pagesize A4
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    # Story represents a list to store the components of the PDF document
    Story = []

    # getSampleStyleSheet obtains predefined font sizes
    styles = getSampleStyleSheet()

    # Headline
    ptext = 'Report for: ' + name
    Story.append(Paragraph(ptext, styles["Title"]))
    # Spacer is the distance to the next paragraph
    Story.append(Spacer(1, 12))

    # Insert the date and time below the heading
    formatted_time = time.ctime()
    ptext = 'Created at: %s' % formatted_time + '<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    # Inserting Values for time period
    ptext = 'Specific values for the period: <br /> '
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    ptext = 'Average: %s <br /> Max: %s <br /> Min: %s <br /> ' % (
        str(avg_value) + "$",
        str(max_value) + "$",
        str(min_value) + "$")
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    # Inserting KPIs
    ptext = 'KPIs: <br /> '
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    ptext = 'EPS: %s <br /> PE: %s <br /> Marketcap: %s <br /> High52: %s <br /> Low52: %s <br /> ' % (
        str(kpis.get('EPS').replace(',', '.') + "$"),
        str(kpis.get('PE').replace(',', '.') + "$"),
        str(kpis.get('Marketcap').replace(',', '.') + "$"),
        str(kpis.get('High52').replace(',', '.') + "$"),
        str(kpis.get('Low52').replace(',', '.') + "$"))
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    # Graph for the daily prices
    image_name = file_names[0]
    im = Image(image_name, width=320, height=240)
    Story.append(im)

    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    ptext = '<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    # Graph for the volume
    image_name = file_names[1]
    im = Image(image_name, width=320, height=240)
    Story.append(im)

    # Building the story (Saving PDF)
    doc.build(Story)
    return filename


def stock_information_for_ticker_from_analysis_service(parameters):
    """
    The function first makes a request to the StockAnalysisService. The result is stored in Json format.
    The information contained therein is extracted. This includes, among other things, values and file names of the
    graphs. Using the file names, a new request is sent to the Analysis Service, which downloads the files and
    stores them locally.
    :param parameters:
        ticker, type=str, required=True, description=The Tickersymbol. E.g. {"ticker":"NASDAQ:AAPL"}
        mail, type=str, required=True, description=The email address for the user.
        password, type=str, required=True, description=The password for the user.
        start_date, type=str, required=False, description=Start date represents the beginning of the analysis.
                                E.g. 12-08-2023. If not specified, the default value is used (One year ago).
        end_date', type=str, required=False, description=End date represents the beginning of the analysis.
                                E.g. 25-09-2023. If not specified, the default value is used (today).
    :return:
        filenames = List of str,
        avg_value = float,
        max_value = float,
        min_value = float,
        kpis = {
                    Ticker: str,
                    EPS: str,
                    PE: str,
                    High52: str,
                    Low52: str,
                    Marketcap: str}
    """
    response = requests.get(STOCK_ANALYSIS_SERVICE + "/startAnalysis", params=parameters)
    response_as_json = response.json()

    kpis = requests.get(STOCK_WEB_SCRAPING_SERVICE + "/getKpisFromTicker", params=parameters)
    kpis_as_json = kpis.json()
    kpis = kpis_as_json.get("KPIs")

    filenames = response_as_json.get("Filename")
    avg_value = response_as_json.get("Avg")
    max_value = response_as_json.get("Max")
    min_value = response_as_json.get("Min")

    for filename in filenames:
        parameters["file_name"] = filename
        response = requests.get(STOCK_ANALYSIS_SERVICE + "/getGraphs",
                                params=parameters)
        open(filename, 'wb').write(response.content)
    return filenames, avg_value, max_value, min_value, kpis
