# -*- encoding: utf-8 -*-
'''
@Time    :   2025/01/13 20:44:43
@File    :   parameterWidget.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   0.1.0
@Contact :   for_freedom_x64@live.com
'''

import sys, os, re, platform
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QRadioButton, QButtonGroup, QCheckBox, QComboBox, QFileDialog, QCompleter, QFileSystemModel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal, Slot
from qfluentwidgets import PushButton, CheckBox, RadioButton, ComboBox, LineEdit, CommandBar, Action, FluentIcon, BodyLabel, StrongBodyLabel

browsersList = ['None', 'firefox', 'chrome', 'edge']

def validateUrl(url):
    pattern = re.compile(r'^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]{2,4}(/\S*)?$')
    return bool(pattern.match(url))


class ParameterWidget(QWidget):
    message = Signal(str)
    videoAndAudio = True

    def __init__(self, haveYt_dlp:bool=False, haveFfmpeg:bool=False, yt_dlpExe:str='yt-dlp', ffmpegExe:str='ffmpeg'):
        super().__init__()
        self.haveYt_dlp, self.haveFfmpeg, self.yt_dlpExe, self.ffmpegExe = haveYt_dlp, haveFfmpeg, yt_dlpExe, ffmpegExe
        self.initUI()
        self.setConnections()

    
    def initUI(self):
        commandBar = CommandBar()
        commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # 逐个添加动作
        self.themeAction = Action(FluentIcon.CONSTRACT, 'Toggle theme', checkable=True)
        self.themeAction.setStatusTip('Toggle theme')
        commandBar.addAction(Action(FluentIcon.PENCIL_INK, 'Generate', triggered=self.slotGenerateCmd))
        self.infoAction = Action(FluentIcon.INFO, 'Yt-Capybara')
        self.infoAction.setStatusTip('About')
        commandBar.addAction(self.themeAction)
        # 添加分隔符

        commandBar.addAction(self.infoAction)
        self.setFixedHeight(600)
        self.setMinimumWidth(900)
        # self.setMinimumSize(900,500)
        self.urlEditor = LineEdit()
        self.urlEditor.setPlaceholderText('url')
        self.generateBtn = PushButton('Generate')
        self.generateBtn.setFixedWidth(100)
        urlLayout = QHBoxLayout()
        urlLayout.addWidget(self.urlEditor)
        urlLayout.addWidget(self.generateBtn)
        formLayout = QFormLayout()
        formLayout.setSpacing(15)
        formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        # Options begin
        self.OptionsLabel = StrongBodyLabel('<h3>Options</h3>')
        self.OptionsLabel.setFixedHeight(50)
        self.OptionsLabel.setMargin(10)
        formLayout.addRow(self.OptionsLabel)
        self.presetComboBox = ComboBox()
        self.presetComboBox.addItems(['Best'])
        quitWithAria2Layout = QHBoxLayout()
        quitWithAria2Layout.addWidget(self.presetComboBox)
        quitWithAria2Layout.addStretch(10)
        formLayout.addRow(BodyLabel('Preset'), quitWithAria2Layout)
        #设置目录补全
        completer = QCompleter()
        model = QFileSystemModel()
        model.setRootPath(os.path.expanduser('~/Downloads'))
        completer.setModel(model)
        # self.pathLineEdit = QLineEdit(self.getDownloadDir())
        self.pathLineEdit = LineEdit()
        self.pathLineEdit.setPlaceholderText('Current path')
        self.pathLineEdit.setCompleter(completer)
        self.pathLineEdit.setMinimumWidth(450)
        self.pathBtn = PushButton('Choose dir')
        self.pathBtn.setFixedWidth(100)
        pathLayout = QHBoxLayout()
        pathLayout.addWidget(self.pathLineEdit)
        pathLayout.addWidget(self.pathBtn)
        formLayout.addRow(BodyLabel('Current download path'), pathLayout)
        self.proxyLineEdit = LineEdit()
        self.proxyLineEdit.setPlaceholderText('socks5://user:pass@127.0.0.1:1080/')
        self.proxyLineEdit.setMinimumWidth(450)
        self.proxyLineEdit.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        formLayout.addRow(BodyLabel('Proxy'), self.proxyLineEdit)

        videoBtn = RadioButton('Video and audio')
        videoBtn.setChecked(True)
        videoBtn.setFixedWidth(150)
        audioBtn = RadioButton('Audio only')
        self.voraGroup = QButtonGroup()
        self.voraGroup.addButton(videoBtn, 0)
        self.voraGroup.addButton(audioBtn, 1)
        self.voraGroup.setExclusive(True)
        voraLayout = QHBoxLayout()
        voraLayout.addWidget(videoBtn)
        voraLayout.addWidget(audioBtn)
        voraLayout.addStretch(1)
        voraLayout.setContentsMargins(20, 5, 20, 5)
        formLayout.addRow(BodyLabel('Video or audio'), voraLayout)
        self.transcodeChckBx = CheckBox('Transcode to mp4')
        self.transcodeChckBx.setEnabled(self.haveFfmpeg)
        self.thumbnailChckBx = CheckBox('Insert thumbnail')
        self.thumbnailChckBx.setChecked(True)
        self.metadataChckBx = CheckBox('Meta data')
        self.metadataChckBx.setChecked(True)
        self.subsChckBx = CheckBox('Subs')
        checkBoxesLayout = QGridLayout()
        checkBoxesLayout.addWidget(self.transcodeChckBx, 0, 0)
        checkBoxesLayout.addWidget(self.thumbnailChckBx, 0, 1)
        hSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        checkBoxesLayout.addItem(hSpacer, 0, 2)
        checkBoxesLayout.setContentsMargins(20, 10, 20, 10)        
        checkBoxesLayout.addWidget(self.metadataChckBx, 1, 0)
        checkBoxesLayout.addWidget(self.subsChckBx, 1, 1)
        checkBoxesLayout.setContentsMargins(20, 5, 20, 5)
        formLayout.addRow(BodyLabel('Video options'), checkBoxesLayout)
        self.cookiesComboBox = ComboBox()
        self.cookiesComboBox.addItems(browsersList)
        formLayout.addRow(BodyLabel('Cookies options'), self.cookiesComboBox)
        commandTitleLabel = StrongBodyLabel('<h3>Command</h3>')
        commandTitleLabel.setFixedHeight(20)
        commandTitleLabel.setContentsMargins(0,0,0,0)
        formLayout.addRow(commandTitleLabel)
        self.downloadBtn = PushButton('Download')
        self.downloadBtn.setToolTip('Download video')
        self.downloadBtn.setStatusTip('Download video by yt-dlp in terminal')
        self.downloadBtn.setEnabled(False)
        self.downloadBtn.setFixedSize(160, 40)
        self.cmdLabel = CmdLabel(self.yt_dlpExe)
        self.cmdLabel.setMinimumWidth(200)
        self.cmdLabel.setFixedHeight(80)
        self.cmdLabel.setContentsMargins(20,10,20,10)
        self.cmdLabel.setStatusTip('Click to copy command')
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.cmdLabel,3)
        bottomLayout.addWidget(self.downloadBtn,1)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(commandBar)
        mainLayout.addLayout(urlLayout)
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)

    def setConnections(self):
        self.urlEditor.returnPressed.connect(self.slotGenerateCmd)
        self.generateBtn.clicked.connect(self.slotGenerateCmd)
        self.pathBtn.clicked.connect(self.slotDir)
        self.voraGroup.idClicked.connect(self.slotVorA)

        self.urlEditor.textChanged.connect(self.slotUrlCheck)
        self.urlEditor.textEdited.connect(self.slotParamererChanged)
        self.presetComboBox.currentIndexChanged.connect(self.slotParamererChanged)
        self.pathLineEdit.textChanged.connect(self.slotParamererChanged)
        self.proxyLineEdit.textEdited.connect(self.slotParamererChanged)
        self.voraGroup.idClicked.connect(self.slotParamererChanged)
        self.transcodeChckBx.checkStateChanged.connect(self.slotParamererChanged)
        self.thumbnailChckBx.checkStateChanged.connect(self.slotParamererChanged)
        self.metadataChckBx.checkStateChanged.connect(self.slotParamererChanged)
        self.subsChckBx.checkStateChanged.connect(self.slotParamererChanged)
        self.cookiesComboBox.currentIndexChanged.connect(self.slotParamererChanged)

    def setOptionsByVorA(self, VandA:bool):
        self.transcodeChckBx.setEnabled(VandA)
        self.thumbnailChckBx.setEnabled(VandA)
        self.metadataChckBx.setEnabled(VandA)
        self.subsChckBx.setEnabled(VandA)

    def getDownloadDir(self):
        if platform.system() == 'Windows':
            return os.path.join(os.path.expanduser('~'), 'Downloads')
        if platform.system() == 'Darwin':
            return os.path.join(os.path.expanduser('~'), 'Downloads')
        if platform.system() == 'Linux':
            return os.path.join(os.path.expanduser('~'), 'Downloads')
        else:
            return None

    @Slot()
    def slotGenerateCmd(self):
        url = self.urlEditor.text()
        if not validateUrl(url):
            self.message.emit('Invalid url')
            return
        if url == '':
            if self.urlEditor.placeholderText() == 'url' or self.urlEditor.placeholderText() == '':
                self.message.emit('Empty url')
                return
            else:
                self.urlEditor.setText(self.urlEditor.placeholderText())
                url = self.urlEditor.placeholderText()

        # cmd = 'yt-dlp '
        cmd = self.yt_dlpExe + ' '
        if self.presetComboBox.currentIndex() == 0:
            preset = " bestvideo+bestaudio"
        proxy = ''
        if self.proxyLineEdit.text() != '':
            proxy = f' --proxy "{self.proxyLineEdit.text()}"'
        path = os.path.join(os.path.expanduser('~'), '')
        if self.pathLineEdit.text() != '':
            path = os.path.join(self.pathLineEdit.text(), '')
        cookies = ''
        if self.cookiesComboBox.currentIndex() != 0:
            cookies = f' --cookies-from-browser {browsersList[self.cookiesComboBox.currentIndex()]}'
        if self.videoAndAudio:
            thumbnail = ''
            if self.thumbnailChckBx.isChecked():
                thumbnail = ' --embed-thumbnail'
            metadata = ''
            if self.metadataChckBx.isChecked():
                metadata = ' --embed-metadata'
            subs = ''
            if self.subsChckBx.isChecked():
                subs = ' --embed-subs'
            transcode = ''
            if self.transcodeChckBx.isChecked():
                if self.ffmpegExe == 'ffmpeg':
                    transcode = ' --merge-output-format mp4'
                else:
                    transcode = f' --merge-output-format mp4 --ffmpeg-location "{self.ffmpegExe}"'
            cmd += f'-f{preset}{cookies}{proxy}{thumbnail}{metadata}{subs}{transcode} -o "{path}%(title)s.%(ext)s" "{url}"'
        else:
            cmd += f'-x --audio-format mp3 "{url}"{cookies}{proxy} -o "{path}%(title)s.%(ext)s"'
        self.cmdLabel.setText(cmd)
        self.message.emit('Generated cmd')

        if self.haveYt_dlp:
            self.downloadBtn.setEnabled(True)

    @Slot()
    def slotUrlCheck(self, url):
        if not validateUrl(url):
            self.cmdLabel.setText(self.yt_dlpExe)

    @Slot()
    def slotDir(self):
        path = QFileDialog.getExistingDirectory(self,'Open dir', self.pathLineEdit.text(), QFileDialog.Option.ShowDirsOnly)
        if path != '':
            self.pathLineEdit.setText(path)

    @Slot()
    def slotVorA(self, id):
        if id ==0 :
            self.videoAndAudio = True
            self.setOptionsByVorA(True)
        else:
            self.videoAndAudio = False
            self.setOptionsByVorA(False)

    @Slot()
    def slotParamererChanged(self):
        if self.downloadBtn.isEnabled():
            self.slotGenerateCmd()


class CmdLabel(QLabel):
    clicked = Signal()

    def __init__(self, argu):
        super().__init__(argu)
        self.setWordWrap(True)
        self.setStyleSheet('CmdLabel{border: 1px solid #919191;border-radius: 5px;color:#dbdbdb;background-color:#031c0a}')

    # rebuild the event of mouse lef button clicked, to copy download commond to clipboard.
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.text())
            self.clicked.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = ParameterWidget(True, True)
    exe.urlEditor.setText('https://www.bilibili.com/video/BV1wA411H7x3')
    exe.show()
    sys.exit(app.exec())