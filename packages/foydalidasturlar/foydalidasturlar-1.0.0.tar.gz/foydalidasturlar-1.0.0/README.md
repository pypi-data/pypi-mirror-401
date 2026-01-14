# Foydalidasturlar

Turli xil tasodifiy ma'lumotlar generatori - test va rivojlantirish uchun.

## O'rnatish
```bash
pip install foydalidasturlar
```

## Foydalanish
```python
from foydalidasturlar import *

# Parol yaratish
parol = parol_yaratish(uzunlik=16)
print(parol)

# Email yaratish
email = email_yaratish()
print(email)

# Telefon raqam
telefon = telefon_yaratish(davlat='uzbekistan')
print(telefon)

# Visa karta
karta = visa_yaratish()
print(karta)

# Manzil
manzil = manzil_yaratish()
print(manzil)

# Ism
shaxs = ism_yaratish(jins='erkak')
print(shaxs['to\'liq_ism'])
```

## Xususiyatlari

- Parol generatori
- Email generatori
- Telefon raqam (ko'p davlatlar uchun)
- Visa/Mastercard karta
- Manzil
- Ism, familiya, otasining ismi
- Username
- Tasodifiy son va sana