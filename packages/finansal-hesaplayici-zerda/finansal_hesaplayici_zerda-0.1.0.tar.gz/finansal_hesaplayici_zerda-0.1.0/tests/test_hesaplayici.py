
from finansal_hesaplayici import FinansalHesaplayici

def test_anuite_bd():
    h = FinansalHesaplayici(10, 5, 1000)
    assert round(h.anuite_bugunku_deger(), 2) == 3790.79
    from finansal_hesaplayici import FinansalHesaplayici

hesap = FinansalHesaplayici(faiz_orani=10, donem_sayisi=5, taksit=1000)

print(hesap.anuite_bugunku_deger())
print(hesap.ertelenmis_anuite(2))
print(hesap.surekli_anuite())

