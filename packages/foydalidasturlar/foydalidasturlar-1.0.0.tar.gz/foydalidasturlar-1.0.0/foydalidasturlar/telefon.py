import random

DAVLATLAR = {
    'uzbekistan': {'kod': '+998', 'format': '## ### ## ##', 'uzunlik': 9},
    'russia': {'kod': '+7', 'format': '### ###-##-##', 'uzunlik': 10},
    'usa': {'kod': '+1', 'format': '(###) ###-####', 'uzunlik': 10},
    'turkey': {'kod': '+90', 'format': '### ### ## ##', 'uzunlik': 10},
    'uk': {'kod': '+44', 'format': '#### ######', 'uzunlik': 10},
    'germany': {'kod': '+49', 'format': '### ########', 'uzunlik': 11},
    'france': {'kod': '+33', 'format': '# ## ## ## ##', 'uzunlik': 9},
    'korea': {'kod': '+82', 'format': '##-####-####', 'uzunlik': 10},
    'japan': {'kod': '+81', 'format': '##-####-####', 'uzunlik': 10},
}

def telefon_yaratish(davlat='uzbekistan'):
    """
    Tasodifiy telefon raqam yaratadi
    
    Args:
        davlat (str): Davlat nomi
    
    Returns:
        str: Yaratilgan telefon raqam
    """
    davlat = davlat.lower()
    
    if davlat not in DAVLATLAR:
        raise ValueError(f"Davlat topilmadi. Mavjud davlatlar: {', '.join(DAVLATLAR.keys())}")
    
    info = DAVLATLAR[davlat]
    raqam = ''.join([str(random.randint(0, 9)) for _ in range(info['uzunlik'])])
    
    # Format qo'llash
    formatted = info['format']
    raqam_index = 0
    natija = info['kod'] + ' '
    
    for char in formatted:
        if char == '#':
            natija += raqam[raqam_index]
            raqam_index += 1
        else:
            natija += char
    
    return natija