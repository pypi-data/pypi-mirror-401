import random
import string

def email_yaratish(domenlar=None, prefix_uzunlik=8):
    """
    Tasodifiy email manzil yaratadi
    
    Args:
        domenlar (list): Ishlatilishi mumkin bo'lgan domenlar ro'yxati
        prefix_uzunlik (int): Email prefiks uzunligi
    
    Returns:
        str: Yaratilgan email
    """
    if domenlar is None:
        domenlar = ['gmail.com', 'yahoo.com', 'outlook.com', 'mail.ru', 
                   'inbox.uz', 'umail.uz']
    
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, 
                                    k=prefix_uzunlik))
    domen = random.choice(domenlar)
    
    return f"{prefix}@{domen}"