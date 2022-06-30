

class Constant:
    ts_address = "http://139.196.152.44:32677"
    admin_username = "admin"
    admin_pwd = "222222"

    init_stations_data = [
        ("fengtai", "Feng Tai", 7),
        ("zhengding", "Zheng Ding", 3),
        ("zhengzhoukonggang", "Zheng Zhou Kong Gang", 5),
        ("xiangyangdong", "Xiang Yang Dong", 3),
        ("wanzhou", "Wan Zhou", 2),
        ("chongqingbei", "Chong Qing Bei", 5),
        ("chengdudong", "Cheng Du Dong", 5),
    ]
    station_list_example1 = "fengtai,zhengding,zhengzhoukonggang,xiangyangdong,chongqingbei,chengdudong"
    distance_list_example1 = "0,150,360,500,1100,1400"
    init_route_data = [
        (station_list_example1, distance_list_example1, "fengtai", "chengdudong")
    ]
    train_types = [
        "GaoTieOne","GaoTieTwo","DongCheOne","ZhiDa","TeKuai","KuaiSu","ManSu"
    ]
    init_train_types_id = [
        "G8001", "G8002", "D8003", "Z8004", "T8005", "K8006", "M8007"
    ]
    travel_start_time = "1367929200000"

    init_user = {
            "document_type": "1",
            "document_num": "5599488099312X",
            "email": "ts@fd1.edu.cn",
            "password": "111111",
            "username": "chair1",
            "gender": "1"
    }

    init_user_contacts = [
        {
            "contact_name": "Contacts_111",
            "document_type": 1,
            "document_number": "5135488099312X",
            "phone_number": "19921940977",
        },
        {
            "contact_name": "Contacts_222",
            "document_type": 1,
            "document_number": "5235488099312X",
            "phone_number": "18921940977",
        },
        {
            "contact_name": "Contacts_333",
            "document_type": 1,
            "document_number": "5335488099312X",
            "phone_number": "17921940977",
        }
    ]


