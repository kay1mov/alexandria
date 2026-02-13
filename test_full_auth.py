import requests, time, random, os
from datetime import datetime, timedelta

class Auth:

    def __init__(self,
                 fcm_token: str = "ejxZuDinQ_eHYo9QJwtstt:APA91bF_BCHKMkT-kCd1IWB6AgJ0xe6SvuxQepExq2JmILTsLaofc2zzaoZVd1lZ70d4ataYM9axkzw-OGBcFPhz7zLSVE-nsdPR2stLuSQbPLodqLLXENw",
                 accept: str = "application/json",
                 accept_encoding: str = "gzip",
                 accept_language: str = "en",
                 app_version_code: str = "333",
                 app_version_name: str ="2.0.38",
                 authorization: str = "Bearer 27498|k1Y4q5z5OYZIGZOo9ypfBtJ43Wb6KZ6jYvIPUEyUab9da1a3",
                 device: str = "samsung SM-S721B s5e9945 Physical Device",
                 host: str = "",
                 is_desktop: str = "false",
                 os_type: str = "android",
                 os_version: str = "BP2A.250605.031.A3.S721BXXS8CYL1",
                 sentry_trace: str = "c728060f51f341ad90378d1ade9732e2-e22ed74c92d64ea6",
                 user_agent: str = "Dart/3.9 (dart:io)"):

        self.fcm_token = fcm_token
        self.accept = accept
        self.accept_encoding = accept_encoding
        self.accept_language = accept_language
        self.app_version_code = app_version_code
        self.app_version_name = app_version_name
        self.authorization = authorization
        self.device = device
        self.host = host
        self.is_desktop = is_desktop
        self.os_type = os_type
        self.os_version = os_version
        self.sentry_trace = sentry_trace
        self.user_agent = user_agent

        self.base_headers = {
            "accept": self.accept,
            "accept-encoding": self.accept_encoding,
            "accept-language": self.accept_language,
            "app-version-code": self.app_version_code,
            "app-version-name": self.app_version_name,
            "authorization": self.authorization,
            "device": self.device,
            "host": self.host, #REQUIRED
            "is_desktop": self.is_desktop,
            "os-type": self.os_type,
            "os-version": self.os_version,
            "sentry-trace": self.sentry_trace,
            "user-agent": self.user_agent
        }

        self.data = {}


    def build_headers(self, host: str):
        trace_id = os.urandom(16).hex()
        span_id = os.urandom(8).hex()
        sampled = "1"

        h = self.base_headers.copy()
        h["host"] = host
        h["sentry-trace"] = f"{trace_id}-{span_id}-{sampled}"
        return h

    def step_1_get_token(self, url = "https://test-cbchat.cambridgeonline.uz/api/v1/students/get-token"):

        response = requests.get(url, headers=self.build_headers("test-cbchat.cambridgeonline.uz"))
        if response.status_code == 200:
            return response.json()

        return None

    def step_2_get_config(self, url = "https://student-api.cambridgeonline.uz/v1/student/app/config"):
        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"))

        if response.status_code == 200:
            return response.json()

        return None

    def step_3_auth2(self, url = "https://student-api.cambridgeonline.uz/v1/auth2/me"):

        response = requests.post(url, headers=self.build_headers("student-api.cambridgeonline.uz"), json={"fcm_token": self.fcm_token})
        if response.status_code == 200:
            return response.json()

        return None

    def survey_status(self, url = "https://student-api.cambridgeonline.uz/v1/get-survey"):
        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"))
        if response.status_code == 200:
            return response.json()

        return None

    def get_active_group(self, url = "https://student-api.cambridgeonline.uz/v1/student/active_group"):
        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"))

        if response.status_code == 200:
            return response.json()

        return None

    def get_user_finger_point(self, url = "https://student-api.cambridgeonline.uz/v1/verification"):

        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"))
        if response.status_code == 200:
            return response.json()
        return None

    def get_progress(self, url = "https://student-api.cambridgeonline.uz/v1/new-progress/ielts"):

        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"))
        if response.status_code == 200:
            return response.json()
        return None

    def get_group_performance(self, url = "https://student-api.cambridgeonline.uz/v1/new-progress/ielts/today/group-performance"):
        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"))
        if response.status_code == 200:
            return response.json()
        return None

    def get_homework_today_days(self, url = "https://student-api.cambridgeonline.uz/v1/today/days"):
        today = datetime.today()
        date_from = today - timedelta(days=4)
        date_to = today + timedelta(days=2)

        string_format_from = date_from.strftime("%Y-%m-%d")
        string_format_to = date_to.strftime("%Y-%m-%d")

        date = {
            'from': string_format_from,
            'to': string_format_to,
        }

        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"), json=date)
        if response.status_code == 200:
            return response.json()
        return None

    def get_homework(self, homework_type, homework_subtype, homework_info):

        available_homework_types = [
            "extra_task",
            "homework"
        ]

        available_homework_subtypes = [
            "reading",
            "listening",
            "grammar",
            "vocabulary",
            "speaking",
            "writing"
        ]

        if homework_type.lower() not in available_homework_types:
            print(f"Error in homework_type: {homework_type}")
            return None

        if homework_subtype.lower() not in available_homework_subtypes:
            print(f"Error in homework_subtype: {homework_subtype}")
            return None

        url = "https://student-api.cambridgeonline.uz/v1/"
        url += homework_type + "/" + homework_subtype + "/" + "start"

        response = requests.get(url, headers=self.build_headers("student-api.cambridgeonline.uz"), json=homework_info)
        if response.status_code == 200:
            return response.json()
        return None

    def _collect(self, _: list):

        results = []

        for elem in _:

            try:
                r = elem()
                results.append(r)
            except Exception as e:
                print(f"Error in {elem.__name__}: {e}")
                results.append(None)

            time.sleep(random.uniform(0.1, 0.17))

        return results


    def collect_data(self):

        tokens = self.step_1_get_token
        config = self.step_2_get_config
        user_info = self.step_3_auth2
        active_group = self.get_active_group
        user_finger_point = self.get_user_finger_point

        _ = [tokens, config, user_info, active_group, user_finger_point]
        token, config, user_info, active_group, user_finger_point = self._collect(_)

        if token is None:
            print("Token request failed")
            return None

        if config is None:
            print("Creating last config data example because config is None:")
            print(config.status_code)
            config = {
                "minimal_required_android_app_build": int(self.app_version_code),
                "minimal_required_ios_app_build": int(self.app_version_code),
                "current_android_app_build": int(self.app_version_code),
                "current_ios_app_build": int(self.app_version_code),
                "base_url": "https:\/\/student-api.cambridgeonline.uz\/v1",
                "base_socket_url": "https:\/\/test-cbchat.cambridgeonline.uz"
            }


        if user_info is None:
            print("No user info:")
            print(user_info.status_code)
            return None

        self.data["token"] = token
        self.data["config"] = config
        self.data["user_info"] = user_info
        self.data["active_group"] = active_group
        self.data["user_finger_point"] = user_finger_point

        return self.data



