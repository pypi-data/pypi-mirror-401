import random
import string

def parol_yaratish(uzunlik=12, katta_harf=True, kichik_harf=True, 
                   raqamlar=True, maxsus_belgilar=True):
    """
    Kuchli tasodifiy parol yaratadi
    
    Args:
        uzunlik (int): Parol uzunligi
        katta_harf (bool): Katta harflar ishlatilsinmi
        kichik_harf (bool): Kichik harflar ishlatilsinmi
        raqamlar (bool): Raqamlar ishlatilsinmi
        maxsus_belgilar (bool): Maxsus belgilar ishlatilsinmi
    
    Returns:
        str: Yaratilgan parol
    """
    belgilar = ''
    
    if katta_harf:
        belgilar += string.ascii_uppercase
    if kichik_harf:
        belgilar += string.ascii_lowercase
    if raqamlar:
        belgilar += string.digits
    if maxsus_belgilar:
        belgilar += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not belgilar:
        raise ValueError("Kamida bitta belgi turi tanlanishi kerak!")
    
    parol = ''.join(random.choice(belgilar) for _ in range(uzunlik))
    return parol