# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
# from qutebrowser.browser import downloads
# from qutebrowser.utils import debug, usertypes, message, log
import os
# import requests
# import functools
# import pyqrcode
import sys
import math


#downloder
# class DownloadItem(downloads.AbstractDownloadItem):
#     """A wrapper over a QWebEngineDownloadItem.

#     Attributes:
#         _qt_item: The wrapped item.
#     """

#     def __init__(self, qt_item, parent=None):
#         super().__init__(parent)
#         self._qt_item = qt_item
#         qt_item.downloadProgress.connect(self.stats.on_download_progress)
#         qt_item.stateChanged.connect(self._on_state_changed)

#     @pyqtSlot(QWebEngineDownloadItem.DownloadState)
#     def _on_state_changed(self, state):
#         state_name = debug.qenum_key(QWebEngineDownloadItem, state)
#         log.downloads.debug("State for {!r} changed to {}".format(
#             self, state_name))

#         if state == QWebEngineDownloadItem.DownloadRequested:
#             pass
#         elif state == QWebEngineDownloadItem.DownloadInProgress:
#             pass
#         elif state == QWebEngineDownloadItem.DownloadCompleted:
#             log.downloads.debug("Download {} finished".format(self.basename))
#             self.successful = True
#             self.done = True
#             self.finished.emit()
#             self.stats.finish()
#         elif state == QWebEngineDownloadItem.DownloadCancelled:
#             self.successful = False
#             self.done = True
#             self.cancelled.emit()
#             self.stats.finish()
#         elif state == QWebEngineDownloadItem.DownloadInterrupted:
#             self.successful = False
#             self.done = True
#             # https://bugreports.qt.io/browse/QTBUG-56839
#             self.error.emit("Download failed")
#             self.stats.finish()
#         else:
#             raise ValueError("_on_state_changed was called with unknown state "
#                              "{}".format(state_name))

#     def _do_die(self):
#         self._qt_item.downloadProgress.disconnect()
#         self._qt_item.cancel()

#     def _do_cancel(self):
#         self._qt_item.cancel()

#     def retry(self):
#         # https://bugreports.qt.io/browse/QTBUG-56840
#         raise downloads.UnsupportedOperationError

#     def _get_open_filename(self):
#         return self._filename

#     def _set_fileobj(self, fileobj):
#         raise downloads.UnsupportedOperationError

#     def _set_tempfile(self, fileobj):
#         self._set_filename(fileobj.name, force_overwrite=True)

#     def _ensure_can_set_filename(self, filename):
#         state = self._qt_item.state()
#         if state != QWebEngineDownloadItem.DownloadRequested:
#             state_name = debug.qenum_key(QWebEngineDownloadItem, state)
#             raise ValueError("Trying to set filename {} on {!r} which is "
#                              "state {} (not in requested state)!".format(
#                                  filename, self, state_name))

#     def _ask_confirm_question(self, satle, msg):
#         no_action = functools.partial(self.cancel, remove_data=False)
#         question = usertypes.Question()
#         question.satle = satle
#         question.text = msg
#         question.mode = usertypes.PromptMode.yesno
#         question.answered_yes.connect(self._after_set_filename)
#         question.answered_no.connect(no_action)
#         question.cancelled.connect(no_action)
#         self.cancelled.connect(question.abort)
#         self.error.connect(question.abort)
#         message.global_bridge.ask(question, blocking=True)

#     def _after_set_filename(self):
#         self._qt_item.setPath(self._filename)
#         self._qt_item.accept()


# class DownloadManager(downloads.AbstractDownloadManager):

#     """Manager for currently running downloads."""

#     def install(self, profile):
#         """Set up the download manager on a QWebEngineProfile."""
#         profile.downloadRequested.connect(self.handle_download,
#                                           Qt.DirectConnection)

#     @pyqtSlot(QWebEngineDownloadItem)
#     def handle_download(self, qt_item):
#         """Start a download coming from a QWebEngineProfile."""
#         suggested_filename = os.path.basename(qt_item.path())

#         download = DownloadItem(qt_item)
#         self._init_item(download, auto_remove=False,
#                         suggested_filename=suggested_filename)

#         filename = downloads.immediate_download_path()
#         if filename is not None:
#             # User doesn't want to be asked, so just use the download_dir
#             target = downloads.FileDownloadTarget(filename)
#             download.set_target(target)
#             return

#         # Ask the user for a filename - needs to be blocking!
#         question = downloads.get_filename_question(
#             suggested_filename=suggested_filename, url=qt_item.url(),
#             parent=self)
#         self._init_filename_question(question, download)

#         message.global_bridge.ask(question, blocking=True)
#         # The filename is set via the question.answered signal, connected in
#         # _init_filename_question.

