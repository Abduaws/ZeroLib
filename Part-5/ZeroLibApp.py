import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from HTMLBuilder import HTMLBuilder
from SparqlQueryHelper import SparqlQueryHelper
from LLMClient import LLMClient


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()


class UniversityLibWorker(QtCore.QThread):
    done = QtCore.pyqtSignal(str, bool)
    error = QtCore.pyqtSignal(Exception)

    def __init__(self, window, userInput, inputType):
        super().__init__()
        self.window = window
        self.userInput = userInput
        self.inputType = inputType

    def run(self):
        try:
            if self.inputType == 'query':
                htmlResult = HTMLBuilder().TestHTML
                query = self.window.modelOutput.toPlainText()
                if query is not None:
                    sparqlQueryHelper = SparqlQueryHelper()
                    htmlResult = HTMLBuilder().buildHTML(
                        sparqlQueryHelper.executeUniversityQuery(
                            query
                        ),
                        True
                    )
                self.done.emit(htmlResult, False)
            else:
                responseString = " "
                results = self.window.llmClient.sendPrompt(self.userInput)
                for chunk in results:
                    if 'content' in chunk['choices'][0]['delta']:
                        for char in chunk['choices'][0]['delta']['content']:
                            responseString += char
                            self.done.emit(responseString, False)
                self.done.emit(responseString, True)
        except Exception as exception:
            self.error.emit(exception)


class MovieLibWorker(QtCore.QThread):
    done = QtCore.pyqtSignal(str, bool)
    error = QtCore.pyqtSignal(Exception)

    def __init__(self, window, movieName, movieActor=None, movieDirector=None, movieGenre=None):
        super().__init__()
        self.window = window
        self.movieName = movieName
        self.movieActor = movieActor
        self.movieDirector = movieDirector
        self.movieGenre = movieGenre

    def run(self):
        try:
            if self.movieActor is None:
                sparqlQueryHelper = SparqlQueryHelper()
                htmlResult = HTMLBuilder().buildHTML(
                    sparqlQueryHelper.executeQuery(
                        sparqlQueryHelper.buildQuery(regex_filter=self.movieName)
                    )
                )
            else:
                sparqlQueryHelper = SparqlQueryHelper()
                htmlResult = HTMLBuilder().buildHTML(
                    sparqlQueryHelper.executeQuery(
                        sparqlQueryHelper.buildQuery(regex_filter=self.movieName,
                                                     actor_filter=self.movieActor,
                                                     genre_filter=self.movieGenre,
                                                     director_filter=self.movieDirector,
                                                     modes=[self.window.filter1State, self.window.filter2State,
                                                            self.window.filter3State, self.window.filter4State])
                    )
                )
            self.done.emit(htmlResult, False)
        except Exception as exception:
            self.error.emit(exception)


