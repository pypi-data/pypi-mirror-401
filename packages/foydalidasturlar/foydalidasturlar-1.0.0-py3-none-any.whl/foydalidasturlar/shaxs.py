import random

ISMLAR_ERKAK = ['Javohir', 'Abbos', 'Dilshod', 'Sardor', 'Jamshid', 'Aziz', 
                'Bobur', 'Timur', 'Islom', 'Jahongir', 'Sherzod', 'Olim']

ISMLAR_AYOL = ['Nilufar', 'Gulnora', 'Feruza', 'Madina', 'Sevinch', 'Zarina',
               'Dildora', 'Oysha', 'Mehrinoz', 'Shahzoda', 'Malika', 'Nazira']

FAMILIYALAR = ['Karimov', 'Rahimov', 'Tursunov', 'Salimov', 'Abdullayev',
               'Rasulev', 'Ismoilov', 'Yusupov', 'Qodirov', 'Haydarov']

OTALARNING_ISMI = ['Abdullo', 'Rahmon', 'Karim', 'Anvar', 'Sobir', 'Nosir',
                   'Shavkat', 'Rustam', 'Farxod', 'Davron']

def ism_yaratish(jins='erkak'):
    """
    Tasodifiy ism, familiya va otasining ismini yaratadi
    
    Args:
        jins (str): 'erkak' yoki 'ayol'
    
    Returns:
        dict: Shaxs ma'lumotlari
    """
    if jins.lower() == 'erkak':
        ism = random.choice(ISMLAR_ERKAK)
    else:
        ism = random.choice(ISMLAR_AYOL)
    
    familiya = random.choice(FAMILIYALAR)
    otasining_ismi = random.choice(OTALARNING_ISMI)
    
    if jins.lower() == 'erkak':
        otasining_ismi_suffix = 'o\'g\'li'
    else:
        otasining_ismi_suffix = 'qizi'
    
    return {
        'ism': ism,
        'familiya': familiya,
        'otasining_ismi': f"{otasining_ismi} {otasining_ismi_suffix}",
        'to\'liq_ism': f"{familiya} {ism} {otasining_ismi} {otasining_ismi_suffix}",
        'jins': jins
    }

def username_yaratish(uzunlik=8):
    """
    Tasodifiy username yaratadi
    
    Args:
        uzunlik (int): Username uzunligi
    
    Returns:
        str: Yaratilgan username
    """
    import string
    
    harflar = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(harflar) for _ in range(uzunlik))
    
    return username