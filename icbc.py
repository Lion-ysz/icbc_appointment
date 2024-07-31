import requests


headers = {
    'Content-type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}


class Location:
    def __init__(self, pos_id, exam_type, exam_date, prf_days_of_week, prf_part_of_day):
        self.pos_id = pos_id
        self.exam_type = exam_type
        self.exam_date = exam_date
        self.prf_days_of_week = prf_days_of_week
        self.prf_part_of_day = prf_part_of_day


class AvailableAppointment:
    def __init__(self, date, time, day_of_week):
        self.date = date
        self.time = time
        self.day_of_week = day_of_week

    def __str__(self):
        return f'{self.date} - {self.time} - {self.day_of_week}'


class ICBC:

    def __init__(self, keyword, last_name, licence_num):
        self.keyword = keyword
        self.last_name = last_name
        self.licence_num = licence_num
        self.token = ""

    def login(self):
        url = "https://onlinebusiness.icbc.com/deas-api/v1/webLogin/webLogin"
        payload = {
            "drvrLastName": self.last_name,
            "licenceNumber": self.licence_num,
            "keyword": self.keyword
        }
        response = requests.put(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise RuntimeError("login failed: " + str(response.status_code))
        self.token = response.headers["Authorization"]
        print("login success, token: " + self.token)

    def get_available_appointments(self, location: Location):
        if self.token == "":
            self.login()

        appointment_url = "https://onlinebusiness.icbc.com/deas-api/v1/web/getAvailableAppointments"
        headers["Authorization"] = self.token
        point_grey = {
            "aPosID": location.pos_id,
            "examType": location.exam_type,
            "examDate": location.exam_date,
            "ignoreReserveTime": "false",
            "prfDaysOfWeek": location.prf_days_of_week,
            "prfPartsOfDay": location.prf_part_of_day,
            "lastName": self.last_name,
            "licenseNumber": self.licence_num
        }
        response = requests.post(appointment_url, json=point_grey, headers=headers)

        if response.status_code != 200:
            raise RuntimeError("get available failed: " + str(response.status_code))
        ret = []
        for a in response.json():
            date = a["appointmentDt"]['date']
            startTm = a["startTm"]
            day_of_week = a["appointmentDt"]['dayOfWeek']
            ret.append(AvailableAppointment(date, startTm, day_of_week))
        return ret


    def make_appointment(self, appointment):
        if self.token == "":
            self.login()
        pass