class ZeroLibApp(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 722)
        MainWindow.setFixedSize(1020, 722)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("resources/appLogo.png")))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color:#181818;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1021, 691))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
        self.searchBtn2 = QtWidgets.QPushButton(self.page1)
        self.searchBtn2.setGeometry(QtCore.QRect(330, 520, 321, 81))
        self.searchBtn2.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.searchBtn2.setFont(font)
        self.searchBtn2.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:25")
        self.searchBtn2.setObjectName("searchBtn2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.page1)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 110, 981, 401))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white;padding-right:45")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.titleInput = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.titleInput.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        self.titleInput.setFont(font)
        self.titleInput.setStyleSheet("background-color:#292929;border-radius:25%;color:#00ACC1;text-align:center;")
        self.titleInput.setText("")
        self.titleInput.setAlignment(QtCore.Qt.AlignCenter)
        self.titleInput.setObjectName("titleInput")
        self.horizontalLayout_5.addWidget(self.titleInput)
        self.filter1Btn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.filter1Btn.setMinimumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.filter1Btn.setFont(font)
        self.filter1Btn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;border: 1px solid white;margin-left: 10px")
        self.filter1Btn.setObjectName("filter1Btn")
        self.horizontalLayout_5.addWidget(self.filter1Btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:white;padding-right:25")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.actorInput = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.actorInput.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        self.actorInput.setFont(font)
        self.actorInput.setStyleSheet("background-color:#292929;border-radius:25%;color:#00ACC1;text-align:center;")
        self.actorInput.setText("")
        self.actorInput.setAlignment(QtCore.Qt.AlignCenter)
        self.actorInput.setObjectName("actorInput")
        self.horizontalLayout_2.addWidget(self.actorInput)
        self.filter2Btn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.filter2Btn.setMinimumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.filter2Btn.setFont(font)
        self.filter2Btn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;border: 1px solid white;margin-left: 10px")
        self.filter2Btn.setObjectName("filter2Btn")
        self.horizontalLayout_2.addWidget(self.filter2Btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white;")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.directorInput = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.directorInput.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        self.directorInput.setFont(font)
        self.directorInput.setStyleSheet("background-color:#292929;border-radius:25%;color:#00ACC1;text-align:center;")
        self.directorInput.setText("")
        self.directorInput.setAlignment(QtCore.Qt.AlignCenter)
        self.directorInput.setObjectName("directorInput")
        self.horizontalLayout_3.addWidget(self.directorInput)
        self.filter3Btn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.filter3Btn.setMinimumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.filter3Btn.setFont(font)
        self.filter3Btn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;border: 1px solid white;margin-left: 10px")
        self.filter3Btn.setObjectName("filter3Btn")
        self.horizontalLayout_3.addWidget(self.filter3Btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:white;padding-right:24")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.genreInput = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.genreInput.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        self.genreInput.setFont(font)
        self.genreInput.setStyleSheet("background-color:#292929;border-radius:25%;color:#00ACC1;text-align:center;")
        self.genreInput.setText("")
        self.genreInput.setAlignment(QtCore.Qt.AlignCenter)
        self.genreInput.setObjectName("genreInput")
        self.horizontalLayout_4.addWidget(self.genreInput)
        self.filter4Btn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.filter4Btn.setMinimumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.filter4Btn.setFont(font)
        self.filter4Btn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;border: 1px solid white;margin-left: 10px")
        self.filter4Btn.setObjectName("filter4Btn")
        self.horizontalLayout_4.addWidget(self.filter4Btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.backBtn = QtWidgets.QPushButton(self.page1)
        self.backBtn.setGeometry(QtCore.QRect(939, 30, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.backBtn.setFont(font)
        self.backBtn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;")
        self.backBtn.setObjectName("backBtn")
        self.stackedWidget.addWidget(self.page1)
        self.page2 = QtWidgets.QWidget()
        self.page2.setObjectName("page2")
        self.advancedSearchBtn = QtWidgets.QPushButton(self.page2)
        self.advancedSearchBtn.setGeometry(QtCore.QRect(400, 520, 201, 51))
        self.advancedSearchBtn.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.advancedSearchBtn.setFont(font)
        self.advancedSearchBtn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:25")
        self.advancedSearchBtn.setObjectName("advancedSearchBtn")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.page2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 190, 991, 301))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(25, -1, 25, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(resource_path("./resources/logo.png")))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:#888888;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.mainMoveInput = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.mainMoveInput.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        self.mainMoveInput.setFont(font)
        self.mainMoveInput.setStyleSheet("background-color:#292929;border-radius:25%;color:#00ACC1;text-align:center;")
        self.mainMoveInput.setAlignment(QtCore.Qt.AlignCenter)
        self.mainMoveInput.setObjectName("mainMoveInput")
        self.horizontalLayout_6.addWidget(self.mainMoveInput)
        self.searchBtn = ClickableLabel(self.horizontalLayoutWidget)
        self.searchBtn.setMaximumSize(QtCore.QSize(30, 30))
        self.searchBtn.setText("")
        self.searchBtn.setPixmap(QtGui.QPixmap(resource_path("./resources/searchpng.png")))
        self.searchBtn.setScaledContents(True)
        self.searchBtn.setObjectName("searchBtn")
        self.horizontalLayout_6.addWidget(self.searchBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.backBtn_4 = QtWidgets.QPushButton(self.page2)
        self.backBtn_4.setGeometry(QtCore.QRect(930, 10, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.backBtn_4.setFont(font)
        self.backBtn_4.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;")
        self.backBtn_4.setObjectName("backBtn_4")
        self.stackedWidget.addWidget(self.page2)
        self.page3 = QtWidgets.QWidget()
        self.page3.setObjectName("page3")
        self.backBtn_2 = QtWidgets.QPushButton(self.page3)
        self.backBtn_2.setGeometry(QtCore.QRect(940, 30, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.backBtn_2.setFont(font)
        self.backBtn_2.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;")
        self.backBtn_2.setObjectName("backBtn_2")
        self.browser = QWebEngineView(self.page3)
        self.browser.setGeometry(QtCore.QRect(20, 90, 981, 601))
        self.browser.setObjectName("browser")

        self.label_7 = QtWidgets.QLabel(self.page3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QtCore.QRect(20, 20, 141, 51))
        font8 = QtGui.QFont()
        font8.setFamily(u"Comic Sans MS")
        font8.setPointSize(24)
        self.label_7.setFont(font8)
        self.label_7.setStyleSheet(u"color:white;")
        self.stackedWidget.addWidget(self.page3)

        self.page4 = QtWidgets.QWidget()
        self.page4.setObjectName("page4")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.page4)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 50, 991, 261))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(25, -1, 25, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap(resource_path("./resources/logo2.png")))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color:#888888;")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.promptInput = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.promptInput.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        self.promptInput.setFont(font)
        self.promptInput.setStyleSheet("background-color:#292929;border-radius:25%;color:#00ACC1;text-align:center;")
        self.promptInput.setAlignment(QtCore.Qt.AlignCenter)
        self.promptInput.setObjectName("promptInput")
        self.horizontalLayout_8.addWidget(self.promptInput)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.executeQueryBtn = QtWidgets.QPushButton(self.page4)
        self.executeQueryBtn.setGeometry(QtCore.QRect(510, 630, 201, 51))
        self.executeQueryBtn.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.executeQueryBtn.setFont(font)
        self.executeQueryBtn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:25")
        self.executeQueryBtn.setObjectName("executeQueryBtn")
        self.modelOutput = QtWidgets.QPlainTextEdit(self.page4)
        self.modelOutput.setGeometry(QtCore.QRect(30, 320, 961, 291))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.modelOutput.setFont(font)
        self.modelOutput.setStyleSheet("""
            QPlainTextEdit{
                background-color:#292929;border-radius:25%;color:#00ACC1;padding: 15 15 15 15;
            }
            QScrollBar:vertical {
                border: none;
                background: #292929;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 0px;
             }
            
            /*  HANDLE BAR VERTICAL */
            QScrollBar::handle:vertical {	
                background-color: #00ACC1;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover{	
                background-color: rgb(0, 216, 240);
            }
            QScrollBar::handle:vertical:pressed {	
                background-color: rgb(0, 163, 181);
            }
            
            /* BTN TOP - SCROLLBAR */
            QScrollBar::sub-line:vertical {
                border: none;
                background-color: #00ACC1;
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical:hover {	
                background-color: rgb(0, 216, 240);
            }
            QScrollBar::sub-line:vertical:pressed {	
                background-color: rgb(0, 163, 181);
            }
            
            /* BTN BOTTOM - SCROLLBAR */
            QScrollBar::add-line:vertical {
                border: none;
                background-color: #00ACC1;
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical:hover {	
                background-color: rgb(0, 216, 240);
            }
            QScrollBar::add-line:vertical:pressed {	
                background-color: rgb(0, 163, 181);
            }
            
            /* RESET ARROW */
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.modelOutput.setObjectName("modelOutput")
        self.executePromptBtn = QtWidgets.QPushButton(self.page4)
        self.executePromptBtn.setGeometry(QtCore.QRect(290, 630, 201, 51))
        self.executePromptBtn.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.executePromptBtn.setFont(font)
        self.executePromptBtn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:25")
        self.executePromptBtn.setObjectName("executePromptBtn")
        self.backBtn_3 = QtWidgets.QPushButton(self.page4)
        self.backBtn_3.setGeometry(QtCore.QRect(930, 10, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.backBtn_3.setFont(font)
        self.backBtn_3.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:20;")
        self.backBtn_3.setObjectName("backBtn_3")
        self.stackedWidget.addWidget(self.page4)
        self.page5 = QtWidgets.QWidget()
        self.page5.setObjectName("page5")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.page5)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(20, 60, 991, 268))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(25, -1, 25, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap(resource_path("./resources/logo.png")))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color:#888888;")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_4.addWidget(self.label_11)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.gotoMoviesBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.gotoMoviesBtn.setMinimumSize(QtCore.QSize(0, 60))
        self.gotoMoviesBtn.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.gotoMoviesBtn.setFont(font)
        self.gotoMoviesBtn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:25;margin-top:10;")
        self.gotoMoviesBtn.setObjectName("gotoMoviesBtn")
        self.horizontalLayout_10.addWidget(self.gotoMoviesBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_9.addLayout(self.verticalLayout_4)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.page5)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 380, 991, 269))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(25, -1, 25, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_12 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap(resource_path("./resources/logo2.png")))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_5.addWidget(self.label_12)
        self.label_13 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color:#888888;")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_5.addWidget(self.label_13)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.gotoUniversityBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.gotoUniversityBtn.setMinimumSize(QtCore.QSize(0, 60))
        self.gotoUniversityBtn.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.gotoUniversityBtn.setFont(font)
        self.gotoUniversityBtn.setStyleSheet("background-color:#00ACC1;color:#0F0F0F;border-radius:25;margin-top:10")
        self.gotoUniversityBtn.setObjectName("gotoUniversityBtn")
        self.horizontalLayout_12.addWidget(self.gotoUniversityBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11.addLayout(self.verticalLayout_5)
        self.stackedWidget.addWidget(self.page5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.previousResultScreen = 1

        self.searchBtn.clicked.connect(self.normalSearch)
        self.searchBtn2.clicked.connect(self.advancedSearch)
        self.backBtn.clicked.connect(lambda: self.goToScreen(1))
        self.advancedSearchBtn.clicked.connect(lambda: self.goToScreen(0))
        self.backBtn_2.clicked.connect(self.customBackClick)
        self.backBtn_3.clicked.connect(lambda: self.goToScreen(4))
        self.backBtn_4.clicked.connect(lambda: self.goToScreen(4))

        self.gotoMoviesBtn.clicked.connect(lambda: self.goToScreen(1))
        self.gotoUniversityBtn.clicked.connect(lambda: self.goToScreen(3))

        self.filter1State = 0
        self.filter2State = 0
        self.filter3State = 0
        self.filter4State = 0
        self.filter1Btn.clicked.connect(lambda: self.filterClick(1))
        self.filter2Btn.clicked.connect(lambda: self.filterClick(2))
        self.filter3Btn.clicked.connect(lambda: self.filterClick(3))
        self.filter4Btn.clicked.connect(lambda: self.filterClick(4))

        self.llmClient = LLMClient()
        self.executePromptBtn.clicked.connect(self.executePrompt)
        self.executeQueryBtn.clicked.connect(self.executeQuery)

        self.thread = None

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def filterClick(self, filterNumber):
        e = f"if self.filter{filterNumber}State == 1:\n" \
            f"\tself.filter{filterNumber}Btn.setStyleSheet('background-color:#00ACC1;color:#0F0F0F;border-radius:20;border: 1px solid white;margin-left: 10px')\n" \
            f"\tself.filter{filterNumber}State = 0\n" \
            f"\tself.filter{filterNumber}Btn.setText('Include')\n" \
            f"else:\n" \
            f"\tself.filter{filterNumber}Btn.setStyleSheet('background-color:rgb(255, 78, 25);color:#0F0F0F;border-radius:20;border: 1px solid white;margin-left: 10px')\n" \
            f"\tself.filter{filterNumber}State = 1\n" \
            f"\tself.filter{filterNumber}Btn.setText('Exclude')\n"

        exec(e)

    def customBackClick(self):
        self.goToScreen(self.previousResultScreen)

    def updateQueryText(self, queryText, doneStatus=False):
        self.modelOutput.setPlainText(queryText)
        self.modelOutput.verticalScrollBar().setValue(
            self.modelOutput.verticalScrollBar().maximum()
        )
        if doneStatus:
            self.executePromptBtn.setDisabled(False)
            self.executeQueryBtn.setDisabled(False)
            self.modelOutput.setReadOnly(False)

    def updateHTML(self, htmlResult, extra):
        self.browser.setHtml(htmlResult)

    def executePrompt(self):
        self.executePromptBtn.setDisabled(True)
        self.executeQueryBtn.setDisabled(True)
        self.modelOutput.setReadOnly(True)
        self.modelOutput.setPlainText("Loading LLM Prompt Results...")
        self.thread = UniversityLibWorker(self, self.promptInput.text(), 'prompt')
        self.thread.error.connect(self.errorPopup)
        self.thread.start()
        self.thread.done.connect(self.updateQueryText)

    def executeQuery(self):
        self.browser.setHtml(HTMLBuilder().loadingHTML)
        self.previousResultScreen = 3
        self.goToScreen(2)
        self.thread = UniversityLibWorker(self, self.modelOutput.toPlainText(), 'query')
        self.thread.error.connect(self.errorPopup)
        self.thread.start()
        self.thread.done.connect(self.updateHTML)

    def normalSearch(self):
        self.previousResultScreen = 1
        self.browser.setHtml(HTMLBuilder().loadingHTML)
        self.goToScreen(2)
        movieName = f".*{self.mainMoveInput.text()}.*"
        self.thread = MovieLibWorker(self, movieName)
        self.thread.error.connect(self.errorPopup)
        self.thread.start()
        self.thread.done.connect(self.updateHTML)

    def advancedSearch(self):
        self.previousResultScreen = 1
        self.browser.setHtml(HTMLBuilder().loadingHTML)
        self.goToScreen(2)
        movieName = self.titleInput.text()
        movieActor = self.actorInput.text()
        movieDirector = self.directorInput.text()
        movieGenre = self.genreInput.text()
        self.thread = MovieLibWorker(self, movieName, movieActor, movieDirector, movieGenre)
        self.thread.start()
        self.thread.done.connect(self.updateHTML)

    def goToScreen(self, screen):
        self.stackedWidget.setCurrentIndex(screen)


    def errorPopup(self, exception: Exception):
        self.goToScreen(self.previousResultScreen)
        err_msg = "Error Occurred"
        extra = str(exception)
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setWindowIcon(QtGui.QIcon(resource_path("resources/appLogo.png")))
        msg.setText("An Error Occurred!")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        # msg.setInformativeText(err_msg)
        if extra != "":
            msg.setDetailedText(extra)
        msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ZeroLib"))
        self.label_7.setText(_translate("MainWindow", "Results"))
        self.searchBtn2.setText(_translate("MainWindow", "Search"))
        self.label_6.setText(_translate("MainWindow", "Title:"))
        self.titleInput.setPlaceholderText(_translate("MainWindow", "Filter Titles"))
        self.filter1Btn.setText(_translate("MainWindow", "Include"))
        self.label_3.setText(_translate("MainWindow", "Actor: "))
        self.actorInput.setPlaceholderText(_translate("MainWindow", "Filter Actors"))
        self.filter2Btn.setText(_translate("MainWindow", "Include"))
        self.label_4.setText(_translate("MainWindow", "Directors: "))
        self.directorInput.setPlaceholderText(_translate("MainWindow", "Filter Directors"))
        self.filter3Btn.setText(_translate("MainWindow", "Include"))
        self.label_5.setText(_translate("MainWindow", "Genres:"))
        self.genreInput.setPlaceholderText(_translate("MainWindow", "Filter Genres"))
        self.filter4Btn.setText(_translate("MainWindow", "Include"))
        self.backBtn.setText(_translate("MainWindow", "<"))
        self.advancedSearchBtn.setText(_translate("MainWindow", "Advanced Search"))
        self.label_2.setText(_translate("MainWindow", "Best Online Movie Library!"))
        self.mainMoveInput.setPlaceholderText(_translate("MainWindow", "Search Movies..."))
        self.backBtn_4.setText(_translate("MainWindow", "<"))
        self.backBtn_2.setText(_translate("MainWindow", "<"))
        self.label_9.setText(_translate("MainWindow", "Best University Library!"))
        self.promptInput.setPlaceholderText(_translate("MainWindow", "Enter Prompt"))
        self.executeQueryBtn.setText(_translate("MainWindow", "Execute Query"))
        self.modelOutput.setPlaceholderText(_translate("MainWindow", "Awaiting LLM Prompt Results"))
        self.executePromptBtn.setText(_translate("MainWindow", "Execute Prompt"))
        self.backBtn_3.setText(_translate("MainWindow", "<"))
        self.label_11.setText(_translate("MainWindow", "Best Online Movie Library!"))
        self.gotoMoviesBtn.setText(_translate("MainWindow", "Go to Movies Lib"))
        self.label_13.setText(_translate("MainWindow", "Best University Library!"))
        self.gotoUniversityBtn.setText(_translate("MainWindow", "Go to University Lib"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    appWindow = QtWidgets.QMainWindow()
    ui = ZeroLibApp()
    ui.setupUi(appWindow)
    appWindow.show()
    sys.exit(app.exec_())
