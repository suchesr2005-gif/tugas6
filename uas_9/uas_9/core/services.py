
from .constants import nilai
def hitung_kelulusan(tetap = 55):

    hasil=0
    hasil2=0

    for n in nilai:
        if n > tetap:
            hasil += 1

        if n < tetap:
            hasil2 += 1
    
    return hasil, hasil2
   
def hitung_ambang_batas(threshold1=75, threshold2=60):

    hasil=0
    hasil2=0
    
    for n in nilai:
            if n > threshold1:
                hasil += 1
            if n < threshold2:
                hasil2 += 1
        
    return hasil, hasil2