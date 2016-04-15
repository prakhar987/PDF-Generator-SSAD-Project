import os
import commands
import re
import time
import sys
import urllib2
import smtplib
import zipfile
import tempfile
from app1.models import *
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.core.mail.message import *
from django.core.mail import EmailMessage
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from reportlab import platypus
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch, landscape, A4
from reportlab.platypus import Image, Table, TableStyle, Paragraph, SimpleDocTemplate
from reportlab.platypus import Spacer, PageTemplate, BaseDocTemplate, NextPageTemplate, PageBreak
from reportlab.lib import colors, utils
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import *
from reportlab.graphics.shapes import Image
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.widgets.markers import makeMarker
from os.path import *


def myfirstpage(canvas, doc):
    canvas.saveState()
    canvas.line(0 * inch, 0.01 * inch, 11.69 * inch, 0.01 * inch)
    canvas.line(0 * inch, 0 * inch, 0 * inch, 8.24 * inch)
    canvas.line(11.69 * inch, 0 * inch, 11.69 * inch, 8.24 * inch)
    canvas.line(0 * inch, 8.23 * inch, 11.69 * inch, 8.23 * inch)
    canvas.setFont('Times-Bold', 16)
    canvas.restoreState()


def mylaterpages(canvas, doc):
    canvas.saveState()
    canvas.line(0 * inch, 0.01 * inch, 11.69 * inch, 0.01 * inch)
    canvas.line(0 * inch, 0 * inch, 0 * inch, 8.24 * inch)
    canvas.line(11.69 * inch, 0 * inch, 11.69 * inch, 8.24 * inch)
    canvas.line(0 * inch, 8.24 * inch, 11.69 * inch, 8.24 * inch)
    canvas.restoreState()


def display_image(filename, elements, x, y, w, q):
    d = Drawing(x * inch, y * inch)
    if not os.path.exists(filename):
        f = open(filename, 'w')
        f.write(response.read())
        f.close()
    im = Image(path=filename, width=None, height=None, x=w * inch, y=q * inch)
    # im.hAlign='LEFT'
    d.add(im)
    elements.append(d)
    return elements


def display_image1(filename, elements, x, y, w, q, x1, x2):
    d = Drawing(x1 * inch, x2 * inch)
    if not os.path.exists(filename):
        f = open(filename, 'w')
        f.write(response.read())
        f.close()
    im = Image(path=filename, width= x *inch, height= y*inch, x=w * inch, y=q * inch)
    # im.hAlign='LEFT'
    d.add(im)
    elements.append(d)
    return elements


def basic_info(elements, user_id):
    user = User.objects.get(id=user_id)
    company = Company.objects.get(id=user.company_id)
    styles = ParagraphStyle(
        name='Normal',
        fontName='Times-Roman',
        fontSize=15,
        alignment=2,
    )
    i = Paragraph(str(user.first_name + " " + user.last_name + " resume"), styles)
    elements.append(i)
    elements.append(Spacer(1, 0.5 * inch))
    dat = [[], [], [], []]
    dat[0].append(str("First Name:"))
    dat[0].append(str(user.first_name))
    dat[1].append(str("Last Name:"))
    dat[1].append(str(user.last_name))
    dat[2].append(str("phone:"))
    dat[2].append(str(user.phone))
    dat[3].append(str("company name"))
    dat[3].append(str(company.name))
    styles = ParagraphStyle(
        name='Normal',
        fontName='Times-Roman',
        fontSize=14,
        textColor=colors.black,
    )
    data2 = [[Paragraph(cell, styles) for cell in row] for row in dat]
    t = Table(data2, colWidths=1.5 * inch, rowHeights=None, splitByRow=1, repeatRows=1, hAlign="RIGHT")
    tattle = (TableStyle([('FONTSIZE', (0, 0), (-1, -1), 800),
                          ('TOPPADDING', (0, 0), (-1, -1), 4),
                          ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                          ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.brown),
                          ('BOX', (0, 0), (-1, -1), 0.50, colors.brown),
                          ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                          ]))
    var = 0
    for _ in data2:
        if var % 2 == 0:
            tattle.add('BACKGROUND', (0, var), (-1, var), colors.lightgrey)
        else:
            tattle.add('BACKGROUND', (0, var), (-1, var), colors.white)
        var += 1
    t.setStyle(tattle)
    elements.append(t)
    # elements.append(Spacer(1,0.2*inch))
    elements = display_image(str(user.picture), elements, 4, 1, 0, 1)
    return elements


