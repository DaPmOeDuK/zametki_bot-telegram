import s_taper as s_t
from s_taper.consts import *

users_sheme = {
    "user_id": INT + KEY,
    "name": TEXT
}

users = s_t.Taper("users", "data.db").create_table(users_sheme)

zametki_sheme = {
    "user_id": INT + KEY,
    "completed": TEXT,
    "uncompleted": TEXT
}

zametki = s_t.Taper("zametki", "data.db").create_table(zametki_sheme)