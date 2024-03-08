from F4_UI import Ui_MainWindow
from F4C_fill_UI import Ui_F4C_fill
from Flyprog import Ui_FlyProg
from Static import Ui_Static
from Info import Ui_Info
from TourI_UI import Ui_TourI
from TourII_UI import Ui_TourII
from Flylist import Ui_Flylist
from Gradelist import Ui_Gradelist
from PyQt5 import QtWidgets, QtGui, QtPrintSupport
from PyQt5.QtWidgets import QWidget, QDialog, QMainWindow, QMessageBox, QFileDialog
from PyQt5.Qt import QApplication, Qt
from PyQt5.QtCore import QDate
import sys
import pickle
from pathlib import Path

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

f4cWindow = QDialog()
f4cui = Ui_F4C_fill()
f4cui.setupUi(f4cWindow)

flywin = QDialog()
flyui = Ui_FlyProg()
flyui.setupUi(flywin)

info = QDialog()
infoui = Ui_Info()
infoui.setupUi(info)

stat = QDialog()
statui = Ui_Static()
statui.setupUi(stat)

tour = QDialog()
tui = Ui_TourI()
tui.setupUi(tour)

tourII = QDialog()
tIIui = Ui_TourII()
tIIui.setupUi(tourII)

# tourIII = QDialog()
# tIIIui = Ui_TourIII()
# tIIIui.setupUi(tourIII)

flylist = QDialog()
flylistui = Ui_Flylist()
flylistui.setupUi(flylist)

gradelist = QDialog()
gradelistui = Ui_Gradelist()
gradelistui.setupUi(gradelist)

# ui.tableWidget.sortItems(0, order=Qt.AscendingOrder)
# ui.tableWidget_2.sortItems(0, order=Qt.AscendingOrder)
# ui.tableWidget_3.sortItems(0, order=Qt.AscendingOrder)
# ui.tableWidget_4.sortItems(0, order=Qt.AscendingOrder)
# tui.tableWidget.sortItems(10, order=Qt.AscendingOrder)

class Info:
    items = []
    
    def __init__(self):
        self.locate = ''
        self.start_date = ''
        self.end_date = ''
        self.ekp_f4c = ''
        self.ekp_f4cu = ''
        Info.items.append(self)


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


locate_data = Info()
referee_1 = Referee()
referee_2 = Referee()
referee_3 = Referee()
referee_4 = Referee()
referee_5 = Referee()
referee_6 = Referee()
referee_7 = Referee()
referee_8 = Referee()
referee_9 = Referee()
referee_10 = Referee()


memberclass = ""
table = None
id = 0


fly_tup = ('---', 'Восьмёрка', 'Снижение по кругу 360 градусов', 'A. Боевой разворот', 'B. Выпуск и уборка шасси',
           'C. Выпуск и уборка закрылков', 'D. Сбрасывание бомб или топливных баков', 'E. Срывной поворот',
           'F. Иммельман', 'G. Одна петля', 'H. Кубинская "8" прямая', 'I. Кубинская "8" обратная',
           'J. Кубинская "8" полная', 'K. Кубинская "8" половина', 'L. Половина “S” (обратная)',
           'M. Нормальный штопор (три витка)', 'N. Бочка', 'O. Парашют', 'P. Касание земли и взлёт (конвейер)',
           'Q. Перелёт при посадке', 'R. Скольжение влево или вправо', 'S. 1-ый полётный маневр прототипа',
           'T. 2-ой полётный маневр прототипа', 'U. Полёт по треугольному маршруту',
           'V. Полёт по четырёхугольному маршруту', 'W. Полёт по прямой на постоянной высоте (6 м)',
           'X. Полёт по прямой с одним из двигателей на малых об.', 'Y. "Ленивая" восьмёрка', 'Z. Поворот на горке',
           'AA. Перевёрнутый полёт', 'AB. Derry Turn', 'AC. Полный разворот', 'AD. Полет на малой скорости')

k_tup = (13, 13, 13, 3, 2, 8, 3, 7, 7, 12, 5, 9, 5)
kh_tup = (5, 5, 5, 3, 2, 3, 2, 4, 0, 6, 0, 0, 0)
fly_k = (11, 7, 7, 7, 7, 7, 7, 7, 7, 11, 4, 9, 9)

f4c_dict = {4: 'Текстура поверхности и реализм', 5: 'Мастерство изготовления', 6: 'Масштабность деталей'}
f4h_dict = {4: 'Реализм', 5: 'Разработка, происхождение и дизайн модели', 6: ''}
f4c_1_dict = {8: 'a) текстура поверхности', 9: 'b) соотв. текстуры масштабу', 10: 'а) качество', 11: 'b) сложность',
              12: 'а) точность', 13: 'b) сложность'}


for fly_items in range(2, 10):
    exec(f'flyui.comboBox_{fly_items}.addItems(fly_tup)')

currentmember = None
file = ''
filein = ''
tournumber = 'I'


def error_(error_massage):
    error = QMessageBox()
    error.setWindowTitle("ФАСР")
    error.setText(error_massage)
    error.setIcon(QMessageBox.Warning)
    error.setStandardButtons(QMessageBox.Ok)
    error.exec_()


def qwestion():
    row = table.currentRow()
    if row == -1:
        error_('Выберите участника!')
        return
    qwest = QMessageBox()
    qwest.setWindowTitle("ФАСР")
    qwest.setText("Вы уверны, что хотите удалить участника?")
    qwest.setIcon(QMessageBox.Question)
    qwest.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    qwest.buttonClicked.connect(qwestuion_action)
    qwest.exec_()


def qwestuion_action(btn):
    if btn.text() in ['OK', '&OK']:
        del_member()


def set_f4c():
    global memberclass
    memberclass = 'F-4C'
    global table
    table = ui.tableWidget
    f4cui.cls_label.setText(memberclass)
    statui.dsb_k.setEnabled(False)
    statui.dsb_bonus.setEnabled(False)


def set_f4cu():
    global memberclass
    memberclass = 'F-4C (Ю)'
    global table
    table = ui.tableWidget_2
    f4cui.cls_label.setText(memberclass)
    statui.dsb_k.setEnabled(False)
    statui.dsb_bonus.setEnabled(False)


def set_f4h():
    global memberclass
    memberclass = 'F-4H'
    global table
    table = ui.tableWidget_3
    f4cui.cls_label.setText(memberclass)
    statui.dsb_k.setEnabled(False)
    statui.dsb_bonus.setEnabled(True)


def set_f4g():
    global memberclass
    memberclass = 'F-4G'
    global table
    table = ui.tableWidget_4
    f4cui.cls_label.setText(memberclass)
    statui.dsb_k.setEnabled(True)
    statui.dsb_bonus.setEnabled(False)


def get_data():
    f4cui.cls_label.setText(memberclass)
    if f4cui.spinBox.value() == 0:
        f4cui.lineEdit_2.setEnabled(False)
        f4cui.lineEdit_3.setEnabled(False)
        f4cui.lineEdit_4.setEnabled(False)
        f4cui.lineEdit_5.setEnabled(False)
        f4cui.lineEdit_6.setEnabled(False)
        f4cui.lineEdit_7.setEnabled(False)
    else:
        f4cui.lineEdit_2.setEnabled(True)
        f4cui.lineEdit_3.setEnabled(True)
        f4cui.lineEdit_4.setEnabled(True)
        f4cui.lineEdit_5.setEnabled(True)
        f4cui.lineEdit_6.setEnabled(True)
        f4cui.lineEdit_7.setEnabled(True)
    f4cui.spinBox.valueChanged.connect(f4c_filling)
    f4cWindow.show()


def f4c_filling():
    f4cui.cls_label.setText(memberclass)
    f4cui.lineEdit_2.clear()
    f4cui.lineEdit_3.clear()
    f4cui.lineEdit_4.clear()
    f4cui.lineEdit_5.clear()
    f4cui.lineEdit_6.clear()
    f4cui.lineEdit_7.clear()
    if f4cui.spinBox.value() == 0:
        f4cui.lineEdit_2.setEnabled(False)
        f4cui.lineEdit_3.setEnabled(False)
        f4cui.lineEdit_4.setEnabled(False)
        f4cui.lineEdit_5.setEnabled(False)
        f4cui.lineEdit_6.setEnabled(False)
        f4cui.lineEdit_7.setEnabled(False)
    else:
        f4cui.lineEdit_2.setEnabled(True)
        f4cui.lineEdit_3.setEnabled(True)
        f4cui.lineEdit_4.setEnabled(True)
        f4cui.lineEdit_5.setEnabled(True)
        f4cui.lineEdit_6.setEnabled(True)
        f4cui.lineEdit_7.setEnabled(True)
    for i in Member.items:
        if i.number == f4cui.spinBox.value():
            f4cui.lineEdit_2.setText(str(i.surname))
            f4cui.lineEdit_3.setText(str(i.name))
            f4cui.lineEdit_4.setText(str(i.region))
            f4cui.lineEdit_5.setText(str(i.prototype))
            f4cui.lineEdit_6.setText(str(i.scale))
            f4cui.lineEdit_7.setText(str(i.speed))


