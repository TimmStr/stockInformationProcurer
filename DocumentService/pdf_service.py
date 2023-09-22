# Grundgerüst stammt aus https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
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


# Funktion zum löschen der Bilder
def deleteFiles(name):
    filename = name + '_autocorr.png'
    # löschen Autokorrelationsgrafik
    os.remove(filename)
    filename = name + '_part_autocorr.png'
    # löschen Partielle-Autokorrelationsgrafik
    os.remove(filename)
    filename = name + '.png'
    # löschen STL-Decomposition Grafik
    os.remove(filename)


# Erstellen der PDF Datei
def create_pdf(file_names, avg_value, max_value, min_value):
    # Abfrage ob der Ordner PDF im aktuellen Pfad existiert
    if not os.path.exists('PDF'):
        os.mkdir('PDF')
    name = file_names[0].split('_')
    name = ''.join(name[1:2])
    print('Name', name)
    print('Filenames',file_names)
    # Datum über die date.today Funktion abspeichern
    dateToday = str(date.today())
    # PDF Dateiname setzt sich aus dem Spaltennamen und dem heutigen Datum zusammen. Bsp. Northern_Hemisphere_2022-02-01
    filename = 'PDF/' + str(name) + '_' + dateToday + '.pdf'

    # Speichern der Vorlage mit dem Dateinamen und dem Format in der doc Variable
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    # Story ist eine Liste zur Speicherung der Bestandteile des PDF Dokuments
    Story = []
    # getSampleStyleSheet bezieht vorgefertigte Schriftgrößen
    styles = getSampleStyleSheet()

    # Überschrift
    ptext = 'Report for: ' + name
    Story.append(Paragraph(ptext, styles["Title"]))
    # Spacer ist der Abstand zum nächsten Absatz
    Story.append(Spacer(1, 12))

    # Einfügen des Datums und der Uhrzeit unterhalb der Unterschrift
    formatted_time = time.ctime()
    ptext = 'Erstellt am: %s' % formatted_time + '<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = 'KPIs: <br /> '
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    # Abfragen ob Werte wie Test Statistic und p-Wer grenzen überschreiten
    # Je nach Fall wird dann Stationarität oder nicht Stationarität ausgegeben

    ptext = 'Avg: %s <br /> Max: %s <br /> Min: %s <br /> ' % (
        avg_value,
        max_value,
        min_value)

    imageName = file_names[0]
    # anhängen der STL-Decomposition Grafik in die Story
    im = Image(imageName, width=320, height=240)
    Story.append(im)

    # hinzufügen der Schriftgröße Justify
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # <br /> steht jeweils für einen Zeilenumbruch
    ptext = '<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    # Augmented Dickey Fuller Test an Story anhängen
    ptext = 'Augmented Dickey-Fuller Test der Region: %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    ptext = 'Test Statistic:  <br /> p-value: s <br /> Lags used: s <br /> Number of Observations Used: s <br /> Critical Value 1: s <br /> Critical Value 5: %s <br /> Critical Value 10: s'

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    # Abfragen ob Werte wie Test Statistic und p-Wer grenzen überschreiten
    # Je nach Fall wird dann Stationarität oder nicht Stationarität ausgegeben

    ptext = '<br /> <br /> <br /> <br />'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    # KPSS Test, Ablauf weitestgehend genauso wie der ADF Test
    ptext = '<br /> KPSS Test der Region: %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    # Autokorrelations Plot
    ptext = 'Autocorrelation der Region : %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    # Partielle Autokorrelations Plot
    ptext = '<br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />  <br /> <br /> Partielle Autocorrelation der Region : %s' % (
        str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    # Anhängen der partiellen Autokorrelationsgrafik
    imageName = file_names[1]
    im = Image(imageName, width=320, height=240)
    Story.append(im)

    # Builden der Story (speichern des Dokuments)
    doc.build(Story)
    print(name + ".pdf erstellt")
    return filename


def get_files(ticker):
    print(type(ticker), ticker)
    response = requests.get(STOCK_ANALYSIS_SERVICE + "/startAnalysis",
                            params=ticker)

    response_as_json = response.json()
    print('Doc Response as json', response_as_json)
    filenames = response_as_json.get("Filename")
    avg_value = response_as_json.get("Avg")
    max_value = response_as_json.get("Max")
    min_value = response_as_json.get("Min")
    print('AVg', avg_value, 'Max', max_value, 'Min', min_value)
    print("mail", ticker.get("mail"))
    print("password",ticker.get("password"))

    for filename in filenames:
        ticker["file_name"] = filename
        print(ticker)
        response = requests.get(STOCK_ANALYSIS_SERVICE + "/getGraphs",
                                params=ticker)
        print('Filename', filename)
        open(filename, 'wb').write(response.content)
    return filenames, avg_value, max_value, min_value