def fetch_data_of_candidate(elements, user_id):
    user = User.objects.get(id=user_id)
    tcqh = TestCandidateQuestionHistory.objects.all()
    array = []
    tes = []
    sec = []
    i = 0
    for row in tcqh:
        if user.id == row.candidate_id:
            array.append([])
            array[i].append(str(Test.objects.get(id=row.test_id).name))  # test name
            if str(array[i][0]) not in tes:
                tes.append(str(array[i][0]))
            array[i].append(str(Company.objects.get(id=Test.objects.get(id=row.test_id).company_id).name))  # name of the company that conducted the test
            array[i].append(str(TestSectionDef.objects.get(id=row.section_id).name))  # section name
            if str(array[i][2]) not in sec:
                sec.append(str(array[i][2]))
            array[i].append(str(Question.objects.get(id=row.question_id).text))  # question
            array[i].append(str(Question.objects.get(id=row.question_id).difficulty_level))
            array[i].append(str(QuestionAnswer.objects.get(id=row.answer_id).text))  # answer id in QuestionAnswer
            array[i].append(str(row.duration))  # duration by user
            array[i].append(str(row.status))  # status of answer
            array[i].append(str(row.score))  # score for that question
            mf = MediaFiles.objects.all()
            count = 0 
            for mf1 in mf:
                if int(mf1.user_id) == int(user_id) and int(mf1.question_id) == int(row.question_id):
                    count += 1
            array[i].append(str(count)) # sending the no of image files for that question
            if count>0:
                for mf1 in mf:
                    if int(mf1.user_id) == int(user_id) and int(mf1.question_id) == int(row.question_id):        
                        array[i].append(str(mf1.media_file))
            i += 1
    # return fun,user.id
    l = 0
    generate_data_for_table(array, elements, i, l, sec, tes)

    return elements


def generate_data_for_table(array, elements, i, l, sec, tes):
    l = 0
    while l < len(tes):
        arr = []
        i1 = 0
        count = 0
        count, styles, arr = fetch_data_belonging_to_a_test(arr, array, count, elements, i, i1, l, tes)
        i1 = 0
        while i1 < len(sec):
            l2 = 0
            ar = []
            count1 = 0
            count1 = headings_to_the_tables(ar, count1, i1, sec)
            count1 += 1
            while l2 < count:
                count1, ar = arrange_data_according_to_sub_sections(ar, arr, count1, elements, i1, l2, sec, styles)
                l2 += 1
            styles = ParagraphStyle(
                name='Normal',
                fontName='Times-Roman',
                fontSize=12,
                alignment=1,
                textColor=colors.black,
            )
            i = generate_table_with_fetched_data(ar, count1, elements, i, i1, sec, styles)
            i1 += 1
        l += 1


def arrange_data_according_to_sub_sections(ar, arr, count1, elements, i1, l2, sec, styles):
    if arr[l2][1] == sec[i1]:
        if count1 == 1 or (count1 == 2 and sec[i1] == "paragraph"):
            styles = ParagraphStyle(
                name='Normal',
                fontName='Times-Roman',
                fontSize=13,
                alignment=0,
                textColor=colors.red,
                allowWidows=0,
                leftIndent=-50,

            )
            x = Paragraph(str("-" + "sub-section:" + sec[i1]), styles)
            elements.append(x)
            elements.append(Spacer(1, 0.1 * inch))
        # elements.append(t)
        ar.append([])
        ar[count1].append(arr[l2][2])
        ar[count1].append("")
        ar[count1].append("")
        ar[count1].append("")
        ar[count1].append(arr[l2][4])
        ar[count1].append(arr[l2][3])
        ar[count1].append(arr[l2][5])
        ar[count1].append(arr[l2][6])
        ar[count1].append(arr[l2][7])
        count1 += 1
        if int(arr[l2][8]) > 0:
            ar.append([])
            ar[count1].append('Images')
            ar[count1].append(' ')
            v = 0
            while v < int(arr[l2][8]):
                image = []
                image = display_image1(str(arr[l2][9 + v]), image, 1, 1, 0, 0, 1, 1)
                x = Paragraph(str("image"), styles)
                image.append(x)
                ar[count1].append(image)
                v += 1
            count1 += 1
    return count1, ar