def new_member():
    if f4cui.spinBox.value() == 0:
        error_('Укажите номер участника')
        get_data()
        return
    row = table.rowCount()
    for i in range(row):
        if int(table.item(i, 0).text()) == f4cui.spinBox.value():
            error_('Участник с таким номером уже зарегистрирован в этом классе')
            get_data()
            return
    global id
    id += 1
    a = 'member_' + str(id)
    globals()[a] = Member(memberclass)
    globals()[a].number = f4cui.spinBox.value()
    globals()[a].surname = f4cui.lineEdit_2.text()
    globals()[a].name = f4cui.lineEdit_3.text()
    globals()[a].region = f4cui.lineEdit_4.text()
    globals()[a].prototype = f4cui.lineEdit_5.text()
    globals()[a].scale = f4cui.lineEdit_6.text()
    globals()[a].speed = f4cui.lineEdit_7.text()
    globals()[a].id = id

    table.insertRow(row)
    table.setItem(row, 11, QtWidgets.QTableWidgetItem(str(id)))
    # table.item(row, 11).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
    table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(globals()[a].surname)))
    table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(globals()[a].name)))
    table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(globals()[a].region)))
    table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(globals()[a].prototype)))
    table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(globals()[a].number)))


def set_grades():
    row = table.currentRow()
    for i in Member.items:
        if int(i.id) == int(table.item(row, 11).text()):
            currentmember = i

    for j in range(1, 14):
        for k in range(1, 4):
            exec(f'currentmember.fly_grade_{str(j)}[{str(tourcount())}][{str(k - 1)}] = '
                 f'gradelistui.sb_{str(k)}_{str(j)}.value()')


    table_filling()
    grade_list()


def del_member():
    row = table.currentRow()
    item = int(table.item(row, 11).text())
    for i in Member.items:
        if int(i.id) == item:
            Member.items.remove(i)
            table.removeRow(row)


def all_results():
    set_f4c()
    row = table.rowCount()
    if row > -1:
        table_filling()
    set_f4cu()
    row = table.rowCount()
    if row > -1:
        table_filling()
    set_f4h()
    row = table.rowCount()
    if row > -1:
        table_filling()
    set_f4g()
    row = table.rowCount()
    if row > -1:
        table_filling()


def get_info():
    try:
        row = table.currentRow()
    except AttributeError:
        error_('Выберите участника!')
        return
    if row == -1:
        error_('Выберите участника!')
        return
    for i in Member.items:
        if int(i.id) == int(table.item(row, 11).text()):
            infoui.label_number.setText(str(i.number))
            infoui.lineEdit_surname.setText(str(i.surname))
            infoui.lineEdit_name.setText(str(i.name))
            infoui.lineEdit_prototype.setText(str(i.prototype))
            infoui.lineEdit_scale.setText(str(i.scale))
            infoui.lineEdit_speed.setText(str(i.speed))
            infoui.lineEdit_region.setText(str(i.region))
            infoui.label_cls.setText(str(i.cls))
            info.show()


def table_filling():
    if memberclass == 'F-4H':
        static_k = kh_tup
        static_lenth = 9
    else:
        static_k = k_tup
        static_lenth = 13

    rowcount = table.rowCount()
    res_list = []
    place_list = []
    for i in range(rowcount):
        for j in Member.items:
            if int(j.id) == int(table.item(i, 11).text()):
                tour_1 = []
                tour_2 = []
                tour_3 = []
                tourlist = []
                stat_sum_1 = 0
                stat_sum_2 = 0
                stat_sum_3 = 0
                for m in range(13):
                    for n in range(3):
                        exec(f'tour_{str(n + 1)}.append(sum(j.fly_grade_{str(m + 1)}[{str(n)}]) * fly_k[{str(m)}])')
                for k in range(13):
                    stat_grade_1 = float(j.stat_grade_1[k])
                    stat_grade_2 = float(j.stat_grade_2[k])
                    stat_grade_3 = float(j.stat_grade_3[k])
                    k_stat = static_k[k]
                    stat_score_1 = str(k_stat * stat_grade_1)
                    stat_score_2 = str(k_stat * stat_grade_2)
                    stat_score_3 = str(k_stat * stat_grade_3)
                    stat_sum_1 = stat_sum_1 + float(stat_score_1)
                    stat_sum_2 = stat_sum_2 + float(stat_score_2)
                    stat_sum_3 = stat_sum_3 + float(stat_score_3)
                stat_total = round((stat_sum_1 + stat_sum_2 + stat_sum_3 + j.bonus) * j.static_k, 2)
                table.setItem(i, 5, QtWidgets.QTableWidgetItem(str(stat_total)))
                table.setItem(i, 6, QtWidgets.QTableWidgetItem(str(round(sum(tour_1), 2))))
                tourlist.append(round(sum(tour_1), 2))
                table.setItem(i, 7, QtWidgets.QTableWidgetItem(str(round(sum(tour_2), 2))))
                tourlist.append(round(sum(tour_2), 2))
                table.setItem(i, 8, QtWidgets.QTableWidgetItem(str(round(sum(tour_3), 2))))
                tourlist.append(round(sum(tour_3), 2))
                tourlist.sort(reverse=True)
                result = (tourlist[0] + tourlist[1]) / 2 + stat_total
                # if tourlist[1] == 0:
                #     result = tourlist[0] + stat_total
                # else:
                #     result = (tourlist[0] + tourlist[1]) / 2 + stat_total
                table.setItem(i, 9, QtWidgets.QTableWidgetItem(str(result)))
                res_list.append(result)
                place_list.append(result)
    place_list.sort(reverse=True)
    for l in range(rowcount):
        place = place_list.index(res_list[l]) + 1
        table.setItem(l, 10, QtWidgets.QTableWidgetItem(str(place)))


def set_info():
    row = table.currentRow()
    table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(infoui.label_number.text())))
    table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(infoui.lineEdit_surname.text())))
    table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(infoui.lineEdit_name.text())))
    table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(infoui.lineEdit_region.text())))
    table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(infoui.lineEdit_prototype.text())))
    for i in Member.items:
        if i.id == int(table.item(row, 11).text()):
            i.number = int(infoui.label_number.text())
            i.surname = infoui.lineEdit_surname.text()
            i.name = infoui.lineEdit_name.text()
            i.region = infoui.lineEdit_region.text()
            i.cls = infoui.label_cls.text()
            i.prototype = infoui.lineEdit_prototype.text()
            i.scale = infoui.lineEdit_scale.text()
            i.speed = infoui.lineEdit_speed.text()


def get_prog():
    global currentmember
    try:
        row = table.currentRow()
    except AttributeError:
        error_('Выберите участника!')
        return
    if row == -1:
        error_('Выберите участника!')
        return
    for i in Member.items:
        if int(i.id) == int(table.item(row, 11).text()):
            currentmember = i
            for j in range(2, 10):
                exec(f'flyui.comboBox_{str(j)}.setCurrentIndex(int(i.fig_{str(j)}[' \
                f'{"1" if flyui.radioButton_2.isChecked() else "2" if flyui.radioButton_3.isChecked() else "0"}]))')

    flywin.show()


def set_prog():
    try:
        row = table.currentRow()
    except AttributeError:
        error_('Выберите участника!')
        return
    for i in Member.items:
        if int(i.id) == int(table.item(row, 11).text()):
            for j in range(2, 10):
                exec(f'i.fig_{str(j)}['
                     f'{"1" if flyui.radioButton_2.isChecked() else "2" if flyui.radioButton_3.isChecked() else "0"}]'
                     f' = flyui.comboBox_{str(j)}.currentIndex()')
                if flyui.radioButton.isChecked():
                    exec(f'i.fig_{str(j)}[1] = i.fig_{str(j)}[0]')
                    exec(f'i.fig_{str(j)}[2] = i.fig_{str(j)}[0]')


