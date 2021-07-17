#!/usr/bin/python
import os
import smtplib
from email.message import EmailMessage

# pdf generation items
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.units import inch, cm # super important, otherwise it won't know about these units

script = os.path.basename(__file__)
script_path = os.path.dirname(os.path.realpath(__file__))

report = SimpleDocTemplate(f"{script_path}/report.pdf")
styles = getSampleStyleSheet()

message = EmailMessage()

sender = 'braidj@gmail.com'
recipient = "braidj@gmail.com"

message['from'] = sender
message['to'] = recipient
message['Subject'] = f"Greetings from {sender} to {recipient} via {script}"

body = """Hey there
I'm practicing using Python
to send an email
lots of love
JJJ"""

message.set_content(body)

try:
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #mail_server.login("braidj@gmail.com", 'edinbkpdkcvdnjml')
    #no_send_recipients = mail_server.send_message(message)

    # print("{} recipients did not receive the message".format(
    #    len(no_send_recipients)))
    # mail_server.quit()

except Exception as e:
    print(e)

fruit = {
    "elderberries": 1,
    "figs": 1,
    "apples": 2,
    "durians": 3,
    "bananas": 5,
    "cherries": 8,
    "grapes": 13
}

# for pdf tables data must be in a list of lists
table_data = []
for k,v in fruit.items():
    table_data.append([k,v])

report_title = Paragraph("A Complete Inventory of My Fruit", styles["h1"])
table_style = [('GRID', (0,0), (-1,-1), 1, colors.black)]
report_table = Table(data=table_data, style=table_style, hAlign="LEFT")

# for pie charts we need two lists, one for data, one for labels
#report_pie = Pie(width=3*inch, height=3*inch)
report_pie = Pie(width=3*inch, height=3*inch)
report_pie.data = []
report_pie.labels = []
for fruit_name in sorted(fruit):
    report_pie.data.append(fruit[fruit_name])
    report_pie.labels.append(fruit_name)

report_chart = Drawing()
report_chart.add(report_pie)

report.build([report_title, report_table, report_chart])

print("Seems it worked")
