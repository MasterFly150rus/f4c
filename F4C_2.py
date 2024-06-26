from F4_UI import Ui_MainWindow
from F4C_fill_UI import Ui_F4C_fill
from TourI import Ui_TourI
from TourII import Ui_TourII
from Flylist import Ui_Flylist
from Timetable import Ui_Timetable
from Data import Ui_Data
from PyQt5 import QtWidgets, QtGui, QtPrintSupport, QtCore
from PyQt5.QtWidgets import QWidget, QDialog, QMainWindow, QMessageBox, QFileDialog, QHeaderView
from PyQt5.Qt import QApplication, Qt
from PyQt5.QtCore import QDate, QAbstractTableModel, QModelIndex, QSortFilterProxyModel, QDateTime
import sys
import pickle
from pathlib import Path

headers = ('№', 'Фамилия', 'Имя', 'Регион', 'Прототип', 'Стенд', 'I тур', 'II тур', 'III тур', 'Результат', 'Место')
tourI_headers = ('Место', 'Фамилия', 'Имя', 'Регион', 'Прототип', 'Стенд', 'I тур', 'Результат')
tourII_headers = ('Место', 'Фамилия', 'Имя', 'Регион', 'Прототип', 'Стенд', 'I тур', 'II тур', 'Результат')
timetable_headers = {0: ('Жеребьёвка', 'Фамилия', 'Имя', 'Регион', 'Прототип'),
                     1: ('П. старта', 'Фамилия', 'Имя', 'Регион', 'Прототип', 'Стенд', 'I тур', 'Результат'),
                     2: ('П. старта', 'Фамилия', 'Имя', 'Регион', 'Прототип', 'Стенд', 'I тур', 'II тур', 'Результат')}

