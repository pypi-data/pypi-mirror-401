import random
from datetime import datetime, timedelta

def tasodifiy_son(min_qiymat=0, max_qiymat=100):
    """
    Tasodifiy son yaratadi
    
    Args:
        min_qiymat (int): Minimal qiymat
        max_qiymat (int): Maksimal qiymat
    
    Returns:
        int: Tasodifiy son
    """
    return random.randint(min_qiymat, max_qiymat)

def tasodifiy_sana(boshlanish=None, tugash=None):
    """
    Tasodifiy sana yaratadi
    
    Args:
        boshlanish (str): Boshlanish sanasi (YYYY-MM-DD)
        tugash (str): Tugash sanasi (YYYY-MM-DD)
    
    Returns:
        str: Tasodifiy sana
    """
    if boshlanish is None:
        boshlanish = datetime(1970, 1, 1)
    else:
        boshlanish = datetime.strptime(boshlanish, '%Y-%m-%d')
    
    if tugash is None:
        tugash = datetime.now()
    else:
        tugash = datetime.strptime(tugash, '%Y-%m-%d')
    
    kunlar_farqi = (tugash - boshlanish).days
    tasodifiy_kunlar = random.randint(0, kunlar_farqi)
    
    tasodifiy_sana = boshlanish + timedelta(days=tasodifiy_kunlar)
    
    return tasodifiy_sana.strftime('%Y-%m-%d')