"""
Foydalidasturlar - Turli xil tasodifiy ma'lumotlar generatori
"""

__version__ = "1.0.0"
__author__ = "Sizning ismingiz"

from .parol import parol_yaratish
from .email import email_yaratish
from .telefon import telefon_yaratish
from .karta import visa_yaratish, mastercard_yaratish
from .manzil import manzil_yaratish
from .shaxs import ism_yaratish, username_yaratish
from .utils import tasodifiy_son, tasodifiy_sana

__all__ = [
    'parol_yaratish',
    'email_yaratish',
    'telefon_yaratish',
    'visa_yaratish',
    'mastercard_yaratish',
    'manzil_yaratish',
    'ism_yaratish',
    'username_yaratish',
    'tasodifiy_son',
    'tasodifiy_sana'
]