def headings_to_the_tables(ar, count1, i1, sec):
    if sec[i1] == "paragraph" and count1 == 0:
        ar.append([])
        ar[count1].append("text")
        ar[count1].append("")
        ar[count1].append("")
        ar[count1].append("")
        ar[count1].append("")
        ar[count1].append("")
        count1 += 1
    ar.append([])
    ar[count1].append(str("question"))
    ar[count1].append("")
    ar[count1].append("")
    ar[count1].append("")
    ar[count1].append("answer")
    ar[count1].append("difficultylevel")
    ar[count1].append("duration")
    ar[count1].append("status")
    ar[count1].append("score")
    return count1


def generate_table_with_fetched_data(ar, count1, elements, i, i1, sec, styles):
    if (count1 > 1): # and sec[i1] != 'paragraph') or (count1 > 2 and sec[i1] == 'paragraph'):
        # data2 = [[Paragraph(cell, styles) for cell in row] for row in ar]
        data2 = []
        counter = 0
        for row in ar:
            data2.append([])
            try:
                for cell in row:
                    data2[counter].append(Paragraph(cell, styles))
            except:
                counter1 = 0
                for cell in row:
                    data2[counter].append(ar[counter][counter1])
                    counter1 += 1
            counter += 1
        i = 0

        t = Table(data2, colWidths=1.2 * inch, rowHeights=None, splitByRow=1, repeatRows=2, hAlign="CENTER")
        tattle = (TableStyle([('FONTSIZE', (0, 0), (-1, -1), 800),
                              ('BOX', (0, 0), (-1, -1), 2, colors.brown),
                              ('TOPPADDING', (0, 0), (-1, -1), 4),
                              ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                              # ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
                              ('BOX', (0, 0), (-1, -1), 0.50, colors.black),

                              ]))
        var = 0
        for _ in ar:
            if var == 0:
                tattle.add('BACKGROUND', (0, var), (-1, var), colors.gray)
            elif var % 2 == 0:
                tattle.add('BACKGROUND', (0, var), (-1, var), colors.lightgrey)
            else:
                tattle.add('BACKGROUND', (0, var), (-1, var), colors.white)
            tattle.add('SPAN', (0, var), (3, var))
            var += 1
        if sec[i1] == "paragraph":
            tattle.add('SPAN', (0, 0), (-1, 0))
            tattle.add('BACKGROUND', (0, 1), (-1, 1), colors.gray)
            tattle.add('BACKGROUND', (0, 0), (-1, 0), colors.cyan)
        t.setStyle(tattle)
        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))
    return i


def fetch_data_belonging_to_a_test(arr, array, count, elements, i, i1, l, tes):
    styles = ParagraphStyle(
                    name='Normal',
                    fontName='Times-Roman',
                    fontSize=15,
                    alignment=1,
                    textColor=colors.green,
                    allowWidows=1,
                )
    while i1 < i:
        if array[i1][0] == tes[l]:
            arr.append([])
            if count == 0:
                styles = ParagraphStyle(
                    name='Normal',
                    fontName='Times-Roman',
                    fontSize=15,
                    alignment=0,
                    textColor=colors.green,
                    allowWidows=1,
                    leftIndent=-70,
                )
                x = Paragraph(str(str(l + 1) + ".section:" + tes[l]), styles)
                elements.append(x)
                elements.append(Spacer(1, 0.1 * inch))
            # arr[0].append(array[i1][0])
            arr[count].append(array[i1][1])  # company
            arr[count].append(array[i1][2])  # section
            arr[count].append(array[i1][3])  # question
            arr[count].append(array[i1][4])  # diff level
            arr[count].append(array[i1][5])  # answer
            arr[count].append(array[i1][6])  # duration
            arr[count].append(array[i1][7])  # status
            arr[count].append(array[i1][8])  # score
            arr[count].append(array[i1][9])  # no of image fields
            v = 0
            while v < int(array[i1][9]):
                arr[count].append(array[i1][10 + v])
                v += 1
            count += 1
        i1 += 1
    return count, styles, arr