def get_static():
    if memberclass == 'F-4H':
        stat_k = kh_tup
        stat_lenth = 10
        dict = f4h_dict
    else:
        stat_k = k_tup
        stat_lenth = 13
        dict = f4c_dict

    global currentmember
    try:
        row = table.currentRow()
    except AttributeError:
        error_('Выберите участника!')
        return
    if row == -1:
        error_('Выберите участника!')
        return
    for i in Member.items:
        if int(i.id) == int(table.item(row, 11).text()):
            currentmember = i
            correct_k = i.static_k if memberclass == 'F-4G' else 1
            statui.surname_lbl.setText(str(currentmember.surname))
            statui.name_lbl.setText(str(currentmember.name))
            statui.number_lbl.setText(f'№ {str(currentmember.number)}')
            statui.prototype_lbl.setText(str(currentmember.prototype))
            statui.texture.setText(dict.get(4))
            statui.skill.setText(dict.get(5))
            statui.scale_2.setText(dict.get(6))
            statui.label_18.setText('' if memberclass == 'F-4H' else f4c_1_dict.get(8))
            statui.label_19.setText('' if memberclass == 'F-4H' else f4c_1_dict.get(9))
            statui.label_20.setText('' if memberclass == 'F-4H' else f4c_1_dict.get(10))
            statui.label_21.setText('' if memberclass == 'F-4H' else f4c_1_dict.get(11))
            statui.label_24.setText('' if memberclass == 'F-4H' else f4c_1_dict.get(12))
            statui.label_25.setText('' if memberclass == 'F-4H' else f4c_1_dict.get(13))
            statui.dsb_1_8.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_2_8.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_3_8.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_1_10.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_1_11.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_1_12.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_2_10.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_2_11.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_2_12.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_3_10.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_3_11.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_3_12.setEnabled(False if memberclass == 'F-4H' else True)
            statui.dsb_k.setValue(correct_k if memberclass == 'F-4G' else 1)
            statui.dsb_bonus.setValue(currentmember.bonus if memberclass == 'F-4H' else 0)

            for k in range(13):
                item = '' if stat_k[k] == 0 else stat_k[k]
                exec(f'statui.k_{str(k)}.setText(str({str(item)}))')
            sum_1 = 0
            sum_2 = 0
            sum_3 = 0
            for j in range(stat_lenth):
                grade_1 = float(currentmember.stat_grade_1[j])
                grade_2 = float(currentmember.stat_grade_2[j])
                grade_3 = float(currentmember.stat_grade_3[j])
                k = stat_k[j]
                score_1 = str(round(k * grade_1, 1))
                score_2 = str(round(k * grade_2, 1))
                score_3 = str(round(k * grade_3, 1))
                sum_1 = sum_1 + float(score_1)
                sum_2 = sum_2 + float(score_2)
                sum_3 = sum_3 + float(score_3)

                exec(f'statui.dsb_1_{str(j)}.setValue(i.stat_grade_1[{str(j)}])')
                exec(f'statui.dsb_2_{str(j)}.setValue(i.stat_grade_2[{str(j)}])')
                exec(f'statui.dsb_3_{str(j)}.setValue(i.stat_grade_3[{str(j)}])')
                exec(f'statui.score_1_{str(j)}.setText(''score_1'')')
                exec('statui.score_2_' + str(j) + '.setText(''score_2'')')
                exec('statui.score_3_' + str(j) + '.setText(''score_3'')')

            total = (sum_1 + sum_2 + sum_3) * correct_k + currentmember.bonus
            statui.sum_1.setText(str(sum_1))
            statui.sum_2.setText(str(sum_2))
            statui.sum_3.setText(str(sum_3))
            statui.total_score.setText(str(total))

    stat.show()


def static_action(btn):
    if btn.text() in ['OK', 'Apply', '&OK', '&Apply']:
        set_static()
        get_static()


def set_static():
    row = table.currentRow()
    for i in Member.items:
        if int(i.id) == int(table.item(row, 11).text()):
            data_1 = []
            data_2 = []
            data_3 = []
            for j in range(13):
                exec(f'data_1.append(statui.dsb_1_{str(j)}.value())')
                exec(f'data_2.append(statui.dsb_2_{str(j)}.value())')
                exec(f'data_3.append(statui.dsb_3_{str(j)}.value())')

            i.stat_grade_1 = data_1
            i.stat_grade_2 = data_2
            i.stat_grade_3 = data_3
            i.static_k = statui.dsb_k.value()
            i.bonus = statui.dsb_bonus.value()

    table_filling()


def filein():
    dialog = QWidget()
    dialog.setWindowTitle("Выберите файл")
    dialog.setGeometry(10, 10, 640, 480)
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(dialog, "Выберите файл", "", "Файл данных (*.f4c)", options=options)
    if filename:
        global filein
        filein = filename
        open_file()


def clear_table():
    row = table.rowCount()
    if row > -1:
        for i in reversed(range(row)):
            table.removeRow(i)


def set_open():
    global id
    idlist = []
    for i in Member.items:
        if i.cls == 'F-4C':
            set_f4c()
        if i.cls == 'F-4C (Ю)':
            set_f4cu()
        if i.cls == 'F-4H':
            set_f4h()
        if i.cls == 'F-4G':
            set_f4g()

        idlist.append(i.id)
        row = table.rowCount()
        # id += 1
        table.insertRow(row)
        table.setItem(row, 11, QtWidgets.QTableWidgetItem(str(i.id)))
        table.item(row, 11).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i.number)))
        table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i.surname)))
        table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i.name)))
        table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i.region)))
        table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i.prototype)))
        table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(i.static)))
        # table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(i.tour_1)))
        # table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(i.tour_2)))
        # table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(i.tour_3)))
        # table_filling()

    id = (0 if idlist == [] else max(idlist))
    set_referees()
    set_data()
    all_results()
    change_tab()


def clear_all():
    Referee.items.clear()
    Member.items.clear()
    Info.items.clear()
    set_f4c()
    clear_table()
    set_f4cu()
    clear_table()
    set_f4h()
    clear_table()
    set_f4g()
    clear_table()
    change_tab()


def open_file():
    clear_all()
    global locate_data
    with open(filein, 'rb') as f:
        locate_data = pickle.load(f)
        reflist = pickle.load(f)
        memberlist = pickle.load(f)
        for i in reflist:
            i = pickle.load(f)
            Referee.items.append(i)
        for j in memberlist:
            j = pickle.load(f)
            Member.items.append(j)

    set_open()


def write():
    reflist = Referee.items
    memberlist = Member.items
    with open(file, 'wb') as f:
        pickle.dump(locate_data, f)
        pickle.dump(reflist, f)
        pickle.dump(memberlist, f)
        for i in reflist:
            pickle.dump(i, f)
        for j in memberlist:
            pickle.dump(j, f)


def save_():
    if file == "":
        save_as()
    else:
        write()


def save_as():
    dialog = QWidget()
    dialog.setWindowTitle("Сохранить файл")
    dialog.setGeometry(10, 10, 640, 480)
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(dialog, "Сохранить файл", "", "Файл данных (*.f4c)", options=options)
    if not Path(fileName).suffix == '.f4c':
        fileName = f'{fileName}.f4c'
    if fileName:
        global file
        file = fileName
        write()

    dialog.show()


def change_tab():
    if ui.tabWidget.currentIndex() == 0:
        ui.pushButton.setEnabled(False)
        ui.pushButton_2.setEnabled(False)
        ui.f4c_btn.setEnabled(False)
        ui.f4c_btn_2.setEnabled(False)
        ui.f4c_btn_4.setEnabled(False)
        ui.f4c_btn_5.setEnabled(False)
        ui.f4c_btn_6.setEnabled(False)
        ui.f4c_btn_7.setEnabled(False)
    else:
        ui.pushButton.setEnabled(True)
        ui.pushButton_2.setEnabled(True)
        ui.f4c_btn.setEnabled(True)
        ui.f4c_btn_2.setEnabled(True)
        ui.f4c_btn_4.setEnabled(True)
        ui.f4c_btn_5.setEnabled(True)
        ui.f4c_btn_6.setEnabled(True)
        ui.f4c_btn_7.setEnabled(True)
    if ui.tabWidget.currentIndex() == 1:
        set_f4c()
    if ui.tabWidget.currentIndex() == 2:
        set_f4cu()
    if ui.tabWidget.currentIndex() == 3:
        set_f4h()
    if ui.tabWidget.currentIndex() == 4:
        set_f4g()


def tourcount():
    global tournumber
    tour = 0
    tournumber = 'I'
    if gradelistui.radioButton_2.isChecked():
        tour = 1
        tournumber = 'II'
    if gradelistui.radioButton_3.isChecked():
        tour = 2
        tournumber = 'III'
    gradelistui.label_54.setText(f'{tournumber} тур')
    return tour


