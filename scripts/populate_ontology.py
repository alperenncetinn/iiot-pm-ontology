import os
import re
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from openai import OpenAI

# =================================================================
# 1. YAPILANDIRMA (CONFIGURATION)
# =================================================================
# OpenAI kullanmak için: Çevre değişkeni olarak OPENAI_API_KEY tanımlayın.
# Yerel Ollama kullanmak için: Çevre değişkenlerini şu şekilde ayarlayabilirsiniz:
# OPENAI_API_KEY="ollama"
# OPENAI_API_BASE="http://localhost:11434/v1"
# LLM_MODEL="llama3" (veya kurulu herhangi bir model)

api_key = os.getenv("OPENAI_API_KEY", "ollama")
base_url = os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1")
model_name = os.getenv("LLM_MODEL", "gemma4:e2b")

# Dosya yolları
ONTOLOGY_PATH = "../ontology/sample_individuals.ttl"
OUTPUT_PATH = "../ontology/populated_data.ttl" # Dinamik üretilen veriler için

# =================================================================
# 2. LLM PIPELINE & FEW-SHOT SYSTEM PROMPT
# =================================================================

def extract_ontology_with_llm(log_text: str) -> str:
    """
    Verilen metin logunu okur, Few-Shot yönlendirmesiyle Turtle formatında RDF üretir.
    """
    client = OpenAI(api_key=api_key, base_url=base_url)

    system_message = (
        "Sen bir Bilgi Mühendisisin (Knowledge Engineer). Görevin, sana verilen ham endüstriyel "
        "IoT log metinlerini analiz edip, bunları 'iiot-pm-ontology' şemasına uygun RDF verilerine (Turtle/TTL formatında) dönüştürmektir.\n\n"
        "Kurallar:\n"
        "1. Prefix olarak 'iiotpmo: <http://example.org/iiot-pm-ontology#>' kullan.\n"
        "2. Çıktı olarak SADECE geçerli bir Turtle (.ttl) kodu üret. Markdown kod blokları (```turtle ... ```) veya ek açıklama metinleri ekleme.\n"
        "3. Sınıfları ve özellikleri ontoloji standartlarına göre eşle:\n"
        "   - iiotpmo:Asset (Cihaz/Varlık)\n"
        "   - iiotpmo:Sensor (Sensör)\n"
        "   - iiotpmo:Measurement (Ölçüm)\n"
        "   - iiotpmo:PredictedFailure (Tahmini Arıza)\n"
        "   - iiotpmo:Alert veya iiotpmo:CriticalAlert (Alarmlar)\n"
        "4. Birey (Individual) isimlerinde boşluk yerine alt çizgi (_) kullan.\n\n"
        "--- FEW-SHOT ÖRNEK ---\n"
        "GİRDİ METNİ:\n"
        "\"2026-05-06 08:30:00 - Motor_X isimli cihazın Sıcaklık_Sensörü_A değerini 82.4C olarak ölçtü. "
        "Bu değer kritik sınır olan 80C'nin üzerinde. GRU_RNN_v1 modeli arıza riskini %86 olarak hesapladı ve Kritik Alarm üretildi.\"\n\n"
        "ÇIKTI TURTLE:\n"
        "@prefix iiotpmo: <http://example.org/iiot-pm-ontology#> .\n"
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n"
        "iiotpmo:Motor_X a iiotpmo:Asset ;\n"
        "    rdfs:label \"Motor X\"@en ;\n"
        "    iiotpmo:hasSensor iiotpmo:Sıcaklık_Sensörü_A ;\n"
        "    iiotpmo:hasPredictedFailure iiotpmo:PredictedFailure_Motor_X_BearingWear .\n\n"
        "iiotpmo:Sıcaklık_Sensörü_A a iiotpmo:Sensor ;\n"
        "    rdfs:label \"Sıcaklık Sensörü A\"@en ;\n"
        "    iiotpmo:monitors iiotpmo:Motor_X ;\n"
        "    iiotpmo:hasThreshold \"80.0\"^^xsd:float ;\n"
        "    iiotpmo:hasObservation iiotpmo:Obs_Sıcaklık_Sensörü_A_20260506_083000 .\n\n"
        "iiotpmo:Obs_Sıcaklık_Sensörü_A_20260506_083000 a iiotpmo:Observation ;\n"
        "    iiotpmo:hasTimestamp \"2026-05-06T08:30:00\"^^xsd:dateTime ;\n"
        "    iiotpmo:hasMeasurement iiotpmo:Meas_Sıcaklık_Sensörü_A_20260506_083000 ;\n"
        "    iiotpmo:generatesAlert iiotpmo:Alert_Motor_X_Sıcaklık_20260506_083000 .\n\n"
        "iiotpmo:Meas_Sıcaklık_Sensörü_A_20260506_083000 a iiotpmo:Measurement ;\n"
        "    iiotpmo:hasValue \"82.4\"^^xsd:float ;\n"
        "    iiotpmo:hasUnit \"degC\" ;\n"
        "    iiotpmo:hasTimestamp \"2026-05-06T08:30:00\"^^xsd:dateTime .\n\n"
        "iiotpmo:Alert_Motor_X_Sıcaklık_20260506_083000 a iiotpmo:CriticalAlert ;\n"
        "    rdfs:label \"Critical Temperature Alert for Motor X\"@en ;\n"
        "    iiotpmo:hasTimestamp \"2026-05-06T08:30:00\"^^xsd:dateTime .\n\n"
        "iiotpmo:PredictedFailure_Motor_X_BearingWear a iiotpmo:PredictedFailure ;\n"
        "    iiotpmo:hasTimestamp \"2026-05-06T08:30:00\"^^xsd:dateTime ;\n"
        "    iiotpmo:hasConfidence \"0.86\"^^xsd:float ;\n"
        "    iiotpmo:predictedBy iiotpmo:GRU_RNN_v1 .\n"
        "--- FEW-SHOT BİTİŞ ---"
    )

    print(f"-> LLM çağrısı yapılıyor (Model: {model_name})...")
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"GİRDİ METNİ:\n\"{log_text}\""}
        ],
        temperature=0.1
    )
    
    ttl_content = response.choices[0].message.content.strip()
    
    # LLM markdown kod bloğu (```turtle ... ``` vb.) içinde döndüyse içeriği güvenli bir şekilde ayıkla
    match = re.search(r"```(?:turtle|ttl|rdf|n3|nt)?\s*(.*?)\s*```", ttl_content, re.DOTALL | re.IGNORECASE)
    if match:
        ttl_content = match.group(1).strip()
    else:
        # Kod bloğu eşleşmediyse ama başlarda/sonlarda üçlü tırnak kaldıysa temizle
        ttl_content = ttl_content.replace("```turtle", "").replace("```ttl", "").replace("```rdf", "").replace("```", "").strip()
        
    return ttl_content

