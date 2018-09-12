# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aqi.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import * 
from pyecharts import GeoLines, Style
from PyQt5 import QtCore, QtWidgets
from qtpy.QtCore import QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView
from pyecharts import Geo,Line
import datetime
import sys
from opendatatools import aqi
import pandas as pd
sys.setrecursionlimit(5000)

local='长沙市'
lastcity=''
nowTime=(datetime.datetime.now()-datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H')#现在
day=(datetime.datetime.now()-datetime.timedelta(hours=1)).strftime('%Y-%m-%d')#当天
print (nowTime)
df_aqi = aqi.get_hour_aqi(nowTime)
aqi_hour = aqi.get_hour_aqi_onecity(local, day)
df_aqi.to_csv('aqi.csv')
aqi_hour.to_csv('daylocal.csv')
df_aqi=pd.read_csv('aqi.csv')
aqi_hour=pd.read_csv('daylocal.csv')
print (df_aqi)
print (aqi_hour)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(442, 824)
        Form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        Form.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton.setGeometry(QtCore.QRect(300, 754, 142, 70))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.commandLinkButton.setStyleSheet("background-color: rgb(209, 175, 222);\n""color: rgb(64, 0, 64);")

        self.commandLinkButton1 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton1.setGeometry(QtCore.QRect(0, 754, 142, 70))
        self.commandLinkButton1.setObjectName("commandLinkButton")
        self.commandLinkButton1.setStyleSheet("background-color: rgb(209, 175, 222);\n""color: rgb(64, 0, 64);")

        self.commandLinkButton.clicked.connect(self.select)
        self.commandLinkButton1.clicked.connect(self.analy)

        
        
        
        self.combobox = QtWidgets.QComboBox(Form)
        self.combobox.setGeometry(QtCore.QRect(146, 754, 140, 35))
        self.combobox.addItems(["AQI散点","AQI热图","分时AQI"])
        #self.combobox.currentIndexChanged.connect(self.analy)
        self.combobox.show()
        
        
        self.combobox1 = QtWidgets.QComboBox(Form)
        self.combobox1.setGeometry(QtCore.QRect(146, 794, 140, 35))
        self.combobox1.addItems(["逃脱路线","推荐城市"])
        self.combobox1.show()
        
        
        self.webView = QWebEngineView(Form)
        self.webView.setGeometry(0,0,440,750)
        self.webView.load(QUrl("file:///D:/源代码/aqi.html"))
       
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "逃离阴霾"))
        self.commandLinkButton.setText(_translate("Form", "\n获取AQI"))
        self.commandLinkButton1.setText(_translate("Form", "\n计划逃跑"))
    
    def analy(self,lastcity):
        if self.combobox1.currentText()==u"推荐城市":
            print('查看更多信息')
            self.best()
            
        if self.combobox1.currentText()==u"逃脱路线":
            print('逃脱')
            self.escape()

            #self.combobox.hide()
            #self.combobox.clear()
            
    def select(self):
        if self.combobox.currentText()==u"分时AQI":
            self.draw_city_aqi(nowTime)
        if self.combobox.currentText()==u"AQI散点":
            self.draw1(nowTime)
            #self.combobox.show()
        if self.combobox.currentText()==u"AQI热图":
            self.draw(nowTime)
        #if self.combobox1.currentText()==u"逃脱路线":
            
    #def draw2(self,time = None):
    def draw_city_aqi(self, time = None):
        #from opendatatools import aqi
        line = Line("长沙当日AQI",
                         width=425,
                         height=730)
        data_dict = {}
        city=local
        print("getting data for %s" % city)
        #df_aqi = aqi.get_daily_aqi_onecity(city)
        aqi_hour=pd.read_csv('daylocal.csv')
    
            #print(df_aqi)
            #print(aqi_hour)
        aqi_hour.set_index('time', inplace=True)
        aqi_hour.sort_index(ascending=True, inplace=True)
        if time is not None:
            aqi_hour = aqi_hour[aqi_hour.index <= time]
            
        data_dict[city] = aqi_hour
        axis_x = aqi_hour.index
        axis_y = aqi_hour['aqi']
        line.add("%s" % (city), axis_x, axis_y, mark_point=["max","min"])
        line.render('aqi.html')
        #return line

        self.webView.load(QUrl("file:///D:/源代码/aqi.html"))

       # self.webView.reload()
        self.webView.repaint()
        self.webView.update()
        
    def draw1(self,time = None):
        global local

        # some city cannot by process by echart
        echart_unsupported_city = [
        "菏泽市", "襄阳市", "恩施州", "湘西州","阿坝州", "延边州",
        "甘孜州", "凉山州", "黔西南州", "黔东南州", "黔南州", "普洱市", "楚雄州", "红河州",
        "文山州", "西双版纳州", "大理州", "德宏州", "怒江州", "迪庆州", "昌都市", "山南市",
        "林芝市", "临夏州", "甘南州", "海北州", "黄南州", "海南州", "果洛州", "玉树州", "海西州",
        "昌吉州", "博州", "克州", "伊犁哈萨克州"]
        if time is None and len(df_aqi) > 0:
            time = df_aqi['time'][0]
        data = []
        for index, row in df_aqi.iterrows():
            city = row['city']
            aqi = row['aqi']
            if city=='长沙市':
                print(city)
                localAQI=aqi
            if city in echart_unsupported_city:
                continue
            data.append( (city, aqi) )
        
        #lcaqi=''.join(localAQI)
        #print(lcaqi)
        if localAQI<70:
            geo = Geo("全国最新主要城市空气质量（AQI) \n 当前城市：长沙 AQI：%s \n \n您在的城市不错,不开心的话，也出去走走吧" % localAQI, "数据来源于环保部网站",
                     title_color="#fff",
                     title_pos="center", width=425,
                     height=730, background_color='#404a59')
        else:
            geo = Geo("全国最新主要城市空气质量（AQI) \n 当前城市：长沙 AQI：%s \n \n环境很差！！出去走走吧,已经为您规划路线" % localAQI, "数据来源于环保部网站",
                     title_color="#fff",
                     title_pos="center", width=425,
                     height=730, background_color='#404a59')
                 
        attr, value = geo.cast(data)
        
        geo.add("", attr, value, visual_range=[0, 150],
            maptype='china',visual_text_color="#fff",
            symbol_size=10, is_visualmap=True,
            label_formatter='{b}', # 指定 label 只显示城市名
            tooltip_formatter='{c}', # 格式：经度、纬度、值
            label_emphasis_textsize=15, # 指定标签选中高亮时字体大小
            label_emphasis_pos='right' # 指定标签选中高亮时字体位置
            )
        #print(data)
        geo.render('aqi.html')
        self.webView.load(QUrl("file:///D:/源代码/aqi.html"))

        #self.webView.reload()
        self.webView.repaint()
        self.webView.update()
        #return geo        
    def draw(self,time = None):
        
        # some city cannot by process by echart
        echart_unsupported_city = [
        "菏泽市", "襄阳市", "恩施州", "湘西州","阿坝州", "延边州",
        "甘孜州", "凉山州", "黔西南州", "黔东南州", "黔南州", "普洱市", "楚雄州", "红河州",
        "文山州", "西双版纳州", "大理州", "德宏州", "怒江州", "迪庆州", "昌都市", "山南市",
        "林芝市", "临夏州", "甘南州", "海北州", "黄南州", "海南州", "果洛州", "玉树州", "海西州",
        "昌吉州", "博州", "克州", "伊犁哈萨克州"]
        if time is None and len(df_aqi) > 0:
            time = df_aqi['time'][0]
        data = []
        for index, row in df_aqi.iterrows():
            city = row['city']
            aqi = row['aqi']
            if city=='长沙市':
                print(city)
                localAQI=aqi
            if city in echart_unsupported_city:
                continue
            data.append( (city, aqi) )
            
            
        if localAQI<70:
            geo = Geo("全国最新主要城市空气质量（AQI) \n 当前城市：长沙 AQI：%s \n \n您在的城市不错,不开心的话，也出去走走吧" % localAQI, "数据来源于环保部网站",
                     title_color="#fff",
                     title_pos="center", width=425,
                     height=730, background_color='#404a59')
        else:
            
            geo = Geo("全国最新主要城市空气质量（AQI) \n 当前城市：长沙 AQI：%s \n \n环境很差！！出去走走吧,已经为您规划路线" % localAQI, "数据来源于环保部网站",
                     title_color="#fff",
                     title_pos="center", width=425,
                     height=730, background_color='#404a59')
                 
        attr, value = geo.cast(data)
        geo.add("", attr, value, type="heatmap", is_visualmap=True, visual_range=[0, 600],
        visual_text_color='#fff')
        #print(data)
        geo.render('aqi.html')
        self.webView.load(QUrl("file:///D:/源代码/aqi.html"))

        #self.webView.reload()
        self.webView.repaint()
        self.webView.update()
        #return geo
        
    def escape(self):
        echart_unsupported_city = [
        "菏泽市", "襄阳市", "恩施州", "湘西州","阿坝州", "延边州",
        "甘孜州", "凉山州", "黔西南州", "黔东南州", "黔南州", "普洱市", "楚雄州", "红河州",
        "文山州", "西双版纳州", "大理州", "德宏州", "怒江州", "迪庆州", "昌都市", "山南市",
        "林芝市", "临夏州", "甘南州", "海北州", "黄南州", "海南州", "果洛州", "玉树州", "海西州",
        "昌吉州", "博州", "克州", "伊犁哈萨克州"]

        data = []
        
        for index, row in df_aqi.iterrows():
            city = row['city']
            aqi = row['aqi']
            if city=='长沙市':
                print(city)
                localAQI=aqi
            if city in echart_unsupported_city:
                continue
        for index, row in df_aqi.iterrows():
            city = row['city']
            aqi = row['aqi']
            if city in echart_unsupported_city:
                continue
            if aqi < localAQI and aqi<20 :
                data.append( ['长沙',city] )
                global lastcity
                lastcity=city
                                
        style = Style(
            title_top="#fff",
            title_pos = "center",
            title_color="#fff",
            width=425,
            height=730,
            background_color="#404a59"
        )
        
        style_geo = style.add(
            is_label_show=True,
            line_curve=0.2,#线条曲度
            line_opacity=0.6,
            legend_text_color="#fff",#图例文字颜色
            legend_pos="right",#图例位置
            geo_effect_symbol="plane",#特效形状
            geo_effect_symbolsize=15,#特效大小
            label_color=['#a6c84c', '#ffa022', '#46bee9'],
            label_pos="right",
            label_formatter="{b}",#//标签内容格式器
            label_text_color="#fff",
        )
        print(data)
        print(lastcity)
        geolines = GeoLines("逃离路线", **style.init_style)
        geolines.add("出发", data, **style_geo)
        geolines.render('aqi.html')
        
        self.webView.load(QUrl("file:///D:/源代码/aqi.html"))
        #self.webView.reload()
        self.webView.repaint()
        self.webView.update()
    
    def best(self):
        global lastcity
        url='https://m.baidu.com/s?from=1019146b&bd_page_type=1&word='+lastcity
        print(url)
        self.webView.load(QUrl(url))
        #self.webView.reload()

        self.webView.repaint()
        self.webView.update()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()                
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    #MainWindow.setWindowTitle('逃离阴霾')
    MainWindow.show()
    
    sys.exit(app.exec_())
