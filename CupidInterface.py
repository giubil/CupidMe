from PyQt5.QtWidgets import *
from cupidme.CupidMe import CupidMe
from PyQt5 import QtCore, QtGui
import sys
import warnings

warnings.filterwarnings("error")

class Cupid_GUI(QWidget):
    
    TAGS = sorted(("who", "where", "minimum_height", "maximum_height", "last_login", "order_by", "minimum_age", "maximum_age", 
            "age_recip", "radius", "availability", "monogamy",
            "ethnicity", "religion", "looking_for", "smoking", "drinking", "drugs", "education", "children", "cats", "dogs", "match_cutoff"))
    
    DIRECTIONS = \
"Welcome to CupidMe (teehee!)\n\n\
Be sure to log in to make the most of CupidMe's features. CupidMe does not store your credentials.\n\n\
Your saved filters are imported from the website, but you can customize them if you like.\n\
Important notes:\n\
\tEnter height in inches\n\
\tUse match_cutoff to filter out low match scores\n\
\t\"Where\" designates location. Enter zip codes for US locations.\n\
\t\"Who\" uses Craiglist notation. For instance,\n\
\t\tE4W = Everyone looking for women\n\t\tW4M = Women who want men\n\n\
Performing a search returns the number of users who fit your filters. To see a list of matching users, make sure \"List_users\" is ticked.\n\n\
\"Flood\" will message and/or like all users last returned by \"List_users\". Be extremely careful with this!\n\n\
Top Matches will search through the largest cities in the United States and return the number of high percentage matches in each. Be patient, this takes a while.\n\n\
Finally, help will redisplay this text. For more detailed information, visit https://github.com/TSS88/CupidMe"

    def __init__(self, parent = None):
        super(Cupid_GUI, self).__init__(parent)
        self.cm = CupidMe()

        cupid_layout = QGridLayout()
        cupid_layout.setSpacing(15)
        
        self.user_line = QLineEdit()
        self.pass_line = QLineEdit()
        self.pass_line.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Log in")
        cupid_layout.addWidget(QLabel("Username:"), 0, 0, 1, 1)
        cupid_layout.addWidget(self.user_line, 0, 1, 1, 1)
        cupid_layout.addWidget(QLabel("Password:"), 0, 2, 1, 1)
        cupid_layout.addWidget(self.pass_line, 0, 3, 1, 3)
        cupid_layout.addWidget(login_button, 0, 6, 1, 1)
        cupid_layout.addWidget(self.line_separator(), 1, 0, 1, 7)
        login_button.clicked.connect(self.submit_login)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem(None)
        self.filter_combo.addItems(self.TAGS)
        self.option_container = QGridLayout()
        set_button = QPushButton("Set")
        cupid_layout.addWidget(QLabel("Filters"), 2, 0, 1, 1, alignment = QtCore.Qt.AlignTop)
        cupid_layout.addWidget(self.filter_combo, 2, 1, 1, 1, alignment = QtCore.Qt.AlignTop)
        cupid_layout.addLayout(self.option_container, 2, 3, 1, 3)
        cupid_layout.addWidget(set_button, 2, 6, 1, 1, alignment = QtCore.Qt.AlignTop)
        cupid_layout.addWidget(self.line_separator(), 3, 0, 1, 7)
        self.filter_combo.currentIndexChanged.connect(self.combo_check)
        set_button.clicked.connect(self.submit_filter)
        
        self.list_users_cb = QCheckBox("List users?")
        self.list_users_cb.setChecked(True)
        search_button = QPushButton("Search")
        cupid_layout.addWidget(self.list_users_cb, 4, 4, 1, 1)
        cupid_layout.addWidget(search_button, 4, 6, 1, 1)
        cupid_layout.addWidget(self.line_separator(), 5, 0, 1, 7)
        search_button.clicked.connect(self.submit_search)
        
        self.msg_line = QTextEdit()
        self.msg_line.setMaximumHeight(50)
        self.like_cb = QCheckBox("Like?")
        flood_button = QPushButton("Flood")
        cupid_layout.addWidget(QLabel("Message:"), 6, 0, 1, 1)
        cupid_layout.addWidget(self.msg_line, 6, 1, 1, 1)
        cupid_layout.addWidget(self.like_cb, 6, 4, 1, 1)
        cupid_layout.addWidget(flood_button, 6, 6, 1, 1)
        cupid_layout.addWidget(self.line_separator(), 7, 0, 1, 7)
        flood_button.clicked.connect(self.submit_flood)
        
        top_button = QPushButton("Top Cities")
        help_button = QPushButton("Help")
        cupid_layout.addWidget(top_button, 8, 5, 1, 1)
        cupid_layout.addWidget(help_button, 8, 6, 1, 1)
        help_button.clicked.connect(self.submit_help)
        top_button.clicked.connect(self.submit_top)
        
        self.log = QTextEdit()
        self.log.setText(self.DIRECTIONS)
        self.log.setReadOnly(True)
        #self.log.setLineWrapMode(QTextEdit.NoWrap)
        self.log.setFont(QtGui.QFont("Courier",12))
        cupid_layout.addWidget(self.log, 9, 0, 5, 7)

        self.setLayout(cupid_layout)
        self.setWindowTitle("CupidMe")
    
    def line_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def submit_login(self):
        self.log.setText("Logging in...\n")
        QtCore.QCoreApplication.processEvents()
        user = self.user_line.text()
        try:
            self.cm.login(user, self.pass_line.text())
            self.log.append("Successfully logged in as " + user)
        except:
            self.log.append("Could not log in as " + user)
        self.pass_line.clear()
        
    def combo_check(self):
        #clear option_container
        for cnt in reversed(range(self.option_container.count())):
            widget = self.option_container.takeAt(cnt).widget()
            if widget is not None: 
                widget.deleteLater()
                
        filter_field = self.filter_combo.currentText()      
        if filter_field in ("minimum_height", "maximum_height", "minimum_age", "maximum_age", "radius"):
            num_field = QLineEdit()
            num_field.setText(str(self.cm.filter.current_filter[filter_field]))
            self.option_container.addWidget(num_field, 0, 0, 1, 1)
        elif filter_field == "match_cutoff":
            num_field = QLineEdit()
            num_field.setText(str(self.cm.filter.match_cutoff))
            self.option_container.addWidget(num_field, 0, 0, 1, 1)
        elif filter_field == "where":
            num_field = QLineEdit()
            num_field.setText(str(self.cm.filter.current_filter["location"]))
            self.option_container.addWidget(num_field, 0, 0, 1, 1)
        elif filter_field == "who":
            self._option_builder(self.cm.filter.common_tags, filter_field)
        elif filter_field == "last_login":
            self._option_builder(self.cm.filter.login_tags, filter_field)
        elif filter_field in self.cm.filter.options:
            self._option_builder(self.cm.filter.options[filter_field], filter_field)
        elif filter_field in self.cm.filter.arr_options:
            self._option_builder(self.cm.filter.arr_options[filter_field], filter_field, True)

    def _option_builder(self, options, filter_field, multi = False):
        #If multiple options are allowed, use checkboxes
        if multi:
            options = sorted((i for i in options))
            row = 0
            
            #Add widgets two per row
            for index, option in enumerate(options):
                checkbox = QCheckBox(option)
                self.option_container.addWidget(checkbox, row, index % 2, 1, 1, alignment = QtCore.Qt.AlignTop)
                
                #If this box is set in filters, check it
                if filter_field in self.cm.filter.current_filter and option in self.cm.filter.current_filter[filter_field]:
                    checkbox.setChecked(True)
                if index % 2 == 1:
                    row += 1
                    
        #Use radio buttons if only one option is usable
        else:
            options = sorted((i for i in options))
            row = 0
            radio_group = QButtonGroup()
            for index, option in enumerate(options):
                radio = QRadioButton(option)
                radio_group.addButton(radio)
                self.option_container.addWidget(radio, row, index % 2, 1, 1, alignment = QtCore.Qt.AlignTop)
                if filter_field in self.cm.filter.current_filter and radio.text() == self.cm.filter.current_filter[filter_field]:
                    radio.setChecked(True)
                if index % 2 == 1:
                    row += 1
        
    def submit_filter(self):  
        self.log.setText("Setting filters...\n")          
        QtCore.QCoreApplication.processEvents()
        filter_field = self.filter_combo.currentText()
        try:
            if filter_field in ("minimum_age", "maximum_age", "minimum_height", "maximum_height", "radius", "match_cutoff"):
                self.cm.filter.set(**{filter_field: int(self.option_container.itemAtPosition(0, 0).widget().text())})
            elif type(self.option_container.itemAt(0).widget()) is QLineEdit:
                self.cm.filter.set(**{filter_field: self.option_container.itemAtPosition(0, 0).widget().text()})
            elif type(self.option_container.itemAt(0).widget()) is QRadioButton:
                items = (self.option_container.itemAt(i) for i in range(self.option_container.count())) 
                for radio in items:
                    if radio.widget().isChecked() is True:
                        self.cm.filter.set(**{filter_field: radio.widget().text()})
                        break
            elif type(self.option_container.itemAt(0).widget()) is QCheckBox:
                items = (self.option_container.itemAt(i) for i in range(self.option_container.count())) 
                for check in items:
                    if check.widget().isChecked() is True:
                        self.cm.filter.set(**{filter_field: check.widget().text()})
            self.log.append("Successfully set " + filter_field)
        except:
            self.log.append("Error setting " + filter_field)
    
    def submit_search(self):
        self.log.setText("Searching...\n")
        QtCore.QCoreApplication.processEvents()
        try:
            list_pref = self.list_users_cb.isChecked()
            self.cm.search(list_users = list_pref)
            self.log.append("Total matches: " + str(self.cm.total_users) + "\n")
            if list_pref:
                for user in self.cm.user_list:
                    self.log.append(user)
        except:
            self.log.append("Search failed")
            
    def submit_flood(self):
        self.log.setText("Flooding...\n")
        QtCore.QCoreApplication.processEvents()
        try:
            msgl = self.msg_line.text()
            if msgl == "":
                self.cm.flood(like = self.like_cb.isChecked())
            else:
                self.cm.flood(msg = msgl, like = self.like_cb.isChecked())
            self.log.append("Flooded " + str(self.cm.total_users) + " users")
        except:
            self.log.append("Flood failed.")
            
    def submit_top(self):
        if not self.cm._logged_in: 
            self.log.setText("Please log in first!")
            return
        try:
            self.log.setText("Searching for top cities...")
            QtCore.QCoreApplication.processEvents()
            self.log.clear()
            zips = [["New York City", "10001", 0], ["Los Angeles", "90001", 0], ["Chicago", "60290", 0], ["Houston", "77001", 0], ["Philadelphia", "19019", 0], ["Phoenix", "85001", 0], ["Jacksonville", "32099", 0], ["Indianapolis", "46201", 0], ["Charlotte", "28201", 0], ["Seattle", "98101", 0], ["Denver", "80123", 0], ["Detroit", "48201", 0], ["Washington D.C.", "20001", 0], ["Boston", "02108", 0], ["Memphis", "37501", 0], ["Portland", "97201", 0], ["Oklahoma City", "73101", 0], ["Las Vegas", "89101", 0], ["Baltimore", "21117", 0], ["Louisville", "40201", 0], ["Milwaukee", "53202", 0], ["Albuquerque", "87101", 0], ["Kansas City", "64101", 0], ["Atlanta", "30301", 0], ["Virginia Beach", "23450", 0], ["Omaha", "68022", 0], ["Minneapolis", "55401", 0], ["Wichita", "67201", 0], ["New Orleans", "70112", 0], ["Honolulu", "96813", 0], ["Anchorage", "99501", 0], ["Boise", "83701", 0], ["Birmingham", "35201", 0], ["Des Moines", "50301", 0], ["Little Rock", "72201", 0], ["Salt Lake City", "84101", 0], ["Tallahassee", "32301", 0], ["Providence", "02901", 0], ["Sioux Falls", "57101", 0], ["Jackson", "39201", 0], ["Bridgeport", "06601", 0], ["Columbus", "43085", 0], ["Fargo", "58102", 0], ["Billings", "59101", 0], ["Wilmington", "19801", 0], ["Manchester", "03101", 0], ["Cheyenne", "82001", 0], ["Burlington", "05401", 0], ["San Antonio", "78201", 0], ["San Diego", "92093", 0], ["Dallas", "75201", 0], ["San Jose", "95101", 0], ["Austin", "73301", 0], ["San Fransisco", "94101", 0], ["Fort Worth", "76101", 0], ["El Paso", "79901", 0], ["Tucson", "85701", 0], ["Fresno", "93650", 0], ["Sacramento", "94203", 0], ["Long Beach", "90801", 0], ["Mesa", "85201", 0], ["Colorado Springs", "80840", 0], ["Raleigh", "27601", 0], ["Miami", "33101", 0], ["Tulsa", "74101", 0], ["Cleveland", "44101", 0], ["Bakersfield", "93301", 0], ["Tampa", "33601", 0], ["Aurora", "60502", 0], ["Santa Ana", "92701", 0], ["Corpus Christi", "78401", 0], ["Riverside", "92501", 0], ["St. Louis", "63101", 0], ["Lexington", "40502", 0], ["Stockton", "95201", 0], ["Pittsburgh", "15201", 0], ["Cincinatti", "45201", 0], ["Greensboro", "27401", 0], ["Plano", "75023", 0], ["Toledo", "43601", 0], ["Lincoln", "68501", 0], ["Orlando", "32801", 0], ["Chandler", "85224", 0], ["Fort Wayne", "46801", 0], ["Buffalo", "14204", 0], ["Durham", "27701", 0], ["Irvine", "92602", 0], ["Laredo", "78040", 0], ["Lubbock", "79401", 0], ["Madison", "53705", 0]]
            self.cm.filter.set(radius = 25, match_cutoff = 85, order_by = "MATCH")
            for locale in zips:
                self.cm.filter.set(where = locale[1])
                self.cm.search()
                locale[2] = self.cm.total_users
            zips.sort(key=lambda x: x[2], reverse = True)
            self.log.setText("Your top cities for matches:\n")
            for pair in zips:
                self.log.append(pair[0].ljust(20) + str(pair[2]))
            self.log.moveCursor(QtGui.QTextCursor.Start)
            self.cm.total_users = 0
            self.cm.user_list.clear()
        except:
            self.log.append("Top 100 search failed")
            
    def submit_help(self):
        self.log.setText(self.DIRECTIONS)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Cupid_GUI()
    screen.show()
    sys.exit(app.exec_())