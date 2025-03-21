# Kullanacağımız kütüphaneleri import ediyoruz. 
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

# Istasyon adlı bir sınıf oluşturuyoruz. Her istasyon, bir isim (ad), indeks (idx) ve hat adı (hat) tutar.
class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx  # İstasyonun benzersiz kimliği (ID)
        self.ad = ad    # İstasyonun adı
        self.hat = hat  # İstasyonun ait olduğu hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # Komşu istasyonlar ve süreleri

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        # Komşu bir istasyonu ve geçiş süresini ekliyoruz.
        self.komsular.append((istasyon, sure))

# MetroAgi adlı bir sınıf oluşturuyoruz. Metro ağını ve istasyonlar arası bağlantıları tutar.
class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}  # İstasyonların ID'ye göre tutulduğu bir dictionary
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)  # Hatlar ve bu hatlara ait istasyonlar
        self.graf: Dict[str, List[Tuple[str, int]]] = defaultdict(list)  # Graf yapısı (istasyon -> [(komsu_istasyon, süre)])

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        # Yeni bir istasyon ekliyoruz, zaten varsa eklemiyoruz.
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon    # İstasyonu dictionary'ye ekliyoruz.
            self.hatlar[hat].append(istasyon)   # Aynı hattan olan istasyonu hatlar listesine ekliyoruz.

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        # İki istasyon arasında bir bağlantı ekliyoruz (bağlantının iki yönlü olduğunu unutmayalım).
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

        # Graf yapısına bağlantıları da ekliyoruz.
        self.graf[istasyon1_id].append((istasyon2_id, sure))
        self.graf[istasyon2_id].append((istasyon1_id, sure))

    def graf_ile_en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[str], int]]:
        """Graf yapısını kullanarak en hızlı rotayı bulur"""
        # Eğer başlangıç veya hedef istasyonu graf yapısında yoksa None döneriz.
        if baslangic_id not in self.graf or hedef_id not in self.graf:
            return None
        
        # A* algoritmasını graf yapısı üzerinde çalıştırıyoruz.
        pq = [(0, baslangic_id, [baslangic_id])]  # (toplam_sure, istasyon_id, rota) şeklinde öncelik kuyruğu
        ziyaret_edildi = set()  # Ziyaret edilen istasyonları takip ediyoruz.

        while pq:
            toplam_sure, istasyon_id, rota = heapq.heappop(pq)   # Kuyruğundan en düşük süreyi çıkarıyoruz.

            # Eğer hedef istasyonuna ulaştıysak rota ve toplam süreyi döndürüyoruz.
            if istasyon_id == hedef_id:
                return (rota, toplam_sure)

            if istasyon_id in ziyaret_edildi:
                continue
            ziyaret_edildi.add(istasyon_id) # İstasyonu ziyaret edilip edilmediğini kontrol ediyoruz.

            # Komşu istasyonları keşfederek kuyruğa ekliyoruz.
            for komsu_id, sure in self.graf[istasyon_id]:
                if komsu_id not in ziyaret_edildi:
                    yeni_rota = rota + [komsu_id]   # Yeni rotayı oluşturuyoruz.
                    yeni_toplam_sure = toplam_sure + sure   # Yeni toplam süreyi hesaplıyoruz.
                    heapq.heappush(pq, (yeni_toplam_sure, komsu_id, yeni_rota)) # Kuyruğa ekliyoruz.

        # Rota bulunamazsa None döndürüyoruz.
        return None

    def metro_agini_gorsellestir(self):
        """Metro ağını networkx kullanarak görselleştirir"""
        G = nx.Graph()  # Networkx grafı oluşturuyoruz.
        pos = {}  # Konumlar için boş bir dictionary oluşturuyoruz.

        # İstasyonları düğüm olarak ekliyoruz.
        for idx, istasyon in self.istasyonlar.items():
            G.add_node(idx, label=istasyon.ad, color=istasyon.hat)  # Her istasyon bir düğüm olacak.

        # Bağlantıları kenar olarak ekliyoruz.
        for idx, istasyon in self.istasyonlar.items():
            for komsu, sure in istasyon.komsular:
                G.add_edge(istasyon.idx, komsu.idx, weight=sure)     # Her bağlantıyı bir kenar olarak ekliyoruz.

        # Görselleştirme
        plt.figure(figsize=(10, 8)) # Görselleştirme penceresinin boyutlarını belirliyoruz.

        # Her hat için renkleri farklı yapıyoruz.
        hat_colors = {
            "Kırmızı Hat": "red",
            "Mavi Hat": "blue",
            "Turuncu Hat": "orange"
        }

        # Düğüm renklerini ve etiketleri ayarlıyoruz.
        node_colors = [hat_colors.get(istasyon.hat, "gray") for istasyon in self.istasyonlar.values()]
        labels = {node: self.istasyonlar[node].ad for node in G.nodes()}

        # Kenar ağırlıklarını alıyoruz.
        edge_labels = nx.get_edge_attributes(G, "weight")

        # Düğümlerin konumlarını hesaplıyoruz (Networkx'in spring layout algoritması ile).
        pos = nx.spring_layout(G, seed=42)  # Layout algoritması

        # Grafı çiziyoruz.
        nx.draw(G, pos, node_size=3000, node_color=node_colors, with_labels=True, font_weight='bold', font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Metro Ağı Görselleştirmesi")
        plt.show()

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur"""
        # Eğer başlangıç veya hedef istasyonu dictionaryde yoksa None dönüyoruz.
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]  # Başlangıç istasyonunu alıyoruz.
        hedef = self.istasyonlar[hedef_id]  # Hedef istasyonunu alıyoruz.
        
        # BFS algoritması için kuyruk oluşturuyoruz, her eleman (istasyon, rota) şeklindedir.
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set([baslangic])   # Başlangıç istasyonunu ziyaret ettiğimizi işaretliyoruz.
        
        while kuyruk:
            istasyon, rota = kuyruk.popleft()   # Kuyruğundan bir istasyon ve rota çıkarıyoruz.

            # Eğer hedef istasyonuna ulaştıysak rotayı döndürüyoruz.
            if istasyon == hedef:
                return rota

            # Komşu istasyonları keşfetmek için döngü başlatıyoruz.
            for komsu, _ in istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    yeni_rota = rota + [komsu]
                    kuyruk.append((komsu, yeni_rota))   # Komşu istasyonu kuyruğa ekliyoruz.
        
        # Rota bulunamazsa None döndürüyoruz.
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur"""
        # Eğer başlangıç veya hedef istasyonu dictionaryde yoksa None dönüyoruz.
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]  # Başlangıç istasyonunu alıyoruz.
        hedef = self.istasyonlar[hedef_id]  # Hedef istasyonunu alıyoruz.
        
        # A* algoritmasında öncelik kuyruğu oluşturuyoruz.
        pq = [(0, id(baslangic), baslangic, [baslangic])]  # (toplam_sure, id, istasyon, rota)
        ziyaret_edildi = set()
        while pq:
            toplam_sure, _, istasyon, rota = heapq.heappop(pq)  # Kuyruğundan en düşük süreyi çıkarıyoruz.

            # Eğer hedef istasyonuna ulaştıysak rota ve toplam süreyi döndürüyoruz.
            if istasyon == hedef:
                return (rota, toplam_sure)

            if istasyon in ziyaret_edildi:
                continue
            ziyaret_edildi.add(istasyon)

            # Komşu istasyonları keşfetmek için for döngüsü oluşturuyoruz.
            for komsu, sure in istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    yeni_rota = rota + [komsu]
                    yeni_toplam_sure = toplam_sure + sure
                    heapq.heappush(pq, (yeni_toplam_sure, id(komsu), komsu, yeni_rota)) # Kuyruğa ekliyoruz.

        # Rota bulunamazsa None döndürüyoruz.
        return None


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()  # Metro ağını başlatıyoruz.
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    # Metro ağını görselleştirme
    metro.metro_agini_gorsellestir()
