'''
read mahasiswa.xlsx -> simpan kedalam variable array -> create class fuzzy dengan attr id, hasil,luaran,layak, y -> Fuzzifikasi -> Inferensi
-> Defuzzifikasi -> loop hingga akhir index mahasiswa.xlsx -> sort besar ke kecil berdasarkan nilai y -> pindahkan index 0 sampai 20
kedalam arrayY -> export nilai arrayY ke bentuk file bantuan.xlsx 
'''
#Luqman Haries 1301180072 if4208

import pandas as pan
import operator
#pip install xlrd
#pip install openpyxl

#fuzzy
class Fuzzy:
    def __init__(self):
        self.id = id[i]

        #OutputFuzzifikasi
        self.derajatHasilBuruk = self.fPenghasilan("rendah",penghasilan[i])
        self.derajatHasilCukup = self.fPenghasilan("sedang",penghasilan[i])
        self.derajatHasilBagus = self.fPenghasilan("tinggi",penghasilan[i])

        #OutputInferensi
        self.derajatLuaranBuruk = self.fPenghasilan("rendah",pengeluaran[i])
        self.derajatLuaranCukup = self.fPenghasilan("sedang",pengeluaran[i])
        self.derajatLuaranBagus = self.fPenghasilan("tinggi",pengeluaran[i])

        self.layakRendah = self.fKelayakan("rendah")
        self.layakTinggi = self.fKelayakan("tinggi")

        #OutputDefuzzifikasi
        self.y = self.fComposition()

    #Fungsi Keanggotaan
    def fSegitiga(self,x,a,b,c):
        if x <= a or x >= c:
            return 0
        if a < x and a <= b :
            return ( (x-a)/(b-a) )
        if b < x and x <= c :
            return ( -(x-c)/(c-b) )

    def fTrapesium(self,x,a,b,c,d):
        if x <= a or x >= d :
            return 0
        if a < x and x < b :
            return ((x-a)/(b-a))
        if b <= x and x <= c :
            return 1
        if c < x and x <= d :
            return ( -(x-d)/(d-c) )

    #Fuzzifikasi
    def fPenghasilan(self,kategori,x):
        if kategori == "rendah" :
            return self.fTrapesium(x,0,0,3,6.563)
        if kategori == "sedang" :
            return self.fSegitiga(x,4,10,13)
        if kategori == "tinggi" :
            return self.fTrapesium(x,10,12,19.69,19.69)


    def fPengeluaran(self,kategori,x):
        if kategori == "rendah" :
            return self.fTrapesium(x,0,0,2,3.76)
        if kategori == "sedang" :
            return self.fSegitiga(x,4,10,13)
        if kategori == "tinggi" :
            return self.fTrapesium(x,10,12,19.69,19.69)

    #Inferensi
    def fKelayakan(self,kategori):
        #init
        kelayakanRendah = 0
        kelayakanTinggi = 0
        temp = 0

        #fuzzy rules
        if self.derajatHasilBuruk != 0 and self. derajatLuaranBuruk:
            temp = min (self.derajatHasilBuruk,self. derajatLuaranBuruk)
            kelayakanRendah = max (temp,kelayakanRendah)
        if self.derajatHasilBuruk != 0 and self. derajatLuaranCukup:
            temp = min (self.derajatHasilBuruk,self. derajatLuaranCukup)
            kelayakanRendah = max (temp,kelayakanRendah)
        if self.derajatHasilBuruk != 0 and self. derajatLuaranBagus:
            temp = min (self.derajatHasilBuruk,self. derajatLuaranBagus)
            kelayakanTinggi = max (temp,kelayakanTinggi)

        if self.derajatHasilCukup != 0 and self. derajatLuaranBuruk:
            temp = min (self.derajatHasilCukup,self. derajatLuaranBuruk)
            kelayakanRendah = max (temp,kelayakanRendah)
        if self.derajatHasilCukup != 0 and self. derajatLuaranCukup:
            temp = min (self.derajatHasilCukup,self. derajatLuaranCukup)
            kelayakanTinggi = max (temp,kelayakanTinggi)
        if self.derajatHasilCukup != 0 and self. derajatLuaranBagus:
            temp = min (self.derajatHasilCukup,self. derajatLuaranBagus)
            kelayakanRendah = max (temp,kelayakanRendah)

        if self.derajatHasilBagus != 0 and self. derajatLuaranBuruk:
            temp = min (self.derajatHasilBagus,self. derajatLuaranBuruk)
            kelayakanTinggi = max (temp,kelayakanTinggi)
        if self.derajatHasilBagus != 0 and self. derajatLuaranCukup:
            temp = min (self.derajatHasilBagus,self. derajatLuaranCukup)
            kelayakanRendah = max (temp,kelayakanRendah)
        if self.derajatHasilBagus != 0 and self. derajatLuaranBagus:
            temp = min (self.derajatHasilBagus,self. derajatLuaranBagus)
            kelayakanRendah = max (temp,kelayakanRendah)

        #add to self
        if kategori == "rendah":
            return kelayakanRendah
        if kategori == "tinggi":
            return kelayakanTinggi

    #Defuzzifikasi
    def fComposition(self):
        #init y
        a = 0
        b = 0
        i = 0
        union = 0

        while i < 100:
            i = i + 1
           
            #P
            union = max( min (self.fTrapesium(i,0,27,36,45),self.layakRendah), min (self.fTrapesium(i,36,45,63,100),self.layakTinggi))

            a = a + (i * union)
            b = b + (i + union)

        return (a/b)

#read file
mhs_xls = pan.read_excel(r'Mahasiswa.xls') #pathfile
id = mhs_xls['Id'].values
penghasilan = mhs_xls['Penghasilan'].values
pengeluaran = mhs_xls['Pengeluaran'].values

i = 0 #iterasi

list = []
while i <= 99:
    F = Fuzzy()
    list.append(F)
    i = i + 1

#sort besar -> kecil
list.sort(key=operator.attrgetter("y"), reverse=True)

#memisahkan 20 id berdasarkan besar nilai y (kelayakan)
arrayY = []
j = 0
while j <= 19:
    arrayY.append(list[j].id)
    j = j + 1
    
#export arrayY ke bantuan.xls
pan.DataFrame(arrayY,columns=['ID']).to_excel('Bantuan.xlsx',index=False)

#Output arrayY
print(arrayY)