def tour_1_out():
    if memberclass == 'F-4H':
        stat_k = kh_tup
        stat_lenth = 10
    else:
        stat_k = k_tup
        stat_lenth = 13

    global tournumber
    tournumber = 'I'
    tour.setWindowTitle(memberclass + ' ФАС России ' + tournumber + ' тур')
    table_1 = tui.tableWidget
    row = table_1.rowCount()
    if row > -1:
        for i in reversed(range(row)):
            table_1.removeRow(i)

    res_list = []
    place_list = []
    for y in Member.items:
        if y.cls == memberclass:
            tour_1 = []
            stat_sum_1 = 0
            stat_sum_2 = 0
            stat_sum_3 = 0
            for m in range(13):
                exec(f'tour_1.append(sum(y.fly_grade_{str(m + 1)}[0]) * fly_k[{str(m)}])')
            for k in range(13):
                stat_grade_1 = float(y.stat_grade_1[k])
                stat_grade_2 = float(y.stat_grade_2[k])
                stat_grade_3 = float(y.stat_grade_3[k])
                stat_score_1 = str(stat_k[k] * stat_grade_1)
                stat_score_2 = str(stat_k[k] * stat_grade_2)
                stat_score_3 = str(stat_k[k] * stat_grade_3)
                stat_sum_1 = stat_sum_1 + float(stat_score_1)
                stat_sum_2 = stat_sum_2 + float(stat_score_2)
                stat_sum_3 = stat_sum_3 + float(stat_score_3)
            stat_total = round((stat_sum_1 + stat_sum_2 + stat_sum_3) * y.static_k + y.bonus, 2)
            result = stat_total + sum(tour_1)
            table_1.insertRow(row)
            table_1.setItem(row, 0, QtWidgets.QTableWidgetItem(str(y.number)))
            table_1.setItem(row, 1, QtWidgets.QTableWidgetItem(str(y.surname)))
            table_1.setItem(row, 2, QtWidgets.QTableWidgetItem(str(y.name)))
            table_1.setItem(row, 3, QtWidgets.QTableWidgetItem(str(y.region)))
            table_1.setItem(row, 4, QtWidgets.QTableWidgetItem(str(y.prototype)))
            table_1.setItem(row, 5, QtWidgets.QTableWidgetItem(str(stat_total)))
            table_1.setItem(row, 6, QtWidgets.QTableWidgetItem(str(sum(tour_1))))
            table_1.setItem(row, 7, QtWidgets.QTableWidgetItem(str(result)))
            res_list.append(result)
            place_list.append(result)
    place_list.sort(reverse=True)
    rowcount = table_1.rowCount()

    for l in range(rowcount):
        place = place_list.index(float(table_1.item(l, 7).text())) + 1
        table_1.setItem(l, 8, QtWidgets.QTableWidgetItem(str(place)))

    tour.show()


def tour_1_request(printer):
    printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
    begin_date = "{}".format(ui.dateEdit.date().toString('dd.MM.yyyy'))
    end_date = "{}".format(ui.dateEdit_2.date().toString('dd.MM.yyyy'))
    table_1 = tui.tableWidget
    row = table_1.rowCount()
    column = table_1.columnCount()

    first = 'Первенство' if memberclass == 'F-4C (Ю)' else 'Чемпионат'
    ekp = locate_data.ekp_f4cu if memberclass == 'F-4C (Ю)' else locate_data.ekp_f4c
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
          f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {memberclass}</u><br><br>' \
          f'{locate_data.locate} {begin_date} - {end_date} г.<br>' \
          f'</td>' \
          f'<td>№ ЕКП:{ekp}</td>' \
          f'</table>' \
          f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
          f'<tr>' \
          f'<td align="center" width="3%">№</td>' \
          f'<td align="center" width="19%">Фамилия</td>' \
          f'<td align="center" width="18%">Имя</td>' \
          f'<td align="center" width="19%">Регион</td>' \
          f'<td align="center" width="19%">Прототип</td>' \
          f'<td align="center" width="6%">Стенд</td>' \
          f'<td align="center" width="6%">I тур</td>' \
          f'<td align="center" width="6%">Рез.</td>' \
          f'<td align="center" width="4%">Место</td>' \
          f'</tr>' \

    for i in range(row):
        content = content + '<tr>'
        for k in range(column):
            item = table_1.item(i, k).text()
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
    page = top  +  content + bottom
    document = QtGui.QTextDocument()
    document.setHtml(page)
    document.print_(printer)


def tour_2_out():
    if memberclass == 'F-4H':
        stat_k = kh_tup
        stat_lenth = 10
    else:
        stat_k = k_tup
        stat_lenth = 13

    global tournumber
    tournumber = 'II'
    tourII.setWindowTitle(memberclass + ' ФАС России ' + tournumber + ' тур')
    table_2 = tIIui.tableWidget
    row = table_2.rowCount()
    if row > -1:
        for i in reversed(range(row)):
            table_2.removeRow(i)

    res_list = []
    place_list = []
    for y in Member.items:
        if y.cls == memberclass:
            tour_1 = []
            tour_2 = []
            tourlist = []
            stat_sum_1 = 0
            stat_sum_2 = 0
            stat_sum_3 = 0
            for m in range(13):
                exec(f'tour_1.append(sum(y.fly_grade_{str(m + 1)}[0]) * fly_k[{str(m)}])')
                exec(f'tour_2.append(sum(y.fly_grade_{str(m + 1)}[1]) * fly_k[{str(m)}])')
            for k in range(13):
                stat_grade_1 = float(y.stat_grade_1[k])
                stat_grade_2 = float(y.stat_grade_2[k])
                stat_grade_3 = float(y.stat_grade_3[k])
                stat_score_1 = str(stat_k[k] * stat_grade_1)
                stat_score_2 = str(stat_k[k] * stat_grade_2)
                stat_score_3 = str(stat_k[k] * stat_grade_3)
                stat_sum_1 = stat_sum_1 + float(stat_score_1)
                stat_sum_2 = stat_sum_2 + float(stat_score_2)
                stat_sum_3 = stat_sum_3 + float(stat_score_3)
            stat_total = round((stat_sum_1 + stat_sum_2 + stat_sum_3) * y.static_k + y.bonus, 2)
            tourlist.append(round(sum(tour_1), 2))
            tourlist.append(round(sum(tour_2), 2))
            tourlist.sort(reverse=True)
            result = stat_total + (tourlist[0] + tourlist[1]) / 2
            # if tourlist[1] == 0:
            #     result = stat_total + tourlist[0]
            # else:
            #     result = stat_total + (tourlist[0] + tourlist[1]) / 2
            table_2.insertRow(row)
            table_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(y.number)))
            table_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(y.surname)))
            table_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(y.name)))
            table_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(y.region)))
            table_2.setItem(row, 4, QtWidgets.QTableWidgetItem(str(y.prototype)))
            table_2.setItem(row, 5, QtWidgets.QTableWidgetItem(str(stat_total)))
            table_2.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(sum(tour_1), 2))))
            table_2.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(sum(tour_2), 2))))
            table_2.setItem(row, 8, QtWidgets.QTableWidgetItem(str(result)))
            res_list.append(result)
            place_list.append(result)
    place_list.sort(reverse=True)
    rowcount = table_2.rowCount()
    for l in range(rowcount):
        place = place_list.index(float(table_2.item(l, 8).text())) + 1
        table_2.setItem(l, 9, QtWidgets.QTableWidgetItem(str(place)))

    tourII.show()


def tour_2_request(printer):
    printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
    begin_date = "{}".format(ui.dateEdit.date().toString('dd.MM.yyyy'))
    end_date = "{}".format(ui.dateEdit_2.date().toString('dd.MM.yyyy'))
    table_2 = tIIui.tableWidget
    row = table_2.rowCount()
    column = table_2.columnCount()

    first = 'Первенство' if memberclass == 'F-4C (Ю)' else 'Чемпионат'
    ekp = locate_data.ekp_f4cu if memberclass == 'F-4C (Ю)' else locate_data.ekp_f4c
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
          f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {memberclass}</u><br><br>' \
          f'{locate_data.locate} {begin_date} - {end_date} г.<br>' \
          f'</td>' \
          f'<td> № ЕКП: {ekp}</td>' \
          f'</table>' \
          f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
          f'<tr>' \
          f'<td align="center" width="3%">№</td>' \
          f'<td align="center" width="18.5%">Фамилия</td>' \
          f'<td align="center" width="17.5%">Имя</td>' \
          f'<td align="center" width="18.5%">Регион</td>' \
          f'<td align="center" width="18.5%">Прототип</td>' \
          f'<td align="center" width="5%">Стенд</td>' \
          f'<td align="center" width="5%">I тур</td>' \
          f'<td align="center" width="5%">II тур</td>' \
          f'<td align="center" width="5%">Рез.</td>' \
          f'<td align="center" width="4%">Место</td>' \
          f'</tr>' \

    for i in range(row):
        content = content + '<tr>'
        for k in range(column):
            item = table_2.item(i, k).text()
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


def tour_3_request(printer):
    printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
    begin_date = "{}".format(ui.dateEdit.date().toString('dd.MM.yyyy'))
    end_date = "{}".format(ui.dateEdit_2.date().toString('dd.MM.yyyy'))
    # table_3 = tIIIui.tableWidget
    row = table.rowCount()
    column = table.columnCount() - 1

    first = 'Первенство' if memberclass == 'F-4C (Ю)' else 'Чемпионат'
    ekp = locate_data.ekp_f4cu if memberclass == 'F-4C (Ю)' else locate_data.ekp_f4c
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
          f'<u>{first} России в классе радиоуправляемых моделей-копий самолетов {memberclass}</u><br><br>' \
          f'{locate_data.locate} {begin_date} - {end_date} г.<br>' \
          f'</td>' \
          f'<td> № ЕКП: {ekp}' \
          f'</td>' \
          f'</table>' \
          f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
          f'<tr>' \
          f'<td align="center" width="3%">№</td>' \
          f'<td align="center" width="16%">Фамилия</td>' \
          f'<td align="center" width="15%">Имя</td>' \
          f'<td align="center" width="16%">Регион</td>' \
          f'<td align="center" width="16%">Прототип</td>' \
          f'<td align="center" width="6%">Стенд</td>' \
          f'<td align="center" width="6%">I тур</td>' \
          f'<td align="center" width="6%">II тур</td>' \
          f'<td align="center" width="6%">III тур</td>' \
          f'<td align="center" width="6%">Рез.</td>' \
          f'<td align="center" width="4%">Место</td>' \
          f'</tr>' \

    for i in range(row):
        content = content + '<tr>'
        for k in range(column):
            try:
                item = table.item(i, k).text()
            except AttributeError:
                error_('Недостаточно данных для вывода результатов')
                return
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


