from django.conf import settings
import os
from django.core.mail import send_mail
from django.core.mail.message import *
import urllib2
from django.shortcuts import render
from app1.models import *
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch, landscape, A4
from reportlab.platypus import Image, Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib import colors, utils
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import *
from reportlab.graphics.shapes import Image
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.widgets.markers import makeMarker
from django.template import RequestContext, loader


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
    # get_python_image(filename)
    d = Drawing(x * inch, y * inch)
    if not os.path.exists(filename):
        f = open(filename, 'w')
        f.write(response.read())
        f.close()
    im = Image(path=filename, width=1.5 * inch, height=1.5 * inch, x=w * inch, y=q * inch)
    # im.hAlign='LEFT'
    d.add(im)
    elements.append(d)
    return elements


def basic_info(fn, ln, elements):
    user = User.objects.get(first_name=fn, last_name=ln)
    company = Company.objects.get(id=user.company_id)
    styles = ParagraphStyle(
        name='Normal',
        fontName='Helvetica-Bold',
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
        fontName='Times-BoldItalic',
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


def other_info(elements, fn, ln):
    user = User.objects.get(first_name=fn, last_name=ln)
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
            ar.append([])
            ar[count1].append("                     question                     ")
            ar[count1].append("answer")
            ar[count1].append("difficultylevel")
            ar[count1].append("duration")
            ar[count1].append("status")
            ar[count1].append("score")
            count1 += 1
            while l2 < count:
                if arr[l2][1] == sec[i1]:
                    if count1 == 1:
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
                    ar[count1].append(arr[l2][4])
                    ar[count1].append(arr[l2][3])
                    ar[count1].append(arr[l2][5])
                    ar[count1].append(arr[l2][6])
                    ar[count1].append(arr[l2][7])
                    count1 += 1
                l2 += 1
            i1 += 1
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
                    var += 1
                t.setStyle(tattle)
                elements.append(t)
                elements.append(Spacer(1, 0.2 * inch))
        l += 1

    return elements


def func(request):
    elements = []
    doc = SimpleDocTemplate("fun.pdf", pagesize=landscape(A4))
    elements = basic_info("prabha", "prabha", elements)  # ,pagesize)
    elements = other_info(elements, "prabha", "prabha")
    doc.build(elements, onFirstPage=myfirstpage, onLaterPages=mylaterpages)
    return render(request, 'app1/prakhar.html', {}) # %s%s"%(tes,fun))


def mail(request):
    subject = "hello veeru"
    message = "how are you?"
    filename = str("fun.pdf")
    if not os.path.exists(filename):
        f = open(filename, 'w')
        f.write(response.read())
        f.close()
    # attach = open( filename , 'r' )
    message.attach(filename, f.read(), 'applications/pdf')
    from_email = settings.EMAIL_HOST_USER
    to_email = ['mandavaveerendra7@gmail.com']

    send_mail(subject,
              message,
              from_email,
              to_email,
              fail_silently=True)
    return HttpResponse("Hello world.You'reat the polls index.")  # %s%s"%(tes,fun))