# =================================================================
# 3. RDFLIB İLE GRAFI MERGE ETME VE KAYDETME
# =================================================================

def merge_and_save_ontology(llm_ttl_data: str, base_ontology_file: str, save_path: str):
    """
    LLM'den gelen Turtle verisini mevcut ontoloji dosyasıyla birleştirip kaydeder.
    """
    # 1. Mevcut grafı yükle (Varsa save_path, yoksa base_ontology_file)
    g = Graph()
    
    if os.path.exists(save_path):
        print(f"-> Mevcut birikimli veri dosyası yükleniyor: {save_path}")
        load_file = save_path
    else:
        print(f"-> Başlangıç örnek veri dosyası yükleniyor: {base_ontology_file}")
        load_file = base_ontology_file

    try:
        # ttl formatında yükle
        g.parse(load_file, format="turtle")
        print(f"   [Başarılı] Mevcut graf {len(g)} üçlü (triples) içeriyor.")
    except Exception as e:
        print(f"   [Uyarı] Dosya yüklenemedi. Yeni bir graf oluşturuluyor. Hata: {e}")
        # Dosya yoksa veya okunamadıysa boş bir graph ile başlar.
    
    # 2. LLM çıktısını geçici bir grafa parse et
    print("-> LLM'den gelen Turtle verisi parse ediliyor...")
    temp_g = Graph()
    try:
        temp_g.parse(data=llm_ttl_data, format="turtle")
        print(f"   [Başarılı] Yeni veriden {len(temp_g)} yeni üçlü parse edildi.")
    except Exception as e:
        print(f"   [HATA] LLM çıktısı geçerli bir Turtle (.ttl) formatında değil!")
        print("LLM Çıktısı:")
        print(llm_ttl_data)
        raise e

    # 3. İki grafı birleştir (merge)
    print("-> Graflar birleştiriliyor (merge)...")
    g += temp_g
    print(f"   [Başarılı] Birleştirilmiş graf toplam {len(g)} üçlü içeriyor.")

    # 4. Güncel grafı diske kaydet
    print(f"-> Güncellenmiş ontoloji kaydediliyor: {save_path}")
    g.serialize(destination=save_path, format="turtle")
    print("   [Tamamlandı] Ontoloji başarıyla güncellendi ve kaydedildi.")


# =================================================================
# 4. ANA ÇALIŞTIRICI (MAIN)
# =================================================================

if __name__ == "__main__":
    # Test Girdisi
    input_log = (
        "2026-05-31 10:15:30 - Motor_A isimli cihazın Vibrasyon_Sensörü_1 değerini 85.4Hz olarak ölçtü. "
        "Bu değer kritik sınır olan 80Hz'in üzerinde. ML_Model_Alpha arıza riskini %92 olarak hesapladı "
        "ve Acil Bakım Uyarısı üretildi."
    )
    
    print("=== IIO-PMO LLM Ontoloji Popülasyon Pipeline ===")
    print(f"Metin Log Girdisi:\n{input_log}\n")

    # Adım 1: LLM ile RDF extraction
    try:
        extracted_ttl = extract_ontology_with_llm(input_log)
        print("\n=== ÇIKARILAN TURTLE (RDF) ===")
        print(extracted_ttl)
        print("==============================\n")
        
        # Adım 2: Mevcut graf ile birleştirme ve kaydetme
        # Çalışma dizinine göre dosya yolunu ayarla
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ontology_abs_path = os.path.join(script_dir, ONTOLOGY_PATH)
        output_abs_path = os.path.join(script_dir, OUTPUT_PATH)
        
        merge_and_save_ontology(extracted_ttl, ontology_abs_path, output_abs_path)
        
    except Exception as e:
        print(f"\n[HATA] İşlem sırasında bir hata oluştu: {e}")
        print("\nNOT: Kodu çalıştırmadan önce lütfen 'OPENAI_API_KEY' çevre değişkeninizi "
              "tanımladığınızdan veya yerel Ollama API adresinizi doğru girdiğinizden emin olun.")
