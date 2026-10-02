import sys
import os
import bcrypt
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, 
                             QLabel, QVBoxLayout,  QScrollArea, 
                             QPushButton, QTableWidgetItem, QMessageBox,
                              QApplication, QMainWindow, QHeaderView)
from PyQt6.QtCore import pyqtSignal, Qt
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from Controller.UserController import (login_user, insert_staff, get_all_staff, get_staff_by_username,
                                       update_staff, get_total_users, get_active_users, get_inactive_users)
from Controller.roomController import  (insert_room, get_all_room, 
                                        get_room_by_number,  update_room, 
                                        delete_room as delete_room_controller, 
                                        get_available_rooms, get_available_rooms, 
                                        update_room_status, get_total_rooms, get_available_rooms_count,
                                        get_occupied_rooms_count, get_room_count_by_category)
from Controller.reservationController import (insert_reservation, get_reservations,
                                              update_reservation_status, update_room_available,
                                              update_room_occupied, update_reservation_room, get_total_revenue,
                                              get_reservation_count_by_status)
from database.DBConnection import connect_db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("user_interfaces/login.ui", self)
        
        self.btnLogin.clicked.connect(self.handle_login)
    
    def handle_login(self):
        username = self.txtUname.text()
        password = self.txtPass.text()

        user = login_user(username, password)
        
        if user == "inactive":
            QMessageBox.warning(self, "Access Denied", "This account is inactive.")
            return
        
        if user:
            self.current_user = user
        
        if user:
            role = user['role']

            print("Login Success:", role)

            if role.lower() == "admin":
                uic.loadUi("user_interfaces/mainwindows.ui", self)

                self.dashboard.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.dashboard_2))
                self.staff.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.staff_2))
                self.rooms.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Rooms))
                self.reports.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Reports))
                self.setting.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Setting))
                self.btnAddStaff.clicked.connect(self.add_staff)
                self.btnAddRoom.clicked.connect(self.add_room)
                self.btnSaveChange.clicked.connect(self.save_user_settings)
                self.btnChangePassword.clicked.connect(self.change_password)
                self.Logout.clicked.connect(self.logout)
                self.txtSearch.textChanged.connect(self.filter_reservations)
                
                self.report_widget = ReportWidget()
                self.verticalLayout_6.addWidget(self.report_widget)
                self.load_staff_table()
                self.load_room_table()
                self.load_user_settings()
                self.load_reservation_table()
                self.load_dashboard_cards()
                self.load_staff_room_cards()

            elif role.lower() == "front desk":
                uic.loadUi("user_interfaces/frontDesk.ui", self)
                
                self.dashboard.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.dashboard_2))
                self.Walkin.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.walkin))
                self.rooms.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.room))
                self.reservation.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.reservations))
                self.setting.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Setting))
                self.checkin.dateChanged.connect(self.load_room_combobox)
                self.checkout.dateChanged.connect(self.load_room_combobox)
                self.cbRoom.currentIndexChanged.connect(self.update_billing)
                self.checkin.dateChanged.connect(self.update_billing)
                self.checkout.dateChanged.connect(self.update_billing)
                self.btnConfirmReservation.clicked.connect(self.confirm_reservation)
                self.txtSearch.textChanged.connect(self.filter_reservations)
                self.btnSaveChange_3.clicked.connect(self.fd_save_user_settings)
                self.btnChangePassword_3.clicked.connect(self.fd_change_password)
                self.Logout.clicked.connect(self.logout)
                
                self.confirmed_container = QWidget()
                self.confirmed_layout = QVBoxLayout(self.confirmed_container)
                self.confirmed_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.confirmed_layout.setSpacing(10)

                confirmed_scroll = self.make_scrollable(self.confirmed_container)
                self.confirmed.setLayout(QVBoxLayout())
                self.confirmed.layout().addWidget(confirmed_scroll)

                self.checkin_container = QWidget()
                self.checkin_layout = QVBoxLayout(self.checkin_container)
                self.checkin_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.checkin_layout.setSpacing(10)

                checkin_scroll = self.make_scrollable(self.checkin_container)
                self.checkin_2.setLayout(QVBoxLayout())
                self.checkin_2.layout().addWidget(checkin_scroll)

                self.checkout_container = QWidget()
                self.checkout_layout = QVBoxLayout(self.checkout_container)
                self.checkout_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.checkout_layout.setSpacing(10)

                checkout_scroll = self.make_scrollable(self.checkout_container)
                self.checkout_2.setLayout(QVBoxLayout())
                self.checkout_2.layout().addWidget(checkout_scroll)
                
                self.load_room_combobox()
                self.clear_form()
                self.load_frontdesk_room_table()
                self.load_reservations()
                self.load_reservation_table()
                self.load_dashboard_cards()
                self.fd_load_user_settings()
                self.load_room_cards()
                self.load_reservation_cards()
            else:
                QMessageBox.warning(self, "Error", "Unknown role!")

        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
    
    def logout(self):
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()
    
    def load_user_settings(self):
        user = self.current_user
        self.txtFname.setText(user["firstname"])
        self.txtLname.setText(user["lastname"])
        self.txtGmail.setText(user["gmail"])
        self.txtUname.setText(user["username"])
        self.cbRole.setCurrentText(user["role"])
        
    def fd_load_user_settings(self):
        user = self.current_user
        self.txtFname_4.setText(user["firstname"])
        self.txtLname_4.setText(user["lastname"])
        self.txtGmail_4.setText(user["gmail"])
        self.txtUname_3.setText(user["username"])
        self.cbRole_3.setCurrentText(user["role"])
    
    def save_user_settings(self):
        fname = self.txtFname.text()
        lname = self.txtLname.text()
        gmail = self.txtGmail.text()
        username = self.current_user["username"]

        if not fname or not lname:
            QMessageBox.warning(self, "Error", "Name required")
            return

        try:
            update_staff(username, fname, lname, gmail, 
                        self.current_user["role"], 
                        self.current_user["status"])

            QMessageBox.information(self, "Success", "Profile updated!")

            self.current_user["firstname"] = fname
            self.current_user["lastname"] = lname
            self.current_user["gmail"] = gmail

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def fd_save_user_settings(self):
        fname = self.txtFname_4.text()
        lname = self.txtLname_4.text()
        gmail = self.txtGmail_4.text()
        username = self.current_user["username"]

        if not fname or not lname:
            QMessageBox.warning(self, "Error", "Name required")
            return

        try:
            update_staff(username, fname, lname, gmail, 
                        self.current_user["role"], 
                        self.current_user["status"])

            QMessageBox.information(self, "Success", "Profile updated!")

            self.current_user["firstname"] = fname
            self.current_user["lastname"] = lname
            self.current_user["gmail"] = gmail

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def change_password(self):
        current_pass = self.txtCurrentPass.text()
        new_pass = self.txtNewPass.text()
        confirm_pass = self.txtConfirmPass.text()

        username = self.current_user["username"]

        if not current_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        if len(new_pass) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT password FROM user WHERE username=%s", (username,))
            user = cursor.fetchone()

            if not user:
                QMessageBox.warning(self, "Error", "User not found!")
                return

            stored_password = user["password"]

            if stored_password.startswith("$2b$"):
                valid = bcrypt.checkpw(current_pass.encode(), stored_password.encode())
            else:
                valid = (current_pass == stored_password)

            if not valid:
                QMessageBox.warning(self, "Error", "Current password is incorrect!")
                return

            hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()

            cursor.execute(
                "UPDATE user SET password=%s WHERE username=%s",
                (hashed, username)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Password updated successfully!")

            self.txtCurrentPass.clear()
            self.txtNewPass.clear()
            self.txtConfirmPass.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def fd_change_password(self):
        current_pass = self.txtCurrentPass_3.text()
        new_pass = self.txtNewPass_3.text()
        confirm_pass = self.txtConfirmPass_3.text()

        username = self.current_user["username"]

        if not current_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        if len(new_pass) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT password FROM user WHERE username=%s", (username,))
            user = cursor.fetchone()

            if not user:
                QMessageBox.warning(self, "Error", "User not found!")
                return

            stored_password = user["password"]

            if stored_password.startswith("$2b$"):
                valid = bcrypt.checkpw(current_pass.encode(), stored_password.encode())
            else:
                valid = (current_pass == stored_password)

            if not valid:
                QMessageBox.warning(self, "Error", "Current password is incorrect!")
                return

            hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()

            cursor.execute(
                "UPDATE user SET password=%s WHERE username=%s",
                (hashed, username)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Password updated successfully!")

            self.txtCurrentPass_3.clear()
            self.txtNewPass_3.clear()
            self.txtConfirmPass_3.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def add_staff(self):
        self.add_staff_window = AddStaffWindow()
        self.add_staff_window.show()
        
        self.add_staff_window.staff_added.connect(self.load_staff_table)
        self.add_staff_window.staff_added.connect(self.load_staff_room_cards)
    
    def load_staff_table(self):
        data = get_all_staff()

        self.table_user.setRowCount(0)
        self.table_user.setColumnCount(7)
        self.table_user.setHorizontalHeaderLabels([
            "First Name", "Last Name", "Gmail", "Username", "Role", "Status", "Action"
        ])

        for row_num, row_data in enumerate(data):
            self.table_user.insertRow(row_num)

            for col_num, col_data in enumerate(row_data):
                self.table_user.setItem(row_num, col_num,
                    QTableWidgetItem(str(col_data)))

            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(lambda _, r=row_num: self.edit_staff(r))
            btn_edit.setStyleSheet("""
                QPushButton {
                    background-color: rgb(245, 192, 34);
                    color: black;  /* ✅ TEXT COLOR HERE */
                    border-radius: 6px;
                    padding: 5px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: rgb(255, 210, 60);
                    color: black;  /* keep consistent */
                }

                QPushButton:pressed {
                    background-color: rgb(200, 150, 10);
                    color: black;
                }
                """)

            self.table_user.setCellWidget(row_num, 6, btn_edit)
        self.table_user.horizontalHeader().setStretchLastSection(True)
        self.table_user.horizontalHeader().setSectionResizeMode(
            self.table_user.horizontalHeader().ResizeMode.Stretch
        )
        self.table_user.verticalHeader().setVisible(False)
    
    def edit_staff(self, row):
        username = self.table_user.item(row, 3).text()

        self.update_staff_window = UpdateStaffWindow(username)
        self.update_staff_window.staff_updated.connect(self.load_staff_table)
        self.update_staff_window.staff_updated.connect(self.load_staff_room_cards)
        self.update_staff_window.show()
    
    def load_room_table(self):
        data = get_all_room()

        self.table_room.setRowCount(0)
        self.table_room.setColumnCount(7)
        self.table_room.setHorizontalHeaderLabels([
            "Room No", "Floor", "Category", "Capacity", "Price", "Status", "Action"
        ])

        for row_num, row_data in enumerate(data):
            self.table_room.insertRow(row_num)

            for col_num, col_data in enumerate(row_data):
                self.table_room.setItem(row_num, col_num,
                    QTableWidgetItem(str(col_data)))

            action_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)

            btn_edit = QPushButton("Edit")
            btn_edit.setStyleSheet("background-color: #FFC107;")
            btn_edit.clicked.connect(lambda _, r=row_num: self.edit_room(r))

            btn_delete = QPushButton("Delete")
            btn_delete.setStyleSheet("background-color: #F44336; color: white;")
            btn_delete.clicked.connect(lambda _, r=row_num: self.delete_room(r))

            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)
            action_widget.setLayout(layout)

            self.table_room.setCellWidget(row_num, 6, action_widget)

        self.table_room.horizontalHeader().setStretchLastSection(True)
        self.table_room.horizontalHeader().setSectionResizeMode(
            self.table_room.horizontalHeader().ResizeMode.Stretch
        )
    def edit_room(self, row):
        room_number = self.table_room.item(row, 0).text()
        self.update_room_window = UpdateRoomWindow(room_number)
        self.update_room_window.room_updated.connect(self.load_room_table)
        self.update_room_window.room_updated.connect(self.load_staff_room_cards)
        self.update_room_window.show()
    def delete_room(self, row):
        room_number = self.table_room.item(row, 0).text()

        reply = QMessageBox.question(
            self, "Delete",
            f"Delete room {room_number}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_room_controller(room_number)

                QMessageBox.information(self, "Deleted", f"Room {room_number} deleted successfully!")
                self.load_room_table()
                self.load_staff_room_cards()

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def add_room(self):
        self.add_room_window = AddRoomWindow()
        self.add_room_window.room_added.connect(self.load_room_table)
        self.add_room_window.room_added.connect(self.load_staff_room_cards)
        self.add_room_window.show()
        
    def load_room_combobox(self):
        checkin = self.checkin.date().toPyDate()
        checkout = self.checkout.date().toPyDate()

        if checkout <= checkin:
            self.cbRoom.clear()
            return

        self.cbRoom.clear()

        rooms = get_available_rooms(checkin, checkout)

        for room in rooms:
            room_id, room_number, category, capacity, price = room
            text = f"{room_number} - {category} ({capacity} pax)"
            self.cbRoom.addItem(text, (room_id, room_number, price))
                
    def update_billing(self):
        data = self.cbRoom.currentData()

        if not data:
            return

        room_id, room_number, price = data

        checkin = self.checkin.date().toPyDate()
        checkout = self.checkout.date().toPyDate()

        nights = (checkout - checkin).days
        if nights <= 0:
            nights = 1  

        total = nights * price

        self.label_23.setText(str(room_number))
        self.label_24.setText(str(price))
        self.label_25.setText(f"{nights} Days")
        self.label_27.setText(str(total))

        self.txtAmount.setText(str(total))
        
    def confirm_reservation(self):
        try:
            fname = self.txtFname.text()
            lname = self.txtLname.text()
            email = self.txtGmail.text()
            phone = self.txtPhone.text()
            type_id = self.cbType.currentText()
            num_id = self.txtIdNum.text()

            checkin = self.checkin.date().toPyDate()
            checkout = self.checkout.date().toPyDate()

            payment_method = self.cbPayMethod.currentText()
            payment_amount = self.txtAmount.text()

            room_data = self.cbRoom.currentData()

            if not room_data:
                QMessageBox.warning(self, "Error", "Please select a room")
                return

            room_id, room_number, price = room_data

            if not fname or not lname:
                QMessageBox.warning(self, "Error", "Name is required")
                return

            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                QMessageBox.warning(self, "Error", "Invalid email format")
                return

            if not re.match(r"^09\d{9}$", phone):
                QMessageBox.warning(self, "Error", "Invalid phone (09XXXXXXXXX)")
                return

            if float(payment_amount) <= 0:
                QMessageBox.warning(self, "Error", "Invalid payment")
                return

            insert_reservation(
                room_id, fname, lname, email, phone,
                type_id, num_id, checkin, checkout,
                payment_method, float(payment_amount)
            )

            update_room_status(room_id, "Occupied")

            receipt = f"""
    ----- NCST HOTEL RECEIPT -----
    Name: {fname} {lname}
    Room: {room_number}
    Check-in: {checkin}
    Check-out: {checkout}
    Payment: {payment_method}
    Total: {payment_amount}
    -----------------------------
    """

            QMessageBox.information(self, "Success", receipt)

            self.load_room_combobox()
            self.clear_form()
            self.load_frontdesk_room_table()
            self.load_reservations()
            self.load_reservation_table()
            self.load_reservation_cards()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def clear_form(self):
        self.txtFname.clear()
        self.txtLname.clear()
        self.txtGmail.clear()
        self.txtPhone.clear()
        self.txtIdNum.clear()
        self.txtAmount.clear()

        self.cbType.setCurrentIndex(0)
        self.cbPayMethod.setCurrentIndex(0)
        self.cbRoom.setCurrentIndex(-1)

        today = datetime.today()
        self.checkin.setDate(today)
        self.checkout.setDate(today)

        self.label_23.setText("-")
        self.label_24.setText("-")
        self.label_25.setText("-")
        self.label_27.setText("-")
        
    def load_frontdesk_room_table(self):
        data = get_all_room()

        self.table_rooms_front.setRowCount(0)
        self.table_rooms_front.setColumnCount(6)
        self.table_rooms_front.setHorizontalHeaderLabels([
            "Room No", "Floor", "Category", "Capacity", "Price", "Status"
        ])

        for row_num, row_data in enumerate(data):
            self.table_rooms_front.insertRow(row_num)

            for col_num, col_data in enumerate(row_data):
                self.table_rooms_front.setItem(
                    row_num, col_num,
                    QTableWidgetItem(str(col_data))
                )

        self.table_rooms_front.horizontalHeader().setStretchLastSection(True)
        self.table_rooms_front.horizontalHeader().setSectionResizeMode(
            self.table_rooms_front.horizontalHeader().ResizeMode.Stretch
        )
        self.table_rooms_front.verticalHeader().setVisible(False)
        self.table_rooms_front.setEditTriggers(
            self.table_rooms_front.EditTrigger.NoEditTriggers
        )
        
    def load_reservations(self):
        data = get_reservations()

        self.clear_layout(self.confirmed_layout)
        self.clear_layout(self.checkin_layout)
        self.clear_layout(self.checkout_layout)

        for res in data:
            status = res["status"].lower()

            if status == "confirmed":
                card = self.create_reservation_card(
                    res,
                    buttons=[
                        ("Check-in", lambda _, r=res: self.handle_checkin(r), "#90EE90"),
                        ("Cancel", lambda _, r=res: self.handle_cancel(r), "#FF6B6B")
                    ]
                )
                self.confirmed_layout.addWidget(card)

            elif status in ["checked-in", "checked in"]:
                card = self.create_reservation_card(
                    res,
                    buttons=[
                        ("Change Room", lambda _, r=res: self.open_change_room(r), "#FFD54F"),
                        ("Check-out", lambda _, r=res: self.handle_checkout(r), "#87CEFA")
                    ]
                )
                self.checkin_layout.addWidget(card)

            elif status == "checked-out":
                card = self.create_reservation_card(res)
                self.checkout_layout.addWidget(card)
    
    def open_change_room(self, res):
        self.change_room_window = ChangeRoomWindow(res, self)
        self.change_room_window.show()
    
    def handle_checkin(self, res):
        update_reservation_status(res["id"], "Checked-in")
        update_room_occupied(res["room_id"])

        self.load_reservations()
        self.load_frontdesk_room_table()
        self.load_room_combobox()
        self.load_reservation_table()
        self.load_reservation_cards()
    
    def handle_checkout(self, res):
        update_reservation_status(res["id"], "Checked-out")
        update_room_available(res["room_id"])
        self.load_reservations()
        self.load_frontdesk_room_table()
        self.load_room_combobox()
        self.load_reservation_table()
        self.load_reservation_cards()
        
    def handle_cancel(self, res):
        update_reservation_status(res["id"], "Cancelled")
        update_room_available(res["room_id"])
        self.load_reservations()
        self.load_frontdesk_room_table()
        self.load_room_combobox()
        self.load_reservation_table()
        self.load_reservation_cards()
        
    def clear_layout(self, layout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
                
    def create_reservation_card(self, res, buttons=None):
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        
        name = QLabel(f"{res['fullname']}")
        name.setStyleSheet("font-weight: bold; font-size: 14px; color: black;")

        room = QLabel(f"Room: {res['room_number']} ({res['category']})")
        room.setStyleSheet("color: black;")

        status = QLabel(f"Status: {res['status']}")
        status.setStyleSheet("color: gray; font-size: 12px;")

        layout.addWidget(name)
        layout.addWidget(room)
        layout.addWidget(status)

        if buttons:
            btn_layout = QHBoxLayout()

            for text, handler, color in buttons:
                btn = QPushButton(text)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: black;
                        border-radius: 6px;
                        padding: 5px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        opacity: 0.8;
                    }}
                """)
                btn.clicked.connect(handler)
                btn_layout.addWidget(btn)

            layout.addLayout(btn_layout)

        card.setLayout(layout)
        return card
    
    def make_scrollable(self, widget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                width: 8px;
            }
        """)

        return scroll
    
    def load_reservation_table(self):
        data = get_reservations()

        self.table_reservation.setRowCount(0)
        self.table_reservation.setColumnCount(7)

        self.table_reservation.setHorizontalHeaderLabels([
            "Full Name", "Room No", "Category",
            "Check-in", "Check-out", "Price", "Status"
        ])

        for row_num, res in enumerate(data):
            self.table_reservation.insertRow(row_num)

            self.table_reservation.setItem(row_num, 0, QTableWidgetItem(res["fullname"]))
            self.table_reservation.setItem(row_num, 1, QTableWidgetItem(str(res["room_number"])))
            self.table_reservation.setItem(row_num, 2, QTableWidgetItem(res["category"]))
            self.table_reservation.setItem(row_num, 3, QTableWidgetItem(str(res["checkin"])))
            self.table_reservation.setItem(row_num, 4, QTableWidgetItem(str(res["checkout"])))
            self.table_reservation.setItem(row_num, 5, QTableWidgetItem(f"₱{res['price']:,}"))

            status_item = QTableWidgetItem(res["status"])
            status_text = res["status"].lower()

            if status_text in ["checked-in", "checked in"]:
                status_item.setBackground(Qt.GlobalColor.green)
            elif status_text == "cancelled":
                status_item.setBackground(Qt.GlobalColor.red)
            elif status_text == "confirmed":
                status_item.setBackground(Qt.GlobalColor.yellow)
            elif status_text == "checked-out":
                status_item.setBackground(Qt.GlobalColor.cyan)

            self.table_reservation.setItem(row_num, 6, status_item)

        
        
    def filter_reservations(self):
        keyword = self.txtSearch.text().lower()

        for row in range(self.table_reservation.rowCount()):
            full_name = self.table_reservation.item(row, 0).text().lower()
            room = self.table_reservation.item(row, 1).text().lower()
            category = self.table_reservation.item(row, 2).text().lower()
            status = self.table_reservation.item(row, 6).text().lower()

            if (keyword in full_name or
                keyword in room or
                keyword in category or
                keyword in status):
                self.table_reservation.setRowHidden(row, False)
            else:
                self.table_reservation.setRowHidden(row, True)
    
    def load_dashboard_cards(self):
        total_rooms = get_total_rooms()
        available = get_available_rooms_count()
        occupied = get_occupied_rooms_count()
        revenue = get_total_revenue()

        self.lblTotalRooms.setText(str(total_rooms))
        self.lblAvailable.setText(str(available))
        self.lblOccupied.setText(str(occupied))
        self.lblRevenue.setText(f"₱{revenue:,}")
        
    def load_staff_room_cards(self):
        total_users = get_total_users()
        active_users = get_active_users()
        inactive_users = get_inactive_users()

        self.lblTotalUsers.setText(str(total_users))
        self.lblActiveUsers.setText(str(active_users))
        self.lblInactiveUsers.setText(str(inactive_users))

        standard = get_room_count_by_category("Standard")
        deluxe = get_room_count_by_category("Deluxe")
        suite = get_room_count_by_category("Suite")

        self.lblStandard.setText(str(standard))
        self.lblDeluxe.setText(str(deluxe))
        self.lblSuite.setText(str(suite))
    
    def load_room_cards(self):
        standard = get_room_count_by_category("Standard")
        deluxe = get_room_count_by_category("Deluxe")
        suite = get_room_count_by_category("Suite")

        self.lblStandard.setText(str(standard))
        self.lblDeluxe.setText(str(deluxe))
        self.lblSuite.setText(str(suite))
        
    def load_reservation_cards(self):
        confirmed = get_reservation_count_by_status("Confirmed")
        checkin = get_reservation_count_by_status("Checked-in")
        checkout = get_reservation_count_by_status("Checked-out")
        cancelled = get_reservation_count_by_status("Cancelled")

        self.lblConfirmed.setText(str(confirmed))
        self.lblCheckin.setText(str(checkin))
        self.lblCheckout.setText(str(checkout))
        self.lblCancelled.setText(str(cancelled))

class ReportWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.bar_canvas = FigureCanvas(Figure(figsize=(4, 3)))
        self.ax_bar = self.bar_canvas.figure.add_subplot(111)

        self.pie_canvas = FigureCanvas(Figure(figsize=(4, 3)))
        self.ax_pie = self.pie_canvas.figure.add_subplot(111)

        layout.addWidget(self.bar_canvas)
        layout.addWidget(self.pie_canvas)

        self.setLayout(layout)

        self.load_data()
        
    def load_data(self):
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT category, COUNT(*) 
                    FROM room 
                    GROUP BY category
                """)
                data = cursor.fetchall()

                categories = [row[0] for row in data]
                counts = [row[1] for row in data]

                self.ax_bar.clear()
                self.ax_bar.bar(categories, counts)
                self.ax_bar.set_title("Rooms by Category")
                self.ax_bar.set_ylabel("Count")

                cursor.execute("""
                    SELECT status, COUNT(*) 
                    FROM reservation 
                    GROUP BY status
                """)
                data = cursor.fetchall()

                labels = [row[0] for row in data]
                sizes = [row[1] for row in data]

                colors = ['#2E5AAC', '#F4C542', '#2ECC71', '#E74C3C']

                self.ax_pie.clear()

                self.ax_pie.pie(
                    sizes,
                    labels=labels,
                    autopct='%1.0f%%',
                    startangle=90,
                    colors=colors,
                    textprops={'fontsize': 10}
                )

                centre_circle = plt.Circle((0, 0), 0.70, fc='white')
                self.ax_pie.add_artist(centre_circle)

                self.ax_pie.set_title("Reservation Status Distribution")

                
                self.bar_canvas.draw()
                self.pie_canvas.draw()

                conn.close()        

class UpdateStaffWindow(QMainWindow):
    staff_updated = pyqtSignal()

    def __init__(self, username):
        super().__init__()
        uic.loadUi("user_interfaces/updateStaff.ui", self)

        self.username = username

        self.load_data()

        self.btnUpdateStaff.clicked.connect(self.save_changes)

    def load_data(self):
        user = get_staff_by_username(self.username)

        if not user:
            QMessageBox.warning(self, "Error", "User not found")
            self.close()
            return

        self.txtFname.setText(user["firstname"])
        self.txtLname.setText(user["lastname"])
        self.txtGmail.setText(user["gmail"])
        self.txtUsername.setText(user["username"])

        self.cbRole.setCurrentText(user["role"])
        self.cbStatus.setCurrentText(user["status"])

    def save_changes(self):
        fname = self.txtFname.text()
        lname = self.txtLname.text()
        gmail = self.txtGmail.text()
        role = self.cbRole.currentText()
        status = self.cbStatus.currentText()

        if not fname or not lname:
            QMessageBox.warning(self, "Error", "Name required")
            return

        try:
            update_staff(self.username, fname, lname, gmail, role, status)

            QMessageBox.information(self, "Success", "Staff updated successfully!")

            self.staff_updated.emit()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class ChangeRoomWindow(QMainWindow):
    def __init__(self, reservation, parent=None):
        super().__init__(parent)
        uic.loadUi("user_interfaces/changeRoom.ui", self)

        self.res = reservation

        self.lblCurrent.setText(f"Current Room: {reservation['room_number']}")

        self.load_rooms()

        self.cbRoom.currentIndexChanged.connect(self.update_price)

        self.pushButton.clicked.connect(self.confirm_change)
        self.pushButton_2.clicked.connect(self.close)

    def load_rooms(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT room_id, room_number, category, capacity, price
            FROM room
            WHERE status = 'Available'
        """)

        rooms = cursor.fetchall()
        conn.close()

        self.cbRoom.clear()

        current_room_id = self.res["room_id"]

        for room in rooms:
            room_id, room_number, category, capacity, price = room

            if room_id == current_room_id:
                continue

            text = f"{room_number} - {category} ({capacity} pax)"
            self.cbRoom.addItem(text, (room_id, price, room_number))

        if self.cbRoom.count() == 0:
            QMessageBox.information(self, "Info", "No available rooms for transfer")

    def update_price(self):
        data = self.cbRoom.currentData()
        if not data:
            return

        room_id, price, room_number = data

        nights = (self.res["checkout"] - self.res["checkin"]).days
        if nights <= 0:
            nights = 1

        total = nights * price

        self.lblPrice.setText(f"New Price: {total}")
        self.new_total = total

    def confirm_change(self):
        data = self.cbRoom.currentData()
        if not data:
            QMessageBox.warning(self, "Error", "Select a room")
            return

        room_id, price, room_number = data

        if not hasattr(self, "new_total"):
            self.update_price()

        reply = QMessageBox.question(
            self,
            "Confirm",
            f"Change to room {room_number}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            update_reservation_room(
                self.res["id"],  
                room_id,
                self.new_total,
            )

            QMessageBox.information(self, "Success", "Room changed successfully!")
            if self.parent():
                self.parent().load_reservations()
                self.parent().load_frontdesk_room_table()
                self.parent().load_room_combobox()
                self.parent().load_reservation_table()
                
            self.close()
            

