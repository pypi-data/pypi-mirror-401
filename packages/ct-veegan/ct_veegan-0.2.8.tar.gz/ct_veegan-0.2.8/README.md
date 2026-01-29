
# 📘 CT-VeeGAN

**Dokumentasi Lengkap & Panduan Penggunaan**

CT-VeeGAN adalah pustaka Python untuk **menangani ketidakseimbangan data (data imbalance) pada teks berurutan**, seperti kalimat atau dokumen, yang telah direpresentasikan dalam bentuk **word embeddings**.

Berbeda dari pendekatan oversampling biasa, CT-VeeGAN **tidak hanya menyeimbangkan jumlah data**, tetapi juga **menjaga struktur urutan kata** agar data sintetis tetap realistis secara semantik dan temporal.

---

## 🔎 Masalah yang Diselesaikan

| Metode              | Kelemahan                          |
| ------------------- | ---------------------------------- |
| SMOTE standar       | Merusak struktur urutan (sequence) |
| GAN teks biasa      | Sulit stabil, sering mode collapse |
| Random oversampling | Duplikasi data → overfitting       |

**CT-VeeGAN** menggabungkan keunggulan **SMOTEENN + GAN berbasis LSTM** untuk mengatasi semua kelemahan tersebut.

---

## 🧠 Konsep Utama

CT-VeeGAN menggunakan **pendekatan hibrida dua tahap**:

1. **SMOTEENN**
   Menyeimbangkan distribusi data secara statistik (global).

2. **LSTM-GAN (WGAN-GP)**
   Merekonstruksi ulang urutan kata agar:

   * koheren
   * memiliki korelasi temporal
   * tidak sekadar duplikat

---

## 📦 Fitur Utama

CT-VeeGAN terdiri dari **tiga komponen inti**:

---

### A. Wrapper (`wrapper.py`) — *Penggunaan Instan*

> **Gunakan ini jika ingin hasil cepat tanpa training ulang**

Fungsi utama:

* `balance()`

Fitur:

* 🔽 Auto-download model pretrained (Bahasa Indonesia)
* 🔄 Alur otomatis:

  ```
  Sequence → Flatten → SMOTEENN → Latent Reconstruction → LSTM Generator
  ```

Cocok jika:

* Seq_Len = **105**
* Token_Dim = **400**
* Menggunakan embedding Word2Vec/FastText serupa

---

### B. Trainer (`trainer.py`) — *Pelatihan Kustom*

> **Gunakan ini jika dimensi data berbeda**

Fitur:

* Training dari nol
* Fine-tuning model lama
* Auto-save checkpoint terbaik

Wajib digunakan jika:

* Token dimension ≠ 400 (misal BERT 768)
* Panjang sequence ≠ 105
* Dataset sangat spesifik

---

### C. Utilities (`utils.py`) — *Pendukung*

Fungsi penting:

* Vector → Text (cosine similarity)
* Gradient Penalty (WGAN-GP)
* Helper evaluasi

---

## ⚙️ Instalasi

```bash
pip install torch numpy scikit-learn imbalanced-learn gensim tqdm requests datasets
```

---

## ⚠️ Persiapan Data (WAJIB)

CT-VeeGAN **tidak menerima teks mentah**.

### Format Input yang Benar

```text
(N, Seq_Len, Token_Dim)
```

| Parameter | Arti                              |
| --------- | --------------------------------- |
| N         | Jumlah kalimat                    |
| Seq_Len   | Panjang kalimat (setelah padding) |
| Token_Dim | Dimensi embedding                 |

### Contoh

```python
X.shape = (1000, 105, 400)
```

---

## 🔄 Cara Kerja CT-VeeGAN

1️⃣ **Vectorization**
Kalimat → Word embeddings

2️⃣ **Flattening**
Data 3D → 2D agar kompatibel dengan SMOTE

3️⃣ **SMOTEENN**
Menyeimbangkan kelas secara statistik

4️⃣ **Reconstruction Network**
Mengubah data sintetis kasar → latent vector

5️⃣ **LSTM Generator**
Latent → sequence kalimat yang koheren

---

## 🧪 Tutorial 1 — Penggunaan Cepat (Wrapper)

Gunakan jika **dimensi data sama dengan model pretrained**.

```python
import numpy as np
from ct_veegan.wrapper import CTVeeGANWrapper

X_train = np.random.randn(100, 105, 400).astype(np.float32)
y_train = np.array([0]*90 + [1]*10)

ct_gan = CTVeeGANWrapper(
    seq_len=105,
    token_dim=400,
    device='cuda'
)

X_final, y_final, mask = ct_gan.balance(
    X_train=X_train,
    y_train=y_train,
    minor_class=1,
    noise_scale=0.05
)
```

📌 **Output**:

* `X_final`: data asli + sintetis
* `y_final`: label baru
* `mask`: penanda data sintetis

---

## 🧪 Tutorial 2 — Training Kustom (Trainer)

Gunakan jika:

* BERT embedding
* Seq len berbeda
* Dataset domain khusus

```python
from ct_veegan.trainer import Trainer
from ct_veegan.models import LSTMGenerator, LSTMDiscriminator

trainer = Trainer(lr_g=1e-4)

trainer.G = LSTMGenerator(
    latent_dim=128,
    latent_step_dim=32,
    num_classes=2,
    embed_dim=32,
    seq_len=50,
    token_dim=768,
    hidden_dim=256
).to(trainer.device)

trainer.D = LSTMDiscriminator(
    num_classes=2,
    embed_dim=32,
    seq_len=50,
    token_dim=768,
    hidden_dim=256
).to(trainer.device)

trainer.train(dataloader, epochs=50)
```

---

## 📊 Validasi Kualitas Data Sintetis

✅ **Disarankan**:

* PCA / t-SNE visualization
* Uji klasifikasi downstream
* Bandingkan recall kelas minoritas

❌ **Hindari**:

* Menggunakan data sintetis untuk test set
* Noise terlalu besar

---

## ⚠️ Error Umum & Solusi

| Error           | Penyebab                        |
| --------------- | ------------------------------- |
| `size mismatch` | seq_len / token_dim tidak cocok |
| GAN collapse    | noise terlalu kecil             |
| Data rusak      | noise terlalu besar             |

---

## 📂 Struktur Proyek

```
project_root/
├── ct_veegan/
│   ├── models.py
│   ├── trainer.py
│   ├── wrapper.py
│   └── utils.py
├── checkpoints/
├── script_saya.py
└── requirements.txt
```

---

## 🙏 Kredit

Dikembangkan untuk penelitian penanganan **data teks Bahasa Indonesia yang tidak seimbang**.

Pretrained model:
**github.com/Benylaode/ct_veegans**


