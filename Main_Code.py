from Main import Main_UI;
from ARF import ARF_UI;
from Paraplegia import Para;
from PyQt5 import QtWidgets
import os
from sklearn.externals import joblib
import numpy as np;
from sklearn.ensemble import RandomForestClassifier;
from sklearn.svm import SVC;
from sklearn.preprocessing import MinMaxScaler
import sys

#Not num then throw the exception
def isNum(value):
    try:
        x = float(value)
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception as e:
        return False
    else:
        return True

def check(parent):
    for i in range(1,12):
        if not isNum(getattr(parent,"textEdit_%d"%i).toPlainText()):
            return False
    if (not parent.radioButton.isChecked()) and (not parent.radioButton_2.isChecked()):
        return False
    if (not parent.radioButton_3.isChecked()) and (not parent.radioButton_4.isChecked()):
        return False
    if (not parent.radioButton_5.isChecked()) and (not parent.radioButton_6.isChecked()):
        return False
    if (not parent.radioButton_7.isChecked()) and (not parent.radioButton_8.isChecked()):
        return False
    if (not parent.radioButton_9.isChecked()) and (not parent.radioButton_10.isChecked()):
        return False
    return True

def check2(parent):
    if not isNum(getattr(parent,"textEdit_1").toPlainText()):
        return False
    for i in range(3,12):
        if not isNum(getattr(parent,"textEdit_%d"%i).toPlainText()):
            return False
    if (not parent.radioButton.isChecked()) and (not parent.radioButton_2.isChecked()):
        return False
    if (not parent.radioButton_3.isChecked()) and (not parent.radioButton_4.isChecked()):
        return False
    if (not parent.radioButton_5.isChecked()) and (not parent.radioButton_6.isChecked()):
        return False
    if (not parent.radioButton_7.isChecked()) and (not parent.radioButton_8.isChecked()):
        return False
    if (not parent.radioButton_9.isChecked()) and (not parent.radioButton_10.isChecked()):
        return False
    if (not parent.radioButton_11.isChecked()) and (not parent.radioButton_12.isChecked()):
        return False
    return True


class myMain(QtWidgets.QWidget, Main_UI):
    def __init__(self):
        super(myMain,self).__init__()
        self.new = Main_UI()
        self.setupUi(self)
        self.myarf = myARF()
        self.mypara = myPara()

    def Aki_pressed(self):
        self.myarf.show()
        app.exec()
    def Para_pressed(self):
        self.mypara.show()
        app.exec()

