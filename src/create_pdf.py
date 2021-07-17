#!/usr/bin/env python3

import pdf_example

if __name__ == "__main__":
    print("in progress")

    pdf_file = "single_table.pdf"
    pdf_title = "Python PDF doc"
    summary_lines=['Hi there,','this is an example of generating a PDF from python.','Thats it really']
    pdf_summary = "<br/>".join(summary_lines)

    table_data = []
    table_data.append([1,'dog'])
    table_data.append([2,'cat'])
    table_data.append([3,'mouse'])

    pie_labels = [x[1] for x in table_data ]
    pie_data = [x[0] for x in table_data ]
    piechart_data = {'labels':pie_labels,'data':pie_data}

    table_data.insert(0,['ID','Animal'])
    
    pdf_example.generate(pdf_file,pdf_title,pdf_summary,table_data,piechart_data)

    print(f"Hopefully {pdf_file} has been created")