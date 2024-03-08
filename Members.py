class Member:
    propertys = []

    def __init__(self, cls):
        self.cls = cls
        self.number = ''
        self.surname = ''
        self.name = ''
        self.region = ''
        self.prototype = ''
        self.scale = ''
        self.speed = 0
        self.count = 0
        self.tour_1 = 0
        self.tour_2 = 0
        self.tour_3 = 0
        self.static = 0
        self.fig_2 = 0
        self.fig_3 = 0
        self.fig_4 = 0
        self.fig_5 = 0
        self.fig_6 = 0
        self.fig_7 = 0
        self.fig_8 = 0
        self.fig_9 = 0
        self.grade_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.grade_2 = ""
        self.grade_3 = ""
        self.fly_grade_1_1 = ""
        self.fly_grade_1_2 = ""
        self.fly_grade_1_3 = ""
        self.fly_grade_2_1 = ""
        self.fly_grade_2_2 = ""
        self.fly_grade_2_3 = ""
        self.fly_grade_3_1 = ""
        self.fly_grade_3_2 = ""
        self.fly_grade_3_3 = ""
        self.set_grade()

    def set_grade(self):
        data = []
        for i in range(13):
            data.append(0)
        self.grade_1 = data
        self.grade_2 = data
        self.grade_3 = data
        self.fly_grade_1_1 = data
        self.fly_grade_1_2 = data
        self.fly_grade_1_3 = data
        self.fly_grade_2_1 = data
        self.fly_grade_2_2 = data
        self.fly_grade_2_3 = data
        self.fly_grade_3_1 = data
        self.fly_grade_3_2 = data
        self.fly_grade_3_3 = data

    def set_propertys(self):
        self.propertys.clear()
        self.propertys.append(self.cls)
        self.propertys.append(self.number)
        self.propertys.append(self.surname)
        self.propertys.append(self.name)
        self.propertys.append(self.region)
        self.propertys.append(self.prototype)
        self.propertys.append(self.scale)
        self.propertys.append(self.speed)
        self.propertys.append(self.count)
        self.propertys.append(self.tour_1)
        self.propertys.append(self.tour_2)
        self.propertys.append(self.tour_3)
        self.propertys.append(self.static)
        self.propertys.append(self.fig_2)
        self.propertys.append(self.fig_3)
        self.propertys.append(self.fig_4)
        self.propertys.append(self.fig_5)
        self.propertys.append(self.fig_6)
        self.propertys.append(self.fig_7)
        self.propertys.append(self.fig_8)
        self.propertys.append(self.fig_9)
        for i in self.grade_1:
            self.propertys.append(i)
        for j in self.grade_2:
            self.propertys.append(j)
        for k in self.grade_3:
            self.propertys.append(k)
        for l in self.fly_grade_1_1:
            self.propertys.append(l)
        for m in self.fly_grade_1_2:
            self.propertys.append(m)
        for o in self.fly_grade_1_3:
            self.propertys.append(o)
        for p in self.fly_grade_2_1:
            self.propertys.append(p)
        for r in self.fly_grade_2_2:
            self.propertys.append(r)
        for s in self.fly_grade_2_3:
            self.propertys.append(s)
        for t in self.fly_grade_3_1:
            self.propertys.append(t)
        for u in self.fly_grade_3_2:
            self.propertys.append(u)
        for v in self.fly_grade_3_3:
            self.propertys.append(v)

    def get_data(self):
        self.cls = self.propertys[0]
        self.number = self.propertys[1]
        self.surname = self.propertys[2]
        self.name = self.propertys[3]
        self.region = self.propertys[4]
        self.prototype = self.propertys[5]
        self.scale = self.propertys[6]
        self.speed = self.propertys[7]
        self.count = self.propertys[8]
        self.tour_1 = self.propertys[9]
        self.tour_2 = self.propertys[10]
        self.tour_3 = self.propertys[11]
        self.static = self.propertys[12]
        self.fig_2 = self.propertys[13]
        self.fig_3 = self.propertys[14]
        self.fig_4 = self.propertys[15]
        self.fig_5 = self.propertys[16]
        self.fig_6 = self.propertys[17]
        self.fig_7 = self.propertys[19]
        self.fig_8 = self.propertys[19]
        self.fig_9 = self.propertys[20]
        data_1 = []
        data_2 = []
        data_3 = []
        data_4 = []
        data_5 = []
        data_6 = []
        for i in range(21, 34):
            data_1.append(self.propertys[i])
        for j in range(34, 47):
            data_2.append(self.propertys[j])
        for k in range(47, 60):
            data_3.append(self.propertys[k])
        for l in range(60, 73):
            data_4.append(self.propertys[l])
        for m in range(73, 86):
            data_5.append(self.propertys[m])
        for n in range(86, 99):
            data_6.append(self.propertys[n])
        self.grade_1 = data_1
        self.grade_2 = data_2
        self.grade_3 = data_3
        self.grade_4 = data_4
        self.grade_5 = data_5
        self.grade_6 = data_6