class F4C(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttons = (self.add_action, self.delete_action, self.info_action, self.line_action, self.tour_I_action,
                        self.tour_II_action, self.result_action)
        self.locate_data = Info()
        self.referees()
        self.memberdata = Data()
        self.f4cui = f4cWindow()
        self.tour = TourI()
        self.tourII = TourII()
        self.flylistui = FlyList()
        self.timetable = Timetable()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_4.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tour.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tourII.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.timetable.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table = None
        self.memberclass = ""
        self.tournumber = 'I'
        self.count_id = 0
        self.fly_tup = (
            '---', 'Восьмёрка', 'Снижение по кругу 360 градусов', 'A. Боевой разворот', 'B. Выпуск и уборка шасси',
            'C. Выпуск и уборка закрылков', 'D. Сбрасывание бомб или топливных баков', 'E. Срывной поворот',
            'F. Иммельман', 'G. Одна петля', 'HJ. Кубинская "8" прямая полная', 'HK. Кубинская "8" прямая половина',
            'IJ. Кубинская "8" обратная полная', 'IK. Кубинская "8" обратная половина', 'L. Половина “S” (обратная)',
            'M. Нормальный штопор (три витка)', 'N. Бочка', 'O. Парашют', 'P. Касание земли и взлёт (конвейер)',
            'Q. Перелёт при посадке', 'R. Скольжение влево или вправо', 'S. 1-ый полётный маневр прототипа',
            'T. 2-ой полётный маневр прототипа', 'U. Полёт по треугольному маршруту',
            'V. Полёт по четырёхугольному маршруту', 'W. Полёт по прямой на постоянной высоте (6 м)',
            'X. Полёт по прямой с одним из двигателей на малых об.', 'Y. "Ленивая" восьмёрка', 'Z. Поворот на горке',
            'AA. Перевёрнутый полёт', 'AB. Derry Turn', 'AC. Полный разворот', 'AD. Полет на малой скорости')
        self.k_tup = (13, 13, 13, 3, 2, 8, 3, 7, 7, 12, 5, 9, 5)
        self.kh_tup = (5, 5, 5, 3, 2, 3, 2, 4, 0, 6, 0, 0, 0)
        self.fly_k = (11, 7, 7, 7, 7, 7, 7, 7, 7, 11, 4, 9, 9)
        self.f4c_dict = {4: 'Текстура поверхности и реализм', 5: 'Мастерство изготовления', 6: 'Масштабность деталей'}
        self.f4h_dict = {4: 'Реализм', 5: 'Разработка, происхождение и дизайн модели', 6: ''}
        self.f4c_1_dict = {8: 'a) текстура поверхности', 9: 'b) соотв. текстуры масштабу', 10: 'а) качество',
                           11: 'b) сложность', 12: 'а) точность', 13: 'b) сложность'}
        for fly_items in range(2, 10):
            exec(f'self.memberdata.comboBox_{fly_items}.addItems(self.fly_tup)')
        self.currentmember = None
        self.file = ''
        self.file_in = ''
        self.saved_flag = False
        self.referee_fields = ((self.lineEdit_0_0, self.lineEdit_0_1, self.lineEdit_0_2),
                               (self.lineEdit_1_0, self.lineEdit_1_1, self.lineEdit_1_2),
                               (self.lineEdit_2_0, self.lineEdit_2_1, self.lineEdit_2_2),
                               (self.lineEdit_3_0, self.lineEdit_3_1, self.lineEdit_3_2),
                               (self.lineEdit_4_0, self.lineEdit_4_1, self.lineEdit_4_2),
                               (self.lineEdit_5_0, self.lineEdit_5_1, self.lineEdit_5_2),
                               (self.lineEdit_6_0, self.lineEdit_6_1, self.lineEdit_6_2),
                               (self.lineEdit_7_0, self.lineEdit_7_1, self.lineEdit_7_2),
                               (self.lineEdit_8_0, self.lineEdit_8_1, self.lineEdit_8_2),
                               (self.lineEdit_9_0, self.lineEdit_9_1, self.lineEdit_9_2))
        self.classes = {'F-4C': self.tableView, 'F-4C (Ю)': self.tableView_2, 'F-4H': self.tableView_3,
                        'F-4G': self.tableView_4}
        self.stat_disable_boxes = (self.memberdata.dsb_1_8, self.memberdata.dsb_2_8, self.memberdata.dsb_3_8,
                                   self.memberdata.dsb_1_10, self.memberdata.dsb_2_10, self.memberdata.dsb_3_10,
                                   self.memberdata.dsb_1_11, self.memberdata.dsb_2_11, self.memberdata.dsb_3_11,
                                   self.memberdata.dsb_1_12, self.memberdata.dsb_2_12, self.memberdata.dsb_3_12)
        for cls in self.classes:
            self.f4cui.cls_box.addItem(cls)
        self.f4cui.cls_box.currentIndexChanged.connect(lambda: self.change_tab(self.f4cui.cls_box.currentIndex() + 1))
        self.f4cui.cls_box.currentIndexChanged.connect(lambda: self.tabWidget.setCurrentIndex(self.f4cui.cls_box.currentIndex() + 1))
        # self.set_start_date()
        # self.set_end_date()
        self.add_action.triggered.connect(self.get_data)
        self.new_action.triggered.connect(self.new_file)
        self.delete_action.triggered.connect(self.qwestion)
        self.info_action.triggered.connect(self.data_filling)
        self.tour_I_action.triggered.connect(self.tour_1_out)
        self.tour_II_action.triggered.connect(self.tour_2_out)
        self.result_action.triggered.connect(lambda: self.handlePreview(self.tour_3_request))
        self.line_action.triggered.connect(self.timetable_preview)
        self.tableView.doubleClicked.connect(self.data_filling)
        self.tableView_2.doubleClicked.connect(self.data_filling)
        self.tableView_3.doubleClicked.connect(self.data_filling)
        self.tableView_4.doubleClicked.connect(self.data_filling)
        self.tour.pushButton.clicked.connect(lambda: self.handlePreview(self.tour_1_request))
        self.tourII.pushButton.clicked.connect(lambda: self.handlePreview(self.tour_2_request))
        self.timetable.print_btn.clicked.connect(lambda: self.handlePreview(self.timetable_1_request
                                                                            if self.timetable.radioButton.isChecked()
                                                                            else self.timetable_2_request
                                                                            if self.timetable.radioButton_2.isChecked()
                                                                            else self.timetable_3_request))
        self.lineEdit_25.textChanged.connect(self.set_locate)
        self.lineEdit_26.textChanged.connect(self.set_ekp_f4c)
        self.lineEdit_27.textChanged.connect(self.set_ekp_f4cu)
        self.dateEdit.dateChanged.connect(self.set_start_date)
        self.dateEdit_2.dateChanged.connect(self.set_end_date)
        self.timetable.dateTimeEdit.dateTimeChanged.connect(self.set_tourtime)
        self.action.triggered.connect(self.save_)
        self.action_2.triggered.connect(self.filein)
        self.action_3.triggered.connect(self.save_as)
        self.about_action.triggered.connect(self.show_about)
        self.tabWidget.currentChanged.connect(lambda: self.change_tab(self.tabWidget.currentIndex()))
        self.f4cui.buttonBox.accepted.connect(self.new_member)
        self.memberdata.radioButton.clicked.connect(self.get_prog)
        self.memberdata.fl_rb_1.clicked.connect(self.get_prog)
        self.memberdata.fl_rb_2.clicked.connect(self.get_prog)
        self.memberdata.fl_rb_3.clicked.connect(self.get_prog)
        self.memberdata.flylist_btn.clicked.connect(self.fly_list)
        self.memberdata.print_grades_btn.clicked.connect(lambda: self.handlePreview(self.gradelist_request))
        self.memberdata.gl_rb_1.clicked.connect(self.grade_list)
        self.memberdata.gl_rb_2.clicked.connect(self.grade_list)
        self.memberdata.gl_rb_3.clicked.connect(self.grade_list)
        self.flylistui.pushButton.clicked.connect(lambda: self.handlePreview(self.flylist_request))
        self.memberdata.print_static_btn.clicked.connect(lambda: self.handlePreview(self.static_f4h_request
                                                                          if self.memberclass == 'F-4H'
                                                                          else self.static_request))
        self.f4c_data =[]
        self.f4cu_data = []
        self.f4h_data = []
        self.f4g_data = []
        self.f4c_in_model = TableModel(headers, self.f4c_data)
        self.f4c_model = QSortFilterProxyModel()
        self.f4c_model.setSourceModel(self.f4c_in_model)
        self.f4cu_in_model = TableModel(headers, self.f4cu_data)
        self.f4cu_model = QSortFilterProxyModel()
        self.f4cu_model.setSourceModel(self.f4cu_in_model)
        self.f4h_in_model = TableModel(headers, self.f4h_data)
        self.f4h_model = QSortFilterProxyModel()
        self.f4h_model.setSourceModel(self.f4h_in_model)
        self.f4g_in_model = TableModel(headers, self.f4g_data)
        self.f4g_model = QSortFilterProxyModel()
        self.f4g_model.setSourceModel(self.f4g_in_model)
        self.classlist = {1: 'F-4C', 2: 'F-4C (Ю)', 3: 'F-4H', 4: 'F-4G'}
        self.dataclasses = {'F-4C': self.f4c_data, 'F-4C (Ю)': self.f4cu_data, 'F-4H': self.f4h_data,
                            'F-4G': self.f4g_data}
        self.models = {'F-4C': self.f4c_model, 'F-4C (Ю)': self.f4cu_model, 'F-4H': self.f4h_model,
                       'F-4G':  self.f4g_model}
        self.in_models = {'F-4C': self.f4c_in_model, 'F-4C (Ю)': self.f4cu_in_model, 'F-4H': self.f4h_in_model,
                       'F-4G': self.f4g_in_model}
        self.clearfields = (self.f4cui.lineEdit_2, self.f4cui.lineEdit_3, self.f4cui.lineEdit_4, self.f4cui.lineEdit_5)
        self.zerofields = (self.f4cui.scale_box, self.f4cui.speed_box, self.f4cui.toss_box)
        self.r_buttons = (self.timetable.radioButton, self.timetable.radioButton_2, self.timetable.radioButton_3)
        for cls in self.classes:
            table = self.classes[cls]
            table.setModel(self.models[cls])
            table.setSortingEnabled(True)
            table.sortByColumn(10, Qt.AscendingOrder)
        self.data = None
        self.model = None
        if len(sys.argv) == 2:
            self.file_in = sys.argv[1]
            self.file = sys.argv[1]
            self.open_file()
        self.timetable.radioButton.index = 0
        self.timetable.radioButton_2.index = 1
        self.timetable.radioButton_3.index = 2
        self.timetable.buttonGroup.buttonClicked.connect(self.timetable_preview)
        self.connect_info_fields()
        self.connect_prog_fields()
        self.connect_grades_fields()
        self.connect_static_fields()
        self.connect_general_fields()

    def connect_info_fields(self):
        self.memberdata.save_info_btn.clicked.connect(self.set_info)
        info_lineedits = (self.memberdata.lineEdit_surname, self.memberdata.lineEdit_name,
                            self.memberdata.lineEdit_region, self.memberdata.lineEdit_prototype)
        info_boxes = (self.memberdata.scale_box, self.memberdata.speed_box, self.memberdata.toss_box)
        for lineedit in info_lineedits:
            lineedit.textChanged.connect(lambda: self.set_enable(self.memberdata.save_info_btn))
        for box in info_boxes:
            box.valueChanged.connect(lambda: self.set_enable(self.memberdata.save_info_btn))

    def connect_prog_fields(self):
        self.memberdata.save_prog_btn.clicked.connect(self.set_prog)
        prog_combo = (self.memberdata.comboBox_2, self.memberdata.comboBox_3, self.memberdata.comboBox_4,
                           self.memberdata.comboBox_5, self.memberdata.comboBox_6, self.memberdata.comboBox_7,
                           self.memberdata.comboBox_8, self.memberdata.comboBox_9)
        prog_buttons = (self.memberdata.radioButton, self.memberdata.fl_rb_1, self.memberdata.fl_rb_2,
                             self.memberdata.fl_rb_3)
        for combo in prog_combo:
            combo.currentIndexChanged.connect(lambda: self.set_enable(self.memberdata.save_prog_btn))
        for flrb in prog_buttons:
            flrb.clicked.connect(lambda: self.set_enable(self.memberdata.save_prog_btn))

    def connect_grades_fields(self):
        self.memberdata.save_grades_btn.clicked.connect(self.set_grades)
        fields = (self.memberdata.sb_1_1, self.memberdata.sb_1_2, self.memberdata.sb_1_3,
                  self.memberdata.sb_1_4, self.memberdata.sb_1_5, self.memberdata.sb_1_6,
                  self.memberdata.sb_1_7, self.memberdata.sb_1_8, self.memberdata.sb_1_9,
                  self.memberdata.sb_1_10, self.memberdata.sb_1_11, self.memberdata.sb_1_12,
                  self.memberdata.sb_2_13, self.memberdata.sb_2_1, self.memberdata.sb_2_2,
                  self.memberdata.sb_2_3, self.memberdata.sb_2_4, self.memberdata.sb_2_5,
                  self.memberdata.sb_2_6, self.memberdata.sb_2_7, self.memberdata.sb_2_8,
                  self.memberdata.sb_2_9, self.memberdata.sb_2_10, self.memberdata.sb_2_11,
                  self.memberdata.sb_2_12, self.memberdata.sb_2_13, self.memberdata.sb_3_1,
                  self.memberdata.sb_3_2, self.memberdata.sb_3_3, self.memberdata.sb_3_4,
                  self.memberdata.sb_3_5, self.memberdata.sb_3_6, self.memberdata.sb_3_7,
                  self.memberdata.sb_3_8, self.memberdata.sb_3_9, self.memberdata.sb_3_10,
                  self.memberdata.sb_3_11, self.memberdata.sb_3_12, self.memberdata.sb_3_13)
        for field in fields:
            field.valueChanged.connect(lambda: self.memberdata.save_grades_btn.setEnabled(True))

    def connect_static_fields(self):
        self.memberdata.save_static_btn.clicked.connect(self.set_static)
        static_fields = (self.memberdata.dsb_1_0, self.memberdata.dsb_1_1, self.memberdata.dsb_1_2,
                         self.memberdata.dsb_1_3, self.memberdata.dsb_1_4, self.memberdata.dsb_1_5,
                         self.memberdata.dsb_1_6, self.memberdata.dsb_1_7, self.memberdata.dsb_1_8,
                         self.memberdata.dsb_1_9, self.memberdata.dsb_1_10, self.memberdata.dsb_1_11,
                         self.memberdata.dsb_1_12, self.memberdata.dsb_2_0, self.memberdata.dsb_2_1,
                         self.memberdata.dsb_2_2, self.memberdata.dsb_2_3, self.memberdata.dsb_2_4,
                         self.memberdata.dsb_2_5, self.memberdata.dsb_2_6, self.memberdata.dsb_2_7,
                         self.memberdata.dsb_2_8, self.memberdata.dsb_2_9, self.memberdata.dsb_2_10,
                         self.memberdata.dsb_2_11, self.memberdata.dsb_2_12, self.memberdata.dsb_3_0,
                         self.memberdata.dsb_3_1, self.memberdata.dsb_3_2, self.memberdata.dsb_3_3,
                         self.memberdata.dsb_3_4, self.memberdata.dsb_3_5, self.memberdata.dsb_3_6,
                         self.memberdata.dsb_3_7, self.memberdata.dsb_3_8, self.memberdata.dsb_3_9,
                         self.memberdata.dsb_3_10, self.memberdata.dsb_3_11, self.memberdata.dsb_3_12)
        for field in static_fields:
            field.valueChanged.connect(lambda: self.memberdata.save_static_btn.setEnabled(True))

    def connect_general_fields(self):
        self.group_1 = (self.lineEdit_0_0, self.lineEdit_1_0, self.lineEdit_2_0, self.lineEdit_3_0, self.lineEdit_4_0,
                   self.lineEdit_5_0, self.lineEdit_6_0, self.lineEdit_7_0, self.lineEdit_8_0, self.lineEdit_9_0)
        self.group_2 = (self.lineEdit_0_1, self.lineEdit_1_1, self.lineEdit_2_1, self.lineEdit_3_1, self.lineEdit_4_1,
                   self.lineEdit_5_1, self.lineEdit_6_1, self.lineEdit_7_1, self.lineEdit_8_1, self.lineEdit_9_1)
        self.group_3 = (self.lineEdit_0_2, self.lineEdit_1_2, self.lineEdit_2_2, self.lineEdit_3_2, self.lineEdit_4_2,
                   self.lineEdit_5_2, self.lineEdit_6_2, self.lineEdit_7_2, self.lineEdit_8_2, self.lineEdit_9_2)
        self.group_4 = (self.lineEdit_25, self.lineEdit_26, self.lineEdit_27)
        for count, field in enumerate(self.group_1):
            field.textChanged.connect(self.set_referee_boxes)
        for count, field in enumerate(self.group_2):
            field.textChanged.connect(self.set_referee_boxes)
        for count, field in enumerate(self.group_3):
            field.textChanged.connect(self.set_referee_boxes)
        self.lineEdit_0_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_0_0.text(), 0))
        self.lineEdit_1_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_1_0.text(), 1))
        self.lineEdit_2_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_2_0.text(), 2))
        self.lineEdit_3_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_3_0.text(), 3))
        self.lineEdit_4_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_4_0.text(), 4))
        self.lineEdit_5_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_5_0.text(), 5))
        self.lineEdit_6_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_6_0.text(), 6))
        self.lineEdit_7_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_7_0.text(), 7))
        self.lineEdit_8_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_8_0.text(), 8))
        self.lineEdit_9_0.textChanged.connect(lambda: self.set_surname(self.lineEdit_9_0.text(), 9))

        self.lineEdit_0_1.textChanged.connect(lambda: self.set_name(self.lineEdit_0_1.text(), 0))
        self.lineEdit_1_1.textChanged.connect(lambda: self.set_name(self.lineEdit_1_1.text(), 1))
        self.lineEdit_2_1.textChanged.connect(lambda: self.set_name(self.lineEdit_2_1.text(), 2))
        self.lineEdit_3_1.textChanged.connect(lambda: self.set_name(self.lineEdit_3_1.text(), 3))
        self.lineEdit_4_1.textChanged.connect(lambda: self.set_name(self.lineEdit_4_1.text(), 4))
        self.lineEdit_5_1.textChanged.connect(lambda: self.set_name(self.lineEdit_5_1.text(), 5))
        self.lineEdit_6_1.textChanged.connect(lambda: self.set_name(self.lineEdit_6_1.text(), 6))
        self.lineEdit_7_1.textChanged.connect(lambda: self.set_name(self.lineEdit_7_1.text(), 7))
        self.lineEdit_8_1.textChanged.connect(lambda: self.set_name(self.lineEdit_8_1.text(), 8))
        self.lineEdit_9_1.textChanged.connect(lambda: self.set_name(self.lineEdit_9_1.text(), 9))

        self.lineEdit_0_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_0_2.text(), 0))
        self.lineEdit_1_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_1_2.text(), 1))
        self.lineEdit_2_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_2_2.text(), 2))
        self.lineEdit_3_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_3_2.text(), 3))
        self.lineEdit_4_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_4_2.text(), 4))
        self.lineEdit_5_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_5_2.text(), 5))
        self.lineEdit_6_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_6_2.text(), 6))
        self.lineEdit_7_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_7_2.text(), 7))
        self.lineEdit_8_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_8_2.text(), 8))
        self.lineEdit_9_2.textChanged.connect(lambda: self.set_patronymic(self.lineEdit_9_2.text(), 9))

    def referees(self):
        self.referee_1 = Referee()
        self.referee_2 = Referee()
        self.referee_3 = Referee()
        self.referee_4 = Referee()
        self.referee_5 = Referee()
        self.referee_6 = Referee()
        self.referee_7 = Referee()
        self.referee_8 = Referee()
        self.referee_9 = Referee()
        self.referee_10 = Referee()

    def new_file(self):
        if self.saved_flag:
            self.save_qwestion()
        else:
            self.clear_all()
            self.referees()
            self.clear_fields()
            self.new_action.setEnabled(False)

    def save_qwestion(self):
        qwest = QMessageBox()
        qwest.setWindowTitle("ФАСР")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        qwest.setWindowIcon(icon)
        qwest.setText("Сохранить изменения?")
        qwest.setIcon(QMessageBox.Question)
        qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel)
        qwest.buttonClicked.connect(self.save_qwestion_action)
        qwest.exec_()

    def save_qwestion_action(self, btn):
        if btn.text() in ['OK', '&OK']:
            self.save_()
            self.clear_all()
            self.referees()
            self.clear_fields()
            self.new_action.setEnabled(False)
        if btn.text() in ['No', '&No']:
            self.clear_all()
            self.referees()
            self.clear_fields()
            self.new_action.setEnabled(False)
            self.action.setEnabled(False)
            self.saved_flag = False

    @staticmethod
    def show_about(self):
        report_ = QMessageBox()
        report_.setWindowTitle("О программе")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        report_.setWindowIcon(icon)
        report_.setText('Программа организации хранения и обработки информации об участниках соревнований по'
                        ' авиамодельному спорту в классах F-4C, F-4C(Ю), F-4H, F-4G ФАС РОССИИ.\n'
                        'Версия 2.4\n'
                        'Автор: Кирсанов Сергей\n'
                        'tel: +7 926-169-91-68\n'
                        'mailto: masterfly@mail.ru')
        report_.setIcon(QMessageBox.Information)
        report_.setStandardButtons(QMessageBox.Ok)
        report_.exec_()

    def set_enable(self, btn):
        if not btn.isEnabled():
            btn.setEnabled(True)

    def set_members(self, cls):
        data = self.dataclasses[cls]
        for i in Member.items:
            if i.cls == cls:
                data.append([i.number, i.surname, i.name, i.region, i.prototype, None, None, None, None, None, None,
                i.id])

    @staticmethod
    def error_(error_massage):
        error = QMessageBox()
        error.setWindowTitle("ФАСР")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        error.setWindowIcon(icon)
        error.setText(error_massage)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    def qwestion(self):
        row = self.table.currentIndex().row()
        if row == -1:
            self.error_('Выберите участника!')
            return
        qwest = QMessageBox()
        qwest.setWindowTitle("ФАСР")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        qwest.setWindowIcon(icon)
        qwest.setText("Вы уверны, что хотите удалить участника?")
        qwest.setIcon(QMessageBox.Question)
        qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        qwest.buttonClicked.connect(self.qwestuion_action)
        qwest.exec_()

    def qwestuion_action(self, btn):
        if btn.text() in ['OK', '&OK']:
            self.del_member()

    def del_member(self):
        row = self.table.currentIndex().row()
        data = self.dataclasses[self.memberclass]
        model = self.in_models[self.memberclass]
        number_index = self.model.index(row, 0)
        member_number = self.model.data(number_index, Qt.DisplayRole)
        for i in Member.items:
            if i.number == member_number:
                Member.items.remove(i)
                for j, k in enumerate(data):
                    if k[0] == member_number:
                        del data[j]
                        model.setItems(data)
        self.commit_changes()

    def get_data(self):
        self.prepare_fields()
        self.f4cui.spinBox.valueChanged.connect(self.f4c_filling)
        self.f4cui.show()

    def f4c_filling(self):
        self.prepare_fields()
        for i in Member.items:
            if i.number == self.f4cui.spinBox.value():
                self.f4cui.cls_box.setCurrentText(str(i.cls))
                self.f4cui.lineEdit_2.setText(str(i.surname))
                self.f4cui.lineEdit_3.setText(str(i.name))
                self.f4cui.lineEdit_4.setText(str(i.region))
                self.f4cui.lineEdit_5.setText(str(i.prototype))
                self.f4cui.scale_box.setValue(float(i.scale))
                self.f4cui.speed_box.setValue(int(i.speed))
                self.f4cui.toss_box.setValue(int(i.id))

    def prepare_fields(self):
        for field in self.clearfields:
            field.clear()
            field.setEnabled(False) if self.f4cui.spinBox.value() == 0 else field.setEnabled(True)
            for field in self.zerofields:
                field.setValue(0)
                field.setEnabled(False) if self.f4cui.spinBox.value() == 0 else field.setEnabled(True)

    def new_member(self):
        if self.f4cui.spinBox.value() == 0:
            self.error_('Укажите номер участника')
            self.get_data()
            return
        data = self.dataclasses[self.memberclass]
        model = self.in_models[self.memberclass]
        for i in Member.items:
            if i.number == self.f4cui.spinBox.value():
                self.error_('Участник с таким номером уже зарегистрирован!')
                self.get_data()
                return
        if self.f4cui.toss_box.value() > 0:
            for rows in data:
                if rows[11] == self.f4cui.toss_box.value():
                    self.error_('Участник с таким жребием уже зарегистрирован в этом классе')
                    self.get_data()
                    return
        a = f'member_{str(self.f4cui.spinBox.value())}'
        globals()[a] = Member(self.memberclass)
        globals()[a].cls = self.memberclass
        globals()[a].number = self.f4cui.spinBox.value()
        globals()[a].surname = self.f4cui.lineEdit_2.text()
        globals()[a].name = self.f4cui.lineEdit_3.text()
        globals()[a].region = self.f4cui.lineEdit_4.text()
        globals()[a].prototype = self.f4cui.lineEdit_5.text()
        globals()[a].scale = self.f4cui.scale_box.value()
        globals()[a].speed = self.f4cui.speed_box.value()
        globals()[a].id = self.f4cui.toss_box.value()

        data.append([globals()[a].number, globals()[a].surname, globals()[a].name, globals()[a].region,
                    globals()[a].prototype, None, None, None, None, None, None, globals()[a].id])
        model.setItems(data)
        self.commit_changes()

    def set_start_date(self):
        self.locate_data.start_date = self.dateEdit.date()
        self.commit_changes()

    def set_end_date(self):
        self.locate_data.end_date = self.dateEdit_2.date()
        self.commit_changes()

    def set_tourtime(self):
        tourindex = self.tourindex()
        if self.memberclass == 'F-4C':
            if tourindex == 0:
                self.locate_data.f4c_tour_1 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 1:
                self.locate_data.f4c_tour_2 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 2:
                self.locate_data.f4c_tour_3 = self.timetable.dateTimeEdit.dateTime()
        if self.memberclass == 'F-4C (Ю)':
            if tourindex == 0:
                self.locate_data.f4cu_tour_1 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 1:
                self.locate_data.f4cu_tour_2 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 2:
                self.locate_data.f4cu_tour_3 = self.timetable.dateTimeEdit.dateTime()
        if self.memberclass == 'F-4H':
            if tourindex == 0:
                self.locate_data.f4h_tour_1 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 1:
                self.locate_data.f4h_tour_2 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 2:
                self.locate_data.f4h_tour_3 = self.timetable.dateTimeEdit.dateTime()
        if self.memberclass == 'F-4G':
            if tourindex == 0:
                self.locate_data.f4g_tour_1 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 1:
                self.locate_data.f4g_tour_2 = self.timetable.dateTimeEdit.dateTime()
            if tourindex == 2:
                self.locate_data.f4g_tour_3 = self.timetable.dateTimeEdit.dateTime()
        self.commit_changes()

    def data_filling(self):
        row = self.table.currentIndex().row()
        if row == -1:
            self.error_('Выберите участника!')
            return
        number_index = self.model.index(row, 0)
        member_number = self.model.data(number_index, Qt.DisplayRole)
        for i in Member.items:
            if i.number == member_number and i.cls == self.memberclass:
                self.currentmember = i
                self.memberdata.label_number.setText(str(i.number))
                self.memberdata.lineEdit_surname.setText(str(i.surname))
                self.memberdata.lineEdit_name.setText(str(i.name))
                self.memberdata.lineEdit_prototype.setText(str(i.prototype))
                self.memberdata.scale_box.setValue(float(i.scale))
                self.memberdata.speed_box.setValue(int(i.speed))
                self.memberdata.lineEdit_region.setText(str(i.region))
                self.memberdata.label_cls.setText(str(i.cls))
                self.memberdata.toss_box.setValue(int(i.id))

                self.memberdata.member_label.setText(f'{i.cls} {i.surname} {i.name}')
                for j in range(2, 10):
                    exec(f'self.memberdata.comboBox_{str(j)}.setCurrentIndex(int(i.fig_{str(j)}[' \
                         f'{"1" if self.memberdata.fl_rb_2.isChecked() else "2" if self.memberdata.fl_rb_3.isChecked() else "0"}]))')

        self.grade_list()
        self.get_static()

        self.memberdata.show()

    def get_prog(self):
        for j in range(2, 10):
            exec(f'self.memberdata.comboBox_{str(j)}.setCurrentIndex(int(self.currentmember.fig_{str(j)}[' \
                 f'{"1" if self.memberdata.fl_rb_2.isChecked() else "2" if self.memberdata.fl_rb_3.isChecked() else "0"}]))')

    def get_static(self):
        if self.memberclass == 'F-4H':
            stat_k = self.kh_tup
            stat_lenth = 10
            dict = self.f4h_dict
        else:
            stat_k = self.k_tup
            stat_lenth = 13
            dict = self.f4c_dict
        correct_k = self.currentmember.static_k if self.memberclass == 'F-4G' else 1
        self.memberdata.surname_lbl.setText(str(self.currentmember.surname))
        self.memberdata.name_lbl.setText(str(self.currentmember.name))
        self.memberdata.number_lbl.setText(f'№ {str(self.currentmember.number)}')
        self.memberdata.prototype_lbl.setText(str(self.currentmember.prototype))
        self.memberdata.texture.setText(dict.get(4))
        self.memberdata.skill.setText(dict.get(5))
        self.memberdata.scale_2.setText(dict.get(6))
        self.memberdata.texture_a_lbl.setText('' if self.memberclass == 'F-4H' else self.f4c_1_dict.get(8))
        self.memberdata.scale_b_lbl.setText('' if self.memberclass == 'F-4H' else self.f4c_1_dict.get(9))
        self.memberdata.quality_lbl.setText('' if self.memberclass == 'F-4H' else self.f4c_1_dict.get(10))
        self.memberdata.difficulty_lbl.setText('' if self.memberclass == 'F-4H' else self.f4c_1_dict.get(11))
        self.memberdata.label_24.setText('' if self.memberclass == 'F-4H' else self.f4c_1_dict.get(12))
        self.memberdata.difficulty_2_lbl.setText('' if self.memberclass == 'F-4H' else self.f4c_1_dict.get(13))
        for box in self.stat_disable_boxes:
            box.setEnabled(False if self.memberclass == 'F-4H' else True)
            if self.memberclass == 'F-4H':
                box.setValue(0.0)
        self.memberdata.dsb_k.setValue(correct_k if self.memberclass == 'F-4G' else 1)
        self.memberdata.dsb_bonus.setValue(self.currentmember.bonus if self.memberclass == 'F-4H' else 0)

        for k in range(13):
            item = '' if stat_k[k] == 0 else stat_k[k]
            exec(f'self.memberdata.k_{str(k)}.setText(str({str(item)}))')
        sum_1 = 0
        sum_2 = 0
        sum_3 = 0
        for j in range(stat_lenth):
            grade_1 = float(self.currentmember.stat_grade_1[j])
            grade_2 = float(self.currentmember.stat_grade_2[j])
            grade_3 = float(self.currentmember.stat_grade_3[j])
            k = stat_k[j]
            score_1 = str(round(k * grade_1, 1))
            score_2 = str(round(k * grade_2, 1))
            score_3 = str(round(k * grade_3, 1))
            sum_1 = sum_1 + float(score_1)
            sum_2 = sum_2 + float(score_2)
            sum_3 = sum_3 + float(score_3)
            exec(f'self.memberdata.dsb_1_{str(j)}.setValue(self.currentmember.stat_grade_1[{str(j)}])')
            exec(f'self.memberdata.dsb_2_{str(j)}.setValue(self.currentmember.stat_grade_2[{str(j)}])')
            exec(f'self.memberdata.dsb_3_{str(j)}.setValue(self.currentmember.stat_grade_3[{str(j)}])')
            exec(f'self.memberdata.score_1_{str(j)}.setText(''score_1'')')
            exec('self.memberdata.score_2_' + str(j) + '.setText(''score_2'')')
            exec('self.memberdata.score_3_' + str(j) + '.setText(''score_3'')')
        total = (sum_1 + sum_2 + sum_3) * correct_k + self.currentmember.bonus
        self.memberdata.sum_1.setText(str(round(sum_1, 1)))
        self.memberdata.sum_2.setText(str(round(sum_2, 1)))
        self.memberdata.sum_3.setText(str(round(sum_3, 1)))
        self.memberdata.total_score.setText(str(round(total, 1)))

    def tour_1_out(self):
        source_data = self.dataclasses[self.memberclass]
        self.tournumber = 'I'
        self.tour.setWindowTitle(f'{self.memberclass} ФАС России {self.tournumber} тур')
        data = []
        res_list = []
        for row in source_data:
            new_row = []
            for col in range(1, 7):
                new_row.append(row[col])
            result = row[5] + row[6]
            new_row.append(result)
            res_list.append(result)
            data.append(new_row)
        table = self.tour.tableView
        place_list = sorted(res_list, reverse=True)
        for l in data:
            place = place_list.index(l[6]) + 1
            l.insert(0, place)
        tourI_in_model = TableModel(tourI_headers, data)
        tourI_model = QSortFilterProxyModel()
        tourI_model.setSourceModel(tourI_in_model)
        table.setModel(tourI_model)
        table.setSortingEnabled(True)
        table.sortByColumn(0, Qt.AscendingOrder)

        self.tour.show()

    def tour_2_out(self):
        source_data = self.dataclasses[self.memberclass]
        self.tournumber = 'II'
        self.tourII.setWindowTitle(f'{self.memberclass} ФАС России {self.tournumber} тур')
        data = []
        res_list = []
        for row in source_data:
            new_row = []
            for col in range(1, 8):
                new_row.append(row[col])
            result = row[5] + (row[6] + row[7]) / 2
            new_row.append(result)
            res_list.append(result)
            data.append(new_row)
        table = self.tourII.tableView
        place_list = sorted(res_list, reverse=True)
        for l in data:
            place = place_list.index(l[7]) + 1
            l.insert(0, place)
        tourII_in_model = TableModel(tourII_headers, data)
        tourII_model = QSortFilterProxyModel()
        tourII_model.setSourceModel(tourII_in_model)
        table.setModel(tourII_model)
        table.setSortingEnabled(True)
        table.sortByColumn(0, Qt.AscendingOrder)
        self.tourII.show()

    def set_locate(self):
        self.locate_data.locate = self.lineEdit_25.text()
        self.commit_changes()

    def set_ekp_f4c(self):
        self.locate_data.ekp_f4c = self.lineEdit_26.text()
        self.commit_changes()

    def set_ekp_f4cu(self):
        self.locate_data.ekp_f4cu = self.lineEdit_27.text()
        self.commit_changes()

    def save_(self):
        if self.file == "":
            self.save_as()
        else:
            self.write()
        self.action.setEnabled(False)
        self.saved_flag = False

    def filein(self):
        if self.saved_flag:
            self.save_qwestion()
        dialog = QWidget()
        dialog.setWindowTitle("Выберите файл")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
        dialog.setGeometry(10, 10, 640, 480)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(dialog, "Выберите файл", "", "Файл данных (*.f4c)", options=options)
        if filename:
            self.file_in = filename
            self.file = filename
            self.open_file()

    def change_tab(self, index):
        if self.tabWidget.currentIndex() == 0:
            for button in self.buttons:
                button.setEnabled(False)
        else:
            for button in self.buttons:
                button.setEnabled(True)
            self.memberclass = self.classlist[index]
            self.table = self.classes[self.memberclass]
            self.data = self.dataclasses[self.memberclass]
            self.model = self.models[self.memberclass]
            self.f4cui.cls_box.setCurrentText(self.memberclass)
            self.memberdata.dsb_bonus.setEnabled(True) if index == 3 else self.memberdata.dsb_bonus.setEnabled(False)
            self.memberdata.dsb_k.setEnabled(True) if index == 4 else self.memberdata.dsb_k.setEnabled(False)

    def save_as(self):
        dialog = QWidget()
        dialog.setWindowTitle("Сохранить файл")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
        dialog.setGeometry(10, 10, 640, 480)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(dialog, "Сохранить файл", "", "Файл данных (*.f4c)", options=options)
        if not Path(fileName).suffix == '.f4c':
            fileName = f'{fileName}.f4c'
        if fileName:
            self.file = fileName
            self.write()
            self.saved_flag = False
            self.action.setEnabled(False)

        dialog.show()

    def write(self):
        reflist = Referee.items
        memberlist = Member.items
        with open(self.file, 'wb') as f:
            pickle.dump(self.locate_data, f)
            pickle.dump(reflist, f)
            pickle.dump(memberlist, f)
            for i in reflist:
                pickle.dump(i, f)
            for j in memberlist:
                pickle.dump(j, f)

    def open_file(self):
        self.clear_all()
        with open(self.file_in, 'rb') as f:
            self.locate_data = pickle.load(f)
            Info.items.append(self.locate_data)
            reflist = pickle.load(f)
            memberlist = pickle.load(f)
            for i in reflist:
                i = pickle.load(f)
                Referee.items.append(i)
            for j in memberlist:
                j = pickle.load(f)
                Member.items.append(j)
        self.set_open()

    def clear_all(self):
        Referee.items.clear()
        Member.items.clear()
        Info.items.clear()
        for cls in self.dataclasses:
            self.dataclasses[cls].clear()

    def clear_fields(self):
        groups = (self.group_1, self.group_2, self.group_3, self.group_4)
        for group in groups:
            for field in group:
                field.clear()
        self.dateEdit.setDate(QDate(2024, 7, 1))
        self.dateEdit_2.setDate(QDate(2024, 7, 1))
        self.locate_data.f4c_tour_1 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4c_tour_2 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4c_tour_3 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4cu_tour_1 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4cu_tour_2 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4cu_tour_3 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4h_tour_1 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4h_tour_2 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4h_tour_3 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4g_tour_1 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4g_tour_2 = QDateTime(2024, 7, 1, 0, 0)
        self.locate_data.f4g_tour_3 = QDateTime(2024, 7, 1, 0, 0)

    def set_open(self):
        idlist = []
        for cls in self.classes:
            self.set_members(cls)
            self.filling(cls)
        for i in Member.items:
            idlist.append(i.id)
        self.count_id = 0 if idlist == [] else max(idlist)
        self.set_referees()
        self.set_data()
        self.change_tab(self.tabWidget.currentIndex())
        self.action.setEnabled(False)
        self.saved_flag = False

    def set_referees(self):
        self.set_referee_boxes()

        for ref_count, ref_field in enumerate(self.referee_fields):
            current_referee = Referee.items[ref_count]
            ref_field[0].setText(current_referee.surname)
            ref_field[1].setText(current_referee.name)
            ref_field[2].setText(current_referee.patronymic)

    def set_referee_boxes(self):
        grade_referee_box = (self.memberdata.grade_ref_box_1, self.memberdata.grade_ref_box_2,
                             self.memberdata.grade_ref_box_3)
        stat_referee_box = (self.memberdata.stend_ref_box_1, self.memberdata.stend_ref_box_2,
                            self.memberdata.stend_ref_box_3)

        for k, field in enumerate(grade_referee_box):
            field.clear()
            stat_referee_box[k].clear()

        self.flylistui.comboBox_1.clear()

        for i in range(5):
            referee = Referee.items[i]
            surname = f'{referee.surname} '
            name = f'{"" if referee.name == "" else referee.name[0]}.'
            patronymic = f'{"" if referee.patronymic == "" else referee.patronymic[0]}.'
            item = surname + name + patronymic
            for j, box in enumerate(grade_referee_box):
                box.addItem(item)
                box.setCurrentIndex(j)
                stat_referee_box[j].addItem(item)
                stat_referee_box[j].setCurrentIndex(j)
            self.flylistui.comboBox_1.addItem(item)
        self.flylistui.comboBox_1.setCurrentIndex(0)

    def set_data(self):
        self.lineEdit_25.setText(self.locate_data.locate)
        self.lineEdit_26.setText(self.locate_data.ekp_f4c)
        self.lineEdit_27.setText(self.locate_data.ekp_f4cu)
        self.dateEdit.setDate(QDate(self.locate_data.start_date))
        self.dateEdit_2.setDate(QDate(self.locate_data.end_date))

    def set_surname(self, surname, num):
        Referee.items[num].surname = surname
        self.commit_changes()

    def set_name(self, name, num):
        Referee.items[num].name = name
        self.commit_changes()

    def set_patronymic(self, patronymic, num):
        Referee.items[num].patronymic = patronymic
        self.commit_changes()

    def filling(self, cls):
        self.data = self.dataclasses[cls]
        self.model = self.in_models[cls]
        results_list = []
        for i in Member.items:
            if i.cls == cls:
                member_data = self.calculate(i)
                results_list.append(member_data[4])
                for row in self.data:
                    if row[0] == i.number:
                        for column, item in enumerate(member_data, 5):
                            self.data[self.data.index(row)][column] = item
        place_list = sorted(results_list, reverse=True)
        for l, r in enumerate(results_list):
            result = results_list[l]
            place = place_list.index(result) + 1
            self.data[l][10] = place
        self.model.setItems(self.data)

    def calculate(self, member):
        static_k = self.kh_tup if member.cls == 'F-4H' else self.k_tup
        fly_grades = [member.fly_grade_1, member.fly_grade_2, member.fly_grade_3, member.fly_grade_4,
                      member.fly_grade_5, member.fly_grade_6, member.fly_grade_7, member.fly_grade_8,
                      member.fly_grade_9, member.fly_grade_10, member.fly_grade_11, member.fly_grade_12,
                      member.fly_grade_13]
        static_grades = [member.stat_grade_1, member.stat_grade_2, member.stat_grade_3]

        static = []
        tour_1 = []
        tour_2 = []
        tour_3 = []
        tourlist = []
        for count, grade in enumerate(fly_grades):
            for static_score in static_grades:
                score = static_score[count] * static_k[count]
                static.append(score)
            tour_1.append(sum(grade[0] * self.fly_k[count]))
            tour_2.append(sum(grade[1] * self.fly_k[count]))
            tour_3.append(sum(grade[2] * self.fly_k[count]))
        tourlist.append(round(sum(tour_1), 2))
        tourlist.append(round(sum(tour_2), 2))
        tourlist.append(round(sum(tour_3), 2))
        tourlist.sort(reverse=True)
        static_total = round((sum(static) + member.bonus) * member.static_k, 2)
        result = (tourlist[0] + tourlist[1]) / 2 + static_total
        return static_total, round(sum(tour_1), 2), round(sum(tour_2), 2), round(sum(tour_3), 2), result

    def handlePreview(self, target):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
        dialog.paintRequested.connect(target)
        dialog.exec_()

    def tour_1_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))
        table = self.tour.tableView
        model = table.model()
        first = 'Первенство' if self.memberclass == 'F-4C (Ю)' else 'Чемпионат'
        ekp = self.locate_data.ekp_f4cu if self.memberclass == 'F-4C (Ю)' else self.locate_data.ekp_f4c
        content = ''
        top = f'<!DOCTYPE html><html lang="ru">' \
              f'<head>' \
              f'<meta charset="UTF-8">' \
              f'</head>' \
              f'<body>' \
              f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td width="25%" align="center"><img src="Ico/FAS-f.png"><br></td>' \
              f'<td rowspan="4" align="center" width="60%"><font size="4">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
              f'<br></font>' \
              f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {self.memberclass}</u><br><br>' \
              f'{self.locate_data.locate} {begin_date} - {end_date} г.<br>' \
              f'</td>' \
              f'<td>№ ЕКП:{ekp}</td>' \
              f'</table>' \
              f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td align="center" width="7%">Место</td>' \
              f'<td align="center" width="19%">Фамилия</td>' \
              f'<td align="center" width="18%">Имя</td>' \
              f'<td align="center" width="19%">Регион</td>' \
              f'<td align="center" width="19%">Прототип</td>' \
              f'<td align="center" width="6%">Стенд</td>' \
              f'<td align="center" width="6%">I тур</td>' \
              f'<td align="center" width="6%">Рез.</td>' \
              f'</tr>'
        for k in range(model.rowCount()):
            content = content + '<tr>'
            for i in range(model.columnCount()):
                index = model.index(k, i)
                item = model.data(index)
                content = content + f'<td align="center">{item}</td>'
            content = content + '</tr>'
        content = content + '</table>'

        bottom = f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                 f'<tr>' \
                 f'<td><br><br><br>Главный судья: {Referee.items[0].surname} ' \
                 f'{"" if Referee.items[0].name == "" else Referee.items[0].name[0]}. ' \
                 f'{"" if Referee.items[0].patronymic == "" else Referee.items[0].patronymic[0]}' \
                 f'._______________</td>' \
                 f'<td><br><br><br>Секретарь: {Referee.items[-1].surname} ' \
                 f'{"" if Referee.items[-1].name == "" else Referee.items[-1].name[0]}. ' \
                 f'{"" if Referee.items[-1].patronymic == "" else Referee.items[-1].patronymic[0]}' \
                 f'._______________</td>' \
                 f'</tr>' \
                 f'</table>' \
                 f'</body>' \
                 f'</html>'
        page = top + content + bottom
        document = QtGui.QTextDocument()
        document.setHtml(page)
        document.print_(printer)

    def tour_2_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))
        table = self.tourII.tableView
        model = table.model()
        first = 'Первенство' if self.memberclass == 'F-4C (Ю)' else 'Чемпионат'
        ekp = self.locate_data.ekp_f4cu if self.memberclass == 'F-4C (Ю)' else self.locate_data.ekp_f4c
        content = ''
        top = f'<!DOCTYPE html><html lang="ru">' \
              f'<head>' \
              f'<meta charset="UTF-8">' \
              f'</head>' \
              f'<body>' \
              f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td width="25%" align="center"><img src="Ico/FAS-f.png"><br></td>' \
              f'<td rowspan="4" align="center" width="60%"><font size="4">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
              f'<br></font>' \
              f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {self.memberclass}</u><br><br>' \
              f'{self.locate_data.locate} {begin_date} - {end_date} г.<br>' \
              f'</td>' \
              f'<td> № ЕКП: {ekp}</td>' \
              f'</table>' \
              f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td align="center" width="7%">Место</td>' \
              f'<td align="center" width="17%">Фамилия</td>' \
              f'<td align="center" width="17.5%">Имя</td>' \
              f'<td align="center" width="18%">Регион</td>' \
              f'<td align="center" width="18%">Прототип</td>' \
              f'<td align="center" width="5.5%">Стенд</td>' \
              f'<td align="center" width="5.5%">I тур</td>' \
              f'<td align="center" width="5.5%">II тур</td>' \
              f'<td align="center" width="6%">Рез.</td>' \
              f'</tr>'
        for i in range(model.rowCount()):
            content = content + '<tr>'
            for k in range(model.columnCount()):
                index = model.index(i, k)
                item = model.data(index)
                content = content + f'<td align="center">{item}</td>'
            content = content + '</tr>'
        content = content + '</table>'

        bottom = f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                 f'<tr>' \
                 f'<td><br><br><br>Главный судья: {Referee.items[0].surname} ' \
                 f'{"" if Referee.items[0].name == "" else Referee.items[0].name[0]}. ' \
                 f'{"" if Referee.items[0].patronymic == "" else Referee.items[0].patronymic[0]}' \
                 f'._______________</td>' \
                 f'<td><br><br><br>Секретарь: {Referee.items[-1].surname} ' \
                 f'{"" if Referee.items[-1].name == "" else Referee.items[-1].name[0]}. ' \
                 f'{"" if Referee.items[-1].patronymic == "" else Referee.items[-1].patronymic[0]}' \
                 f'._______________</td>' \
                 f'</tr>' \
                 f'</table>' \
                 f'</body>' \
                 f'</html>'
        page = top + content + bottom
        document = QtGui.QTextDocument()
        document.setHtml(page)
        document.print_(printer)

    def tour_3_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))
        table = self.table
        model = table.model()
        out_data = []
        for i in range(model.rowCount()):
            row = []
            for k in range(model.columnCount()):
                index = model.index(i, k)
                item = model.data(index)
                row.append(item)
            new_row = row[0:-1]
            new_row[0] = row[-1]
            out_data.append(new_row)
        first = 'Первенство' if self.memberclass == 'F-4C (Ю)' else 'Чемпионат'
        ekp = self.locate_data.ekp_f4cu if self.memberclass == 'F-4C (Ю)' else self.locate_data.ekp_f4c
        content = ''
        top = f'<!DOCTYPE html><html lang="ru">' \
              f'<head>' \
              f'<meta charset="UTF-8">' \
              f'</head>' \
              f'<body>' \
              f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td width="25%" align="center">' \
              f'<img src="Ico/FAS-f.png"><br></td>' \
              f'<td rowspan="4" align="center" width="60%"><font size="4">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
              f'<br></font>' \
              f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {self.memberclass}</u><br><br>' \
              f'{self.locate_data.locate} {begin_date} - {end_date} г.<br>' \
              f'</td>' \
              f'<td> № ЕКП: {ekp}' \
              f'</td>' \
              f'</table>' \
              f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td align="center" width="5%">Место</td>' \
              f'<td align="center" width="15%">Фамилия</td>' \
              f'<td align="center" width="14%">Имя</td>' \
              f'<td align="center" width="14%">Регион</td>' \
              f'<td align="center" width="15%">Прототип</td>' \
              f'<td align="center" width="7%">Стенд</td>' \
              f'<td align="center" width="7%">I тур</td>' \
              f'<td align="center" width="7%">II тур</td>' \
              f'<td align="center" width="7%">III тур</td>' \
              f'<td align="center" width="9%">Результат</td>' \
              f'</tr>'
        for row in out_data:
            content = content + '<tr>'
            for item in row:
                content = content + f'<td align="center">{item}</td>'
            content = content + '</tr>'
        content = content + '</table>'

        bottom = f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                 f'<tr>' \
                 f'<td><br><br><br>Главный судья: {Referee.items[0].surname} ' \
                 f'{"" if Referee.items[0].name == "" else Referee.items[0].name[0]}. ' \
                 f'{"" if Referee.items[0].patronymic == "" else Referee.items[0].patronymic[0]}' \
                 f'._______________</td>' \
                 f'<td><br><br><br>Секретарь: {Referee.items[-1].surname} ' \
                 f'{"" if Referee.items[-1].name == "" else Referee.items[-1].name[0]}. ' \
                 f'{"" if Referee.items[-1].patronymic == "" else Referee.items[-1].patronymic[0]}' \
                 f'._______________</td>' \
                 f'</tr>' \
                 f'</table>' \
                 f'</body>' \
                 f'</html>'
        page = top + content + bottom
        document = QtGui.QTextDocument()
        document.setHtml(page)
        document.print_(printer)

    def timetable_1_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))
        date = "{}".format(self.timetable.dateTimeEdit.date().toString('dd.MM.yyyy'))
        time = "{}".format(self.timetable.dateTimeEdit.time().toString('hh:mm'))

        table = self.timetable.tableView
        model = table.model()
        first = 'Первенство' if self.memberclass == 'F-4C (Ю)' else 'Чемпионат'
        ekp = self.locate_data.ekp_f4cu if self.memberclass == 'F-4C (Ю)' else self.locate_data.ekp_f4c
        content = ''
        top = f'<!DOCTYPE html><html lang="ru">' \
              f'<head>' \
              f'<meta charset="UTF-8">' \
              f'</head>' \
              f'<body>' \
              f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td width="25%" align="center"><img src="Ico/FAS-f.png"><br></td>' \
              f'<td rowspan="4" align="center" width="60%"><font size="4">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
              f'<br></font>' \
              f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {self.memberclass}</u><br><br>' \
              f'{self.locate_data.locate} {begin_date} - {end_date} г.<br><br>' \
              f'ПОЛЕТНАЯ ТАБЛИЦА<br>' \
              f'I ТУР <br>' \
              f'Начало: {time} {date}' \
              f'</td>' \
              f'<td>№ ЕКП:{ekp}</td>' \
              f'</table>' \
              f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td align="center" width="12%">Жеребьевка</td>' \
              f'<td align="center" width="22%">Фамилия</td>' \
              f'<td align="center" width="22%">Имя</td>' \
              f'<td align="center" width="22%">Регион</td>' \
              f'<td align="center" width="22%">Прототип</td>' \
              f'</tr>'

        for i in range(model.rowCount()):
            content = content + '<tr>'
            for k in range(model.columnCount()):
                index = model.index(i, k)
                item = model.data(index)
                content = content + f'<td align="center">{item}</td>'
            content = content + '</tr>'
        content = content + '</table>'
        bottom = f'</body>' \
                 f'</html>'
        page = top + content + bottom
        document = QtGui.QTextDocument()
        document.setHtml(page)
        document.print_(printer)

    def timetable_2_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))
        date = "{}".format(self.timetable.dateTimeEdit.date().toString('dd.MM.yyyy'))
        time = "{}".format(self.timetable.dateTimeEdit.time().toString('hh:mm'))

        table = self.timetable.tableView
        model = table.model()
        first = 'Первенство' if self.memberclass == 'F-4C (Ю)' else 'Чемпионат'
        ekp = self.locate_data.ekp_f4cu if self.memberclass == 'F-4C (Ю)' else self.locate_data.ekp_f4c
        content = ''
        top = f'<!DOCTYPE html><html lang="ru">' \
              f'<head>' \
              f'<meta charset="UTF-8">' \
              f'</head>' \
              f'<body>' \
              f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td width="25%" align="center"><img src="Ico/FAS-f.png"><br></td>' \
              f'<td rowspan="4" align="center" width="60%"><font size="4">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
              f'<br></font>' \
              f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {self.memberclass}</u><br><br>' \
              f'{self.locate_data.locate} {begin_date} - {end_date} г.<br><br>' \
              f'ПОЛЕТНАЯ ТАБЛИЦА<br>' \
              f'II ТУР <br>' \
              f'Начало: {time} {date}' \
              f'</td>' \
              f'<td>№ ЕКП:{ekp}</td>' \
              f'</table>' \
              f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td align="center" width="9%">П. старта</td>' \
              f'<td align="center" width="13%">Фамилия</td>' \
              f'<td align="center" width="13%">Имя</td>' \
              f'<td align="center" width="13%">Регион</td>' \
              f'<td align="center" width="13%">Прототип</td>' \
              f'<td align="center" width="13%">Стенд</td>' \
              f'<td align="center" width="13%">I тур</td>' \
              f'<td align="center" width="13%">Результат</td>' \
              f'</tr>'

        for i in range(model.rowCount()):
            content = content + '<tr>'
            for k in range(model.columnCount()):
                index = model.index(i, k)
                item = model.data(index)
                content = content + f'<td align="center">{item}</td>'
            content = content + '</tr>'
        content = content + '</table>'
        bottom = f'</body>' \
                 f'</html>'
        page = top + content + bottom
        document = QtGui.QTextDocument()
        document.setHtml(page)
        document.print_(printer)

    def timetable_3_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))
        date = "{}".format(self.timetable.dateTimeEdit.date().toString('dd.MM.yyyy'))
        time = "{}".format(self.timetable.dateTimeEdit.time().toString('hh:mm'))

        table = self.timetable.tableView
        model = table.model()
        first = 'Первенство' if self.memberclass == 'F-4C (Ю)' else 'Чемпионат'
        ekp = self.locate_data.ekp_f4cu if self.memberclass == 'F-4C (Ю)' else self.locate_data.ekp_f4c
        content = ''
        top = f'<!DOCTYPE html><html lang="ru">' \
              f'<head>' \
              f'<meta charset="UTF-8">' \
              f'</head>' \
              f'<body>' \
              f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td width="25%" align="center"><img src="Ico/FAS-f.png"><br></td>' \
              f'<td rowspan="4" align="center" width="60%"><font size="4">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
              f'<br></font>' \
              f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {self.memberclass}</u><br><br>' \
              f'{self.locate_data.locate} {begin_date} - {end_date} г.<br><br>' \
              f'ПОЛЕТНАЯ ТАБЛИЦА<br>' \
              f'III ТУР <br>' \
              f'Начало: {time} {date}' \
              f'</td>' \
              f'<td>№ ЕКП:{ekp}</td>' \
              f'</table>' \
              f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
              f'<tr>' \
              f'<td align="center" width="9%">П. старта</td>' \
              f'<td align="center" width="14%">Фамилия</td>' \
              f'<td align="center" width="13%">Имя</td>' \
              f'<td align="center" width="13%">Регион</td>' \
              f'<td align="center" width="15%">Прототип</td>' \
              f'<td align="center" width="10%">Стенд</td>' \
              f'<td align="center" width="10%">I тур</td>' \
              f'<td align="center" width="10%">II тур</td>' \
              f'<td align="center" width="6%">Результат</td>' \
              f'</tr>'

        for i in range(model.rowCount()):
            content = content + '<tr>'
            for k in range(model.columnCount()):
                index = model.index(i, k)
                item = model.data(index)
                content = content + f'<td align="center">{item}</td>'
            content = content + '</tr>'
        content = content + '</table>'
        bottom = f'</body>' \
                 f'</html>'
        page = top + content + bottom
        document = QtGui.QTextDocument()
        document.setHtml(page)
        document.print_(printer)

    def fly_list(self):
        self.flylistui.surname_lbl.setText(str(self.currentmember.surname))
        self.flylistui.name_lbl.setText(str(self.currentmember.name))
        self.flylistui.number_lbl.setText(str(self.currentmember.number))
        self.flylistui.region_lbl.setText(str(self.currentmember.region))
        self.flylistui.prototype_lbl.setText(str(self.currentmember.prototype))
        self.flylistui.scale_lbl.setText(f'1:{str(self.currentmember.scale)}')
        self.flylistui.speed_lbl.setText(str(self.currentmember.speed))
        self.flylistui.cls_label.setText(str(self.currentmember.cls))
        for j in range(1, 9):
            exec(f'self.flylistui.label_{str(j)}_1.setText(self.memberdata.comboBox_{str(j + 1)}.currentText())')
        for k in range(13):
            exec(f'self.flylistui.label_{str(k)}_3.setText("X" if (self.memberdata.fl_rb_1.isChecked()'
                 f' or self.memberdata.fl_rb_2.isChecked()) else "")')
            exec(f'self.flylistui.label_{str(k)}_4.setText("X" if (self.memberdata.fl_rb_1.isChecked()'
                 f' or self.memberdata.fl_rb_3.isChecked()) else "")')
            exec(f'self.flylistui.label_{str(k)}_5.setText("X" if (self.memberdata.fl_rb_2.isChecked()'
                 f' or self.memberdata.fl_rb_3.isChecked()) else "")')

        self.flylistui.show()

    def grade_list(self):
        total_list = []
        bonus = self.currentmember.bonus

        self.memberdata.name.setText(f'{self.currentmember.surname} {self.currentmember.prototype}')

        for m in range(2, 10):
            exec(f'self.memberdata.fig_{str(m)}.setText(self.fly_tup[self.currentmember.fig_{str(m)}[{str(self.tourcount())}]])')

        for j in range(1, 14):
            exec(f'self.memberdata.total_{str(j)}.'
                 f'setText(str(sum(self.currentmember.fly_grade_{str(j)}[{str(self.tourcount())}]) * '
                 f'int(self.memberdata.gk_{str(j)}.text())))')
            exec(f'total_list.append(float(self.memberdata.total_{str(j)}.text()))')

        for k in range(1, 14):
            for l in range(1, 4):
                exec(f'self.memberdata.sb_{str(l)}_{str(k)}.setValue(self.currentmember.'
                     f'fly_grade_{str(k)}[{str(self.tourcount())}][{str(l - 1)}])')
        self.memberdata.total.setText(str(sum(total_list)))

    def tourcount(self):
        tour = 0
        self.tournumber = 'I'
        if self.memberdata.gl_rb_2.isChecked():
            tour = 1
            self.tournumber = 'II'
        if self.memberdata.gl_rb_3.isChecked():
            tour = 2
            self.tournumber = 'III'
        self.memberdata.label_55.setText(f'{self.tournumber} тур')
        return tour

    def set_prog(self):
        for j in range(2, 10):
            exec(f'self.currentmember.fig_{str(j)}['
                 f'{"1" if self.memberdata.fl_rb_2.isChecked() else "2" if self.memberdata.fl_rb_3.isChecked() else "0"}]'
                 f' = self.memberdata.comboBox_{str(j)}.currentIndex()')
            if self.memberdata.radioButton.isChecked():
                exec(f'self.currentmember.fig_{str(j)}[1] = self.currentmember.fig_{str(j)}[0]')
                exec(f'self.currentmember.fig_{str(j)}[2] = self.currentmember.fig_{str(j)}[0]')
        self.memberdata.save_prog_btn.setEnabled(False)
        self.commit_changes()

    def set_info(self):
        row = self.table.currentIndex().row()
        number_index = self.model.index(row, 0)
        member_number = self.model.data(number_index, Qt.DisplayRole)
        if self.memberdata.toss_box.value() > 0:
            for m in Member.items:
                if m.cls == self.memberclass and m.id == self.memberdata.toss_box.value() and m.number != member_number:
                    self.error_('Участник с таким жребием уже зарегистрирован в этом классе')
                    return
        for i in Member.items:
            if i.number == member_number and i.cls == self.memberclass:
                i.surname = self.memberdata.lineEdit_surname.text()
                i.name = self.memberdata.lineEdit_name.text()
                i.region = self.memberdata.lineEdit_region.text()
                i.cls = self.memberdata.label_cls.text()
                i.prototype = self.memberdata.lineEdit_prototype.text()
                i.scale = self.memberdata.scale_box.value()
                i.speed = self.memberdata.speed_box.value()
                i.id = self.memberdata.toss_box.value()
                self.data[row][1] = self.memberdata.lineEdit_surname.text()
                self.data[row][2] = self.memberdata.lineEdit_name.text()
                self.data[row][3] = self.memberdata.lineEdit_region.text()
                self.data[row][4] = self.memberdata.lineEdit_prototype.text()
                self.data[row][11] = self.memberdata.toss_box.value()
        self.memberdata.save_info_btn.setEnabled(False)
        self.commit_changes()

    def set_grades(self):
        for j in range(1, 14):
            for k in range(1, 4):
                exec(f'self.currentmember.fly_grade_{str(j)}[{str(self.tourcount())}][{str(k - 1)}] = '
                     f'self.memberdata.sb_{str(k)}_{str(j)}.value()')

        self.filling(self.currentmember.cls)
        self.grade_list()
        self.memberdata.save_grades_btn.setEnabled(False)
        self.commit_changes()

    def timetable_preview(self):
        table = self.timetable.tableView
        tourindex = self.tourindex()
        if self.memberclass == 'F-4C':
            if tourindex == 0 and self.locate_data.f4c_tour_1 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4c_tour_1))
            if tourindex == 1 and self.locate_data.f4c_tour_2 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4c_tour_2))
            if tourindex == 2 and self.locate_data.f4c_tour_3 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4c_tour_3))
        if self.memberclass == 'F-4C (Ю)':
            if tourindex == 0 and self.locate_data.f4cu_tour_1 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4cu_tour_1))
            if tourindex == 1 and self.locate_data.f4cu_tour_2 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4cu_tour_2))
            if tourindex == 2 and self.locate_data.f4cu_tour_3 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4cu_tour_3))
        if self.memberclass == 'F-4H':
            if tourindex == 0 and self.locate_data.f4h_tour_1 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4h_tour_1))
            if tourindex == 1 and self.locate_data.f4h_tour_2 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4h_tour_2))
            if tourindex == 2 and self.locate_data.f4h_tour_3 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4h_tour_3))
        if self.memberclass == 'F-4G':
            if tourindex == 0 and self.locate_data.f4g_tour_1 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4g_tour_1))
            if tourindex == 1 and self.locate_data.f4g_tour_2 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4g_tour_2))
            if tourindex == 2 and self.locate_data.f4g_tour_3 != None:
                self.timetable.dateTimeEdit.setDateTime(QDateTime(self.locate_data.f4g_tour_3))
        timetable_model = self.set_timetable_1(tourindex) if tourindex == 0 else self.set_timetable_2(tourindex)\
            if tourindex == 1 else self.set_timetable_3(tourindex)

        table.setModel(timetable_model)
        if tourindex == 0:
            table.setSortingEnabled(False)
            table.sortByColumn(0, Qt.AscendingOrder)
        if tourindex == 2:
            table.sortByColumn(8, Qt.AscendingOrder)
        self.timetable.show()

    def tourindex(self):
        for btn in self.r_buttons:
            if btn.isChecked():
                index = btn.index
        return index

    def set_timetable_1(self, index):
        data = []
        headers = timetable_headers[index]
        for member in Member.items:
            if member.cls == self.memberclass:
                data.append([member.id, member.surname, member.name, member.region, member.prototype])
        timetable_in_model = TableModel(headers, data)
        timetable_model = QSortFilterProxyModel()
        timetable_model.setSourceModel(timetable_in_model)
        return timetable_model

    def set_timetable_2(self, index):
        in_data = []
        data = []
        in_tosslist = []
        tosslist = []
        headers = timetable_headers[index]
        source_data = self.dataclasses[self.memberclass]
        if source_data == []:
            self.error_('Нет данных для вывода!')
            return
        for row in source_data:
            new_row = []
            new_row.append(row[11])
            for col in range(1, 7):
                new_row.append(row[col])
            if row[5] == None or row[6] == None:
                result = 0
            else:
                result = row[5] + row[6]
            new_row.append(result)
            in_tosslist.append(row[11])
            in_data.append(new_row)
        in_tosslist.sort()
        start_number = round(max(in_tosslist) * 2 / 3)
        for item in range(in_tosslist.index(start_number) + 1, len(in_tosslist)):
            tosslist.append(in_tosslist[item])
        for item in range(in_tosslist.index(start_number) + 1):
            tosslist.append(in_tosslist[item])
        for num, toss in enumerate(tosslist):
            for row in in_data:
                if row[0] == toss:
                    tmp_row = []
                    tmp_row.append(num + 1)
                    for i, item in enumerate(row):
                        if i == 0:
                            continue
                        tmp_row.append(item)
                    data.append(tmp_row)
        timetable_in_model = TableModel(headers, data)
        timetable_model = QSortFilterProxyModel()
        timetable_model.setSourceModel(timetable_in_model)
        return timetable_model

    def set_timetable_3(self, index):
        data = []
        res_list = []
        headers = timetable_headers[index]
        source_data = self.dataclasses[self.memberclass]
        if source_data == []:
            self.error_('Нет данных для вывода!')
            return
        for row in source_data:
            new_row = []
            for col in range(1, 8):
                new_row.append(row[col])
            if row[5] == None or row[6] == None or row[7] == None:
                result = 0
            else:
                result = row[5] + (row[6] + row[7]) / 2
            new_row.append(result)
            res_list.append(result)
            data.append(new_row)
        res_list.sort()
        for l in data:
            place = res_list.index(l[7]) + 1
            l.insert(0, place)
        timetable_in_model = TableModel(headers, data)
        timetable_model = QSortFilterProxyModel()
        timetable_model.setSourceModel(timetable_in_model)
        return timetable_model

    def gradelist_request(self, printer):
        figure = {2: self.currentmember.fig_2, 3: self.currentmember.fig_3, 4: self.currentmember.fig_4,
                  5: self.currentmember.fig_5, 6: self.currentmember.fig_6, 7: self.currentmember.fig_7,
                  8: self.currentmember.fig_8, 9: self.currentmember.fig_9}
        grade = {1: self.currentmember.fly_grade_1, 2: self.currentmember.fly_grade_2, 3: self.currentmember.fly_grade_3,
                 4: self.currentmember.fly_grade_4, 5: self.currentmember.fly_grade_5, 6: self.currentmember.fly_grade_6,
                 7: self.currentmember.fly_grade_7, 8: self.currentmember.fly_grade_8, 9: self.currentmember.fly_grade_9,
                 10: self.currentmember.fly_grade_10, 11: self.currentmember.fly_grade_11, 12: self.currentmember.fly_grade_12,
                 13: self.currentmember.fly_grade_13}
        tour = self.tourcount()
        current_year = "{}".format(self.dateEdit.date().toString('yyyy'))
        program = ''
        tour_list = []
        for k in range(13):
            tour_list.append(sum(grade.get(k + 1)[tour]) * self.fly_k[k])
        total = sum(tour_list)

        for i in range(2, 10):
            program = program + '<tr>'
            program = program + f'<td width="5%">{i}</td><td>{self.fly_tup[figure.get(i)[tour]]}</td><td>7</td>' \
                                f'<td>{grade.get(i)[tour][0]}</td><td>{grade.get(i)[tour][1]}</td>' \
                                f'<td>{grade.get(i)[tour][2]}</td><td>{sum(grade.get(i)[tour]) * self.fly_k[i - 1]}</td>'
            program = program + '</tr>'
        gradelist_page = f'<!DOCTYPE html><html lang="ru">' \
                         f'<head>' \
                         f'<meta charset="UTF-8">' \
                         f'</head>' \
                         f'<body>' \
                         f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
                         f'<tr>' \
                         f'<td colspan="5" align="center">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
                         f'Чемпионат России в классе радиоуправляемых<br>' \
                         f'моделей-копий самолетов<br>' \
                         f'{current_year} г.<br>' \
                         f'{self.memberclass}' \
                         f'</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td colspan="5" align="center">{self.tournumber} тур</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td>Участник:</td>' \
                         f'<td align="center">{self.currentmember.surname}</td>' \
                         f'<td colspan="2" align="center">{self.currentmember.name}</td>' \
                         f'<td align="center">№ {self.currentmember.number}</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td colspan="2" align="center">Регион:</td>' \
                         f'<td colspan="3" align="center">{self.currentmember.region}</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td colspan="2" align="center">Прототип:</td>' \
                         f'<td colspan="3" align="center">{self.currentmember.prototype}</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td align="center">Масштаб</td>' \
                         f'<td align="center">1:{self.currentmember.scale}</td>' \
                         f'<td align="center">V max (км/ч)</td>' \
                         f'<td colspan="2" align="center">{self.currentmember.speed}</td>' \
                         f'</tr>' \
                         f'</table>' \
                         f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                         f'<tr>' \
                         f'<td colspan="2" rowspan="2" align="center">ПРОГРАММА ПОЛЕТА</td>' \
                         f'<td rowspan="2" align="center" width="5%">k</td>' \
                         f'<td colspan="4" align="center">Оценки</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td align="center">С1</td>' \
                         f'<td align="center">С2</td>' \
                         f'<td align="center">С3</td>' \
                         f'<td align="center">Сумма</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td>1</td><td>Взлет</td><td>11</td><td>{self.currentmember.fly_grade_1[tour][0]}</td>' \
                         f'<td>{self.currentmember.fly_grade_1[tour][1]}</td>' \
                         f'<td>{self.currentmember.fly_grade_1[tour][2]}</td>' \
                         f'<td>{sum(self.currentmember.fly_grade_1[tour]) * self.fly_k[0]}</td>' \
                         f'</tr>' \
                         f'{program}' \
                         f'<tr>' \
                         f'<td>10</td><td>Заход на посадку и приземление</td><td>11</td>' \
                         f'<td>{self.currentmember.fly_grade_10[tour][0]}</td>' \
                         f'<td>{self.currentmember.fly_grade_10[tour][1]}</td>' \
                         f'<td>{self.currentmember.fly_grade_10[tour][2]}</td>' \
                         f'<td>{sum(self.currentmember.fly_grade_10[tour]) * self.fly_k[9]}</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td>11a</td><td>Реализм полета a) презентация полета</td><td>4</td>' \
                         f'<td>{self.currentmember.fly_grade_11[tour][0]}</td>' \
                         f'<td>{self.currentmember.fly_grade_11[tour][1]}</td>' \
                         f'<td>{self.currentmember.fly_grade_11[tour][2]}</td>' \
                         f'<td>{sum(self.currentmember.fly_grade_11[tour]) * self.fly_k[10]}</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td>11b</td><td>b) скорость модели</td><td>9</td>' \
                         f'<td>{self.currentmember.fly_grade_12[tour][0]}</td>' \
                         f'<td>{self.currentmember.fly_grade_12[tour][1]}</td>' \
                         f'<td>{self.currentmember.fly_grade_12[tour][2]}</td>' \
                         f'<td>{sum(self.currentmember.fly_grade_12[tour]) * self.fly_k[11]}</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td>11c</td><td>c) плавность полета</td><td>9</td>' \
                         f'<td>{self.currentmember.fly_grade_13[tour][0]}</td>' \
                         f'<td>{self.currentmember.fly_grade_13[tour][1]}</td>' \
                         f'<td>{self.currentmember.fly_grade_13[tour][2]}</td>' \
                         f'<td>{sum(self.currentmember.fly_grade_13[tour]) * self.fly_k[12]}</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td colspan="3"></td>' \
                         f'<td colspan="3">Итоговая оценка:</td>' \
                         f'<td>{total}</td>' \
                         f'</tr>' \
                         f'</table>' \
                         f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                         f'<tr>' \
                         f'<td><br><br><br>C1: {self.memberdata.grade_ref_box_1.currentText()}_______________</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td><br><br>C2: {self.memberdata.grade_ref_box_2.currentText()}_______________</td>' \
                         f'</tr>' \
                         f'<tr>' \
                         f'<td><br><br>C3: {self.memberdata.grade_ref_box_3.currentText()}_______________</td>' \
                         f'</tr>' \
                         f'</table>' \
                         f'</body>' \
                         f'</html>'
        document = QtGui.QTextDocument()
        document.setHtml(gradelist_page)
        document.print_(printer)

    def flylist_request(self, printer):
        flylist_dict = {'label_0_0': self.flylistui.label_0_0.text(), 'label_0_1': self.flylistui.label_0_1.text(),
                        'label_0_2': self.flylistui.label_0_2.text(), 'label_0_3': self.flylistui.label_0_3.text(),
                        'label_0_4': self.flylistui.label_0_4.text(), 'label_0_5': self.flylistui.label_0_5.text(),
                        'label_1_0': self.flylistui.label_1_0.text(), 'label_1_1': self.flylistui.label_1_1.text(),
                        'label_1_2': self.flylistui.label_1_2.text(), 'label_1_3': self.flylistui.label_1_3.text(),
                        'label_1_4': self.flylistui.label_1_4.text(), 'label_1_5': self.flylistui.label_1_5.text(),
                        'label_2_0': self.flylistui.label_2_0.text(), 'label_2_1': self.flylistui.label_2_1.text(),
                        'label_2_2': self.flylistui.label_2_2.text(), 'label_2_3': self.flylistui.label_2_3.text(),
                        'label_2_4': self.flylistui.label_2_4.text(), 'label_2_5': self.flylistui.label_2_5.text(),
                        'label_3_0': self.flylistui.label_3_0.text(), 'label_3_1': self.flylistui.label_3_1.text(),
                        'label_3_2': self.flylistui.label_3_2.text(), 'label_3_3': self.flylistui.label_3_3.text(),
                        'label_3_4': self.flylistui.label_3_4.text(), 'label_3_5': self.flylistui.label_2_5.text(),
                        'label_4_0': self.flylistui.label_4_0.text(), 'label_4_1': self.flylistui.label_4_1.text(),
                        'label_4_2': self.flylistui.label_4_2.text(), 'label_4_3': self.flylistui.label_4_3.text(),
                        'label_4_4': self.flylistui.label_4_4.text(), 'label_4_5': self.flylistui.label_4_5.text(),
                        'label_5_0': self.flylistui.label_5_0.text(), 'label_5_1': self.flylistui.label_5_1.text(),
                        'label_5_2': self.flylistui.label_5_2.text(), 'label_5_3': self.flylistui.label_5_3.text(),
                        'label_5_4': self.flylistui.label_5_4.text(), 'label_5_5': self.flylistui.label_2_5.text(),
                        'label_6_0': self.flylistui.label_6_0.text(), 'label_6_1': self.flylistui.label_6_1.text(),
                        'label_6_2': self.flylistui.label_6_2.text(), 'label_6_3': self.flylistui.label_6_3.text(),
                        'label_6_4': self.flylistui.label_6_4.text(), 'label_6_5': self.flylistui.label_6_5.text(),
                        'label_7_0': self.flylistui.label_7_0.text(), 'label_7_1': self.flylistui.label_7_1.text(),
                        'label_7_2': self.flylistui.label_7_2.text(), 'label_7_3': self.flylistui.label_7_3.text(),
                        'label_7_4': self.flylistui.label_7_4.text(), 'label_7_5': self.flylistui.label_7_5.text(),
                        'label_8_0': self.flylistui.label_8_0.text(), 'label_8_1': self.flylistui.label_8_1.text(),
                        'label_8_2': self.flylistui.label_8_2.text(), 'label_8_3': self.flylistui.label_8_3.text(),
                        'label_8_4': self.flylistui.label_8_4.text(), 'label_8_5': self.flylistui.label_8_5.text(),
                        'label_9_0': self.flylistui.label_9_0.text(), 'label_9_1': self.flylistui.label_9_1.text(),
                        'label_9_2': self.flylistui.label_9_2.text(), 'label_9_3': self.flylistui.label_9_3.text(),
                        'label_9_4': self.flylistui.label_9_4.text(), 'label_9_5': self.flylistui.label_9_5.text(),
                        'label_10_0': self.flylistui.label_10_0.text(), 'label_10_1': self.flylistui.label_10_1.text(),
                        'label_10_2': self.flylistui.label_10_2.text(), 'label_10_3': self.flylistui.label_10_3.text(),
                        'label_10_4': self.flylistui.label_10_4.text(), 'label_10_5': self.flylistui.label_10_5.text(),
                        'label_11_0': self.flylistui.label_11_0.text(), 'label_11_1': self.flylistui.label_11_1.text(),
                        'label_11_2': self.flylistui.label_11_2.text(), 'label_11_3': self.flylistui.label_11_3.text(),
                        'label_11_4': self.flylistui.label_11_4.text(), 'label_11_5': self.flylistui.label_11_5.text(),
                        'label_12_0': self.flylistui.label_12_0.text(), 'label_12_1': self.flylistui.label_12_1.text(),
                        'label_12_2': self.flylistui.label_12_2.text(), 'label_12_3': self.flylistui.label_12_3.text(),
                        'label_12_4': self.flylistui.label_12_4.text(), 'label_12_5': self.flylistui.label_12_5.text()}
        current_year = "{}".format(self.dateEdit.date().toString('yyyy'))
        program = ''
        scale_speed = round(int(self.currentmember.speed) / float(self.currentmember.scale), 2) if\
            float(self.currentmember.scale) > 0 else '---'
        base_time = round(360 / scale_speed, 2) if float(self.currentmember.scale) > 0 else '---'

        for i in range(13):
            program = program + '<tr>'
            for j in range(6):
                item = flylist_dict.get("label_{}_{}".format(str(i), str(j)))
                program = program + f'<td>{item}</td>'
            program = program + '</tr>'
        flylist_page = f'<!DOCTYPE html><html lang="ru">' \
                       f'<head>' \
                       f'<meta charset="UTF-8">' \
                       f'</head>' \
                       f'<body>' \
                       f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
                       f'<tr>' \
                       f'<td rowspan="4" width="52%" align="center">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
                       f'Чемпионат России в классе радиоуправляемых<br>' \
                       f'моделей-копий самолетов {self.memberclass}<br>' \
                       f'{current_year} г.' \
                       f'</td>' \
                       f'<td align="center">III тур</td>' \
                       f'<td align="center">II тур</td>' \
                       f'<td align="center">I тур</td>' \
                       f'</tr>' \
                       f'<tr>' \
                       f'<td align="center">{self.currentmember.surname}</td>' \
                       f'<td align="center">{self.currentmember.surname}</td>' \
                       f'<td align="center">{self.currentmember.surname}</td>' \
                       f'</tr>' \
                       f'<tr>' \
                       f'<td align="center">№ {self.currentmember.number}</td>' \
                       f'<td align="center">№ {self.currentmember.number}</td>' \
                       f'<td align="center">№ {self.currentmember.number}</td>' \
                       f'</tr>' \
                       f'<tr>'\
                       f'<td align="center">{self.memberclass}</td>' \
                       f'<td align="center">{self.memberclass}</td>' \
                       f'<td align="center">{self.memberclass}</td>' \
                       f'</tr>' \
                       f'</table>' \
                       f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                       f'<tr>' \
                       f'<td width="5%"></td>' \
                       f'<td width="42%" align="center">ПРОГРАММА ПОЛЕТА</td>' \
                       f'<td width="5%" align="center">k</td>' \
                       f'<td align="center">Очки</td>' \
                       f'<td align="center">Очки</td>' \
                       f'<td align="center">Очки</td>' \
                       f'</tr>' \
                       f'{program}' \
                       f'<tr>' \
                       f'<td width="2%"></td>' \
                       f'<td colspan="2">Прототип: {self.currentmember.prototype}</td>' \
                       f'<td>Судья</td>' \
                       f'<td>Судья</td>' \
                       f'<td>Судья</td>' \
                       f'</tr>' \
                       f'<tr>' \
                       f'<td></td>' \
                       f'<td colspan="2">Скорость прототипа: {self.currentmember.speed} км/ч<br>' \
                       f'Масштабная скорость: {scale_speed} км/ч<br>' \
                       f'Пролёт базы: {base_time} сек.</td>' \
                       f'<td>{self.flylistui.comboBox_1.currentText()}<br><br>_____________</td>' \
                       f'<td>{self.flylistui.comboBox_1.currentText()}<br><br>_____________</td>' \
                       f'<td>{self.flylistui.comboBox_1.currentText()}<br><br>_____________</td>' \
                       f'</tr>' \
                       f'</table>' \
                       f'</body>' \
                       f'</html>'
        document = QtGui.QTextDocument()
        document.setHtml(flylist_page)
        document.print_(printer)

    def static_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))

        default = ''
        total_1 = []
        total_2 = []
        total_3 = []
        for i in range(13):
            total_1.append(self.currentmember.stat_grade_1[i] * self.k_tup[i])
            total_2.append(self.currentmember.stat_grade_2[i] * self.k_tup[i])
            total_3.append(self.currentmember.stat_grade_3[i] * self.k_tup[i])

        static_page = f'<!DOCTYPE html><html lang="ru">' \
                      f'<head>' \
                      f'<meta charset="UTF-8">' \
                      f'</head>' \
                      f'<body>' \
                      f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
                      f'<tr>' \
                      f'<td rowspan="4" align="center" width="60%">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
                      f'Чемпионат России в классе радиоуправляемых<br>' \
                      f'моделей-копий самолетов<br>' \
                      f'{self.locate_data.locate} {begin_date} - {end_date} г.<br>' \
                      f'{self.memberclass}' \
                      f'</td>' \
                      f'<td>Участник:</td>' \
                      f'<td align="center">{self.currentmember.surname}</td>' \
                      f'<td colspan="2" align="center">{self.currentmember.name}</td>' \
                      f'<td align="center">№ {self.currentmember.number}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td colspan="2" align="center">Регион:</td>' \
                      f'<td colspan="3" align="center">{self.currentmember.region}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td colspan="2" align="center">Прототип:</td>' \
                      f'<td colspan="3" align="center">{self.currentmember.prototype}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">Масштаб</td>' \
                      f'<td align="center">{self.currentmember.scale}</td>' \
                      f'<td align="center">V max (км/ч)</td>' \
                      f'<td colspan="2" align="center">{self.currentmember.speed}</td>' \
                      f'</tr>' \
                      f'</table>' \
                      f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
                      f'<tr>' \
                      f'<td colspan="3" align="center">ПАРАМЕТРЫ СТЕНДОВОЙ ОЦЕНКИ</td>' \
                      f'<td align="center" width="2.5%">k</td>' \
                      f'<td align="center" width="5%"><font size="2">Оценка</font></td>' \
                      f'<td align="center" width="12%"><font size="2">Очки</font></td>' \
                      f'<td align="center" width="5%"><font size="2">Оценка</font></td>' \
                      f'<td align="center" width="12%"><font size="2">Очки</font></td>' \
                      f'<td align="center" width="5%"><font size="2">Оценка</font></td>' \
                      f'<td align="center" width="12%"><font size="2">Очки</font></td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="3" width="2.5%">1</td>' \
                      f'<td align="center" rowspan="3" width="20%">МАСШТАБНАЯ ТОЧНОСТЬ:</td>' \
                      f'<td align="center" width="24%">a) вид сбоку (справа и слева)</td>' \
                      f'<td align="center">13</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[0] == 0.0 else round(self.currentmember.stat_grade_1[0], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[0] * self.k_tup[0], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[0] == 0.0 else round(self.currentmember.stat_grade_2[0], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[0] * self.k_tup[0], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[0] == 0.0 else round(self.currentmember.stat_grade_3[0], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[0] * self.k_tup[0], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) виды спереди и сзади</td>' \
                      f'<td align="center">13</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[1] == 0.0 else round(self.currentmember.stat_grade_1[1], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[1] * self.k_tup[1], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[1] == 0.0 else round(self.currentmember.stat_grade_2[1], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[1] * self.k_tup[1], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[1] == 0.0 else round(self.currentmember.stat_grade_3[1], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[1] * self.k_tup[1], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">c) виды сверху и снизу</td>' \
                      f'<td align="center">13</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[2] == 0.0 else round(self.currentmember.stat_grade_1[2], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[2] * self.k_tup[2], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[2] == 0.0 else round(self.currentmember.stat_grade_2[2], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[2] * self.k_tup[2], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[2] == 0.0 else round(self.currentmember.stat_grade_3[2], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[2] * self.k_tup[2], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="2" width="3%">2</td>' \
                      f'<td align="center" rowspan="2">ОКРАСКА:</td>' \
                      f'<td align="center">a) точность</td>' \
                      f'<td align="center">3</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[3] == 0.0 else round(self.currentmember.stat_grade_1[3], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[3] * self.k_tup[3], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[3] == 0.0 else round(self.currentmember.stat_grade_2[3], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[3] * self.k_tup[3], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[3] == 0.0 else round(self.currentmember.stat_grade_3[3], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[3] * self.k_tup[3], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) сложность</td>' \
                      f'<td align="center">2</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[4] == 0.0 else round(self.currentmember.stat_grade_1[4], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[4] * self.k_tup[4], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[4] == 0.0 else round(self.currentmember.stat_grade_2[4], 1)}' \
                      f'</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[4] * self.k_tup[4], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[4] == 0.0 else self.currentmember.stat_grade_3[4]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[4] * self.k_tup[4], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="2" width="3%">3</td>' \
                      f'<td align="center" rowspan="2">ОПОЗНАВАТЕЛЬНЫЕ ЗНАКИ:</td>' \
                      f'<td align="center">a) точность</td>' \
                      f'<td align="center">8</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[5] == 0.0 else self.currentmember.stat_grade_1[5]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[5] * self.k_tup[5], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[5] == 0.0 else self.currentmember.stat_grade_2[5]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[5] * self.k_tup[5], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[5] == 0.0 else self.currentmember.stat_grade_3[5]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[5] * self.k_tup[5], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) сложность</td>' \
                      f'<td align="center">3</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[6] == 0.0 else self.currentmember.stat_grade_1[6]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[6] * self.k_tup[6], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[6] == 0.0 else self.currentmember.stat_grade_2[6]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[6] * self.k_tup[6], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[6] == 0.0 else self.currentmember.stat_grade_3[6]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[6] * self.k_tup[6], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="2" width="3%">4</td>' \
                      f'<td align="center" rowspan="2">ТЕКСТУРА ПОВЕРХНОСТИ И РЕАЛИЗМ:</td>' \
                      f'<td align="center">a) текстура поверхности</td>' \
                      f'<td align="center">7</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[7] == 0.0 else self.currentmember.stat_grade_1[7]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[7] * self.k_tup[7], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[7] == 0.0 else self.currentmember.stat_grade_2[7]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[7] * self.k_tup[7], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[7] == 0.0 else self.currentmember.stat_grade_3[7]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[7] * self.k_tup[7], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) соотв. текстуры масштабу</td>' \
                      f'<td align="center">7</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[8] == 0.0 else self.currentmember.stat_grade_1[8]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[8] * self.k_tup[8], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[8] == 0.0 else self.currentmember.stat_grade_2[8]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[8] * self.k_tup[8], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[8] == 0.0 else self.currentmember.stat_grade_3[8]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[8] * self.k_tup[8], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="2" width="3%">5</td>' \
                      f'<td align="center" rowspan="2">МАСТЕРСТВО ИЗГОТОВЛЕНИЯ:</td>' \
                      f'<td align="center">a) качество</td>' \
                      f'<td align="center">12</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[9] == 0.0 else self.currentmember.stat_grade_1[9]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[9] * self.k_tup[9], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[9] == 0.0 else self.currentmember.stat_grade_2[9]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[9] * self.k_tup[9], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[9] == 0.0 else self.currentmember.stat_grade_3[9]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[9] * self.k_tup[9], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) сложность</td>' \
                      f'<td align="center">5</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[10] == 0.0 else self.currentmember.stat_grade_1[10]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[10] * self.k_tup[10], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[10] == 0.0 else self.currentmember.stat_grade_2[10]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[10] * self.k_tup[10], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[10] == 0.0 else self.currentmember.stat_grade_3[10]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[10] * self.k_tup[10], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="2" width="3%">6</td>' \
                      f'<td align="center" rowspan="2">МАСШТАБНОСТЬ ДЕТАЛЕЙ:</td>' \
                      f'<td align="center">a) точность</td>' \
                      f'<td align="center">9</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[11] == 0.0 else self.currentmember.stat_grade_1[11]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[11] * self.k_tup[11], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[11] == 0.0 else self.currentmember.stat_grade_2[11]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[11] * self.k_tup[11], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[11] == 0.0 else self.currentmember.stat_grade_3[11]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[11] * self.k_tup[11], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) сложность</td>' \
                      f'<td align="center">5</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[12] == 0.0 else self.currentmember.stat_grade_1[12]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[12] * self.k_tup[12], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[12] == 0.0 else self.currentmember.stat_grade_2[12]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[12] * self.k_tup[12], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[12] == 0.0 else self.currentmember.stat_grade_3[12]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[12] * self.k_tup[12], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td colspan="4" rowspan="2"><br><br>' \
                      f'Коэффициент статической оценки: {self.currentmember.static_k}<br>' \
                      f'Итоговые очки: {round(sum(total_1) + sum(total_2) + sum(total_3), 1)}</td>' \
                      f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_1)}</td>' \
                      f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_2)}</td>' \
                      f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_2)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                      f'{self.memberdata.stend_ref_box_1.currentText()}' \
                      f'<br><br>_______________</td>' \
                      f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                      f'{self.memberdata.stend_ref_box_2.currentText()}' \
                      f'<br><br>_______________</td>' \
                      f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                      f'{self.memberdata.stend_ref_box_3.currentText()}' \
                      f'<br><br>_______________</td>' \
                      f'</tr>' \
                      f'</table>' \
                      f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                      f'<tr>' \
                      f'<td><br><br><br>Главный судья: {Referee.items[0].surname} ' \
                      f'{"" if Referee.items[0].name == "" else Referee.items[0].name[0]}. ' \
                      f'{"" if Referee.items[0].patronymic == "" else Referee.items[0].patronymic[0]}' \
                      f'._______________</td>' \
                      f'</tr>' \
                      f'</table>' \
                      f'</body>' \
                      f'</html>'
        document = QtGui.QTextDocument()
        document.setHtml(static_page)
        document.print_(printer)

    def static_f4h_request(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        begin_date = "{}".format(self.dateEdit.date().toString('dd.MM.yyyy'))
        end_date = "{}".format(self.dateEdit_2.date().toString('dd.MM.yyyy'))

        total_1 = []
        total_2 = []
        total_3 = []
        default = ''
        for i in range(13):
            total_1.append(self.currentmember.stat_grade_1[i] * self.kh_tup[i])
            total_2.append(self.currentmember.stat_grade_2[i] * self.kh_tup[i])
            total_3.append(self.currentmember.stat_grade_3[i] * self.kh_tup[i])

        static_page = f'<!DOCTYPE html><html lang="ru">' \
                      f'<head>' \
                      f'<meta charset="UTF-8">' \
                      f'</head>' \
                      f'<body>' \
                      f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
                      f'<tr>' \
                      f'<td rowspan="4" align="center" width="60%">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
                      f'Чемпионат России в классе радиоуправляемых<br>' \
                      f'моделей-копий самолетов<br>' \
                      f'{self.locate_data.locate} {begin_date} - {end_date} г.<br>' \
                      f'{self.memberclass}' \
                      f'</td>' \
                      f'<td>Участник:</td>' \
                      f'<td align="center">{self.currentmember.surname}</td>' \
                      f'<td colspan="2" align="center">{self.currentmember.name}</td>' \
                      f'<td align="center">№ {self.currentmember.number}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td colspan="2" align="center">Регион:</td>' \
                      f'<td colspan="3" align="center">{self.currentmember.region}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td colspan="2" align="center">Прототип:</td>' \
                      f'<td colspan="3" align="center">{self.currentmember.prototype}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">Масштаб</td>' \
                      f'<td align="center">{self.currentmember.scale}</td>' \
                      f'<td align="center">V max (км/ч)</td>' \
                      f'<td colspan="2" align="center">{self.currentmember.speed}</td>' \
                      f'</tr>' \
                      f'</table>' \
                      f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
                      f'<tr>' \
                      f'<td colspan="3" align="center">ПАРАМЕТРЫ СТЕНДОВОЙ ОЦЕНКИ</td>' \
                      f'<td align="center" width="2.5%">k</td>' \
                      f'<td align="center" width="5%"><font size="2">Оценка</font></td>' \
                      f'<td align="center" width="12%"><font size="2">Очки</font></td>' \
                      f'<td align="center" width="5%"><font size="2">Оценка</font></td>' \
                      f'<td align="center" width="12%"><font size="2">Очки</font></td>' \
                      f'<td align="center" width="5%"><font size="2">Оценка</font></td>' \
                      f'<td align="center" width="12%"><font size="2">Очки</font></td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="3" width="2.5%">1</td>' \
                      f'<td align="center" rowspan="3" width="20%">МАСШТАБНАЯ ТОЧНОСТЬ:</td>' \
                      f'<td align="center" width="24%">a) вид сбоку (справа и слева)</td>' \
                      f'<td align="center">5</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[0] == 0.0 else self.currentmember.stat_grade_1[0]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[0] * self.kh_tup[0], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[0] == 0.0 else self.currentmember.stat_grade_2[0]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[0] * self.kh_tup[0], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[0] == 0.0 else self.currentmember.stat_grade_3[0]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[0] * self.kh_tup[0], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) виды спереди и сзади</td>' \
                      f'<td align="center">5</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[1] == 0.0 else self.currentmember.stat_grade_1[1]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[1] * self.kh_tup[1], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[1] == 0.0 else self.currentmember.stat_grade_2[1]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[1] * self.kh_tup[1], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[1] == 0.0 else self.currentmember.stat_grade_3[1]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[1] * self.kh_tup[1], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">c) виды сверху и снизу</td>' \
                      f'<td align="center">5</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[2] == 0.0 else self.currentmember.stat_grade_1[2]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[2] * self.kh_tup[2], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[2] == 0.0 else self.currentmember.stat_grade_2[2]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[2] * self.kh_tup[2], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[2] == 0.0 else self.currentmember.stat_grade_3[2]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[2] * self.kh_tup[2], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="2" width="3%">2</td>' \
                      f'<td align="center" rowspan="2">ОКРАСКА:</td>' \
                      f'<td align="center">a) точность</td>' \
                      f'<td align="center">3</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[3] == 0.0 else self.currentmember.stat_grade_1[3]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[3] * self.kh_tup[3], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[3] == 0.0 else self.currentmember.stat_grade_2[3]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[3] * self.kh_tup[3], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[3] == 0.0 else self.currentmember.stat_grade_3[3]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[3] * self.kh_tup[3], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) сложность</td>' \
                      f'<td align="center">2</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[4] == 0.0 else self.currentmember.stat_grade_1[4]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[4] * self.kh_tup[4], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[4] == 0.0 else self.currentmember.stat_grade_2[4]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[4] * self.kh_tup[4], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[4] == 0.0 else self.currentmember.stat_grade_3[4]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[4] * self.kh_tup[4], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" rowspan="2" width="3%">3</td>' \
                      f'<td align="center" rowspan="2">ОПОЗНАВАТЕЛЬНЫЕ ЗНАКИ:</td>' \
                      f'<td align="center">a) точность</td>' \
                      f'<td align="center">3</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[5] == 0.0 else self.currentmember.stat_grade_1[5]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[5] * self.kh_tup[5], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[5] == 0.0 else self.currentmember.stat_grade_2[5]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[5] * self.kh_tup[5], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[5] == 0.0 else self.currentmember.stat_grade_3[5]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[5] * self.kh_tup[5], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center">b) сложность</td>' \
                      f'<td align="center">2</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[6] == 0.0 else self.currentmember.stat_grade_1[6]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[6] * self.kh_tup[6], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[6] == 0.0 else self.currentmember.stat_grade_2[6]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[6] * self.kh_tup[6], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[6] == 0.0 else self.currentmember.stat_grade_3[6]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[6] * self.kh_tup[6], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" width="3%">4</td>' \
                      f'<td align="center" colspan="2">РЕАЛИЗМ:</td>' \
                      f'<td align="center">4</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[7] == 0.0 else self.currentmember.stat_grade_1[7]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[7] * self.kh_tup[7], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[7] == 0.0 else self.currentmember.stat_grade_2[7]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[7] * self.kh_tup[7], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[7] == 0.0 else self.currentmember.stat_grade_3[7]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[7] * self.kh_tup[7], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center" width="3%">5</td>' \
                      f'<td align="center" colspan="2">РАЗРАБОТКА, ПРОИСХОЖДЕНИЕ И ДИЗАЙН МОДЕЛИ:</td>' \
                      f'<td align="center">6</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_1[9] == 0.0 else self.currentmember.stat_grade_1[9]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_1[9] * self.kh_tup[9], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_2[9] == 0.0 else self.currentmember.stat_grade_2[9]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_2[9] * self.kh_tup[9], 1)}</td>' \
                      f'<td align="center">' \
                      f'{default if self.currentmember.stat_grade_3[9] == 0.0 else self.currentmember.stat_grade_3[9]}</td>' \
                      f'<td align="center">{round(self.currentmember.stat_grade_3[9] * self.kh_tup[9], 1)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td colspan="4" rowspan="2"><br><br>' \
                      f'Бонус: {self.currentmember.bonus}<br>' \
                      f'Итоговые очки: {round(sum(total_1) + sum(total_2) + sum(total_3) + self.currentmember.bonus, 1)}</td>' \
                      f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_1)}</td>' \
                      f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_2)}</td>' \
                      f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_2)}</td>' \
                      f'</tr>' \
                      f'<tr>' \
                      f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                      f'{self.memberdata.stend_ref_box_1.currentText()}' \
                      f'<br><br>_______________</td>' \
                      f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                      f'{self.memberdata.stend_ref_box_2.currentText()}' \
                      f'<br><br>_______________</td>' \
                      f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                      f'{self.memberdata.stend_ref_box_3.currentText()}' \
                      f'<br><br>_______________</td>' \
                      f'</tr>' \
                      f'</table>' \
                      f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                      f'<tr>' \
                      f'<td><br><br><br>Главный судья: {Referee.items[0].surname} ' \
                      f'{"" if Referee.items[0].name == "" else Referee.items[0].name[0]}. ' \
                      f'{"" if Referee.items[0].patronymic == "" else Referee.items[0].patronymic[0]}' \
                      f'._______________</td>' \
                      f'</tr>' \
                      f'</table>' \
                      f'</body>' \
                      f'</html>'
        document = QtGui.QTextDocument()
        document.setHtml(static_page)
        document.print_(printer)

    def set_static(self):
        data_1 = []
        data_2 = []
        data_3 = []
        for j in range(13):
            exec(f'data_1.append(self.memberdata.dsb_1_{str(j)}.value())')
            exec(f'data_2.append(self.memberdata.dsb_2_{str(j)}.value())')
            exec(f'data_3.append(self.memberdata.dsb_3_{str(j)}.value())')
        self.currentmember.stat_grade_1 = data_1
        self.currentmember.stat_grade_2 = data_2
        self.currentmember.stat_grade_3 = data_3
        self.currentmember.static_k = self.memberdata.dsb_k.value()
        self.currentmember.bonus = self.memberdata.dsb_bonus.value()
        self.calculate_static()
        self.filling(self.currentmember.cls)
        self.memberdata.save_static_btn.setEnabled(False)
        self.commit_changes()

    def calculate_static(self):
        if self.memberclass == 'F-4H':
            stat_k = self.kh_tup
            stat_lenth = 10
        else:
            stat_k = self.k_tup
            stat_lenth = 13
        correct_k = self.currentmember.static_k if self.memberclass == 'F-4G' else 1
        for k in range(13):
            item = '' if stat_k[k] == 0 else stat_k[k]
            exec(f'self.memberdata.k_{str(k)}.setText(str({str(item)}))')
        sum_1 = 0
        sum_2 = 0
        sum_3 = 0
        for j in range(stat_lenth):
            grade_1 = float(self.currentmember.stat_grade_1[j])
            grade_2 = float(self.currentmember.stat_grade_2[j])
            grade_3 = float(self.currentmember.stat_grade_3[j])
            k = stat_k[j]
            score_1 = str(round(k * grade_1, 1))
            score_2 = str(round(k * grade_2, 1))
            score_3 = str(round(k * grade_3, 1))
            sum_1 = sum_1 + float(score_1)
            sum_2 = sum_2 + float(score_2)
            sum_3 = sum_3 + float(score_3)

            exec(f'self.memberdata.dsb_1_{str(j)}.setValue(self.currentmember.stat_grade_1[{str(j)}])')
            exec(f'self.memberdata.dsb_2_{str(j)}.setValue(self.currentmember.stat_grade_2[{str(j)}])')
            exec(f'self.memberdata.dsb_3_{str(j)}.setValue(self.currentmember.stat_grade_3[{str(j)}])')
            exec(f'self.memberdata.score_1_{str(j)}.setText(''score_1'')')
            exec('self.memberdata.score_2_' + str(j) + '.setText(''score_2'')')
            exec('self.memberdata.score_3_' + str(j) + '.setText(''score_3'')')

        total = (sum_1 + sum_2 + sum_3) * correct_k + self.currentmember.bonus
        self.memberdata.sum_1.setText(str(sum_1))
        self.memberdata.sum_2.setText(str(sum_2))
        self.memberdata.sum_3.setText(str(sum_3))
        self.memberdata.total_score.setText(str(total))

    def commit_changes(self):
        self.saved_flag = True
        self.action.setEnabled(True)
        self.new_action.setEnabled(True)

    def closeEvent(self, event):
        if self.saved_flag:
            self.save_qwestion()