def set_surname(surname, num):
    Referee.items[num].surname = surname
    # set_referees()


def set_name(name, num):
    Referee.items[num].name = name
    # set_referees()


def set_patronymic(patronymic, num):
    Referee.items[num].patronymic = patronymic
    # set_referees()


def set_referees():
    for k in range(9, 12):
        exec(f'gradelistui.comboBox_{str(k)}.clear()')
        exec(f'statui.comboBox_{str(k - 8)}.clear()')

    flylistui.comboBox_1.clear()

    for i in range(5):
        referee = Referee.items[i]
        surname = f'{referee.surname} '
        name = f'{"" if referee.name == "" else referee.name[0]}.'
        patronymic = f'{"" if referee.patronymic == "" else referee.patronymic[0]}.'
        item = surname + name + patronymic
        for j in range(9, 12):
            exec(f'gradelistui.comboBox_{str(j)}.addItem(item)')
            exec(f'gradelistui.comboBox_{str(j)}.setCurrentIndex({str(j - 9)})')
            exec(f'statui.comboBox_{str(j - 8)}.addItem(item)')
            exec(f'statui.comboBox_{str(j - 8)}.setCurrentIndex({str(j - 9)})')
        flylistui.comboBox_1.addItem(item)
    flylistui.comboBox_1.setCurrentIndex(0)

    for o in range(10):
        referee = Referee.items[o]
        print(Referee.items[o].surname)
        surname = f'{referee.surname}'
        name = f'{referee.name}'
        patronymic = f'{referee.patronymic}'
        exec(f'ui.lineEdit_{str(o)}_0.setText(surname)')
        exec(f'ui.lineEdit_{str(o)}_1.setText(name)')
        exec(f'ui.lineEdit_{str(o)}_2.setText(patronymic)')



def set_start_date():
    locate_data.start_date = ui.dateEdit.date()


def set_end_date():
    locate_data.end_date = ui.dateEdit_2.date()


def set_locate():
    locate_data.locate = ui.lineEdit_25.text()


def set_ekp_f4c():
    locate_data.ekp_f4c = ui.lineEdit_26.text()


def set_ekp_f4cu():
    locate_data.ekp_f4cu = ui.lineEdit_27.text()


def set_data():
    ui.lineEdit_25.setText(locate_data.locate)
    ui.lineEdit_26.setText(locate_data.ekp_f4c)
    ui.lineEdit_27.setText(locate_data.ekp_f4cu)
    ui.dateEdit.setDate(QDate(locate_data.start_date))
    ui.dateEdit_2.setDate(QDate(locate_data.end_date))


def fly_list():
    flylistui.surname_lbl.setText(str(currentmember.surname))
    flylistui.name_lbl.setText(str(currentmember.name))
    flylistui.number_lbl.setText(str(currentmember.number))
    flylistui.region_lbl.setText(str(currentmember.region))
    flylistui.prototype_lbl.setText(str(currentmember.prototype))
    flylistui.scale_lbl.setText(str(currentmember.scale))
    flylistui.speed_lbl.setText(str(currentmember.speed))
    flylistui.cls_label.setText(str(currentmember.cls))
    for j in range(1, 9):
        exec(f'flylistui.label_{str(j)}_1.setText(flyui.comboBox_{str(j + 1)}.currentText())')
    for k in range(13):
        exec(f'flylistui.label_{str(k)}_3.setText("X" if (flyui.radioButton_1.isChecked()'
             f' or flyui.radioButton_2.isChecked()) else "")')
        exec(f'flylistui.label_{str(k)}_4.setText("X" if (flyui.radioButton_1.isChecked()'
             f' or flyui.radioButton_3.isChecked()) else "")')
        exec(f'flylistui.label_{str(k)}_5.setText("X" if (flyui.radioButton_2.isChecked()'
             f' or flyui.radioButton_3.isChecked()) else "")')

    flylist.show()


def grade_list():
    total_list = []
    bonus = currentmember.bonus

    gradelistui.name.setText(f'{currentmember.surname} {currentmember.prototype}')

    for m in range(2, 10):
        exec(f'gradelistui.fig_{str(m)}.setText(fly_tup[currentmember.fig_{str(m)}[{str(tourcount())}]])')

    for j in range(1, 14):
        exec(f'gradelistui.total_{str(j)}.'
             f'setText(str(sum(currentmember.fly_grade_{str(j)}[{str(tourcount())}]) * '
             f'int(gradelistui.k_{str(j)}.text())))')
        exec(f'total_list.append(float(gradelistui.total_{str(j)}.text()))')



    for k in range(1, 14):
        for l in range(1, 4):
            exec(f'gradelistui.sb_{str(l)}_{str(k)}.setValue(currentmember.'
                 f'fly_grade_{str(k)}[{str(tourcount())}][{str(l - 1)}])')
    gradelistui.total.setText(str(sum(total_list)))
    gradelist.show()


def gradelist_action(btn):
    if btn.text() in ['OK', 'Apply', '&OK', '&Apply']:
        set_grades()


def handlePreview(target):
    dialog = QtPrintSupport.QPrintPreviewDialog()
    dialog.paintRequested.connect(target)
    dialog.exec_()


