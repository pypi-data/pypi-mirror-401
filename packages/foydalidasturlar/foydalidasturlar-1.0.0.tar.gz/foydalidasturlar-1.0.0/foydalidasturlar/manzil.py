import random

SHAHARLAR_UZ = ['Toshkent', 'Samarqand', 'Buxoro', 'Andijon', 'Namangan', 
                'Farg\'ona', 'Qashqadaryo', 'Surxondaryo', 'Xorazm']

KOCHALAR = ['Amir Temur', 'Mustaqillik', 'Bobur', 'Navoi', 'Buyuk Ipak Yo‘li','Abdulla Qodiriy', 'Mirzo Ulug\'bek', 'Shota Rustaveli', 'Maksim Gorkiy']

def manzil_yaratish(davlat='uzbekistan'):
    """
    Tasodifiy manzil yaratadi
    
    Args:
        davlat (str): Davlat nomi
    
    Returns:
        dict: Manzil ma'lumotlari
    """
    if davlat.lower() == 'uzbekistan':
        shahar = random.choice(SHAHARLAR_UZ)
        kocha = random.choice(KOCHALAR)
        uy = random.randint(1, 200)
        xonadon = random.randint(1, 100)
        pochta_indeks = random.randint(100000, 199999)
        
        return {
            'shahar': shahar,
            'ko\'cha': f"{kocha} ko'chasi",
            'uy': uy,
            'xonadon': xonadon,
            'pochta_indeks': pochta_indeks,
            'to\'liq': f"{shahar} sh., {kocha} ko'chasi, {uy}-uy, {xonadon}-xonadon",
            'davlat': 'O\'zbekiston'
        }
    else:
        # Boshqa davlatlar uchun umumiy format
        return {
            'shahar': f"City_{random.randint(1, 100)}",
            'ko\'cha': f"Street {random.randint(1, 500)}",
            'uy': random.randint(1, 200),
            'pochta_indeks': random.randint(10000, 99999),
            'davlat': davlat.title()
        }