import cv2
import cx_Oracle
import numpy as np
from ServerSide import Tesseract

class Zoning:
    def __init__(self, img):
        self.img = img

    def zoning(self):
        img = self.img
        cv2.imwrite('C:/Users/H P/Desktop/UBSForm1120Extractor/intermediate/0dummy.jpg',img)
        datadict = {}
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='BOBUBS1')  # if needed, place an 'r' before any parameter in order to address any special character such as '\'.
        conn = cx_Oracle.connect(user='UBS1', password='UBS1', dsn=dsn_tns)  # if needed, place an 'r' before any parameter in order to address any special character such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

        c = conn.cursor()
        c.execute('select * from FORM1120_MASTER ORDER BY SEQ_NO')  # use triple quotes if you want to spread your query across multiple lines
        for row in c:
            label = row[0]
            if row[1] != 0:
                # print(row[0], '-', row[1]) # this only shows the first two columns. To add an additional column you'll need to add , '-', row[2], etc.
                cropped = img[row[2]:row[4], row[1]:row[3]]
                if row[5] == 'N':
                    obj = Tesseract.Tesseract(cropped)
                    result = obj.tesseract()

                    if row[7] == 'Y':
                        label = oldlabel
                        result = result.replace(" ", "")

                        if result == '':
                            result = oldresult +".00"
                        else:
                            result=oldresult+"."+result

                    oldlabel = label
                    oldresult = result

                else:
                    result = np.mean(cropped, axis=None)
                    if int(result) < 180:
                        result = 'Ticked'
                    else:
                        result = 'UnTicked'
                print(label + ': ' + str(result))
                datadict[label] = str(result)
                cv2.imwrite('C:/Users/H P/Desktop/UBSForm1120Extractor/intermediate/' + str(row[6]).zfill(4) +row[0] + '.jpg', cropped)
        conn.close()

        # cv2.imshow("cropped", cropped)
        # cv2.waitKey(0)
        print(datadict)
        return datadict