def flylist_request(printer):
    flylist_dict = {'label_0_0': flylistui.label_0_0.text(), 'label_0_1': flylistui.label_0_1.text(),
                    'label_0_2': flylistui.label_0_2.text(), 'label_0_3': flylistui.label_0_3.text(),
                    'label_0_4': flylistui.label_0_4.text(), 'label_0_5': flylistui.label_0_5.text(),
                    'label_1_0': flylistui.label_1_0.text(), 'label_1_1': flylistui.label_1_1.text(),
                    'label_1_2': flylistui.label_1_2.text(), 'label_1_3': flylistui.label_1_3.text(),
                    'label_1_4': flylistui.label_1_4.text(), 'label_1_5': flylistui.label_1_5.text(),
                    'label_2_0': flylistui.label_2_0.text(), 'label_2_1': flylistui.label_2_1.text(),
                    'label_2_2': flylistui.label_2_2.text(), 'label_2_3': flylistui.label_2_3.text(),
                    'label_2_4': flylistui.label_2_4.text(), 'label_2_5': flylistui.label_2_5.text(),
                    'label_3_0': flylistui.label_3_0.text(), 'label_3_1': flylistui.label_3_1.text(),
                    'label_3_2': flylistui.label_3_2.text(), 'label_3_3': flylistui.label_3_3.text(),
                    'label_3_4': flylistui.label_3_4.text(), 'label_3_5': flylistui.label_2_5.text(),
                    'label_4_0': flylistui.label_4_0.text(), 'label_4_1': flylistui.label_4_1.text(),
                    'label_4_2': flylistui.label_4_2.text(), 'label_4_3': flylistui.label_4_3.text(),
                    'label_4_4': flylistui.label_4_4.text(), 'label_4_5': flylistui.label_4_5.text(),
                    'label_5_0': flylistui.label_5_0.text(), 'label_5_1': flylistui.label_5_1.text(),
                    'label_5_2': flylistui.label_5_2.text(), 'label_5_3': flylistui.label_5_3.text(),
                    'label_5_4': flylistui.label_5_4.text(), 'label_5_5': flylistui.label_2_5.text(),
                    'label_6_0': flylistui.label_6_0.text(), 'label_6_1': flylistui.label_6_1.text(),
                    'label_6_2': flylistui.label_6_2.text(), 'label_6_3': flylistui.label_6_3.text(),
                    'label_6_4': flylistui.label_6_4.text(), 'label_6_5': flylistui.label_6_5.text(),
                    'label_7_0': flylistui.label_7_0.text(), 'label_7_1': flylistui.label_7_1.text(),
                    'label_7_2': flylistui.label_7_2.text(), 'label_7_3': flylistui.label_7_3.text(),
                    'label_7_4': flylistui.label_7_4.text(), 'label_7_5': flylistui.label_7_5.text(),
                    'label_8_0': flylistui.label_8_0.text(), 'label_8_1': flylistui.label_8_1.text(),
                    'label_8_2': flylistui.label_8_2.text(), 'label_8_3': flylistui.label_8_3.text(),
                    'label_8_4': flylistui.label_8_4.text(), 'label_8_5': flylistui.label_8_5.text(),
                    'label_9_0': flylistui.label_9_0.text(), 'label_9_1': flylistui.label_9_1.text(),
                    'label_9_2': flylistui.label_9_2.text(), 'label_9_3': flylistui.label_9_3.text(),
                    'label_9_4': flylistui.label_9_4.text(), 'label_9_5': flylistui.label_9_5.text(),
                    'label_10_0': flylistui.label_10_0.text(), 'label_10_1': flylistui.label_10_1.text(),
                    'label_10_2': flylistui.label_10_2.text(), 'label_10_3': flylistui.label_10_3.text(),
                    'label_10_4': flylistui.label_10_4.text(), 'label_10_5': flylistui.label_10_5.text(),
                    'label_11_0': flylistui.label_11_0.text(), 'label_11_1': flylistui.label_11_1.text(),
                    'label_11_2': flylistui.label_11_2.text(), 'label_11_3': flylistui.label_11_3.text(),
                    'label_11_4': flylistui.label_11_4.text(), 'label_11_5': flylistui.label_11_5.text(),
                    'label_12_0': flylistui.label_12_0.text(), 'label_12_1': flylistui.label_12_1.text(),
                    'label_12_2': flylistui.label_12_2.text(), 'label_12_3': flylistui.label_12_3.text(),
                    'label_12_4': flylistui.label_12_4.text(), 'label_12_5': flylistui.label_12_5.text()}
    current_year = "{}".format(ui.dateEdit.date().toString('yyyy'))
    program = ''

    for i in range(13):
        program = program + '<tr>'
        for j in range(6):
            item = flylist_dict.get("label_{}_{}".format(str(i), str(j)))
            program = program + f'<td>{item}</td>'
        program = program + '</tr>'
    flylist_page = f'<!DOCTYPE html><html lang="ru">'\
                   f'<head>' \
                   f'<meta charset="UTF-8">' \
                   f'</head>' \
                   f'<body>' \
                   f'<table width="100%" border="1" bordercolor="ffffff" cellspacing="0" cellpadding="3">' \
                   f'<tr>' \
                   f'<td rowspan="5" width="52%" align="center">ФЕДЕРАЦИЯ АВИАМОДЕЛЬНОГО СПОРТА РОССИИ<br>' \
                   f'Чемпионат России в классе радиоуправляемых<br>' \
                   f'моделей-копий самолетов<br>' \
                   f'{current_year} г.<br>' \
                   f'{memberclass}' \
                   f'</td>' \
                   f'<td align="center">III тур</td>' \
                   f'<td align="center">II тур</td>' \
                   f'<td align="center">I тур</td>' \
                   f'</tr>' \
                   f'<tr>' \
                   f'<td align="center">{currentmember.surname}</td>' \
                   f'<td align="center">{currentmember.surname}</td>' \
                   f'<td align="center">{currentmember.surname}</td>' \
                   f'</tr>' \
                   f'<tr>' \
                   f'<td align="center">№ {currentmember.number}</td>' \
                   f'<td align="center">№ {currentmember.number}</td>' \
                   f'<td align="center">№ {currentmember.number}</td>' \
                   f'</tr>' \
                   f'<tr>' \
                   f'<td align="center">{memberclass}</td>' \
                   f'<td align="center">{memberclass}</td>' \
                   f'<td align="center">{memberclass}</td>' \
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
                   f'<td colspan="2"></td>' \
                   f'<td>Судья</td>' \
                   f'<td>Судья</td>' \
                   f'<td>Судья</td>' \
                   f'</tr>' \
                   f'<tr>' \
                   f'<td></td>' \
                   f'<td colspan="2"></td>' \
                   f'<td>{flylistui.comboBox_1.currentText()}<br><br>_____________</td>' \
                   f'<td>{flylistui.comboBox_1.currentText()}<br><br>_____________</td>' \
                   f'<td>{flylistui.comboBox_1.currentText()}<br><br>_____________</td>' \
                   f'</tr>' \
                   f'</table>' \
                   f'</body>' \
                   f'</html>'
    document = QtGui.QTextDocument()
    document.setHtml(flylist_page)
    document.print_(printer)


def gradelist_request(printer):
    figure = {2: currentmember.fig_2, 3: currentmember.fig_3, 4: currentmember.fig_4, 5: currentmember.fig_5,
              6: currentmember.fig_6, 7: currentmember.fig_7, 8: currentmember.fig_8, 9: currentmember.fig_9}
    grade = {1: currentmember.fly_grade_1, 2: currentmember.fly_grade_2, 3: currentmember.fly_grade_3,
             4: currentmember.fly_grade_4, 5: currentmember.fly_grade_5, 6: currentmember.fly_grade_6,
             7: currentmember.fly_grade_7, 8: currentmember.fly_grade_8, 9: currentmember.fly_grade_9,
             10: currentmember.fly_grade_10, 11: currentmember.fly_grade_11, 12: currentmember.fly_grade_12,
             13: currentmember.fly_grade_13}
    tour = tourcount()
    current_year = "{}".format(ui.dateEdit.date().toString('yyyy'))
    program = ''
    tour_list = []
    for k in range(13):
        tour_list.append(sum(grade.get(k + 1)[tour]) * fly_k[k])
    total = sum(tour_list)

    for i in range(2, 10):
        program = program + '<tr>'
        program = program + f'<td width="5%">{i}</td><td>{fly_tup[figure.get(i)[tour]]}</td><td>7</td>' \
                            f'<td>{grade.get(i)[tour][0]}</td><td>{grade.get(i)[tour][1]}</td>' \
                            f'<td>{grade.get(i)[tour][2]}</td><td>{sum(grade.get(i)[tour]) * fly_k[i - 1]}</td>'
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
                     f'{memberclass}' \
                     f'</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td colspan="5" align="center">{tournumber} тур</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td>Участник:</td>' \
                     f'<td align="center">{currentmember.surname}</td>' \
                     f'<td colspan="2" align="center">{currentmember.name}</td>' \
                     f'<td align="center">№ {currentmember.number}</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td colspan="2" align="center">Регион:</td>' \
                     f'<td colspan="3" align="center">{currentmember.region}</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td colspan="2" align="center">Прототип:</td>' \
                     f'<td colspan="3" align="center">{currentmember.prototype}</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td align="center">Масштаб</td>' \
                     f'<td align="center">{currentmember.scale}</td>' \
                     f'<td align="center">V max (км/ч)</td>' \
                     f'<td colspan="2" align="center">{currentmember.speed}</td>' \
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
                     f'<td>1</td><td>Взлет</td><td>11</td><td>{currentmember.fly_grade_1[tour][0]}</td>' \
                     f'<td>{currentmember.fly_grade_1[tour][1]}</td>' \
                     f'<td>{currentmember.fly_grade_1[tour][2]}</td>' \
                     f'<td>{sum(currentmember.fly_grade_1[tour]) * fly_k[0]}</td>' \
                     f'</tr>' \
                     f'{program}' \
                     f'<tr>' \
                     f'<td>10</td><td>Заход на посадку и приземление</td><td>11</td>' \
                     f'<td>{currentmember.fly_grade_10[tour][0]}</td>' \
                     f'<td>{currentmember.fly_grade_10[tour][1]}</td>' \
                     f'<td>{currentmember.fly_grade_10[tour][2]}</td>' \
                     f'<td>{sum(currentmember.fly_grade_10[tour]) * fly_k[9]}</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td>11a</td><td>Реализм полета a) презентация полета</td><td>4</td>' \
                     f'<td>{currentmember.fly_grade_11[tour][0]}</td>' \
                     f'<td>{currentmember.fly_grade_11[tour][1]}</td>' \
                     f'<td>{currentmember.fly_grade_11[tour][2]}</td>' \
                     f'<td>{sum(currentmember.fly_grade_11[tour]) * fly_k[10]}</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td>11b</td><td>b) скорость модели</td><td>9</td>' \
                     f'<td>{currentmember.fly_grade_12[tour][0]}</td>' \
                     f'<td>{currentmember.fly_grade_12[tour][1]}</td>' \
                     f'<td>{currentmember.fly_grade_12[tour][2]}</td>' \
                     f'<td>{sum(currentmember.fly_grade_12[tour]) * fly_k[11]}</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td>11c</td><td>c) плавность полета</td><td>9</td>' \
                     f'<td>{currentmember.fly_grade_13[tour][0]}</td>' \
                     f'<td>{currentmember.fly_grade_13[tour][1]}</td>' \
                     f'<td>{currentmember.fly_grade_13[tour][2]}</td>' \
                     f'<td>{sum(currentmember.fly_grade_13[tour]) * fly_k[12]}</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td colspan="3"></td>' \
                     f'<td colspan="3">Итоговая оценка:</td>' \
                     f'<td>{total}</td>' \
                     f'</tr>' \
                     f'</table>' \
                     f'<table width="100%" border="0" bordercolor="ffffff" cellspacing="0" cellpadding="5">' \
                     f'<tr>' \
                     f'<td><br><br><br>C1: {gradelistui.comboBox_9.currentText()}_______________</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td><br><br>C2: {gradelistui.comboBox_10.currentText()}_______________</td>' \
                     f'</tr>' \
                     f'<tr>' \
                     f'<td><br><br>C3: {gradelistui.comboBox_11.currentText()}_______________</td>' \
                     f'</tr>' \
                     f'</table>' \
                     f'</body>' \
                     f'</html>'
    document = QtGui.QTextDocument()
    document.setHtml(gradelist_page)
    document.print_(printer)