class AddStaffWindow(QMainWindow):
    staff_added = pyqtSignal()
    def __init__(self):
        super().__init__()
        uic.loadUi("user_interfaces/addStaff.ui", self)
        self.btnSaveStaff.clicked.connect(self.save_staff)
    
    def save_staff(self):
        firstname = self.txtFname.text().strip()
        lastname = self.txtLname.text().strip()
        gmail = self.txtGmail.text().strip()
        username = self.txtUname.text().strip()
        role = self.cbRole.currentText()
        password = self.txtPass.text().strip()

        if not firstname or not lastname or not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters!")
            return

        if "@" not in gmail:
            QMessageBox.warning(self, "Error", "Invalid email format!")
            return

        try:
            insert_staff(firstname, lastname, gmail, role, username, password)
            self.staff_added.emit()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class AddRoomWindow(QMainWindow):
    room_added = pyqtSignal() 

    def __init__(self):
        super().__init__()
        uic.loadUi("user_interfaces/addRoom.ui", self)
        self.btnSaveRoom.clicked.connect(self.save_room)

    def save_room(self):
        roomnumber = self.txtRnum.text().strip()
        floornumber = self.cbFnum.currentText()
        category = self.cbCategory.currentText()
        status = self.cbStatus.currentText()
        price = self.txtPrice.text().strip()
        capacity = self.txtCapacity.text().strip()

        if not roomnumber or not price or not capacity:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            price = int(price)
            capacity = int(capacity)
        except ValueError:
            QMessageBox.warning(self, "Error", "Price must be number and capacity must be integer!")
            return

        roomnumber = str(roomnumber).zfill(2)
        combined_room = f"{floornumber}{roomnumber}"

        if get_room_by_number(combined_room):
            QMessageBox.warning(self, "Error", "Room already exists!")
            return

        try:
            insert_room(combined_room, floornumber, category, status, price, capacity)
            QMessageBox.information(self, "Success", f"Room {combined_room} added successfully!")
            self.room_added.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class UpdateRoomWindow(QMainWindow):
    room_updated = pyqtSignal()

    def __init__(self, room_number):
        super().__init__()
        uic.loadUi("user_interfaces/updateRoom.ui", self)
        self.original_room_number = room_number
        self.load_room_data()
        self.btnSaveRoom.clicked.connect(self.update_room)

    def load_room_data(self):
        data = get_room_by_number(self.original_room_number)
        if data:
            room_number, floor, category, status, price, capacity = data
            self.txtRnum.setText(room_number[-2:]) 
            self.cbFnum.setCurrentText(str(floor))
            self.cbCategory.setCurrentText(category)
            self.cbStatus.setCurrentText(status)
            self.txtPrice.setText(str(price))
            self.txtCapacity.setText(str(capacity))
        else:
            QMessageBox.warning(self, "Error", "Room not found!")

    def update_room(self):
        roomnumber = self.txtRnum.text().strip()
        floornumber = self.cbFnum.currentText()
        category = self.cbCategory.currentText()
        status = self.cbStatus.currentText()
        price = self.txtPrice.text().strip()
        capacity = self.txtCapacity.text().strip()

        if not roomnumber or not price or not capacity:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            price = int(price)
            capacity = int(capacity)
        except ValueError:
            QMessageBox.warning(self, "Error", "Price must be number and capacity must be integer!")
            return

        combined_room = f"{floornumber}{str(roomnumber).zfill(2)}"

        try:
            update_room(self.original_room_number, combined_room, floornumber, category, status, price, capacity)
            QMessageBox.information(self, "Success", f"Room {combined_room} updated successfully!")
            self.room_updated.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