def other_info(elements, user_id):
    user = User.objects.get(id=user_id)
    tcqh = TestCandidateQuestionHistory.objects.all()
    array = []
    tes = []
    sec = []
    i = 0
    for row in tcqh:
        if user.id == row.candidate_id:
            array.append([])
            array[i].append(str(Test.objects.get(id=row.test_id).name))  # test name
            if array[i][0] not in tes:
                tes.append(array[i][0])
            array[i].append(str(Company.objects.get(
                id=Test.objects.get(id=row.test_id).company_id).name))  # name of the company that conducted the test
            array[i].append(str(TestSectionDef.objects.get(id=row.section_id).name))  # section name
            if array[i][2] not in sec:
                sec.append(array[i][2])
            array[i].append(str(Question.objects.get(id=row.question_id).text))  # question
            array[i].append(str(Question.objects.get(id=row.question_id).difficulty_level))
            array[i].append(str(QuestionAnswer.objects.get(id=row.answer_id).text))  # answer id in QuestionAnswer
            array[i].append(str(row.duration))  # duration by user
            array[i].append(str(row.status))  # status of answer
            array[i].append(str(row.score))  # score for that question
            i += 1
    # return fun,user.id
    l = 0
    while l < len(tes):
        arr = []
        i1 = 0
        count = 0
        while i1 < i:
            if array[i1][0] == tes[l]:
                arr.append([])
                if count == 0:
                    styles = ParagraphStyle(
                        name='Normal',
                        fontName='Courier-BoldOblique',
                        fontSize=15,
                        alignment=1,
                        textColor=colors.green,
                        allowWidows=1,
                    )
                    x = Paragraph(str(str(l + 1) + ".section:" + tes[l]), styles)
                    elements.append(x)
                    elements.append(Spacer(1, 0.1 * inch))
                # arr[0].append(array[i1][0])
                arr[count].append(array[i1][1])  # company
                arr[count].append(array[i1][2])  # section
                arr[count].append(array[i1][3])  # question
                arr[count].append(array[i1][4])  # diff level
                arr[count].append(array[i1][5])  # answer
                arr[count].append(array[i1][6])  # duration
                arr[count].append(array[i1][7])  # status
                arr[count].append(array[i1][8])  # score
                count += 1
            i1 += 1
        i1 = 0

        while i1 < len(sec):
            l2 = 0
            ar = []
            count1 = 0
            if sec[i1] == "paragraph":
                ar.append([])
                ar[count1].append("text")
                ar[count1].append("")
                ar[count1].append("")
                ar[count1].append("")
                ar[count1].append("")
                ar[count1].append("")
                count1 += 1
            ar.append([])
            ar[count1].append(str("question"))
            ar[count1].append("")
            ar[count1].append("")
            ar[count1].append("")
            ar[count1].append("answer")
            ar[count1].append("difficultylevel")
            ar[count1].append("duration")
            ar[count1].append("status")
            ar[count1].append("score")
            count1 += 1
            while l2 < count:
                if arr[l2][1] == sec[i1]:
                    if count1 == 1 or (count1 == 2 and sec[i1] == "paragraph"):
                        styles = ParagraphStyle(
                            name='Normal',
                            fontName='Courier-Bold',
                            fontSize=13,
                            alignment=0,
                            textColor=colors.brown,
                            allowWidows=0,
                        )
                        x = Paragraph(str("-" + "sub-section:" + sec[i1]), styles)
                        elements.append(x)
                        elements.append(Spacer(1, 0.1 * inch))
                    # elements.append(t)
                    ar.append([])
                    ar[count1].append(arr[l2][2])
                    ar[count1].append("")
                    ar[count1].append("")
                    ar[count1].append("")
                    ar[count1].append(arr[l2][4])
                    ar[count1].append(arr[l2][3])
                    ar[count1].append(arr[l2][5])
                    ar[count1].append(arr[l2][6])
                    ar[count1].append(arr[l2][7])

                    count1 += 1
                l2 += 1
            styles = ParagraphStyle(
                name='Normal',
                fontName='Times-Italic',
                fontSize=12,
                alignment=1,
                textColor=colors.black,
            )
            if count1 > 1:
                data2 = [[Paragraph(cell, styles) for cell in row] for row in ar]
                t = Table(data2, colWidths=None, rowHeights=None, splitByRow=1, repeatRows=2, hAlign="CENTER")
                tattle = (TableStyle([('FONTSIZE', (0, 0), (-1, -1), 800),
                                      ('BOX', (0, 0), (-1, -1), 2, colors.brown),
                                      ('TOPPADDING', (0, 0), (-1, -1), 4),
                                      ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                                      # ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
                                      ('BOX', (0, 0), (-1, -1), 0.50, colors.black),

                                      ]))
                var = 0
                for _ in ar:
                    if var == 0:
                        tattle.add('BACKGROUND', (0, var), (-1, var), colors.gray)
                    elif var % 2 == 0:
                        tattle.add('BACKGROUND', (0, var), (-1, var), colors.lightgrey)
                    else:
                        tattle.add('BACKGROUND', (0, var), (-1, var), colors.white)
                    tattle.add('SPAN', (0, var), (3, var))
                    var += 1
                if sec[i1] == "paragraph":
                    tattle.add('SPAN', (0, 0), (-1, 0))
                    tattle.add('BACKGROUND', (0, 1), (-1, 1), colors.gray)
                    tattle.add('BACKGROUND', (0, 0), (-1, 0), colors.cyan)
                t.setStyle(tattle)
                elements.append(t)
                elements.append(Spacer(1, 0.2 * inch))
            i1 += 1
        l += 1

    return elements


