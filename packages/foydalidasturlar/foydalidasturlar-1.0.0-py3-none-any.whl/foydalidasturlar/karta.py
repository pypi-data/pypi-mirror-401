import random

def luhn_checksum(karta_raqami):
    """Luhn algoritmi yordamida checksum hisoblaydi"""
    def raqamlar(n):
        return [int(d) for d in str(n)]
    
    raqamlar_list = raqamlar(karta_raqami)
    teskari = raqamlar_list[::-1]
    
    checksum = 0
    for i, raqam in enumerate(teskari):
        if i % 2 == 1:
            raqam = raqam * 2
            if raqam > 9:
                raqam = raqam - 9
        checksum += raqam
    
    return checksum % 10

def visa_yaratish():
    """
    Tasodifiy Visa karta raqami yaratadi (test uchun)
    
    Returns:
        dict: Karta ma'lumotlari
    """
    # Visa 4 bilan boshlanadi
    karta = '4' + ''.join([str(random.randint(0, 9)) for _ in range(14)])
    
    # Luhn checksum qo'shish
    checksum = luhn_checksum(int(karta))
    checksum_digit = (10 - checksum) % 10
    karta += str(checksum_digit)
    
    # Format qilish
    formatted = f"{karta[0:4]} {karta[4:8]} {karta[8:12]} {karta[12:16]}"
    
    cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    oy = random.randint(1, 12)
    yil = random.randint(25, 30)
    
    return {
        'raqam': formatted,
        'cvv': cvv,
        'amal_qilish': f"{oy:02d}/{yil}",
        'turi': 'Visa'
    }

def mastercard_yaratish():
    """
    Tasodifiy Mastercard karta raqami yaratadi (test uchun)
    
    Returns:
        dict: Karta ma'lumotlari
    """
    # Mastercard 51-55 orasida boshlanadi
    prefix = str(random.randint(51, 55))
    karta = prefix + ''.join([str(random.randint(0, 9)) for _ in range(13)])
    
    # Luhn checksum qo'shish
    checksum = luhn_checksum(int(karta))
    checksum_digit = (10 - checksum) % 10
    karta += str(checksum_digit)
    
    # Format qilish
    formatted = f"{karta[0:4]} {karta[4:8]} {karta[8:12]} {karta[12:16]}"
    
    cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    oy = random.randint(1, 12)
    yil = random.randint(25, 30)
    
    return {
        'raqam': formatted,
        'cvv': cvv,
        'amal_qilish': f"{oy:02d}/{yil}",
        'turi': 'Mastercard'
    }