class f4cWindow(QDialog, Ui_F4C_fill):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class TourI(QDialog, Ui_TourI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class TourII(QDialog, Ui_TourII):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class FlyList(QDialog, Ui_Flylist):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Timetable(QDialog, Ui_Timetable):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class Data(QDialog, Ui_Data):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class Referee:
    items = []

    def __init__(self):
        self.name = ''
        self.surname = ''
        self.patronymic = ''
        Referee.items.append(self)


class Member:
    items = []

    def __init__(self, cls):
        self.cls = cls
        self.id = 0
        self.number = 0
        self.surname = ''
        self.name = ''
        self.region = ''
        self.prototype = ''
        self.scale = ''
        self.speed = 0
        self.tour_1 = 0
        self.tour_2 = 0
        self.tour_3 = 0
        self.static = 0
        self.fig_2 = [0, 0, 0]
        self.fig_3 = [0, 0, 0]
        self.fig_4 = [0, 0, 0]
        self.fig_5 = [0, 0, 0]
        self.fig_6 = [0, 0, 0]
        self.fig_7 = [0, 0, 0]
        self.fig_8 = [0, 0, 0]
        self.fig_9 = [0, 0, 0]
        self.stat_grade_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.stat_grade_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.stat_grade_3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.fly_grade_1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_4 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_5 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_6 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_7 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_8 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_9 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_10 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_11 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_12 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.fly_grade_13 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.static_k = 1
        self.bonus = 0
        Member.items.append(self)


class Info:
    items = []

    def __init__(self):
        self.locate = ''
        self.start_date = ''
        self.end_date = ''
        self.ekp_f4c = ''
        self.ekp_f4cu = ''
        self.f4c_tour_1 = None
        self.f4c_tour_2 = None
        self.f4c_tour_3 = None
        self.f4cu_tour_1 = None
        self.f4cu_tour_2 = None
        self.f4cu_tour_3 = None
        self.f4h_tour_1 = None
        self.f4h_tour_2 = None
        self.f4h_tour_3 = None
        self.f4g_tour_1 = None
        self.f4g_tour_2 = None
        self.f4g_tour_3 = None
        Info.items.append(self)


class TableModel(QAbstractTableModel):

    def __init__(self, headers, data_in, parent=None):

        super().__init__(parent)
        self.headers = headers
        self.data_in = data_in
        self.insertRows(len(self.data_in), 1)
        self.items = []

    def setItems(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]

    def data(self, index, role):

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            value = self.data_in[row][col]
            return value

    def columnCount(self, parent):

        return len(self.headers)

    def rowCount(self, parent):

        return len(self.data_in)

    def insertRows(self, position, rows, parent=QModelIndex()):

        self.beginInsertRows(parent, position, position + rows - 1)
        self.endInsertRows()
        return True

    # def removeRow(self, row: int, parent=QModelIndex()):
    #     self.beginRemoveRows(row, row)
    #     self.endRemoveRows()
    #     return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_window = F4C()
    app_window.show()
    sys.exit(app.exec_())
