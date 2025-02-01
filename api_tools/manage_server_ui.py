import requests
from PyQt5 import QtWidgets, QtCore, QtGui
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv('API_KEY', 'default_api_key')  # Use environment variable for API key
print(f'Loaded API_KEY: {API_KEY}')  # Debug statement to verify API key

BASE_URL = 'http://localhost:8095'
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'images')
ICON_PATH = os.path.join(IMAGES_DIR, 'MainLogo.ico')

class ServerManagementUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SafeRS Website API Management UI")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))

        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("SafeRS Website API Manager")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Slots/Status Section
        slots_group = QtWidgets.QGroupBox("Update Slots/Status")
        slots_layout = QtWidgets.QGridLayout()
        self.slots_entry = QtWidgets.QLineEdit()
        self.slots_entry.setPlaceholderText("Enter 'm' for maintenance or 0-max slots")
        self.slots_output = QtWidgets.QLabel("")
        slots_button = QtWidgets.QPushButton("Update")
        slots_button.clicked.connect(self.update_slots)
        slots_layout.addWidget(QtWidgets.QLabel("Slots:"), 0, 0)
        slots_layout.addWidget(self.slots_entry, 0, 1)
        slots_layout.addWidget(slots_button, 0, 2)
        slots_layout.addWidget(self.slots_output, 1, 0, 1, 3)
        slots_group.setLayout(slots_layout)
        layout.addWidget(slots_group)

        # Pricing Section
        pricing_group = QtWidgets.QGroupBox("Update Pricing")
        pricing_layout = QtWidgets.QGridLayout()
        self.plan_dropdown = QtWidgets.QComboBox()
        self.plan_dropdown.addItems(['1 Month', '3 Months', 'Lifetime'])
        self.price_entry = QtWidgets.QLineEdit()
        self.price_entry.setPlaceholderText("Enter price")
        self.pricing_output = QtWidgets.QLabel("")
        pricing_button = QtWidgets.QPushButton("Update")
        pricing_button.clicked.connect(self.update_pricing)
        pricing_layout.addWidget(QtWidgets.QLabel("Plan:"), 0, 0)
        pricing_layout.addWidget(self.plan_dropdown, 0, 1)
        pricing_layout.addWidget(QtWidgets.QLabel("Price:"), 1, 0)
        pricing_layout.addWidget(self.price_entry, 1, 1)
        pricing_layout.addWidget(pricing_button, 1, 2)
        pricing_layout.addWidget(self.pricing_output, 2, 0, 1, 3)
        pricing_group.setLayout(pricing_layout)
        layout.addWidget(pricing_group)

        # XP and Hours Section
        stats_group = QtWidgets.QGroupBox("Update XP and Hours")
        stats_layout = QtWidgets.QGridLayout()
        self.xp_entry = QtWidgets.QLineEdit()
        self.xp_entry.setPlaceholderText("Enter XP gained")
        self.hours_entry = QtWidgets.QLineEdit()
        self.hours_entry.setPlaceholderText("Enter hours botted")
        self.stats_output = QtWidgets.QLabel("")
        xp_button = QtWidgets.QPushButton("Update XP")
        xp_button.clicked.connect(self.update_xp)
        hours_button = QtWidgets.QPushButton("Update Hours")
        hours_button.clicked.connect(self.update_hours)
        stats_layout.addWidget(QtWidgets.QLabel("XP Gained:"), 0, 0)
        stats_layout.addWidget(self.xp_entry, 0, 1)
        stats_layout.addWidget(xp_button, 0, 2)
        stats_layout.addWidget(QtWidgets.QLabel("Hours Botted:"), 1, 0)
        stats_layout.addWidget(self.hours_entry, 1, 1)
        stats_layout.addWidget(hours_button, 1, 2)
        stats_layout.addWidget(self.stats_output, 2, 0, 1, 3)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Offerings Section
        offerings_title = QtWidgets.QLabel("Manage Offerings")
        offerings_title.setAlignment(QtCore.Qt.AlignCenter)
        offerings_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(offerings_title)

        self.offerings_listbox = QtWidgets.QListWidget()
        self.offerings_listbox.itemSelectionChanged.connect(self.populate_offering_fields)
        layout.addWidget(self.offerings_listbox)

        offerings_form_layout = QtWidgets.QFormLayout()
        self.tag_dropdown = QtWidgets.QComboBox()
        self.tag_dropdown.addItems(['Combat', 'Skilling', 'Bossing', 'Minigame', 'PKing', 'General Features'])
        self.image_dropdown = QtWidgets.QComboBox()
        self.image_dropdown.addItems(self.get_image_files())
        self.title_entry = QtWidgets.QLineEdit()
        self.description_entry = QtWidgets.QLineEdit()
        offerings_form_layout.addRow("Tag:", self.tag_dropdown)
        offerings_form_layout.addRow("Image:", self.image_dropdown)
        offerings_form_layout.addRow("Title:", self.title_entry)
        offerings_form_layout.addRow("Description:", self.description_entry)
        layout.addLayout(offerings_form_layout)

        offerings_buttons_layout = QtWidgets.QHBoxLayout()
        add_button = QtWidgets.QPushButton("Add Offering")
        add_button.clicked.connect(self.add_offering)
        remove_button = QtWidgets.QPushButton("Remove Offering")
        remove_button.clicked.connect(self.remove_offering)
        edit_button = QtWidgets.QPushButton("Edit Offering")
        edit_button.clicked.connect(self.edit_offering)
        refresh_button = QtWidgets.QPushButton("Refresh Offerings")
        refresh_button.clicked.connect(self.refresh_offerings)
        offerings_buttons_layout.addWidget(add_button)
        offerings_buttons_layout.addWidget(remove_button)
        offerings_buttons_layout.addWidget(edit_button)
        offerings_buttons_layout.addWidget(refresh_button)
        layout.addLayout(offerings_buttons_layout)

        self.offerings_output = QtWidgets.QLabel("")
        layout.addWidget(self.offerings_output)

        self.setLayout(layout)
        self.refresh_offerings()

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #3e3e3e;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton {
                background-color: #555555;
                color: #ffffff;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QLabel {
                color: #ffffff;
            }
        """)

    def get_image_files(self):
        return [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]

    def update_slots(self):
        new_slots = self.slots_entry.text()
        if not new_slots.isdigit():
            new_slots = 'maintenance'
        url = f'{BASE_URL}/update_slots'
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        data = {'available_slots': new_slots}
        response = requests.post(url, json=data, headers=headers)
        try:
            response_data = response.json()
            if response.status_code == 200:
                self.slots_output.setText(f'Successfully updated slots to {new_slots}')
                self.slots_output.setStyleSheet("color: green;")
            else:
                self.slots_output.setText(f'Failed to update slots: {response_data}')
                self.slots_output.setStyleSheet("color: red;")
        except requests.exceptions.JSONDecodeError:
            self.slots_output.setText('Failed to update slots: Invalid response from server')
            self.slots_output.setStyleSheet("color: red;")

    def update_pricing(self):
        plan = self.plan_dropdown.currentText()
        price = self.price_entry.text()
        url = f'{BASE_URL}/update_pricing'
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        data = {'plan': plan, 'price': price}
        response = requests.post(url, json=data, headers=headers)
        try:
            response_data = response.json()
            if response.status_code == 200:
                self.pricing_output.setText(f'Successfully updated pricing for {plan} to ${price}')
                self.pricing_output.setStyleSheet("color: green;")
            else:
                self.pricing_output.setText(f'Failed to update pricing: {response_data}')
                self.pricing_output.setStyleSheet("color: red;")
        except requests.exceptions.JSONDecodeError:
            self.pricing_output.setText('Failed to update pricing: Invalid response from server')
            self.pricing_output.setStyleSheet("color: red;")

    def update_xp(self):
        xp_gained = self.xp_entry.text()
        url = f'{BASE_URL}/update_xp_gained'
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        data = {'xp_gained': xp_gained}
        response = requests.post(url, json=data, headers=headers)
        try:
            response_data = response.json()
            if response.status_code == 200:
                self.stats_output.setText(f'Successfully updated XP gained to {xp_gained}')
                self.stats_output.setStyleSheet("color: green;")
            else:
                self.stats_output.setText(f'Failed to update XP: {response_data}')
                self.stats_output.setStyleSheet("color: red;")
        except requests.exceptions.JSONDecodeError:
            self.stats_output.setText('Failed to update XP: Invalid response from server')
            self.stats_output.setStyleSheet("color: red;")

    def update_hours(self):
        hours_botted = self.hours_entry.text()
        url = f'{BASE_URL}/update_hours_botted'
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        data = {'hours_botted': hours_botted}
        response = requests.post(url, json=data, headers=headers)
        try:
            response_data = response.json()
            if response.status_code == 200:
                self.stats_output.setText(f'Successfully updated hours botted to {hours_botted}')
                self.stats_output.setStyleSheet("color: green;")
            else:
                self.stats_output.setText(f'Failed to update hours: {response_data}')
                self.stats_output.setStyleSheet("color: red;")
        except requests.exceptions.JSONDecodeError:
            self.stats_output.setText('Failed to update hours: Invalid response from server')
            self.stats_output.setStyleSheet("color: red;")

    def refresh_offerings(self):
        self.offerings_listbox.clear()
        offerings = self.list_offerings()
        for offering in offerings:
            item = QtWidgets.QListWidgetItem(f"ID: {offering[0]} - Title: {offering[3]}")
            item.setData(QtCore.Qt.UserRole, offering)
            self.offerings_listbox.addItem(item)

    def populate_offering_fields(self):
        selected_items = self.offerings_listbox.selectedItems()
        if selected_items:
            offering = selected_items[0].data(QtCore.Qt.UserRole)
            self.tag_dropdown.setCurrentText(offering[1])
            self.image_dropdown.setCurrentText(offering[2].split('/')[-1])
            self.title_entry.setText(offering[3])
            self.description_entry.setText(offering[4])

    def add_offering(self):
        tag = self.tag_dropdown.currentText()
        image = self.image_dropdown.currentText()
        title = self.title_entry.text()
        description = self.description_entry.text()
        image_path = f'/images/{image}'
        url = f'{BASE_URL}/add_offering'
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        data = {'tag': tag, 'image': image_path, 'title': title, 'description': description}
        response = requests.post(url, json=data, headers=headers)
        try:
            response_data = response.json()
            if response.status_code == 200:
                self.offerings_output.setText(f'Successfully added offering with ID {response_data.get("id")}')
                self.offerings_output.setStyleSheet("color: green;")
                self.refresh_offerings()
            else:
                self.offerings_output.setText(f'Failed to add offering: {response_data}')
                self.offerings_output.setStyleSheet("color: red;")
        except requests.exceptions.JSONDecodeError:
            self.offerings_output.setText('Failed to add offering: Invalid response from server')
            self.offerings_output.setStyleSheet("color: red;")

    def remove_offering(self):
        selected_items = self.offerings_listbox.selectedItems()
        if not selected_items:
            self.offerings_output.setText("No offering selected")
            self.offerings_output.setStyleSheet("color: red;")
            return
        offering = selected_items[0].data(QtCore.Qt.UserRole)
        offering_id = offering[0]
        url = f'{BASE_URL}/remove_offering'
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        data = {'id': offering_id}
        response = requests.post(url, json=data, headers=headers)
        try:
            response_data = response.json()
            if response.status_code == 200:
                self.offerings_output.setText(f'Successfully removed offering with ID {response_data.get("removed_id")}')
                self.offerings_output.setStyleSheet("color: green;")
                self.refresh_offerings()
            else:
                self.offerings_output.setText(f'Failed to remove offering: {response_data}')
                self.offerings_output.setStyleSheet("color: red;")
        except requests.exceptions.JSONDecodeError:
            self.offerings_output.setText('Failed to remove offering: Invalid response from server')
            self.offerings_output.setStyleSheet("color: red;")

    def edit_offering(self):
        selected_items = self.offerings_listbox.selectedItems()
        if not selected_items:
            self.offerings_output.setText("No offering selected")
            self.offerings_output.setStyleSheet("color: red;")
            return
        offering = selected_items[0].data(QtCore.Qt.UserRole)
        offering_id = offering[0]
        tag = self.tag_dropdown.currentText()
        image = self.image_dropdown.currentText()
        title = self.title_entry.text()
        description = self.description_entry.text()
        image_path = f'/images/{image}'
        url = f'{BASE_URL}/edit_offering'
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        data = {
            'id': offering_id,
            'tag': tag,
            'image': image_path,
            'title': title,
            'description': description
        }
        response = requests.post(url, json=data, headers=headers)
        try:
            response_data = response.json()
            if response.status_code == 200:
                self.offerings_output.setText(f'Successfully edited offering with ID {response_data.get("edited_id")}')
                self.offerings_output.setStyleSheet("color: green;")
                self.refresh_offerings()
            else:
                self.offerings_output.setText(f'Failed to edit offering: {response_data}')
                self.offerings_output.setStyleSheet("color: red;")
        except requests.exceptions.JSONDecodeError:
            self.offerings_output.setText('Failed to edit offering: Invalid response from server')
            self.offerings_output.setStyleSheet("color: red;")

    def list_offerings(self):
        url = f'{BASE_URL}/offerings'
        try:
            response = requests.get(url)
            if not response.content.strip():
                return []
            data = response.json()
            if 'error' in data:
                return []
            offerings = data.get('offerings', [])
            if not offerings:
                return []
            return offerings
        except Exception as e:
            return []

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ServerManagementUI()
    window.show()
    sys.exit(app.exec_())