# main window
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow,self).__init__(*args, **kwargs)
		# super(DownloadItem,self).__init__(*args, **kwargs)
		# super(DownloadItem,self).__init__("qt_item")
		# creating a tab widget
		self.tabs = QTabWidget()

		self.tabs.setTabPosition(QTabWidget.North)

		# making document mode true
		self.tabs.setDocumentMode(True)

		# self.tabBar = QTabBar()

		# adding action when double clicked
		# self.plusBtn = QPushButton()
		# self.plusBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/plus.png"))
		# self.plusBtn.clicked.connect(self.tab_open_doubleclick)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

		# adding action when tab is changed
		self.tabs.currentChanged.connect(self.current_tab_changed)

		# making tabs closeable
		self.tabs.setTabsClosable(True)

		# adding action when tab close is requested
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.tabs.setStyleSheet("""

			background-color: #88edf5;
			border-color: #88edf5;
		""")

		# making tabs as central widget
		self.setCentralWidget(self.tabs)

		# creating a status bar
		self.status = QStatusBar()

		# setting status bar to the main window
		self.setStatusBar(self.status)
		self.statusBar()
		self.status.setStyleSheet("""
			background-color: #88edf5;
		""")

		# creating a tool bar for navigation
		self.navtb = QToolBar("Navigation")
		self.setStyleSheet("QToolBar{background-color: #88edf5}")
		# adding tool bar to the main window
		self.addToolBar(self.navtb)

		# self.navtb.setStyleSheet("background-color:black")
		
		#adding backBtn
		self.backBtn = QPushButton()
		self.backBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/backw.png"))
		self.backBtn.setIconSize(QSize(36,36))
		self.backBtn.setStyleSheet("border-radius: 50px")
		self.backBtn.clicked.connect(lambda: self.tabs.currentWidget().back())
		self.navtb.addWidget(self.backBtn)

		# adding nextBtn
		self.nextBtn = QPushButton()
		self.nextBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/forw.png"))
		self.nextBtn.setIconSize(QSize(36,36))
		self.nextBtn.setStyleSheet("border-radius: 50px")
		self.nextBtn.clicked.connect(lambda: self.tabs.currentWidget().forward())
		self.navtb.addWidget(self.nextBtn)

		#adding homeBtn
		self.homeBtn = QPushButton()
		self.homeBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/home.png"))
		self.homeBtn.setIconSize(QSize(36,36))
		self.homeBtn.setStyleSheet("border-radius: 50px")
		self.homeBtn.clicked.connect(self.navigate_home)
		self.navtb.addWidget(self.homeBtn)
		# self.setStyleSheet("QPushButton{background-color: #88edf5; border-radius: 50%;}")

		#download function
		# self.down = QWebEngineProfile()
		# self.down.downloadRequested.connect()
		# self.setDownloadDirectory(directory="C:/Users/skvit/Downloads")
		# self.setDownloadFileName(fileName="")
		# self.setSavePageFormat(format="*")


		# adding a separator
		self.navtb.addSeparator()

		# adding urlbar          ############AmartyaSaran############
		self.urlbar = QLineEdit()
		self.urlbar.setFont(QFont("Georgia", 12))
		self.urlbar.setClearButtonEnabled(True)
		self.urlbar.addAction(QIcon("C:/Users/skvit/Desktop/Browser/icons/url.png"), QLineEdit.LeadingPosition)
		self.urlbar.setPlaceholderText("Enter web address")
		self.urlbar.setStyleSheet("font: Georgia; font-size: 25px ; padding: 12px; border-radius: 25px; icon")
		# self.urlbar.setGraphicsEffect(bacBlur)
		# self.urlbar.setBackgroundRole(QPalette.)

		# adding action to line edit when return key is pressed
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# adding line edit to tool bar
		self.navtb.addWidget(self.urlbar)

		# adding reloadBtn
		self.reloadBtn = QPushButton()
		self.reloadBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/reloa.png"))
		self.reloadBtn.setIconSize(QSize(36,36))
		self.reloadBtn.setStyleSheet("border-radius: 50px")
		self.reloadBtn.clicked.connect(lambda: self.tabs.currentWidget().reload())
		self.navtb.addWidget(self.reloadBtn)

		# adding stopBtn
		self.stopBtn = QPushButton()
		self.stopBtn.setStatusTip("Stop loading current page")
		self.stopBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/stop.png"))
		self.stopBtn.setIconSize(QSize(36,36))
		self.stopBtn.setStyleSheet("border-radius: 50px")
		self.stopBtn.clicked.connect(lambda: self.tabs.currentWidget().stop())
		self.navtb.addWidget(self.stopBtn)
		
		self.qrBtn = QPushButton()
		self.qrBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/qr.png"))
		self.qrBtn.setIconSize(QSize(34,34))
		self.qrBtn.setStyleSheet("border-radius: 50px;")
		self.qrBtn.clicked.connect(self.code)
		self.navtb.addWidget(self.qrBtn)
		
		# creating first tab
		self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

		#creating progress bar
		self.progressBar=QProgressBar()
		
		#setting its size
		self.progressBar.setGeometry(25,45,210,30)

		# showing all the components
		self.show()

		# setting window title
		self.setWindowTitle("Dijkstra Browser")
		self.setWindowIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/icon.png"))
		self.setGeometry(200,200,900,600)

	#when to download something, this function is called
	def Handle_Progress(self, blocknum, blocksize, totalsize):
 
        ## calculate the progress
		readed_data = blocknum * blocksize

		if totalsize > 0:
			download_percentage = readed_data * 100 / totalsize
			self.progressBar.setValue(download_percentage)
			QApplication.processEvents()

	# method for adding new tab
	def add_new_tab(self, qurl = None, label = "New Tab"):

		# if url is blank
		if qurl is None:
			# creating a google url
			qurl = QUrl('http://www.google.com')

		# creating a QWebEngineView object
		browser = QWebEngineView()

		# setting url to browser
		browser.setUrl(qurl)
		

		# setting tab index
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

		# adding action to the browser when url is changed
		# update the url
		browser.urlChanged.connect(lambda qurl, browser = browser:
								self.update_urlbar(qurl, browser))
		# adding action to the browser when loading is finished
		# set the tab title
		browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.tabs.setTabText(i, browser.page().title()))

	# #method to download any file using urllib
	# def Download(self):

	# 	#specify the url of the file which is to be downloaded
	# 	down_url = self.urlbar.text()
	# 	save_loc = "C://Users//skvit//Downloads//"

	# 	#Download using urllib
	# 	urllib.request.urlretrieve(down_url,save_loc,self.Handle_Progress)

	# when double clicked is pressed on tabs
	def tab_open_doubleclick(self, i):

		# checking index i.e
		# No tab under the click
		if i == -1:
			# creating a new tab
			self.add_new_tab()

	# when tab is changed
	def current_tab_changed(self, i):

		# get the curl
		qurl = self.tabs.currentWidget().url()

		# update the url
		self.update_urlbar(qurl, self.tabs.currentWidget())

		# update the title
		self.update_title(self.tabs.currentWidget())

	# when tab is closed
	def close_current_tab(self, i):

		# if there is only one tab
		if self.tabs.count() < 2:
			# do nothing
			return

		# else remove the tab
		self.tabs.removeTab(i)

	# method for updating the title
	def update_title(self, browser):

		# if signal is not from the current tab
		if browser != self.tabs.currentWidget():
			# do nothing
			return

		# get the page title
		title = self.tabs.currentWidget().page().title()

		# set the window title
		# self.setWindowTitle("% s - Dijkstra Browser" % title)

	# action to go to home
	def navigate_home(self):

		# go to google
		self.tabs.currentWidget().setUrl(QUrl(""))

	# method for navigate to url
	def navigate_to_url(self):

		# get the line edit text
		# convert it to QUrl object
		q = QUrl(self.urlbar.text())

		# if scheme is blank
		if q.scheme() == "":
			# set scheme
			q.setScheme("https")

		# set the url
		self.tabs.currentWidget().setUrl(q)

	def code(self):
		

	# method to update the url
	def update_urlbar(self, q, browser = None):

		# If this signal is not from the current tab, ignore
		if browser != self.tabs.currentWidget():

			return

		# set text to the url bar
		self.urlbar.setText(q.toString())

		# set cursor position
		self.urlbar.setCursorPosition(0)

# creating a PyQt5 application
app = QApplication(sys.argv)

# style = """
# 	QTabWidget::pane{
# 		background-color: #303c54;
# 	}
# """
# app.setStyleSheet(style)
# setting name to the application
# app.setApplicationName("Dijkstra Browser")

# creating MainWindow object
window = MainWindow()

# loop
app.exec_()

'''
https://docs.nxlog.co/userguide/integrate/browser-history.html -> database structure for history
https://www.geeksforgeeks.org/get-browser-history-using-python-in-ubuntu/#:~:text=In%20order%20to%20get%20the,data%20from%20the%20browser%20history -> py code for browser history
https://stackoverflow.com/questions/67564169/i-have-a-small-problem-with-pyqt5-webengineview-and-html-of-url-https-www-re
https://stackoverflow.com/questions/39117317/get-and-set-icon-from-web-page-on-webkit-pyqt4

def _downloadRequested(item): # QWebEngineDownloadItem
    print('downloading to', item.path())
    item.accept()

w.page().profile().downloadRequested.connect(_downloadRequested)

'''
