#!/usr/bin/env python

import requests
import sys
import argparse

def main():
    args = arAyristir()
    bag = args.bag_adres
    konum = args.konum
    ayrik = bag.split("/")
    dosyaAdi = ayrik[len(ayrik)-1]
    print "Baglanti kuruluyor..."
    try:
        r = requests.get(bag,stream=True)
    except requests.exceptions.ConnectionError:
        print "Baglanti kurulamadi!"
        sys.exit(1)
    if r.status_code == 200:
        print "Baglanti kuruldu. Indirme baslatiliyor."
        print "Indirilen dosyanin adi: "+dosyaAdi
        dosyaBoyut = float(r.headers.get('content-length'))
        if konum == None:
            dosya = open(dosyaAdi,"w")
        else:
            dosya = open(konum+"/"+dosyaAdi,"w")
        if dosyaBoyut is None:
            print "Dosya boyutu tanimlanamadi!"
            print "Dosya indiriliyor..."
            dosya.write(r.content)
        else:
            print "Dosya buyuklugu: "+str(dosyaBoyut/(1024*1024))+" MB"
            ind = 0
            dosyaBoyut = int(dosyaBoyut)
            basla = 0
            for data in r.iter_content(chunk_size=8192):
                ind += len(data)
                dosya.write(data)
                yuzde = int(100*ind/dosyaBoyut)
                tmm = int(50*ind/dosyaBoyut)
                sys.stdout.write("\r[%s%s] %%%s Tamamlanan: %.2f MB  " %
                                ('='*tmm,' '*(50-tmm),
                                 yuzde,float(ind)/(1024*1024)))
                sys.stdout.flush()
        dosya.close
        print
    else:
        print "Baglanti hatasi! Tekrar deneyin."

def arAyristir():
    arAyrac = argparse.ArgumentParser(description="Basit Indirme Araci")
    arAyrac.add_argument("-b","--bag-adres",
                         help="Indirilecek baglanti adresi",required=True)
    arAyrac.add_argument("-k","--konum",help="Dosyanin kaydedilecegi yer")
    args = arAyrac.parse_args()
    return args

if __name__ == "__main__":
    main()