def chat_question(elements, user_id):
    user = User.objects.get(id=user_id)
    tct = TestChatTranscripts.objects.all()
    i = 1
    styles = ParagraphStyle(
        name='Normal',
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=0,
    )
    data = []
    count = 0
    data.append([])
    data[count].append(str("Questions"))
    count += 1
    for row in tct:
        if row.candidate_id == user.id:
            data.append([])
            x = row.question
            x = str(i) + "." + x + "\n"
            i += 1
            data[count].append(str(x))
            count += 1
    i = 1
    data.append([])
    data[count].append(str("Answers"))
    count += 1
    for row in tct:
        if row.candidate_id == user.id:
            data.append([])
            x = row.transcripts
            x = str(i) + ". Answer" + x + "\n"
            i += 1
            data[count].append(str(x))
            count += 1
    data2 = [[Paragraph(cell, styles) for cell in row] for row in data]
    t = Table(data2, colWidths=None, rowHeights=None, splitByRow=1, repeatRows=0, hAlign="CENTER")
    tattle = (TableStyle([('FONTSIZE', (0, 0), (-1, -1), 800),
                          ('BOX', (0, 0), (-1, -1), 2, colors.brown),
                          ('TOPPADDING', (0, 0), (-1, -1), 4),
                          ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                          ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                          ]))
    var = 0
    for _ in data:
        if var == 0 or var == count / 2:
            tattle.add('BACKGROUND', (0, var), (-1, var), colors.gray)
        elif var % 2 == 0:
            tattle.add('BACKGROUND', (0, var), (-1, var), colors.lightgrey)
        else:
            tattle.add('BACKGROUND', (0, var), (-1, var), colors.white)
        var += 1
    t.setStyle(tattle)
    if count > 1:
        x = "Chart Transcript"
        i = Paragraph(str(x), styles)
        elements.append(i)
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))
    return elements


def generate_certificate(elements):
    elements.append(Spacer(1, 0.5 * inch))
    data = [
        (13, 5, 20, 22, 37, 45, 19, 4),
        (14, 6, 21, 23, 38, 46, 20, 5)
    ]  # data for drawing bar graphs
    verticalbargraph(data, elements)
    horizontallinegraph(data, elements)
    data = [
        ((1, 1), (2, 2), (2.5, 1), (3, 3), (4, 5)),
        ((1, 2), (2, 3), (2.5, 2), (3.5, 5), (4, 6))
    ]
    elements.append(Spacer(1, 0.1 * inch))
    lineplotgraph(data, elements)
    piegraph(elements)
    styles = ParagraphStyle(
        name='Normal',
        fontName='Helvetica',
        fontSize=15,
        alignment=0,
    )
    elements.append(Spacer(1, 0.5 * inch))
    i = Paragraph(str("Please click on black square to play the video."), styles)
    elements.append(i)
    elements.append(platypus.flowables.Macro('canvas.saveState()'))
    elements.append(platypus.flowables.Macro('canvas.linkURL("fun.mp4",(400,510,410,500),relative=0,thickness=10)'))
    elements.append(platypus.flowables.Macro('canvas.restoreState()'))
    return elements


def piegraph(elements):
    drawing = Drawing(100, 350)
    pc = Pie()
    pc.x = 65
    pc.y = 15
    pc.width = 300
    pc.height = 300
    pc.data = [10, 20, 30, 40, 50, 60]
    pc.labels = ['a', 'b', 'c', 'd', 'e', 'f']
    pc.slices.strokeWidth = 0.5
    pc.slices[3].popout = 10
    pc.slices[3].strokeWidth = 2
    pc.slices[3].strokeDashArray = [2, 2]
    pc.slices[3].labelRadius = 1.75
    pc.slices[3].fontColor = colors.red
    drawing.add(pc)
    elements.append(drawing)
    elements.append(Spacer(1, 0.7 * inch))


