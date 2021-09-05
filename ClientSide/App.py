
from flask import Flask, Response, render_template, request, redirect, url_for, send_file
import numpy as np
import cv2
from ServerSide import ServiceImpl
import pandas as pd


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filestr = request.files['file'].read()
        npimg = np.fromstring(filestr, np.uint8)

        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        obj = ServiceImpl.ServiceImpl(img)
        data = obj.serviceImpl()
        return render_template("form.html", data=data)



@app.route("/getSpreadSheet" , methods = ['GET', 'POST'])
def getSpreadSheet():
    if request.method == 'POST':
        data = {}
        for v in request.form:
            if v != 'action' or v != ' ':
                data[v] = request.form[v]
        df = pd.DataFrame(data=data, index=[0]).T
        df.to_excel('OUTPUT.xls')
        return send_file('OUTPUT.xls', attachment_filename='OUTPUT.xls')

app.run(debug=True)