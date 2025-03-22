# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)
## Projenin Kısa Açıklaması
Bu proje, bir metro ağında iki istasyon arasındaki en hızlı ve en az aktarmalı rotayı bulmayı amaçlayan bir simülasyon geliştirmeyi hedeflemektedir. Gerçek dünyadaki metro ağlarını simüle ederek, kullanıcıların farklı noktalar arasındaki en uygun rotayı bulmalarını sağlayan algoritmalar geliştirilmiştir.
Projede iki temel algoritma kullanılmaktadır:
1.	**BFS (Breadth-First Search)** algoritması ile en az aktarmalı rota.
2.	**A*** algoritması ile en hızlı rota.
Proje, metro ağı üzerinde algoritmaların nasıl çalıştığını anlamaya ve uygulamaya yönelik bir çözümdür.

## Kullanılan Teknolojiler ve Kütüphaneler
Bu projede aşağıdaki Python kütüphaneleri kullanılmıştır:
*	**networkx:** Grafik yapıları ve algoritmaları için kullanılır. Metro ağını modellemek ve görselleştirmek için tercih edilmiştir.
*	**matplotlib:** Metro ağını görselleştirmek için kullanılır. Grafiksel gösterim sağlar.
*	**collections.deque:** BFS algoritmasında kuyruk yapısını sağlamak için kullanılmıştır.
*	**heapq:** A* algoritmasında öncelik kuyruğu kullanmak için tercih edilmiştir.
*	**typing:** Veri tiplerini tanımlamak için kullanılmıştır.

## Algoritmaların Çalışma Mantığı
### BFS Algoritması (En Az Aktarmalı Rota)
BFS algoritması, graf üzerinde en kısa yolu bulmak için kullanılır. Bu algoritma, tüm komşuları aynı seviyede keşfeder ve her adımda bir "aktarma" noktası ekler. Bu şekilde, en az aktarmalı rotayı bulmaya çalışır.
#### Adımlar:
1.	**Kuyruk Yapısı (Deque):** Başlangıç istasyonu kuyrukta yer alır.
2.	**Ziyaret Edilenler:** Ziyaret edilen istasyonlar bir set içinde tutulur.
3.	**Komşu Keşfi:** Her istasyon için komşu istasyonlar keşfedilir. Eğer komşu istasyon ziyaret edilmemişse, kuyrukta bir sonraki istasyon olarak yer alır.
4.	**En Kısa Rota:** Hedef istasyon bulunana kadar adımlar atılır.
BFS algoritması ile hedef istasyon bulunana kadar en kısa aktarmalı yol izlenir.
### A* Algoritması (En Hızlı Rota)
A* algoritması, her bir rotayı değerlendirmek için iki kriter kullanır:
* **Toplam süre:** Başlangıç noktasından hedefe kadar olan toplam süreyi hesaplar.
*	**Heuristik:** Hedef istasyona olan tahmini mesafe, hızla varılabilecek bir yol belirlemek için kullanılır.
#### Adımlar:
1.	**Öncelik Kuyruğu (Heapq):** Başlangıç istasyonu ve rotalar, öncelik kuyruğuna yerleştirilir.
2.	**Ziyaret Edilenler:** Ziyaret edilen istasyonlar bir set içinde tutulur.
3.	**Toplam Süre:** Komşular keşfedilirken toplam süre güncellenir ve rotalar kuyruğa eklenir.
4.	**En Hızlı Rota:** Hedef istasyon bulunana kadar en kısa süreli yol takip edilir.
A* algoritması, toplam süreyi minimize ederek en hızlı rotayı bulur.

## Örnek Kullanım ve Test Sonuçları
Aşağıda, metro ağını kullanarak farklı test senaryolarında en hızlı ve en az aktarmalı rotaların nasıl bulunacağına dair örnekler yer almaktadır.
### Senaryo 1: AŞTİ'den OSB'ye:
*	**En az aktarmalı rota:** AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB
*	**En hızlı rota (25 dakika):** AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB
### Senaryo 2: Batıkent'ten Keçiören'e:
*	**En az aktarmalı rota:** Batıkent -> Demetevler -> Gar -> Keçiören
*	**En hızlı rota (21 dakika):** Batıkent -> Demetevler -> Gar -> Keçiören
### Senaryo 3: Keçiören'den AŞTİ'ye:
*	**En az aktarmalı rota:** Keçiören -> Gar -> Gar -> Sıhhiye -> Kızılay -> AŞTİ
*	**En hızlı rota (19 dakika):** Keçiören -> Gar -> Gar -> Sıhhiye -> Kızılay -> AŞTİ

![Test_Senaryolari](https://github.com/user-attachments/assets/a8564eb6-af5c-4597-a76c-0e9a3d2c180f)


## Metro Ağının Görselleştirilmesi
Projede, metro ağı görselleştirilmiş ve farklı hatlar için renkler atanmıştır. Görselleştirme, NetworkX ve Matplotlib kütüphaneleri kullanılarak yapılmıştır.
*	Kırmızı Hat: **Kırmızı**
*	Mavi Hat: **Mavi**
*	Turuncu Hat: **Turuncu**

![Metro_agi_gorsellestirme](https://github.com/user-attachments/assets/aea72d69-c52f-4196-bdf1-e32695c659c8)


## Projeyi Geliştirme Fikirleri
Bu projeyi daha da geliştirmek için aşağıdaki fikirler üzerinde çalışabiliriz:
1.	**Yeni Hatlar ve İstasyonlar:** Gerçek dünyadan ilham alarak yeni metro hatları ve istasyonları eklemek.
2.	**Daha Karmaşık Algoritmalar:** Diğer yol bulma algoritmalarını (örneğin, Dijkstra algoritması) eklemek.
3.	**Dinamik Zamanlar:** Her bir istasyon için hareketli süreleri eklemek ve farklı saat dilimlerinde metro sürelerini değiştirmek.
4.	**Kullanıcı Arayüzü:** Kullanıcıların metro ağını görsel olarak keşfetmesine olanak tanıyacak bir arayüz geliştirmek.

## Kod Yapısı
Projenin temel yapısı aşağıdaki gibidir:

### Sınıflar
1. **Istasyon:** Her istasyonun kimliği (ID), adı, hattı ve komşu istasyonlarını tutar.
2. **MetroAgi:** Metro ağını ve istasyonlar arası bağlantıları yönetir. Ayrıca, BFS ve A* algoritmalarını içerir.

### Metotlar
* **istasyon_ekle**: Yeni bir istasyon ekler.
* **baglanti_ekle:** İki istasyon arasında bağlantı ekler.
* **en_az_aktarma_bul:** BFS algoritması ile en az aktarmalı rotayı bulur.
* **en_hizli_rota_bul:** A* algoritması ile en hızlı rotayı bulur.
* **metro_agini_gorsellestir:** Metro ağını görselleştirir.

## Örnek Kullanım

![Ornek_Kullanim](https://github.com/user-attachments/assets/9b1cf0bb-cd1e-49c4-b63a-923d1ad6c888)