def lineplotgraph(data, elements):
    drawing = Drawing(0, 400)  # for indices
    lp = LinePlot()
    lp.x = 0
    lp.y = 50
    lp.height = 300
    lp.width = 600
    lp.data = data
    lp.joinedLines = 1
    lp.lines[0].symbol = makeMarker('FilledCircle')
    lp.lines[1].symbol = makeMarker('Circle')
    lp.lineLabelFormat = '%2.0f'
    lp.strokeColor = colors.black
    lp.xValueAxis.valueMin = 0
    lp.xValueAxis.valueMax = 5
    lp.xValueAxis.valueSteps = [1, 2, 2.5, 3, 4, 5]
    lp.xValueAxis.labelTextFormat = '%2.1f'
    lp.yValueAxis.valueMin = 0
    lp.yValueAxis.valueMax = 7
    lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6]
    drawing.add(lp)
    elements.append(drawing)
    elements.append(Spacer(1, 0.1 * inch))


def horizontallinegraph(data, elements):
    drawing = Drawing(0, 175)  # for indices
    lc = HorizontalLineChart()
    lc.x = 0
    lc.y = 10
    lc.height = 150
    lc.width = 300
    lc.data = data
    lc.joinedLines = 1
    catnames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
    lc.categoryAxis.categoryNames = catnames
    lc.categoryAxis.labels.boxAnchor = 'n'
    lc.valueAxis.valueMin = 0
    lc.valueAxis.valueMax = 60
    lc.valueAxis.valueStep = 15
    lc.lines[0].strokeWidth = 2
    lc.lines[1].strokeWidth = 1.5
    drawing.add(lc)
    elements.append(drawing)


def verticalbargraph(data, elements):
    drawing = Drawing(0, 200)  # for indices
    bc = VerticalBarChart()
    bc.x = 0  # x,y define the left bottom of graph
    bc.y = 0
    bc.height = 150
    bc.width = 300
    bc.data = data
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 50
    bc.valueAxis.valueStep = 10
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 6  # next 3 lines is for naming indices
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 60
    bc.categoryAxis.categoryNames = ['Jan-99', 'Feb-99', 'Mar-99',
                                     'Apr-99', 'May-99', 'Jun-99', 'Jul-99', 'Aug-99']
    drawing.add(bc)
    elements.append(drawing)
    elements.append(Spacer(1, 0.5 * inch))


def func(request, user_id=6):
    elements = []
    filename = str(str(user_id) + ".pdf")
    doc = SimpleDocTemplate("pdfs/" + filename, pagesize=landscape(A4))
    elements = basic_info(elements, user_id)  # ,pagesize)
    elements = fetch_data_of_candidate(elements, user_id)
    elements = chat_question(elements, user_id)
    elements = generate_certificate(elements)
    doc.build(elements, onFirstPage=myfirstpage, onLaterPages=mylaterpages)
    return HttpResponse("Hello world.You'reat the polls index.")  # %s%s"%(tes,fun))


def mail(request, user_id=6):
    subject = "Here is the update in project."
    message = "This mail is sent by running the script.\n This contain a zip file, which contain a pdf and video.In the lastpage of the pdf there is a link(a black square) which on clicking plays the video that is in zip folder. \n Thank you,"
    filename = str("pdfs/" + str(user_id) + ".pdf")
    zf = tempfile.TemporaryFile(prefix='mail', suffix='.zip')
    zip = zipfile.ZipFile(zf, 'w')
    zip.write(filename)
    zip.write('pdfs/fun.mp4')
    zip.close()
    zf.seek(0)
    from_email = settings.EMAIL_HOST_USER
    to_email = ['mandavaveerendra7@gmail.com']
    mail = EmailMessage(subject, message, from_email, to_email)
    mail.attach("fun" + '.zip', zf.read(), 'applications/zip')
    mail.send()
    return HttpResponse("Hello world.You'reat the a;nf;kandgsd index.")  # %s%s"%(tes,fun))


def all_users(request):
    return render_to_response('all_users.html',
                              {'users': User.objects.all()})


def user(request, user_id=6):
    return render_to_response('user.html',
                              {'user': User.objects.get(id=user_id)})