def static_f4h_request(printer):
    printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
    begin_date = "{}".format(ui.dateEdit.date().toString('dd.MM.yyyy'))
    end_date = "{}".format(ui.dateEdit_2.date().toString('dd.MM.yyyy'))

    total_1 = []
    total_2 = []
    total_3 = []
    default = ''
    for i in range(13):
        total_1.append(currentmember.stat_grade_1[i] * kh_tup[i])
        total_2.append(currentmember.stat_grade_2[i] * kh_tup[i])
        total_3.append(currentmember.stat_grade_3[i] * kh_tup[i])

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
                  f'{locate_data.locate} {begin_date} - {end_date} г.<br>' \
                  f'{memberclass}' \
                  f'</td>' \
                  f'<td>Участник:</td>' \
                  f'<td align="center">{currentmember.surname}</td>' \
                  f'<td colspan="2" align="center">{currentmember.name}</td>' \
                  f'<td align="center">№ {currentmember.number}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td colspan="2" align="center">Регион:</td>' \
                  f'<td colspan="3" align="center">{currentmember.region}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td colspan="2" align="center">Прототип:</td>' \
                  f'<td colspan="3" align="center">{currentmember.prototype}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">Масштаб</td>' \
                  f'<td align="center">{currentmember.scale}</td>' \
                  f'<td align="center">V max (км/ч)</td>' \
                  f'<td colspan="2" align="center">{currentmember.speed}</td>' \
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
                  f'{default if currentmember.stat_grade_1[0] == 0.0 else currentmember.stat_grade_1[0]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[0] * kh_tup[0], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[0] == 0.0 else currentmember.stat_grade_2[0]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[0] * kh_tup[0], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[0] == 0.0 else currentmember.stat_grade_3[0]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[0] * kh_tup[0], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) виды спереди и сзади</td>' \
                  f'<td align="center">5</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[1] == 0.0 else currentmember.stat_grade_1[1]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[1] * kh_tup[1], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[1] == 0.0 else currentmember.stat_grade_2[1]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[1] * kh_tup[1], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[1] == 0.0 else currentmember.stat_grade_3[1]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[1] * kh_tup[1], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">c) виды сверху и снизу</td>' \
                  f'<td align="center">5</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[2] == 0.0 else currentmember.stat_grade_1[2]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[2] * kh_tup[2], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[2] == 0.0 else currentmember.stat_grade_2[2]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[2] * kh_tup[2], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[2] == 0.0 else currentmember.stat_grade_3[2]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[2] * kh_tup[2], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" rowspan="2" width="3%">2</td>' \
                  f'<td align="center" rowspan="2">ОКРАСКА:</td>' \
                  f'<td align="center">a) точность</td>' \
                  f'<td align="center">3</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[3] == 0.0 else currentmember.stat_grade_1[3]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[3] * kh_tup[3], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[3] == 0.0 else currentmember.stat_grade_2[3]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[3] * kh_tup[3], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[3] == 0.0 else currentmember.stat_grade_3[3]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[3] * kh_tup[3], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) сложность</td>' \
                  f'<td align="center">2</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[4] == 0.0 else currentmember.stat_grade_1[4]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[4] * kh_tup[4], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[4] == 0.0 else currentmember.stat_grade_2[4]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[4] * kh_tup[4], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[4] == 0.0 else currentmember.stat_grade_3[4]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[4] * kh_tup[4], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" rowspan="2" width="3%">3</td>' \
                  f'<td align="center" rowspan="2">ОПОЗНАВАТЕЛЬНЫЕ ЗНАКИ:</td>' \
                  f'<td align="center">a) точность</td>' \
                  f'<td align="center">3</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[5] == 0.0 else currentmember.stat_grade_1[5]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[5] * kh_tup[5], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[5] == 0.0 else currentmember.stat_grade_2[5]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[5] * kh_tup[5], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[5] == 0.0 else currentmember.stat_grade_3[5]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[5] * kh_tup[5], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) сложность</td>' \
                  f'<td align="center">2</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[6] == 0.0 else currentmember.stat_grade_1[6]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[6] * kh_tup[6], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[6] == 0.0 else currentmember.stat_grade_2[6]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[6] * kh_tup[6], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[6] == 0.0 else currentmember.stat_grade_3[6]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[6] * kh_tup[6], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" width="3%">4</td>' \
                  f'<td align="center" colspan="2">РЕАЛИЗМ:</td>' \
                  f'<td align="center">4</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[7] == 0.0 else currentmember.stat_grade_1[7]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[7] * kh_tup[7], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[7] == 0.0 else currentmember.stat_grade_2[7]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[7] * kh_tup[7], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[7] == 0.0 else currentmember.stat_grade_3[7]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[7] * kh_tup[7], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" width="3%">5</td>' \
                  f'<td align="center" colspan="2">РАЗРАБОТКА, ПРОИСХОЖДЕНИЕ И ДИЗАЙН МОДЕЛИ:</td>' \
                  f'<td align="center">6</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[9] == 0.0 else currentmember.stat_grade_1[9]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[9] * kh_tup[9], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[9] == 0.0 else currentmember.stat_grade_2[9]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[9] * kh_tup[9], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[9] == 0.0 else currentmember.stat_grade_3[9]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[9] * kh_tup[9], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td colspan="4" rowspan="2"><br><br>' \
                  f'Бонус: {currentmember.bonus}<br>' \
                  f'Итоговые очки: {sum(total_1) + sum(total_2) + sum(total_3) + currentmember.bonus}</td>' \
                  f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_1)}</td>' \
                  f'<td align="center"><font size="2">сумма:</font>:</td><td align="center">{sum(total_2)}</td>' \
                  f'<td align="center"><font size="2">сумма:</font>:</td><td align="center">{sum(total_2)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                  f'{statui.comboBox_1.currentText()}' \
                  f'<br><br>_______________</td>' \
                  f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                  f'{statui.comboBox_2.currentText()}' \
                  f'<br><br>_______________</td>' \
                  f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                  f'{statui.comboBox_3.currentText()}' \
                  f'<br><br>_______________</td>' \
                  f'</tr>' \
                  f'</table>'\
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


def static_request(printer):
    printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
    begin_date = "{}".format(ui.dateEdit.date().toString('dd.MM.yyyy'))
    end_date = "{}".format(ui.dateEdit_2.date().toString('dd.MM.yyyy'))

    # program = ''
    default = ''
    total_1 = []
    total_2 = []
    total_3 = []
    for i in range(13):
        total_1.append(currentmember.stat_grade_1[i] * k_tup[i])
        total_2.append(currentmember.stat_grade_2[i] * k_tup[i])
        total_3.append(currentmember.stat_grade_3[i] * k_tup[i])

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
                  f'{locate_data.locate} {begin_date} - {end_date} г.<br>' \
                  f'{memberclass}' \
                  f'</td>' \
                  f'<td>Участник:</td>' \
                  f'<td align="center">{currentmember.surname}</td>' \
                  f'<td colspan="2" align="center">{currentmember.name}</td>' \
                  f'<td align="center">№ {currentmember.number}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td colspan="2" align="center">Регион:</td>' \
                  f'<td colspan="3" align="center">{currentmember.region}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td colspan="2" align="center">Прототип:</td>' \
                  f'<td colspan="3" align="center">{currentmember.prototype}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">Масштаб</td>' \
                  f'<td align="center">{currentmember.scale}</td>' \
                  f'<td align="center">V max (км/ч)</td>' \
                  f'<td colspan="2" align="center">{currentmember.speed}</td>' \
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
                  f'{default if currentmember.stat_grade_1[0] == 0.0 else round(currentmember.stat_grade_1[0], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[0] * k_tup[0], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[0] == 0.0 else round(currentmember.stat_grade_2[0], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[0] * k_tup[0], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[0] == 0.0 else round(currentmember.stat_grade_3[0], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[0] * k_tup[0], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) виды спереди и сзади</td>' \
                  f'<td align="center">13</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[1] == 0.0 else round(currentmember.stat_grade_1[1], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[1] * k_tup[1], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[1] == 0.0 else round(currentmember.stat_grade_2[1], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[1] * k_tup[1], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[1] == 0.0 else round(currentmember.stat_grade_3[1], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[1] * k_tup[1], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">c) виды сверху и снизу</td>' \
                  f'<td align="center">13</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[2] == 0.0 else round(currentmember.stat_grade_1[2], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[2] * k_tup[2], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[2] == 0.0 else round(currentmember.stat_grade_2[2], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[2] * k_tup[2], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[2] == 0.0 else round(currentmember.stat_grade_3[2], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[2] * k_tup[2], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" rowspan="2" width="3%">2</td>' \
                  f'<td align="center" rowspan="2">ОКРАСКА:</td>' \
                  f'<td align="center">a) точность</td>' \
                  f'<td align="center">3</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[3] == 0.0 else round(currentmember.stat_grade_1[3], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[3] * k_tup[3], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[3] == 0.0 else round(currentmember.stat_grade_2[3], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[3] * k_tup[3], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[3] == 0.0 else round(currentmember.stat_grade_3[3], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[3] * k_tup[3], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) сложность</td>' \
                  f'<td align="center">2</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[4] == 0.0 else round(currentmember.stat_grade_1[4], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[4] * k_tup[4], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[4] == 0.0 else round(currentmember.stat_grade_2[4], 1)}' \
                  f'</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[4] * k_tup[4], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[4] == 0.0 else currentmember.stat_grade_3[4]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[4] * k_tup[4], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" rowspan="2" width="3%">3</td>' \
                  f'<td align="center" rowspan="2">ОПОЗНАВАТЕЛЬНЫЕ ЗНАКИ:</td>' \
                  f'<td align="center">a) точность</td>' \
                  f'<td align="center">8</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[5] == 0.0 else currentmember.stat_grade_1[5]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[5] * k_tup[5], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[5] == 0.0 else currentmember.stat_grade_2[5]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[5] * k_tup[5], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[5] == 0.0 else currentmember.stat_grade_3[5]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[5] * k_tup[5], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) сложность</td>' \
                  f'<td align="center">3</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[6] == 0.0 else currentmember.stat_grade_1[6]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[6] * k_tup[6], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[6] == 0.0 else currentmember.stat_grade_2[6]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[6] * k_tup[6], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[6] == 0.0 else currentmember.stat_grade_3[6]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[6] * k_tup[6], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" rowspan="2" width="3%">4</td>' \
                  f'<td align="center" rowspan="2">ТЕКСТУРА ПОВЕРХНОСТИ И РЕАЛИЗМ:</td>' \
                  f'<td align="center">a) текстура поверхности</td>' \
                  f'<td align="center">7</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[7] == 0.0 else currentmember.stat_grade_1[7]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[7] * k_tup[7], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[7] == 0.0 else currentmember.stat_grade_2[7]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[7] * k_tup[7], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[7] == 0.0 else currentmember.stat_grade_3[7]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[7] * k_tup[7], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) соотв. текстуры масштабу</td>' \
                  f'<td align="center">7</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[8] == 0.0 else currentmember.stat_grade_1[8]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[8] * k_tup[8], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[8] == 0.0 else currentmember.stat_grade_2[8]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[8] * k_tup[8], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[8] == 0.0 else currentmember.stat_grade_3[8]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[8] * k_tup[8], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" rowspan="2" width="3%">5</td>' \
                  f'<td align="center" rowspan="2">МАСТЕРСТВО ИЗГОТОВЛЕНИЯ:</td>' \
                  f'<td align="center">a) качество</td>' \
                  f'<td align="center">12</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[9] == 0.0 else currentmember.stat_grade_1[9]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[9] * k_tup[9], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[9] == 0.0 else currentmember.stat_grade_2[9]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[9] * k_tup[9], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[9] == 0.0 else currentmember.stat_grade_3[9]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[9] * k_tup[9], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) сложность</td>' \
                  f'<td align="center">5</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[10] == 0.0 else currentmember.stat_grade_1[10]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[10] * k_tup[10], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[10] == 0.0 else currentmember.stat_grade_2[10]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[10] * k_tup[10], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[10] == 0.0 else currentmember.stat_grade_3[10]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[10] * k_tup[10], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center" rowspan="2" width="3%">6</td>' \
                  f'<td align="center" rowspan="2">МАСШТАБНОСТЬ ДЕТАЛЕЙ:</td>' \
                  f'<td align="center">a) точность</td>' \
                  f'<td align="center">9</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[11] == 0.0 else currentmember.stat_grade_1[11]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[11] * k_tup[11], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[11] == 0.0 else currentmember.stat_grade_2[11]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[11] * k_tup[11], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[11] == 0.0 else currentmember.stat_grade_3[11]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[11] * k_tup[11], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center">b) сложность</td>' \
                  f'<td align="center">5</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_1[12] == 0.0 else currentmember.stat_grade_1[12]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_1[12] * k_tup[12], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_2[12] == 0.0 else currentmember.stat_grade_2[12]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_2[12] * k_tup[12], 1)}</td>' \
                  f'<td align="center">' \
                  f'{default if currentmember.stat_grade_3[12] == 0.0 else currentmember.stat_grade_3[12]}</td>' \
                  f'<td align="center">{round(currentmember.stat_grade_3[12] * k_tup[12], 1)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td colspan="4" rowspan="2"><br><br>' \
                  f'Коэффициент статической оценки: {currentmember.static_k}<br>' \
                  f'Итоговые очки: {sum(total_1) + sum(total_2) + sum(total_3)}</td>' \
                  f'<td align="center"><font size="2">сумма:</font></td><td align="center">{sum(total_1)}</td>' \
                  f'<td align="center"><font size="2">сумма:</font>:</td><td align="center">{sum(total_2)}</td>' \
                  f'<td align="center"><font size="2">сумма:</font>:</td><td align="center">{sum(total_2)}</td>' \
                  f'</tr>' \
                  f'<tr>' \
                  f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                  f'{statui.comboBox_1.currentText()}' \
                  f'<br><br>_______________</td>' \
                  f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                  f'{statui.comboBox_2.currentText()}' \
                  f'<br><br>_______________</td>' \
                  f'<td align="center"><font size="2">судья:</font></td><td align="center">' \
                  f'{statui.comboBox_3.currentText()}' \
                  f'<br><br>_______________</td>' \
                  f'</tr>' \
                  f'</table>'\
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


def flyui_action(btn):
    if btn.text() in ['OK', '&OK', 'Apply', '&Apply']:
        set_prog()


set_start_date()
set_end_date()


ui.pushButton.clicked.connect(get_data)
ui.pushButton_2.clicked.connect(qwestion)
ui.f4c_btn_2.clicked.connect(get_prog)
ui.f4c_btn.clicked.connect(get_info)
ui.f4c_btn_4.clicked.connect(get_static)
ui.f4c_btn_5.clicked.connect(tour_1_out)
ui.f4c_btn_6.clicked.connect(tour_2_out)
ui.f4c_btn_7.clicked.connect(lambda: handlePreview(tour_3_request))


for ref_item in range(10):
    exec(f'ui.lineEdit_{str(ref_item)}_0.textChanged.connect'
         f'(lambda: set_surname(ui.lineEdit_{str(ref_item)}_0.text(), {str(ref_item)}))')
    exec(f'ui.lineEdit_{str(ref_item)}_1.textChanged.connect'
         f'(lambda: set_name(ui.lineEdit_{str(ref_item)}_1.text(), {str(ref_item)}))')
    exec(f'ui.lineEdit_{str(ref_item)}_2.textChanged.connect'
         f'(lambda: set_patronymic(ui.lineEdit_{str(ref_item)}_2.text(), {str(ref_item)}))')


ui.lineEdit_25.textChanged.connect(set_locate)
ui.lineEdit_26.textChanged.connect(set_ekp_f4c)
ui.lineEdit_27.textChanged.connect(set_ekp_f4cu)
ui.dateEdit.dateChanged.connect(set_start_date)
ui.dateEdit_2.dateChanged.connect(set_end_date)
ui.action.triggered.connect(save_)
ui.action_2.triggered.connect(filein)
ui.action_3.triggered.connect(save_as)

ui.tabWidget.currentChanged.connect(change_tab)

f4cui.buttonBox.accepted.connect(new_member)

flyui.radioButton.clicked.connect(get_prog)
flyui.radioButton_1.clicked.connect(get_prog)
flyui.radioButton_2.clicked.connect(get_prog)
flyui.radioButton_3.clicked.connect(get_prog)
flyui.pushButton.clicked.connect(fly_list)
flyui.pushButton_2.clicked.connect(grade_list)
flyui.buttonBox.clicked.connect(flyui_action)

infoui.buttonBox.accepted.connect(set_info)

tui.pushButton.clicked.connect(lambda: handlePreview(tour_1_request))
tIIui.pushButton.clicked.connect(lambda: handlePreview(tour_2_request))

gradelistui.pushButton.clicked.connect(lambda: handlePreview(gradelist_request))
gradelistui.buttonBox.clicked.connect(gradelist_action)
gradelistui.radioButton_1.clicked.connect(grade_list)
gradelistui.radioButton_2.clicked.connect(grade_list)
gradelistui.radioButton_3.clicked.connect(grade_list)

flylistui.pushButton.clicked.connect(lambda: handlePreview(flylist_request))

statui.pushButton.clicked.connect(lambda: handlePreview(static_f4h_request if memberclass == 'F-4H'
                                                        else static_request))
statui.buttonBox.clicked.connect(static_action)

MainWindow.show()
sys.exit(app.exec_())
