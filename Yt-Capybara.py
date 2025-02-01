# -*- encoding: utf-8 -*-
'''
@Time    :   2025/01/13 18:21:43
@File    :   Yt_Capybara.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   0.1.0
@Contact :   for_freedom_x64@live.com
'''

import sys, platform,os
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStatusBar
from PySide6.QtGui import QAction, QFont, QIcon, QPixmap, QPalette, QColor
from PySide6.QtCore import Qt, Slot
from parameterWidget import ParameterWidget
from cmdOperate import CmdOperate
from terminalWidget import TerminalWidget
from qfluentwidgets import qconfig, toggleTheme, setThemeColor, QConfig, ConfigItem


def getResourceConfigPath():
    BASEPATH, CONFIGPATH = '',  ''
    """获取资源文件的绝对路径,与程序实际运行目录有所区别"""
    if platform.system() == 'Windows':
        pass
    elif platform.system() ==  'win32':
        pass
    else:
        CONFIGPATH = os.path.join(os.path.expanduser('~'), '.config', 'Yt-Capybara', 'config.json')
        if platform.system() == 'Linux':
            # for pyinstaller:如果打包后运行， pyinstaller会在系统参数中添加'frozen'参数表示released文件，而 sys._MEIPASS 是程序的临时目录
            if getattr(sys, 'frozen', False):
                BASEPATH = sys._MEIPASS # + '----Linux1'
            else:
                BASEPATH = os.path.dirname(os.path.abspath(__file__))  # + '----Linux2'
        elif platform.system() == 'Darwin':
            if getattr(sys, 'frozen', False):
                # BASEPATH = sys._MEIPASS + '----Darwin1'# BASEPATH = sys._MEIPASS
                BASEPATH = os.path.dirname(os.path.abspath(__file__))   # + '----Darwin1'
            else:
                CONTENTSPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # app&terminal
                BASEPATH = os.path.join(CONTENTSPATH, 'Resources')      # + '----Darwin2'
        else:
            print('error')
    return BASEPATH, CONFIGPATH

class MyConfig(QConfig):
    """ Config of application """
    mainConfig1 = ConfigItem("Yt-aa", "key1", "value1")
    mainConfig2 = ConfigItem("Yt-aa", "key2", "value2")