"""

One of received responses through collect_data function

token {'connection_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyNjc4OTIifQ.OeB7Btjsw-gWt6WNlSK5Ai855Wk-Ue5d2Uz0IL-U_fQ', 'sub_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaGFubmVsIjoiZ3JvdXA6MTgyMzMiLCJzdWIiOiIyNjc4OTIifQ.2wm4H84vc0K9TP9YVe2Vkd8xra9yIw3sijIce1uYLpo', 'supervisor_sub_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaGFubmVsIjoic3VwZXJ2aXNvci1zdHVkZW50LWNoYXQ6MjY3ODkyIiwic3ViIjoiMjY3ODkyIn0.WaB8X9IIdNZjSpE56YBtz5k1eZJwyS2pBedv5sVX5-A'}
config {'success': True, 'message': 'success', 'error_code': -1, 'data': {'minimal_required_android_app_build': 333, 'minimal_required_ios_app_build': 333, 'current_android_app_build': 333, 'current_ios_app_build': 333, 'base_url': 'https://student-api.cambridgeonline.uz/v1', 'base_socket_url': 'https://test-cbchat.cambridgeonline.uz'}}
user_info {'success': True, 'message': 'Success', 'error_code': -1, 'data': {'id': 267892, 'phone': '915327838', 'receive_notification': 1, 'show_mini_translator': 1, 'is_test_user': False, 'created_at': '2025-09-20T15:49:55.000000Z', 'updated_at': '2026-01-25T21:04:36.000000Z', 'deleted_at': None, 'lang': 1, 'account_type': None, 'student_info': {'id': 266617, 'name': 'Umarbek', 'surname': 'Kayimov', 'gender': 'm', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/266617/APMG8QuTCFjd4t0HtRV6a3XmJzuxICaf9nQnQCHO.jpg', 'phone': '915327838', 'mock_exam_photo': 'https://student-api.cambridgeonline.uz/storage/mock-avatars/266617/L6dSQ4ivvh1MZiyLfn8B8t68NBo2iugaJJxkD1IZ.jpg', 'date_of_birth': '2009-12-12', 'balance': 0, 'points': 3381, 'coins': 275, 'points_for_exchange': 131, 'date_of_payment': '2025-10-01', 'payment_sum': 930000, 'oferta_file': 'https://student-api.cambridgeonline.uz/ofertas/v2/oferta_cb_group.pdf', 'oferta': 1, 'oferta_time': '2025-09-27 20:22:01', 'active_group': [{'id': 18233, 'days': 'tts', 'exact_days': [], 'time': '17:00:00', 'all_week': None, 'level': {'id': 6, 'name': 'IELTS L2', 'is_ielts': True, 'course_id': 2}, 'teacher': {'id': 2289, 'user_id': 256803, 'name': "Umerov Javohir Jamol o'g'li", 'nickname': 'Mr.Javokhir'}, 'branch': {'id': 40, 'name': 'Samarkand'}, 'current_week': {'id': 430852, 'week_num': 8, 'date': '2026-02-12', 'week_day_num': 2, 'is_done': 1}}], 'strikes': 0, 'is_debtor': False, 'payment_link': 'https://cambridgeonline.uz/online-pay?phone=915327838', 'last_certificate': 'Intermediate C', 'progress_type': 'new', 'is_verified': True}}}
active_group {'data': {'id': 18233, 'days': 'tts', 'exact_days': [], 'time': '17:00:00', 'level': {'id': 6, 'name': 'IELTS L2', 'is_ielts': True, 'course_id': 2}, 'next_level': 'IELTS L3', 'current_unit': '8.2', 'week': 8, 'completeness': 62, 'teacher': {'id': 2289, 'user_id': 256803, 'name': "Umerov Javohir Jamol o'g'li", 'nickname': 'Mr.Javokhir'}, 'support': {'id': 2266, 'user_id': 255047, 'name': 'Umirzoqova Nafisa', 'nickname': 'Ms.Nafisa'}, 'branch': {'id': 40, 'name': 'Samarkand'}, 'students': [{'id': 252242, 'user_id': 253593, 'name': 'Muqaddas', 'surname': 'Doniyorova', 'gender': 'f', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/252242/htRir3BHrNqmaVhRiLsbuXeWyzHz97w5gfbcJwGD.jpg'}, {'id': 274154, 'user_id': 275034, 'name': 'Mushtariy', 'surname': 'Abduxononova', 'gender': 'f', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/274154/gZqnKzJUOS4X0NCzgWibE31J55Y3Z6b3q1vbWkDU.jpg'}, {'id': 270164, 'user_id': 271257, 'name': 'Gulsevar', 'surname': 'Sherkulova', 'gender': 'm', 'photo': None}, {'id': 269235, 'user_id': 270343, 'name': 'Xursandbek', 'surname': 'Xursandov', 'gender': 'm', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/269235/Ebxg5XjgNP4BbyMb0OxvHxTCJV3UOZPxlIZqok8f.jpg'}, {'id': 270352, 'user_id': 271442, 'name': 'Azizjon', 'surname': 'Boliboyev', 'gender': 'm', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/270352/NDMwpQLeiprrBaFozGphOS368zOf58vSrKH9fVJb.jpg'}, {'id': 263850, 'user_id': 265158, 'name': 'Shahlo', 'surname': 'Rashidova', 'gender': 'f', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/263850/YY20sBnPdZjg8XMvIpVHVnPvRv11fHUskc4e8AME.jpg'}, {'id': 272491, 'user_id': 273472, 'name': 'Nigora', 'surname': 'Odilova', 'gender': 'f', 'photo': None}, {'id': 272273, 'user_id': 273278, 'name': 'Munojot', 'surname': 'Ziyoyeva', 'gender': 'f', 'photo': None}, {'id': 253991, 'user_id': 255356, 'name': 'Farzona', 'surname': 'Raxmatullayeva', 'gender': 'f', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/253991/OfhlzPLz0Pe0AgABwp2himkDvpNVHYWKzeeKxrW9.jpg'}, {'id': 268540, 'user_id': 269671, 'name': 'Doston', 'surname': 'Keldibekov', 'gender': 'm', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/268540/t4VvfNm2EZawYwEnsdfT5U2xBAvhzwUqO5Ikv0ys.jpg'}, {'id': 266617, 'user_id': 267892, 'name': 'Umarbek', 'surname': 'Kayimov', 'gender': 'm', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/266617/APMG8QuTCFjd4t0HtRV6a3XmJzuxICaf9nQnQCHO.jpg'}, {'id': 265967, 'user_id': 267246, 'name': 'Amina', 'surname': 'Komilova', 'gender': 'f', 'photo': 'https://student-api.cambridgeonline.uz/storage/student-avatars/265967/3EsRoLeTvsh7xLk12cm2ZUXMqwo8EvWvEDSguMak.jpg'}], 'current_week': {'id': 430852, 'week_num': 8, 'date': '2026-02-12', 'week_day_num': 2, 'is_done': 1}}}
user_finger_point {'success': True, 'message': '', 'error_code': -1, 'data': {'is_verified': True, 'face_data': [-0.0058807270670158986, 0.016483376640376607, 0.002466248427839348, -0.0035306897613032167, -0.0182011265166425, -0.0856291002436792, 0.024137566227930365, -0.08960268089346399, -0.028589509512551833, -0.0198568912914864, 0.02370524445302965, 0.003725196236086977, 0.00544787676658695, 0.01170164553333135, -0.0008979602158528746, -0.22890476949287977, -0.020153983174316135, 0.0019875104700284394, 0.003121223106623763, -0.00023606713499352503, 0.10660052381735996, 0.005059529246957618, -0.22126226241497557, 0.0028137285841130333, 0.2316740011169589, 0.007311573728784839, -0.017362116687790925, -0.1264417092859246, -0.12551756912846582, 0.05407555437622848, 0.007183161117536157, 0.30661855221648066, 0.14153038575405072, -1.963009950302697e-05, 0.151412179592287, -0.05319508951951322, -0.04269769149773319, 0.02110203410606887, -0.0022964515692382457, 0.03523740325815796, -0.002518811106529181, -8.139519417034097e-05, -0.004012188159053647, 0.02381841317732486, -0.008856669448968372, 0.03294726628841362, -0.20258213810154, 0.09037051533029868, -0.004981978486652631, 0.0655624900225905, 0.09223819695588432, -0.0009465931209758024, -0.1276585529345144, -0.004500532708624395, 0.0905748400398842, 0.009049092788112886, -0.13265866706453489, 0.00119718913461251, -0.01196809224874882, 0.001664418507253833, -0.05354906285637339, -0.029829908170234194, -0.05753953024603112, -0.024932429506844964, -0.006078917155183867, 0.1784100272588199, -0.0010037530986463908, 0.012978854713486582, 0.0030477343094753974, -0.0014030569291929012, -0.005331650044808129, -0.17436616528663432, 0.07701886711453432, 0.0050462225108388985, -0.1230770794516242, 0.0013073145297537502, -0.00012179214506760818, 0.002645084935618244, 0.03416698213564494, 0.02069898193522324, 0.010361580465201003, 0.18054502079844104, -0.004200765601865417, -0.00163363433995595, 0.14808950397471923, 0.005803008668657905, -0.0022111079677747084, 0.02189092947029641, 0.017893601958980605, 0.012667017201249816, 0.2194821251059605, -0.004043282689580223, -0.009569012896290087, -0.00014829896632496817, -0.13507433885895126, 0.0485055416464942, 0.02468873965712325, 0.038475984177757085, 0.0005584945554967171, 0.028296390651578372, -0.0038325691075300873, 0.00030574730326172946, 0.00373478769385592, 0.00021544532616732623, 0.0032075189853606346, 0.0016324719330397845, 0.01782281399713069, 0.0066082655068589605, 0.014797947380730534, 0.004496719408579736, -0.12926926405129005, 0.003931839705908471, 0.01574924304013148, -0.09278094936688112, 0.010093195667626264, -0.12145019312537836, -0.000603417711997312, -0.03950060285889842, 0.298207890326796, -0.0030431582562895545, 0.11156197688706689, -0.018046292285594824, 0.023495849623663172, -0.0032656253613311697, 0.0005272843663550973, 0.00836063496937717, -0.004273288151902699, -0.0014951356222666391, 0.011594276154347678, -0.03403840002369822, 0.0031306303953650273, 0.01025981485380036, 0.005433409136951155, 0.05683860946937682, -0.027255401183238347, -0.001321754918205931, -0.0862160122431282, -0.0380868701796965, 0.001442129401228224, 0.008251816452557499, 0.00836188759816214, -0.002750031246244073, -0.00026644994594245033, 0.08785896202014222, 0.051381614589690046, 0.06714368939145672, 0.004998578844851686, 0.0031509979531441647, 0.00020072136456072208, 0.00020912691407186655, -0.001495775790081561, -0.1485348102481479, 0.01820877267450467, -0.012382891190497684, -0.002409861040404026, 0.001026763051236057, -0.006511146729155429, 0.002851328635249442, -0.0943378374927712, -0.005475559862734826, -0.01748559887763616, -0.002997129270715684, 0.0020916318617350944, -0.002502424021186452, 0.003925931395862478, 0.006607117651857118, 0.007281509240961741, 0.04857916455408497, -0.005186661289745827, 0.00244333230599324, -0.11138998769526144, -0.005614132271318272, 0.006311321704309382, -0.06394268919805178, 0.050171659002433824, 0.0002655085243972021, -0.05102767105515041, 0.012925243132812307, -0.0035425911317442235, -0.00023245273051384, -0.06574067809706714, -0.08512490458487408, -0.0030346876451694694, -0.0038964780884409695, 0.024946894808174466, -0.09311597960375148, -0.05340401123704121, 0.050551429973006795, 0.2285954363068904, -0.0013711786907685155, -0.022753905952792936, -0.010915719225287078], 'home_address': 'MRVH+Q37', 'home_address_latitude': 39.6935387, 'home_address_longitude': 66.8254703, 'study_work_address': 'MRVH+74C', 'study_work_address_latitude': 39.69373913, 'study_work_address_longitude': 66.82748641, 'instagram_account': None, 'has_instagram_account': False, 'telegram_account': 'kay1mov', 'telegram_account_phone_number': None, 'can_set_home_address': False, 'can_set_work_address': True, 'home_address_title': 'Available from 20:30 to 07:30', 'home_address_text': "We only allow filling in your home address at night to make sure you're actually at home. Don't worry—the app will detect your location for you!", 'work_address_title': 'Available Monday to Saturday, 07:30 to 20:30', 'work_address_text': "You can fill in your study or work address only on weekdays during the day—this helps us make sure you're not at home. Don't worry, the app will detect your location automatically!"}}

"""

auth = Auth()
#active_group = auth.get_active_group()
#level = active_group.get("data", None).get("level", None).get("id", None)

homework_info = {
    "level_id": 6,
    "unit": 8,
    "subunit": 2,
    "day": 4,
    "date": "2026-02-13",
    "from": None,
    "to": None,
    "book_type": None
}

result = auth.get_homework("extra_task", "reading", homework_info)
print(result)