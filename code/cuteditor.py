import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import numpy as np
from PIL import Image
from fileinput import filename
import webbrowser

import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("cuteditor.ui")
form_class = uic.loadUiType(form)[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.filebutton.clicked.connect(self.filebuttonFunction)
        self.margingo.clicked.connect(self.marginFunction)
        self.slicego.clicked.connect(self.sliceFunction)
        self.github.clicked.connect(self.GitHub)

    def GitHub(self):
        webbrowser.open('https://github.com/Sujin-Github/CutEditor')

    def filebuttonFunction(self):
        fname = QFileDialog.getOpenFileName(self, '', '', 'All File(*);; png(*.png) ;; jpg(*.jpg)')
        self.filecheck.setText(fname[0])
        impath = fname[0]
        im = Image.open(impath)
        width = im.size[0]
        height = im.size[1]
        im_array = np.array(im)
        WL = im_array[0]
        temp = 1
        mark = []
        for i in range(len(im_array)):
            line = im_array[i]
            if np.array_equal(line, WL):
                if temp == 1:
                    mark.append(i)
                temp = 0
            else:
                if temp == 0:
                    mark.append(i)
                temp = 1

        self.mark = mark
        self.height = height
        self.width = width
        self.impath = impath
        self.im = im

    def marginFunction(self):
        mark = self.mark
        height = self.height
        width = self.width
        impath = self.impath
        im = self.im

        marginsize = int(self.margin.text())
        savename = self.name.text()

        n = len(mark)
        bg = Image.new('RGB', (width, height + marginsize * n), (255, 255, 255))
        marginim = Image.new('RGB', (width, marginsize), (255, 255, 255))
        i = 0
        y = 0
        while i < n - 1:
            cuttemp = im.crop((0, mark[i], width, mark[i + 1]))
            bg.paste(cuttemp, (0, y))
            y = y + mark[i + 1] - mark[i]
            bg.paste(marginim, (0, y))
            y += marginsize
            i += 1
        saveas = impath[:-4] + '_' + savename + '.png'
        bg.save(saveas)
        self.margindone.setText(saveas + '로 저장되었습니다.')

    def sliceFunction(self):
        mark = self.mark
        height = self.height
        width = self.width
        impath = self.impath
        im = self.im
        savename = self.slicefolder.text()
        if savename:
            impath = impath[:impath.rfind('/')] + '/' + savename
            os.mkdir(impath)
        cut = []
        n = len(mark)
        i = 0
        if self.slicemargincheck.isChecked():
            while i < n - 1:
                cuttemp = im.crop((0, mark[i], width, mark[i + 2]))
                arrtemp = np.array(cuttemp)
                i += 2
                cut.append(arrtemp)
                saveas = impath + '/' + str(len(cut)).zfill(2) + '.png'
                Image.fromarray(arrtemp).save(saveas)
            if n % 2 == 1:
                cuttemp = im.crop((0, mark[i], width, height))
                arrtemp = np.array(cuttemp)
                cut.append(arrtemp)
                saveas = impath + '/' + str(len(cut)).zfill(2) + '.png'
                Image.fromarray(arrtemp).save(saveas)
        else:
            while i < n - 1:
                cuttemp = im.crop((0, mark[i], width, mark[i + 1]))
                arrtemp = np.array(cuttemp)
                i += 1
                if arrtemp.sum() != arrtemp.size * 255:
                    cut.append(arrtemp)
                    saveas = impath + '/' + str(len(cut)).zfill(2) + '.png'
                    Image.fromarray(arrtemp).save(saveas)
        self.slicedone.setText('저장되었습니다.')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.setWindowTitle('컷에디터')
    myWindow.setWindowIcon(QIcon('icon.ico'))
    myWindow.show()
    app.exec_()