class Yt_Capybara(QMainWindow):
    __instance = None

    def __new__(cls, *argu):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *argu)
        return cls.__instance

    def __init__(self, basePath:str=None, configPath:str=None):
        super().__init__()
        self.BASEPATH = basePath
        self.cmdOperate = CmdOperate()
        self.loadConfig(configPath)
        self.iniUI()

    def iniUI(self): 
        if qconfig.theme.value == 'Dark':
            self.setPalette(self.depictTheme(True))
        else:
            self.setPalette(self.depictTheme(False))
        self.mainWidget = ParameterWidget(self.cmdOperate.haveYt_dlp, 
                                          self.cmdOperate.haveFfmpeg, 
                                          self.cmdOperate.yt_dlpExe, 
                                          self.cmdOperate.ffmpegExe)
        
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('Yt-Capybara')
        self.setWindowIcon(QIcon(os.path.join(self.BASEPATH, 'icons', 'capybara.png')))
        self.createStatusBar()
        self.setConnections()
        setThemeColor('#2b67b1')

    def createStatusBar(self) -> None:   #设置状态栏
        self.yt_dlpIcon = QLabel()
        self.yt_dlpIcon.setFixedSize(10,10)
        self.yt_dlpIcon.setScaledContents(True)
        self.yt_dlpIcon.setToolTip('status of yt-dlp')
        self.yt_dlpIcon.setOpenExternalLinks(True)
        self.yt_dlpLabel = QLabel()
        self.yt_dlpLabel.setMinimumWidth(80)
        self.yt_dlpLabel.setToolTip('status of yt-dlp')
        self.yt_dlpLabel.setToolTip(self.cmdOperate.yt_dlpExe)
        if self.cmdOperate.haveYt_dlp:
            self.yt_dlpIcon.setStyleSheet('border-radius: 5px; border:1px solid #0000005e; background:#16e384')
            self.yt_dlpIcon.setStatusTip('installed yt-dlp')
            self.yt_dlpLabel.setText('Has yt-dlp')
            self.yt_dlpLabel.setStatusTip('installed yt-dlp')
        else:
            self.yt_dlpIcon.setStyleSheet('border-radius: 5px; border:1px solid #0000005e; background:#e44949')
            self.yt_dlpIcon.setStatusTip('have not installed yt-dlp')
            self.yt_dlpLabel.setText('No yt-dlp')
            self.yt_dlpLabel.setStatusTip('have not installed yt-dlp')

        self.ffmpegIcon = QLabel()
        self.ffmpegIcon.setFixedSize(10,10)
        self.ffmpegIcon.setScaledContents(True)
        self.ffmpegIcon.setToolTip('status of ffmpeg')
        self.ffmpegLabel = QLabel()
        self.ffmpegLabel.setMinimumWidth(80)
        self.ffmpegLabel.setToolTip('status of ffmpeg')
        self.ffmpegLabel.setToolTip(self.cmdOperate.ffmpegExe)

        if self.cmdOperate.haveFfmpeg:
            self.ffmpegIcon.setStyleSheet('border-radius: 5px; border:1px solid #0000005e; background:#16e384')
            self.ffmpegIcon.setStatusTip('installed ffmpeg')
            self.ffmpegLabel.setText('Has ffmpeg')
            self.ffmpegLabel.setStatusTip(' installed ffmpeg')
        else:
            self.ffmpegIcon.setStyleSheet('border-radius: 5px; border:1px solid #0000005e; background:#e44949')
            self.ffmpegIcon.setStatusTip('have not installed ffmpeg')
            self.ffmpegLabel.setText('No ffmpeg')
            self.ffmpegLabel.setStatusTip('have not installed ffmpeg')
        self.statusBar = QStatusBar()
        self.statusBar.setContentsMargins(0,1,10,2)
        self.statusBar.addPermanentWidget(self.yt_dlpIcon)
        self.statusBar.addPermanentWidget(self.yt_dlpLabel)
        self.statusBar.addPermanentWidget(self.ffmpegIcon)
        self.statusBar.addPermanentWidget(self.ffmpegLabel)
        self.setStatusBar(self.statusBar)

    def setConnections(self):
        self.mainWidget.message.connect(self.slotBarMessage)
        self.mainWidget.cmdLabel.clicked.connect(self.slotCopidBarMessage)
        self.mainWidget.downloadBtn.clicked.connect(self.slotDownloadTerminal)
        self.mainWidget.infoAction.triggered.connect(self.slotAbout)
        self.mainWidget.themeAction.triggered.connect(self.slotChangeTheme)

    def loadConfig(self, configPath:str):
        # print(configPath)
        # cfg= MyConfig()
        cfg= QConfig()
        # qconfig.load("config11/config12.json", cfg)
        qconfig.load(configPath, cfg)
        # print(cfg.get(cfg.mainConfig1))
        # print(cfg.mainConfig1)
        # print(qconfig.toDict())

    def depictTheme(self, isToDark:bool=True) -> QPalette:
        themePalette = self.palette()
        if isToDark:
            windowColor = QColor(65, 65, 65, 120)
            textColor = QColor(255, 255, 255)
        else:
            windowColor = QColor(250, 250, 255, 230)
            textColor = QColor(0, 0, 0)
        themePalette.setColor(QPalette.ColorRole.Window, windowColor)
        themePalette.setColor(QPalette.ColorRole.WindowText, textColor)
        return themePalette

    @Slot()
    def slotDownloadTerminal(self):
        self.downloadTerminal = TerminalWidget()
        self.downloadTerminal.signalQuit.connect(self.slotTerminalClose)
        self.downloadTerminal.show()
        self.downloadTerminal.runCommand(self.mainWidget.cmdLabel.text())
        self.mainWidget.downloadBtn.setEnabled(False)
        self.mainWidget.urlEditor.setPlaceholderText(self.mainWidget.urlEditor.text())
        self.mainWidget.urlEditor.clear()

    @Slot()
    def slotTerminalClose(self):
        self.mainWidget.downloadBtn.setEnabled(True)

    @Slot()
    def slotCopidBarMessage(self):
        self.statusBar.showMessage('Copied', 3000)

    @Slot()
    def slotBarMessage(self, info):
        self.statusBar.showMessage(info, 3000)

    @Slot()
    def slotChangeTheme(self):
        if qconfig.theme.value == 'Dark':       #Then toggle theme to light
            self.setPalette(self.depictTheme(False))
        else:               #Then toggle theme to dark
            self.setPalette(self.depictTheme(True))
        toggleTheme(True)

    @Slot()
    def slotQuit(self):
        sys.exit(0)

    @Slot()
    def slotAbout(self):
        aboutTitle = QLabel('<h1 style="Text-align: center;">Yt-Capybara</h1>')
        aboutTitle.setFixedHeight(40)
        infoLIcon = QLabel()
        infoLIcon.setPixmap(QPixmap(os.path.join(self.BASEPATH, 'icons', 'capybara.png')))
        infoLIcon.setScaledContents(True)
        infoLIcon.setFixedSize(220, 220)
        infoLIcon.setMargin(20)
        aboutText = QLabel(f'<table><tr><td colspan="2"><b>Yt-Capybara</b>为yt-dlp可视化程序。旨在简化操作，方便下载视频音频。</td></tr><tr><td colspan="2">项目地址:<a href="https://github.com/PanZK/Yt-Capybara">Yt-Capybara</a></td></tr><tr><td colspan="2">Yt-Capybara version: 0.0.1<br></td></tr><tr><td><b>编译环境</b></td><td><b>当前环境</b></td></tr><tr><td>Python version: 3.12.3</td><td><a href=https://github.com/yt-dlp/yt-dlp>yt-dlp</a> version: {self.cmdOperate.getYt_dlpVersion()}</td></tr><tr><td><a href=https://doc.qt.io/qtforpython-6>QPySide6</a> version: 6.8.1.1</td><td><a href=https://ffmpeg.org>ffmpeg</a> version: {self.cmdOperate.getFfmpegVersion()}</td></tr><tr><td><a href=https://qfluentwidgets.com>QFluentWidgets</a> version: 1.7.4</td></tr></table>')
        aboutText.setOpenExternalLinks(True)
        aboutText.setFixedWidth(500)
        aboutText.setMargin(10)
        aboutLayout = QHBoxLayout()
        aboutLayout.addWidget(infoLIcon)
        aboutLayout.addWidget(aboutText)
        aboutLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        aboutInfoLayout = QVBoxLayout()
        aboutInfoLayout.addWidget(aboutTitle)
        aboutInfoLayout.addLayout(aboutLayout)
        aboutInfoLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aboutInfo = QWidget()
        self.aboutInfo.setFixedSize(750, 400)
        self.aboutInfo.setLayout(aboutInfoLayout)
        if qconfig.theme.value == 'Dark':
            self.aboutInfo.setPalette(self.depictTheme(True))
        else:
            self.aboutInfo.setPalette(self.depictTheme(False))
        self.aboutInfo.show()

class MyApplication(QApplication):

    def __init__(self, arguments):
        super().__init__(arguments)
        self.setApplicationVersion('0.1.0')
        self.setOrganizationName('PanZK')
        self.setApplicationName("Yt-Capybara")


if __name__ == '__main__':
    BASEPATH, CONFIGPATH = getResourceConfigPath()
    app = MyApplication(sys.argv)
    if platform.system() == 'Darwin':
        app.setFont(QFont('Hiragino Sans GB'))  #防止mac系统上运行速度受阻，选用“冬青黑体简体中文”为默认字体
    app.setWindowIcon(QIcon(os.path.join(BASEPATH, 'icons', 'capybara.png')))
    exe = Yt_Capybara(BASEPATH, CONFIGPATH)
    exe.show()
    del exe
    sys.exit(app.exec())