class myARF(QtWidgets.QWidget,ARF_UI):
    def __init__(self):
        super(myARF,self).__init__()
        self.new = ARF_UI()
        self.setupUi(self)

    tmp =[]
    def arf_predict(self):
        if check(self):
            path_AKI_scaler = os.path.split(os.path.realpath(__file__))[0] + os.sep + "aki_scaler"
            aki_scaler = joblib.load(path_AKI_scaler)
            path_AKI = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'AKImodel.pkl'
            akimodel = joblib.load(path_AKI)
            #Right Renal Artery Block Time(min)
            self.tmp.append(float(self.textEdit_1.toPlainText()))
            #PreOperation Serum Creatinine(μmoI/L)
            self.tmp.append(float(self.textEdit_2.toPlainText()))
            #age
            self.tmp.append(float(self.textEdit_3.toPlainText()))
            #sex female =1 male =2
            if self.radioButton.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(2)
            #hypertension
            if self.radioButton_3.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            #Marfan
            if self.radioButton_5.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            #PreCardiacOperation Times
            self.tmp.append(float(self.textEdit_4.toPlainText()))
            #Ranal Artery Involved by Dissection
            if self.radioButton_7.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            #Opeartion Time(hour)
            self.tmp.append(float(self.textEdit_5.toPlainText()))
            #CSFD
            if self.radioButton_9.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            #RBC(unit)
            self.tmp.append(float(self.textEdit_6.toPlainText()))
            #Plasm(ml)
            self.tmp.append(float(self.textEdit_7.toPlainText()))
            #Platelet(unit)
            self.tmp.append(float(self.textEdit_8.toPlainText()))
            #Bleeding(ml)
            self.tmp.append(float(self.textEdit_9.toPlainText()))
            #Highest LDH During the Opeartion
            self.tmp.append(float(self.textEdit_10.toPlainText()))
            #BMI
            self.tmp.append(float(self.textEdit_11.toPlainText()))
            #Data Operation
            self.tmp = np.array(self.tmp)
            data_predict = np.vstack((self.tmp,self.tmp))
            data_predict = aki_scaler.transform(data_predict)
            #data_predict = aki_scaler.transform(self.tmp)
            #Predict
            #if akimodel.predict(data_predict[0,:])[0] == 1:
            predicted = akimodel.predict(data_predict)
            if akimodel.predict(data_predict)[0] == 1:
                infromation = "The patient would suffer from AKI, please evaluate the necessity of CRRT"
            else:
                infromation = "The patient may not suffer from AKI"
            QtWidgets.QMessageBox.information(self,"Predicted",infromation,QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please fulfill the features correctly",QtWidgets.QMessageBox.Ok);


class myPara(QtWidgets.QWidget,Para):
    def __init__(self):
        super(myPara,self).__init__()
        self.new = Para()
        self.setupUi(self)
    tmp = []
    def para_predict(self):
        if check2(self):
            path_para_scaler = os.path.split(os.path.realpath(__file__))[0] + os.sep + "para_scaler"
            para_scaler = joblib.load(path_para_scaler)
            path_Para = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'Paraplegia_model.pkl'
            Paramodel = joblib.load(path_Para)
            #Opration-time
            self.tmp.append(float(self.textEdit_5.toPlainText()))
            #ICA  Block Time(min)
            self.tmp.append(float(self.textEdit_1.toPlainText()))
            # age
            self.tmp.append(float(self.textEdit_3.toPlainText()))
            # sex female =0 male =1
            if self.radioButton.isChecked():
                self.tmp.append(0)
            else:
                self.tmp.append(1)
            # hypertension
            if self.radioButton_3.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            # Marfan
            if self.radioButton_5.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            # PreCardiacOperation Times
            self.tmp.append(float(self.textEdit_4.toPlainText()))
            # CTA-Dissection
            if self.radioButton_11.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            # RA-Dissection
            if self.radioButton_7.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            # CSFD
            if self.radioButton_9.isChecked():
                self.tmp.append(1)
            else:
                self.tmp.append(0)
            # RBC(unit)
            self.tmp.append(float(self.textEdit_6.toPlainText()))
            # Plasm(ml)
            self.tmp.append(float(self.textEdit_7.toPlainText()))
            # Platelet(unit)
            self.tmp.append(float(self.textEdit_8.toPlainText()))
            # Bleeding(ml)
            self.tmp.append(float(self.textEdit_9.toPlainText()))
            # Highest LDH During the Opeartion
            self.tmp.append(float(self.textEdit_10.toPlainText()))
            # BMI
            self.tmp.append(float(self.textEdit_11.toPlainText()))
            # Data Operation
            data_predict = np.vstack((self.tmp, self.tmp))
            data_predict = para_scaler.transform(data_predict)
            # Predict
            if Paramodel.predict(data_predict[0,:])[0] == 1:
                infromation = "The patient would suffer from Paraplegia, please deal with it"
            else:
                infromation = "The patient may not suffer from Paraplegia"
            QtWidgets.QMessageBox.information(self, "Predicted", infromation, QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please fulfill the features correctly", QtWidgets.QMessageBox.Ok);

app=QtWidgets.QApplication(sys.argv)
mymain = myMain();
mymain.show()
sys.exit(app.exec_())
