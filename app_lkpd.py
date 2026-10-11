"""
🔎 MATH DETECTIVE — LKPD Interaktif Noir & Jazz Edition
Menemukan Rumus Suku ke-n Barisan Aritmatika
=================================================================

Cara menjalankan:
    pip install streamlit numpy
    streamlit run app_lkpd.py

Struktur LKPD (1 langkah = 1 halaman):
    Halaman 1   Sampul & Identitas
    Halaman 2   Petunjuk, Tujuan & Orientasi Masalah
    Halaman 3   Langkah 1 - Menentukan suku pertama (a)
    Halaman 4   Langkah 2 - Menentukan beda (b)
    Halaman 5   Langkah 3 - Menyusun rumus suku ke-n
    Halaman 6   Langkah 4 - Menggunakan rumus
    Halaman 7   Langkah 5 - Penalaran kritis
    Halaman 8   Langkah 6 - Masalah nyata: kursi bioskop
    Halaman 9   Langkah 7 - Masalah nyata: menabung mandiri
    Halaman 10  Langkah 8 - Total tabungan (Sₙ)
    Halaman 11  Hasil, Kesimpulan & Refleksi
"""

import base64
import html
import os
import random
from datetime import datetime

import streamlit as st

# =========================================================
# KONFIGURASI HALAMAN & TEMA DETEKTIF NOIR KLASIK
# =========================================================

st.set_page_config(
    page_title="LKPD Math Detective - Barisan Aritmatika",
    page_icon="🔎",
    layout="centered",
)

st.markdown(
    """
<style>
/* Background aplikasi bertema ruang investigasi klasik (Noir/Sepia Gelap) */
.stApp {
    background: radial-gradient(circle at center, #1a1510 0%, #0d0a08 100%);
    color: #e2d9cc;
    font-family: 'Courier New', Courier, monospace;
}

/* Container utama bergaya Map Kasus Rahasia (Casefile) */
.block-container {
    max-width: 950px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    background: rgba(28, 23, 18, 0.92);
    backdrop-filter: blur(8px);
    border-radius: 12px;
    border: 2px solid #3d3024;
    box-shadow: 0 0 35px rgba(0, 0, 0, 0.9), inset 0 0 15px rgba(212, 175, 55, 0.05);
}

/* Judul & Subjudul bertema Detektif */
.main-title {
    text-align: center; font-size: 36px; font-weight: 900;
    color: #d4af37; letter-spacing: 3px;
    text-shadow: 0 0 12px rgba(212, 175, 55, 0.4);
    font-family: 'Georgia', serif; margin-bottom: 2px;
}
.subtitle {
    text-align: center; font-size: 15px; color: #a39585;
    font-style: italic; margin-bottom: 14px;
}

/* Tag & Elemen Papan Bukti */
.lkpd-tag {
    display: inline-block; padding: 4px 16px; border-radius: 4px;
    background: #8b0000; color: #f5e6d3; font-size: 13px; font-weight: 800;
    letter-spacing: 1.5px; margin-bottom: 6px; border: 1px solid #b22222;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.6);
}
.sequence-box {
    padding: 22px; border-radius: 8px; text-align: center;
    font-size: 30px; font-weight: 800; margin: 14px 0;
    border: 2px dashed #d4af37; background: rgba(212, 175, 55, 0.06);
    color: #f3e5ab; font-family: 'Courier New', monospace; letter-spacing: 2px;
}
.kartu {
    padding: 16px 20px; border-radius: 6px; margin: 12px 0;
    border-left: 5px solid #d4af37; background: #241d17;
    color: #d9ceb2; line-height: 1.6; box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}
.progress-text { text-align: center; font-size: 14px; color: #8c7d6b; margin-bottom: 4px; }

/* Custom Sidebar Tema Detektif */
[data-testid="stSidebar"] {
    background-color: #120e0b !important;
    border-right: 1px solid #2d231b;
}

/* Custom Tombol / Button */
.stButton>button {
    background: linear-gradient(180deg, #3a2e22 0%, #241c14 100%) !important;
    color: #d4af37 !important;
    border: 1px solid #6b553d !important;
    font-weight: bold !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}
.stButton>button:hover {
    background: #d4af37 !important;
    color: #120e0b !important;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.5) !important;
}

@media (max-width: 600px) {
    .main-title { font-size: 26px; }
    .sequence-box { font-size: 20px; padding: 14px; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# DATA
# =========================================================

SOAL = [
    {"nama": "Barisan 1", "a": 3, "b": 3},
    {"nama": "Barisan 2", "a": 5, "b": 4},
    {"nama": "Barisan 3", "a": 7, "b": 5},
    {"nama": "Barisan 4", "a": 10, "b": 2},
    {"nama": "Barisan 5", "a": 12, "b": 6},
    {"nama": "Barisan 6", "a": 4, "b": 7},
    {"nama": "Barisan 7", "a": 8, "b": 3},
    {"nama": "Barisan 8", "a": 15, "b": 5},
    {"nama": "Barisan 9", "a": 6, "b": 8},
    {"nama": "Barisan 10", "a": 20, "b": 4},
    {"nama": "Barisan 11", "a": 9, "b": 6},
    {"nama": "Barisan 12", "a": 11, "b": 3},
]

POIN = {
    "jawab_a": 10,
    "jawab_b": 10,
    "jawab_rumus": 20,
    "jawab_suku": 20,
    "jawab_uji": 20,
    "jawab_kursi": 20,
    "jawab_tabung": 20,
    "jawab_sn": 30,
}
LABEL_TAHAP = {
    "jawab_a": "Langkah 1 - Suku pertama (a)",
    "jawab_b": "Langkah 2 - Beda (b)",
    "jawab_rumus": "Langkah 3 - Rumus suku ke-n",
    "jawab_suku": "Langkah 4 - Menghitung Uₙ",
    "jawab_uji": "Langkah 5 - Penalaran kritis",
    "jawab_kursi": "Langkah 6 - Kursi bioskop",
    "jawab_tabung": "Langkah 7 - Menabung mandiri",
    "jawab_sn": "Langkah 8 - Total tabungan (Sₙ)",
}
SKOR_MAKS_MISI = sum(POIN.values())
TOTAL_HALAMAN = 11

# =========================================================
# FUNGSI BANTU
# =========================================================

_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def sub(n):
    """Angka -> subskrip unicode, mis. 3 -> ₃."""
    return str(n).translate(_SUB)


def buat_barisan(a, b, jumlah=5):
    return [a + i * b for i in range(jumlah)]


def rumus_latex(a, b):
    """U_n = bn + (a-b) dalam bentuk paling sederhana."""
    k = a - b
    if b == 0:
        return f"U_n = {k}"
    suku_n = "n" if b == 1 else "-n" if b == -1 else f"{b}n"
    if k == 0:
        return f"U_n = {suku_n}"
    return f"U_n = {suku_n} + {k}" if k > 0 else f"U_n = {suku_n} - {abs(k)}"


def rumus_teks(a, b):
    return rumus_latex(a, b).replace("U_n", "Uₙ")


def rumus_ruas_kanan(a, b):
    return rumus_latex(a, b).split("= ", 1)[1]


def kotak_barisan(urutan):
    st.markdown(
        f'<div class="sequence-box">{", ".join(map(str, urutan))}, ...</div>',
        unsafe_allow_html=True,
    )


def judul_langkah(tag, judul):
    st.markdown(f'<span class="lkpd-tag">{tag}</span>', unsafe_allow_html=True)
    st.header(judul)


def kartu(teks):
    st.markdown(f'<div class="kartu">{teks}</div>', unsafe_allow_html=True)


def tampil_svg(svg, maks=780):
    """Menampilkan ilustrasi SVG (disematkan sebagai gambar base64)."""
    data = base64.b64encode(svg.encode("utf-8")).decode()
    st.markdown(
        f'<div style="text-align:center;margin:10px 0">'
        f'<img alt="ilustrasi" src="data:image/svg+xml;base64,{data}" '
        f'style="width:100%;max-width:{maks}px;border-radius:10px;border:1px solid #3d3024;"></div>',
        unsafe_allow_html=True,
    )


# =========================================================
# ILUSTRASI (SVG dibuat langsung dari Python, tanpa file gambar)
# =========================================================

def svg_sampul():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 260" font-family="Georgia, serif">
<rect width="800" height="260" rx="12" fill="#140f0c"/>
<path d="M0 0 L800 260 L0 260 Z" fill="#0d0a08" opacity="0.6"/>
<text x="40" y="85" font-size="18" fill="#8b0000" font-weight="900" letter-spacing="4">CONFIDENTIAL CASE FILE</text>
<text x="40" y="145" font-size="44" fill="#d4af37" font-weight="800">MATH DETECTIVE</text>
<text x="40" y="185" font-size="20" fill="#a39585" font-style="italic">Pecahkan misteri rumus suku ke-n Barisan Aritmatika</text>
<circle cx="640" cy="130" r="75" fill="none" stroke="#d4af37" stroke-width="6" opacity="0.4"/>
<line x1="695" y1="185" x2="755" y2="245" stroke="#d4af37" stroke-width="14" stroke-linecap="round"/>
<text x="640" y="125" text-anchor="middle" fill="#d4af37" font-size="22" font-weight="700">a + (n−1)b</text>
<text x="640" y="155" text-anchor="middle" fill="#8b0000" font-size="18" font-weight="900">Uₙ = ?</text>
</svg>"""


def svg_kasus(urutan):
    kotak = ""
    for i, v in enumerate(urutan):
        x = 372 + i * 68
        kotak += (
            f'<rect x="{x}" y="82" width="58" height="58" rx="8" fill="#241d17" stroke="#d4af37" stroke-width="2"/>'
            f'<text x="{x + 29}" y="119" text-anchor="middle" font-size="22" font-weight="700" fill="#d4af37">{v}</text>'
        )
    x = 372 + len(urutan) * 68
    kotak += (
        f'<rect x="{x}" y="82" width="58" height="58" rx="8" fill="#8b0000" stroke="#b22222" stroke-width="2"/>'
        f'<text x="{x + 29}" y="123" text-anchor="middle" font-size="32" font-weight="800" fill="#fff">?</text>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Courier New, monospace">
<rect width="800" height="300" rx="12" fill="#120e0b"/>
<rect x="40" y="40" width="300" height="220" rx="12" fill="#1c1712" stroke="#3d3024" stroke-width="4"/>
<circle cx="190" cy="150" r="58" fill="#0d0a08" stroke="#d4af37" stroke-width="5"/>
<circle cx="190" cy="150" r="14" fill="#d4af37"/>
<rect x="184" y="98" width="12" height="38" rx="4" fill="#d4af37"/>
<text x="190" y="52" text-anchor="middle" font-size="14" fill="#a39585" font-weight="700">BRANKAS RAHASIA</text>
<text x="372" y="62" font-size="18" fill="#d4af37" font-weight="700">KODE PETUNJUK:</text>
{kotak}
<text x="372" y="190" font-size="16" fill="#d9ceb2">Kode berikutnya mengikuti pola tertentu.</text>
<text x="372" y="222" font-size="16" fill="#d9ceb2">Tugasmu: temukan rumus kode ke-n!</text>
<text x="372" y="252" font-size="15" fill="#a39585">Detektif, brankas menunggumu... 🔎</text>
</svg>"""


def svg_tangga(urutan):
    m = max(urutan)
    isi = ""
    for i, v in enumerate(urutan):
        h = 190 * v / m
        x = 50 + i * 145
        y = 250 - h
        warna = "#d4af37" if i == 0 else "#6b553d"
        label = f"U{sub(i + 1)}" + (" = a" if i == 0 else "")
        isi += (
            f'<rect x="{x}" y="{y:.1f}" width="100" height="{h:.1f}" rx="6" fill="{warna}"/>'
            f'<text x="{x + 50}" y="{y - 8:.1f}" text-anchor="middle" font-size="24" font-weight="700" fill="#f3e5ab">{v}</text>'
            f'<text x="{x + 50}" y="276" text-anchor="middle" font-size="18" font-weight="700" fill="#a39585">{label}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Courier New, monospace">
<rect width="800" height="300" rx="12" fill="#120e0b"/>
<line x1="30" y1="250" x2="770" y2="250" stroke="#3d3024" stroke-width="3"/>
{isi}
<text x="400" y="26" text-anchor="middle" font-size="15" fill="#a39585">Tinggi tiap batang = nilai suku. Batang emas adalah suku pertama.</text>
</svg>"""


def svg_loncatan(urutan, b=None):
    label = "+ ?" if b is None else (f"+ {b}" if b >= 0 else f"− {abs(b)}")
    xs = [90 + i * 155 for i in range(len(urutan))]
    y = 200
    isi = ""
    for i in range(len(urutan) - 1):
        x1, x2 = xs[i] + 22, xs[i + 1] - 26
        mid = (xs[i] + xs[i + 1]) / 2
        isi += (
            f'<path d="M{x1} {y - 30} Q{mid} {y - 135} {x2} {y - 30}" fill="none" '
            f'stroke="#d4af37" stroke-width="4" marker-end="url(#pa)"/>'
            f'<rect x="{mid - 34}" y="{y - 112}" width="68" height="30" rx="6" fill="#241d17" stroke="#d4af37" stroke-width="2"/>'
            f'<text x="{mid}" y="{y - 91}" text-anchor="middle" font-size="18" font-weight="800" fill="#d4af37">{label}</text>'
        )
    for i, (x, v) in enumerate(zip(xs, urutan)):
        warna = "#d4af37" if i == 0 else "#3a2e22"
        isi += (
            f'<circle cx="{x}" cy="{y}" r="36" fill="{warna}" stroke="#6b553d" stroke-width="3"/>'
            f'<text x="{x}" y="{y + 9}" text-anchor="middle" font-size="26" font-weight="800" fill="#f3e5ab">{v}</text>'
            f'<text x="{x}" y="{y + 66}" text-anchor="middle" font-size="17" font-weight="700" fill="#a39585">U{sub(i + 1)}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Courier New, monospace">
<defs><marker id="pa" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#d4af37"/></marker></defs>
<rect width="800" height="300" rx="12" fill="#120e0b"/>
{isi}
</svg>"""


def svg_mesin(rhs, masukan="n", keluaran="Uₙ"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 260" font-family="Courier New, monospace">
<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#a39585"/></marker></defs>
<rect width="800" height="260" rx="12" fill="#120e0b"/>
<text x="100" y="78" text-anchor="middle" font-size="16" fill="#a39585" font-weight="700">MASUKAN</text>
<rect x="40" y="92" width="120" height="80" rx="8" fill="#241d17" stroke="#3d3024" stroke-width="2"/>
<text x="100" y="146" text-anchor="middle" font-size="38" font-weight="800" fill="#d4af37">{masukan}</text>
<line x1="165" y1="132" x2="255" y2="132" stroke="#a39585" stroke-width="4" marker-end="url(#ar)"/>
<rect x="260" y="40" width="280" height="180" rx="12" fill="#1c1712" stroke="#d4af37" stroke-width="3"/>
<text x="400" y="84" text-anchor="middle" font-size="16" fill="#d4af37" font-weight="700" letter-spacing="2">MESIN RUMUS</text>
<rect x="290" y="105" width="220" height="60" rx="8" fill="#241d17"/>
<text x="400" y="146" text-anchor="middle" font-size="26" font-weight="800" fill="#f3e5ab">{rhs}</text>
<text x="400" y="200" text-anchor="middle" font-size="14" fill="#a39585">nomor suku masuk, nilai suku keluar</text>
<line x1="545" y1="132" x2="635" y2="132" stroke="#a39585" stroke-width="4" marker-end="url(#ar)"/>
<text x="700" y="78" text-anchor="middle" font-size="16" fill="#a39585" font-weight="700">KELUARAN</text>
<rect x="640" y="92" width="120" height="80" rx="8" fill="#8b0000" stroke="#b22222" stroke-width="2"/>
<text x="700" y="146" text-anchor="middle" font-size="38" font-weight="800" fill="#fff">{keluaran}</text>
</svg>"""


def svg_grafik(a, b, n_max=8):
    x0, x1, y0, ytop = 80, 760, 290, 50
    vmax = a + (n_max - 1) * b
    sx = (x1 - x0) / (n_max + 1)
    pts = []
    for n in range(1, n_max + 1):
        v = a + (n - 1) * b
        pts.append((x0 + n * sx, y0 - v / vmax * (y0 - ytop), n, v))
    garis = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in pts)
    isi = ""
    for x, y, n, v in pts:
        warna = "#d4af37" if n == 1 else "#3a2e22"
        isi += (
            f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y:.1f}" stroke="#6b553d" stroke-width="1.5" stroke-dasharray="4 4"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{warna}" stroke="#6b553d" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y - 16:.1f}" text-anchor="middle" font-size="16" font-weight="700" fill="#d4af37">{v}</text>'
            f'<text x="{x:.1f}" y="{y0 + 24}" text-anchor="middle" font-size="16" fill="#a39585">{n}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 340" font-family="Courier New, monospace">
<rect width="800" height="340" rx="12" fill="#120e0b"/>
<line x1="{x0}" y1="{y0}" x2="775" y2="{y0}" stroke="#3d3024" stroke-width="3"/>
<line x1="{x0}" y1="{y0}" x2="{x0}" y2="30" stroke="#3d3024" stroke-width="3"/>
<text x="775" y="{y0 + 24}" font-size="18" font-weight="700" fill="#a39585">n</text>
<text x="{x0 + 8}" y="30" font-size="18" font-weight="700" fill="#a39585">Uₙ</text>
<polyline points="{garis}" fill="none" stroke="#d4af37" stroke-width="3"/>
{isi}
<text x="400" y="334" text-anchor="middle" font-size="15" fill="#a39585">Titik-titik suku barisan aritmatika selalu naik secara teratur (garis lurus).</text>
</svg>"""


def svg_lup(n1, n2):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 220" font-family="Courier New, monospace">
<rect width="800" height="220" rx="12" fill="#120e0b"/>
<circle cx="120" cy="100" r="56" fill="none" stroke="#d4af37" stroke-width="10"/>
<line x1="160" y1="142" x2="205" y2="187" stroke="#d4af37" stroke-width="14" stroke-linecap="round"/>
<text x="120" y="118" text-anchor="middle" font-size="52" font-weight="800" fill="#d4af37">?</text>
<text x="500" y="62" text-anchor="middle" font-size="20" fill="#a39585" font-weight="700">Dua angka mencurigakan:</text>
<rect x="290" y="82" width="170" height="70" rx="8" fill="#241d17" stroke="#3d3024" stroke-width="2"/>
<text x="375" y="130" text-anchor="middle" font-size="40" font-weight="800" fill="#d4af37">{n1}</text>
<rect x="520" y="82" width="170" height="70" rx="8" fill="#8b0000" stroke="#b22222" stroke-width="2"/>
<text x="605" y="130" text-anchor="middle" font-size="40" font-weight="800" fill="#fff">{n2}</text>
<text x="500" y="190" text-anchor="middle" font-size="18" fill="#a39585">Mana yang benar-benar suku barisan?</text>
</svg>"""


def svg_piala():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 260" font-family="Georgia, serif">
<rect width="800" height="260" rx="12" fill="#140f0c"/>
<text x="400" y="130" text-anchor="middle" font-size="72" fill="#d4af37">★</text>
<text x="400" y="210" text-anchor="middle" font-size="28" font-weight="800" fill="#f3e5ab" letter-spacing="4">MISI SELESAI!</text>
</svg>"""


# =========================================================
# STATE & LOGIKA
# =========================================================

def pindah_halaman(nomor):
    st.session_state.halaman = nomor
    st.rerun()


# ---------- Pencatatan jawaban & analisis kesalahan ----------

def _f(x):
    return str(x)


def item(label, jawab, benar, ok, catatan="", f=_f):
    """Satu butir jawaban siswa yang akan dibahas di bagian Refleksi."""
    return {
        "label": label,
        "jawab": f(jawab),
        "benar": f(benar),
        "ok": bool(ok),
        "catatan": catatan,
    }


def catat(kunci, daftar, masukan):
    """Menyimpan jawaban terkirim. Boleh dikirim ulang sebelum lanjut."""
    rekam = st.session_state.rekam
    lama = rekam.get(kunci, {})
    jumlah_ok = sum(1 for d in daftar if d["ok"])
    poin = round(POIN[kunci] * jumlah_ok / len(daftar))
    selisih = poin - lama.get("poin", 0)
    st.session_state.skor_misi += selisih
    st.session_state.skor_total += selisih
    rekam[kunci] = {
        "items": daftar,
        "poin": poin,
        "kirim": lama.get("kirim", 0) + 1,
        "masukan": masukan,
    }
    st.session_state[kunci] = True


def awal(kunci, nama, default=0):
    """Nilai terakhir yang dikirim siswa (untuk mengisi kembali kolom)."""
    return st.session_state.rekam.get(kunci, {}).get("masukan", {}).get(nama, default)


def info_terkirim(kunci):
    if st.session_state[kunci]:
        st.success(
            "📨 Jawabanmu sudah terkirim! Kamu boleh mengubahnya lalu kirim "
            "lagi, atau lanjut ke langkah berikutnya. Benar atau salahnya "
            "akan dibahas di bagian **Refleksi** pada akhir LKPD."
        )


def ab_siswa():
    """a dan b yang dikirim siswa pada Langkah 1 dan 2."""
    return awal("jawab_a", "a", 0), awal("jawab_b", "b", 0)


def rumus_siswa():
    """(koefisien n, konstanta) yang dikirim siswa pada Langkah 3."""
    return awal("jawab_rumus", "koef", 0), awal("jawab_rumus", "konst", 0)


# ---------- Diagnosis letak kesalahan (kesalahan umum) ----------

def cat_a(v, a, b, f=_f):
    benar = f"Suku pertama a = U₁ adalah angka paling awal pada barisan, yaitu {f(a)}."
    if v == 0:
        return "Bagian ini belum kamu isi (nilainya masih 0). " + benar
    if v == a + b:
        return "Kamu menulis suku kedua (U₂). " + benar
    if v == b:
        return "Kamu menulis beda (b), padahal yang ditanyakan suku pertama (a). " + benar
    return benar


def cat_b(v, a, b, f=_f):
    benar = f"Beda b = U₂ − U₁ = {f(a + b)} − {f(a)} = {f(b)}."
    if v == 0:
        return "Bagian ini belum kamu isi (nilainya masih 0). " + benar
    if v == -b:
        return ("Tandanya terbalik: beda dihitung dari suku berikutnya dikurangi "
                "suku sebelumnya (U₂ − U₁). " + benar)
    if v == a:
        return "Kamu menulis suku pertama (a), padahal beda adalah selisih dua suku berurutan. " + benar
    if v == a + b:
        return "Kamu menulis suku kedua (U₂), bukan selisihnya. " + benar
    return benar


def cat_koef(v, a, b, f=_f):
    benar = f"Karena (n − 1)b dijabarkan menjadi bn − b, koefisien n adalah b = {f(b)}."
    if v == 0:
        return "Bagian ini belum kamu isi (nilainya masih 0). " + benar
    if v == a:
        return "Kamu menulis a sebagai koefisien n. " + benar
    return benar


def cat_konst(v, a, b, f=_f):
    benar = f"Konstanta = a − b = {f(a)} − {f(b)} = {f(a - b)}."
    if v == 0:
        return "Bagian ini belum kamu isi (nilainya masih 0). " + benar
    if v == a:
        return ("Kamu belum menggabungkan −b hasil penjabaran (n − 1)b dengan a. " + benar)
    if v == a + b:
        return ("Tanda b keliru: (n − 1)b = bn − b, sehingga b dikurangkan, bukan ditambahkan. "
                + benar)
    if v == -b:
        return "Kamu hanya menulis −b dan lupa menambahkan a. " + benar
    return benar


def cat_un(v, a, b, n, f=_f):
    k = a - b
    hasil = b * n + k
    benar = (f"Substitusikan n = {n} ke Uₙ = {b}n + ({k}): "
             f"{b} × {n} + ({k}) = {f(hasil)}.")
    if v == 0:
        return "Bagian ini belum kamu isi (nilainya masih 0). " + benar
    if v == a + n * b:
        return "Kamu memakai n, bukan (n − 1), sehingga hasilnya lebih besar satu beda. " + benar
    if v == b * n:
        return "Kamu lupa menambahkan konstanta pada rumus. " + benar
    return benar


def cat_n(v, a, b, n_target, f=_f):
    k = a - b
    nilai = a + (n_target - 1) * b
    benar = (f"Susun {b}n + ({k}) = {f(nilai)}, lalu "
             f"n = ({nilai} − ({k})) ÷ {b} = {n_target}.")
    if v == 0:
        return "Bagian ini belum kamu isi (nilainya masih 0). " + benar
    if abs(v - n_target) == 1:
        return "Jawabanmu selisih satu dari yang benar. Cek dengan memasukkan n ke rumus. " + benar
    return benar


# ---------- Pembahasan di bagian Refleksi ----------

def status_langkah(kunci):
    """(jumlah butir benar, jumlah butir) atau None jika belum dikerjakan."""
    r = st.session_state.rekam.get(kunci)
    if not r:
        return None
    return sum(1 for d in r["items"] if d["ok"]), len(r["items"])


def tampil_pembahasan():
    rekam = st.session_state.rekam

    baris = ["| Langkah | Hasil | Poin |", "|---|---|---|"]
    for kunci in POIN:
        st_ = status_langkah(kunci)
        if st_ is None:
            hasil, poin = "⏭️ belum dikerjakan", 0
        else:
            ok, n = st_
            hasil = "✅ benar semua" if ok == n else (
                f"⚠️ {ok} dari {n} bagian benar" if ok else "❌ belum tepat")
            poin = rekam[kunci]["poin"]
        baris.append(f"| {LABEL_TAHAP[kunci]} | {hasil} | {poin} / {POIN[kunci]} |")
    st.markdown("\n".join(baris))

    ada_salah = False
    for kunci in POIN:
        r = rekam.get(kunci)
        if not r:
            continue
        salah = [d for d in r["items"] if not d["ok"]]
        if not salah:
            continue
        ada_salah = True
        with st.expander(
            f"❌ {LABEL_TAHAP[kunci]} — {len(salah)} bagian perlu diperbaiki",
            expanded=True,
        ):
            for d in salah:
                st.markdown(f"**{d['label']}**")
                st.markdown(
                    f"- Jawabanmu: `{d['jawab']}`\n"
                    f"- Jawaban yang benar: `{d['benar']}`\n"
                    f"- 💡 **Letak kesalahan:** {d['catatan']}"
                )
    if not ada_salah:
        st.success("🎉 Semua jawabanmu benar. Pertahankan caramu bernalar!")
    return ada_salah


def reset_misi():
    for kunci in POIN:
        st.session_state[kunci] = False
    for kunci in ("hint_a", "hint_b", "hint_rumus", "hint_uji",
                  "hint_kursi", "hint_tabung", "hint_sn"):
        st.session_state[kunci] = False
    st.session_state.skor_misi = 0
    st.session_state.rekam = {}
    st.session_state.uji = None
    st.session_state.konteks = None
    st.session_state.misi_dihitung = False
    st.session_state.refleksi = ""
    st.session_state.perbaikan = ""
    st.session_state.refleksi_selesai = False
    for kunci in ("in_a", "in_b", "in_koef", "in_konst", "in_n", "in_suku",
                  "in_uji_a", "in_uji_b"):
        st.session_state.pop(kunci, None)
    for kasus in ("kursi", "tabung"):
        for butir in ("a", "b", "koef", "konst", "un", "n"):
            st.session_state.pop(f"in_{kasus}_{butir}", None)
    for butir in ("p", "q", "s6", "un", "sn", "tc"):
        st.session_state.pop(f"in_sn_{butir}", None)


def tombol_petunjuk(flag_hint, flag_jawab, label="💡 Minta Petunjuk"):
    if not st.session_state[flag_jawab]:
        if st.button(label, key=f"btn_{flag_hint}"):
            st.session_state[flag_hint] = True


def navigasi(kembali_ke, lanjut_ke, terbuka, label_kembali="⬅️ Kembali",
             label_lanjut="➡️ Langkah Berikutnya", aksi_lanjut=None):
    st.markdown("---")
    kol1, kol2 = st.columns(2)
    with kol1:
        if st.button(label_kembali, use_container_width=True, key="nav_kembali"):
            pindah_halaman(kembali_ke)
    with kol2:
        if terbuka:
            if st.button(label_lanjut, use_container_width=True, key="nav_lanjut"):
                if aksi_lanjut:
                    aksi_lanjut()
                pindah_halaman(lanjut_ke)
        else:
            st.button(f"🔒 {label_lanjut.split(' ', 1)[-1]}", disabled=True,
                      use_container_width=True, key="nav_kunci")


# ---------- Soal kehidupan nyata ----------

def rupiah(x):
    """10000 -> 'Rp10.000'"""
    return "Rp" + f"{x:,}".replace(",", ".")


def ambil_konteks():
    """Data soal kehidupan nyata: diacak sekali, tetap selama satu misi."""
    if st.session_state.konteks is None:
        baris = random.randint(8, 12)
        st.session_state.konteks = {
            "kursi": {
                "a": random.choice([8, 10, 12, 14]),
                "b": random.choice([2, 3, 4]),
                "n_tanya": baris,
                "n_cari": random.randint(4, baris - 1),
            },
            "tabung": {
                "a": random.choice([10000, 15000, 20000]),
                "b": random.choice([2000, 3000, 5000]),
                "n_tanya": random.randint(8, 12),
                "n_cari": random.randint(13, 20),
            },
        }
    return st.session_state.konteks


def svg_bioskop(a, b):
    isi = ""
    for i in range(4):
        jml = a + i * b
        y = 100 + i * 46
        x_awal = 400 - jml * 20 / 2
        for j in range(jml):
            x = x_awal + j * 20
            isi += (
                f'<rect x="{x:.1f}" y="{y}" width="16" height="16" rx="4" fill="#ef4444"/>'
                f'<rect x="{x + 2:.1f}" y="{y - 3}" width="12" height="5" rx="2" fill="#b91c1c"/>'
            )
        isi += (
            f'<text x="40" y="{y + 14}" font-size="16" font-weight="700" fill="#e0e7ff">Baris {i + 1}</text>'
            f'<text x="760" y="{y + 14}" text-anchor="end" font-size="16" fill="#fde68a">{jml} kursi</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Arial, sans-serif">
<rect width="800" height="300" rx="22" fill="#1e1b4b"/>
<path d="M200 20 L600 20 L640 68 L160 68 Z" fill="#e2e8f0"/>
<text x="400" y="52" text-anchor="middle" font-size="22" font-weight="800" fill="#1e1b4b" letter-spacing="6">LAYAR</text>
{isi}
<text x="400" y="284" text-anchor="middle" font-size="16" fill="#c7d2fe">⋮  baris-baris berikutnya bertambah dengan pola yang sama</text>
</svg>"""


def svg_tabungan(a, b):
    vmax = a + 4 * b
    batang = ""
    for i in range(5):
        v = a + i * b
        h = 150 * v / vmax
        x = 300 + i * 95
        y = 230 - h
        batang += (
            f'<rect x="{x}" y="{y:.1f}" width="64" height="{h:.1f}" rx="8" fill="#f59e0b"/>'
            f'<circle cx="{x + 32}" cy="{y:.1f}" r="15" fill="#fde68a" stroke="#d97706" stroke-width="3"/>'
            f'<text x="{x + 32}" y="{y + 5:.1f}" text-anchor="middle" font-size="13" font-weight="800" fill="#b45309">Rp</text>'
            f'<text x="{x + 32}" y="{y - 24:.1f}" text-anchor="middle" font-size="16" font-weight="700" fill="#9a3412">{v // 1000}rb</text>'
            f'<text x="{x + 32}" y="254" text-anchor="middle" font-size="15" fill="#475569">Mgg {i + 1}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Arial, sans-serif">
<rect width="800" height="300" rx="22" fill="#fdf2f8"/>
<ellipse cx="130" cy="165" rx="76" ry="56" fill="#f9a8d4" stroke="#ec4899" stroke-width="4"/>
<polygon points="95,122 108,88 136,120" fill="#ec4899"/>
<ellipse cx="202" cy="172" rx="22" ry="17" fill="#f472b6" stroke="#ec4899" stroke-width="3"/>
<circle cx="196" cy="172" r="3" fill="#9d174d"/><circle cx="208" cy="172" r="3" fill="#9d174d"/>
<circle cx="166" cy="146" r="6" fill="#1f2937"/>
<rect x="84" y="206" width="24" height="32" rx="6" fill="#ec4899"/>
<rect x="150" y="206" width="24" height="32" rx="6" fill="#ec4899"/>
<path d="M56 160 q-26 -10 -10 -32" fill="none" stroke="#ec4899" stroke-width="5" stroke-linecap="round"/>
<rect x="108" y="116" width="44" height="8" rx="4" fill="#9d174d"/>
<circle cx="130" cy="86" r="15" fill="#fde68a" stroke="#d97706" stroke-width="3"/>
<text x="130" y="91" text-anchor="middle" font-size="13" font-weight="800" fill="#b45309">Rp</text>
<text x="130" y="275" text-anchor="middle" font-size="18" font-weight="800" fill="#9d174d">Tabunganku</text>
<line x1="270" y1="230" x2="780" y2="230" stroke="#64748b" stroke-width="3"/>
<text x="525" y="30" text-anchor="middle" font-size="16" fill="#9a3412">Setoran tiap minggu naik secara teratur</text>
{batang}
</svg>"""


def halaman_masalah(kunci, tag, judul, svg, cerita, c, fmt, tanya_un,
                    tanya_n, sebelum, sesudah, step=1,
                    label_lanjut="➡️ Langkah Berikutnya", aksi_lanjut=None):
    """Satu halaman soal cerita barisan aritmatika (kursi & tabungan).

    c = {"a", "b", "n_tanya", "n_cari"}; fmt = fungsi penampil nilai.
    Jawaban dikirim apa adanya; pembahasan benar-salah ada di Refleksi.
    """
    flag = f"jawab_{kunci}"
    a_, b_ = c["a"], c["b"]
    k_ = a_ - b_
    n_tanya, n_cari = c["n_tanya"], c["n_cari"]
    un_tanya = a_ + (n_tanya - 1) * b_
    batas = 100_000_000

    judul_langkah(tag, judul)
    tampil_svg(svg)
    kartu(cerita)

    st.markdown("### ✏️ Lembar Jawaban")

    st.markdown("**1. Kenali polanya**")
    k1, k2 = st.columns(2)
    ia = k1.number_input("Suku pertama (a):", -batas, batas, awal(flag, "a"), step, key=f"in_{kunci}_a")
    ib = k2.number_input("Beda (b):", -batas, batas, awal(flag, "b"), step, key=f"in_{kunci}_b")

    st.markdown("**2. Susun rumus** dalam bentuk $U_n = bn + k$")
    k3, k4 = st.columns(2)
    ik = k3.number_input("Koefisien n (b):", -batas, batas, awal(flag, "koef"), step, key=f"in_{kunci}_koef")
    ikon = k4.number_input("Konstanta (k):", -batas, batas, awal(flag, "konst"), step, key=f"in_{kunci}_konst")

    st.markdown(f"**3.** {tanya_un}")
    iun = st.number_input("Jawabanmu:", -batas, batas, awal(flag, "un"), step, key=f"in_{kunci}_un")

    st.markdown(f"**4.** {tanya_n}")
    iN = st.number_input("Nilai n:", 0, 1000, awal(flag, "n"), 1, key=f"in_{kunci}_n")

    if st.button("📨 Kirim Jawaban", use_container_width=True, key=f"kirim_{kunci}"):
        catat(
            flag,
            [
                item("1a. Suku pertama (a)", ia, a_, ia == a_, cat_a(ia, a_, b_, fmt), fmt),
                item("1b. Beda (b)", ib, b_, ib == b_, cat_b(ib, a_, b_, fmt), fmt),
                item("2a. Koefisien n pada rumus", ik, b_, ik == b_, cat_koef(ik, a_, b_, fmt), fmt),
                item("2b. Konstanta pada rumus", ikon, k_, ikon == k_, cat_konst(ikon, a_, b_, fmt), fmt),
                item(f"3. {tanya_un}", iun, un_tanya, iun == un_tanya,
                     cat_un(iun, a_, b_, n_tanya, fmt), fmt),
                item(f"4. {tanya_n}", iN, n_cari, iN == n_cari, cat_n(iN, a_, b_, n_cari, fmt)),
            ],
            {"a": ia, "b": ib, "koef": ik, "konst": ikon, "un": iun, "n": iN},
        )

    info_terkirim(flag)

    tombol_petunjuk(f"hint_{kunci}", flag)
    if st.session_state[f"hint_{kunci}"] and not st.session_state[flag]:
        st.info(
            "Petunjuk: nilai pada urutan pertama adalah a, dan selisih dua "
            "urutan berdekatan adalah b. Gunakan $U_n = a + (n-1)b$. "
            "Untuk nomor 4, tulis $U_n$ sama dengan nilai yang ditanyakan, "
            "lalu cari $n$."
        )

    navigasi(sebelum, sesudah, st.session_state[flag],
             label_lanjut=label_lanjut, aksi_lanjut=aksi_lanjut)


def svg_pasangan(a, b, n=6):
    """Ilustrasi trik pasangan: suku pertama + terakhir = suku kedua + ke-(n-1) ..."""
    nilai = [a + i * b for i in range(n)]
    xs = [70 + i * 118 for i in range(n)]
    warna = ["#ef4444", "#f59e0b", "#10b981"]
    puncak = [50, 88, 126]
    isi = ""
    for k in range(n // 2):
        x1 = xs[k] + 45
        x2 = xs[n - 1 - k] + 45
        mid = (x1 + x2) / 2
        ctrl = 2 * puncak[k] - 190
        isi += (
            f'<path d="M{x1} 186 Q{mid} {ctrl} {x2} 186" fill="none" '
            f'stroke="{warna[k]}" stroke-width="5"/>'
            f'<rect x="{mid - 52}" y="{puncak[k] - 14}" width="104" height="28" rx="14" '
            f'fill="#ffffff" stroke="{warna[k]}" stroke-width="3"/>'
            f'<text x="{mid}" y="{puncak[k] + 5}" text-anchor="middle" font-size="14" '
            f'font-weight="800" fill="#0f172a">jumlah = ?</text>'
        )
    for i, (x, v) in enumerate(zip(xs, nilai)):
        w = warna[min(i, n - 1 - i)]
        isi += (
            f'<rect x="{x}" y="190" width="90" height="70" rx="14" fill="{w}"/>'
            f'<text x="{x + 45}" y="234" text-anchor="middle" font-size="26" '
            f'font-weight="800" fill="#ffffff">{v // 1000}rb</text>'
            f'<text x="{x + 45}" y="284" text-anchor="middle" font-size="15" '
            f'fill="#334155">Mgg {i + 1}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Arial, sans-serif">
<rect width="800" height="300" rx="22" fill="#f0f9ff"/>
<text x="400" y="24" text-anchor="middle" font-size="15" fill="#0369a1">Pasangkan minggu pertama dengan minggu terakhir, kedua dengan sebelum terakhir, dst.</text>
{isi}
</svg>"""


def putar_backsound():
    """Memutar musik jazz langsung dari URL online tanpa butuh file lokal."""
    st.caption("🎷 Backsound Jazz Online Aktif")
    # Link audio jazz bebas royalti
    jazz_url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
    
    audio_html = f"""
        <iframe src="{jazz_url}" allow="autoplay" id="audio" style="display:none"></iframe>
        <audio autoplay loop controls style="width: 100%; height: 40px; margin-top: 5px;">
            <source src="{jazz_url}" type="audio/mpeg">
            Browser kamu tidak mendukung pemutar audio.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def buat_lkpd_html():
    """Lembar hasil LKPD (cetak / simpan PDF dari browser)."""
    s = st.session_state
    e = html.escape
    d = SOAL[s.soal_index]
    a_, b_ = d["a"], d["b"]

    baris, detail = "", ""
    for kunci in POIN:
        st_ = status_langkah(kunci)
        if st_ is None:
            hasil, poin = "Belum dikerjakan", 0
        else:
            ok, n = st_
            hasil = "✅ Benar semua" if ok == n else f"{'⚠️' if ok else '❌'} {ok} dari {n} bagian benar"
            poin = s.rekam[kunci]["poin"]
        baris += (f"<tr><td>{e(LABEL_TAHAP[kunci])}</td><td>{hasil}</td>"
                  f"<td>{poin} / {POIN[kunci]}</td></tr>")
        if st_ is not None:
            for it in s.rekam[kunci]["items"]:
                if not it["ok"]:
                    detail += (
                        f"<div class='salah'><b>{e(LABEL_TAHAP[kunci])}</b><br>"
                        f"<b>{e(it['label'])}</b><br>"
                        f"Jawabanmu: <code>{e(it['jawab'])}</code> &nbsp;|&nbsp; "
                        f"Jawaban benar: <code>{e(it['benar'])}</code><br>"
                        f"💡 {e(it['catatan'])}</div>"
                    )
    if not detail:
        detail = "<p>🎉 Semua jawaban benar.</p>"

    refleksi = e(s.refleksi).replace("\n", "<br>") or "<i>(belum diisi)</i>"
    perbaikan = e(s.perbaikan).replace("\n", "<br>") or "<i>(belum diisi)</i>"
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"><title>LKPD Math Detective - {e(s.nama)}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 780px; margin: 30px auto; color: #0f172a; }}
h1 {{ color: #4c1d95; margin-bottom: 0; }}
h2 {{ color: #1e3a8a; border-bottom: 2px solid #c7d2fe; padding-bottom: 4px; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid #94a3b8; padding: 8px; text-align: left; }}
th {{ background: #e0e7ff; }}
.kotak {{ background: #eef2ff; padding: 12px 16px; border-radius: 10px; font-size: 20px; }}
.salah {{ background: #fef2f2; border-left: 5px solid #ef4444; padding: 10px 14px; margin: 10px 0; border-radius: 8px; }}
</style></head><body>
<h1>🔎 LKPD Math Detective</h1>
<p>Menemukan Rumus Suku ke-n dan Jumlah n Suku Pertama Barisan Aritmatika</p>
<table>
<tr><th>Nama</th><td>{e(s.nama)}</td><th>Kelas</th><td>{e(s.kelas)}</td></tr>
<tr><th>Tanggal</th><td>{datetime.now().strftime('%d-%m-%Y %H:%M')}</td><th>Barisan</th><td>{e(d['nama'])}</td></tr>
</table>
<h2>Barisan yang diselidiki</h2>
<div class="kotak">{', '.join(map(str, buat_barisan(a_, b_)))}, ...</div>
<p>Suku pertama (a) = <b>{a_}</b> &nbsp;|&nbsp; Beda (b) = <b>{b_}</b></p>
<div class="kotak">Uₙ = a + (n − 1)b → <b>{e(rumus_teks(a_, b_))}</b></div>
<h2>Rekap hasil</h2>
<table><tr><th>Langkah</th><th>Hasil</th><th>Poin</th></tr>{baris}
<tr><th>Total misi</th><th></th><th>{s.skor_misi} / {SKOR_MAKS_MISI}</th></tr></table>
<h2>Pembahasan: letak kesalahan</h2>
{detail}
<h2>Refleksi</h2>
<p>{refleksi}</p>
<h2>Rencana perbaikan</h2>
<p>{perbaikan}</p>
</body></html>""".encode("utf-8")


DEFAULTS = {
    "halaman": 1, "nama": "", "kelas": "", "soal_index": 0,
    "skor_misi": 0, "skor_total": 0, "misi_selesai": 0, "misi_dihitung": False,
    "jawab_a": False, "jawab_b": False, "jawab_rumus": False,
    "jawab_suku": False, "jawab_uji": False,
    "jawab_kursi": False, "jawab_tabung": False, "jawab_sn": False,
    "hint_a": False, "hint_b": False, "hint_rumus": False, "hint_uji": False,
    "hint_kursi": False, "hint_tabung": False, "hint_sn": False,
    "uji": None, "konteks": None, "rekam": {},
    "refleksi": "", "perbaikan": "", "refleksi_selesai": False,
}
for kunci, nilai in DEFAULTS.items():
    st.session_state.setdefault(kunci, nilai)

# Soal aktif
data = SOAL[st.session_state.soal_index]
a = data["a"]
b = data["b"]
konstanta = a - b
barisan = buat_barisan(a, b)
halaman = st.session_state.halaman

# =========================================================
# HEADER, PROGRESS, SIDEBAR
# =========================================================

st.markdown('<div class="main-title">🔎 MATH DETECTIVE</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">LKPD Eksplorasi Rumus Suku ke-n Barisan Aritmatika</div>',
    unsafe_allow_html=True,
)
st.progress((halaman - 1) / (TOTAL_HALAMAN - 1))
st.markdown(
    f'<div class="progress-text">Halaman {halaman} dari {TOTAL_HALAMAN}</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.checkbox("🎷 Backsound Jazz", value=True, key="musik_aktif")
    if st.session_state.musik_aktif:
        putar_backsound()
    st.markdown("---")
    st.title("🔎 Math Detective")
    st.markdown("---")
    if st.session_state.nama:
        st.write(f"👤 **{st.session_state.nama}**")
    if st.session_state.kelas:
        st.write(f"🏫 **{st.session_state.kelas}**")
    st.markdown("---")
    terkirim = sum(1 for k in POIN if st.session_state[k])
    st.metric("📨 Jawaban Terkirim", f"{terkirim} / {len(POIN)}")
    st.metric("🎯 Misi Selesai", st.session_state.misi_selesai)
    st.caption("Skor dan pembahasan kesalahan muncul di bagian Refleksi pada akhir LKPD.")
    st.markdown("---")
    st.write("### 🗂️ Tahapan LKPD")
    tahap = [
        (2, "Petunjuk & Masalah"),
        (3, "Langkah 1: Suku pertama"),
        (4, "Langkah 2: Beda"),
        (5, "Langkah 3: Rumus Uₙ"),
        (6, "Langkah 4: Hitung Uₙ"),
        (7, "Langkah 5: Penalaran kritis"),
        (8, "Langkah 6: Kursi bioskop"),
        (9, "Langkah 7: Menabung (Uₙ)"),
        (10, "Langkah 8: Total tabungan (Sₙ)"),
        (11, "Hasil & Refleksi"),
    ]
    for nomor, label in tahap:
        if halaman > nomor:
            st.write(f"✅ {label}")
        elif halaman == nomor:
            st.write(f"▶️ **{label}**")
        else:
            st.write(f"🔒 {label}")

# =========================================================
# HALAMAN 1 - SAMPUL & IDENTITAS
# =========================================================

if halaman == 1:
    tampil_svg(svg_sampul())

    st.header("🎯 Selamat Datang, Detektif Matematika!")
    st.write(
        "Lembar Kerja Peserta Didik (LKPD) ini membimbingmu menemukan "
        "**rumus suku ke-n barisan aritmatika** langkah demi langkah, "
        "seperti seorang detektif yang memecahkan kasus."
    )

    st.markdown("### 👤 Identitas Siswa")
    nama = st.text_input("Nama", value=st.session_state.nama)
    kelas = st.text_input(
        "Kelas", value=st.session_state.kelas, placeholder="Contoh: VIII A"
    )

    st.markdown("---")
    st.subheader("📚 Pilih Barisan Kasusmu")
    pilihan = st.selectbox(
        "Pilih barisan yang ingin diselidiki:",
        options=list(range(len(SOAL))),
        index=st.session_state.soal_index,
        format_func=lambda i: (
            f"{SOAL[i]['nama']} (Suku awal {SOAL[i]['a']}, naik {SOAL[i]['b']})"
        ),
    )
    kotak_barisan(buat_barisan(SOAL[pilihan]["a"], SOAL[pilihan]["b"]))

    if st.button("🚀 Mulai Misi", use_container_width=True):
        if not nama.strip():
            st.warning("Masukkan nama terlebih dahulu.")
        elif not kelas.strip():
            st.warning("Masukkan kelas terlebih dahulu.")
        else:
            st.session_state.nama = nama.strip()
            st.session_state.kelas = kelas.strip()
            st.session_state.soal_index = pilihan
            reset_misi()
            pindah_halaman(2)

# =========================================================
# HALAMAN 2 - PETUNJUK, TUJUAN, ORIENTASI MASALAH
# =========================================================

elif halaman == 2:
    judul_langkah("PENDAHULUAN", "📖 Petunjuk, Tujuan & Kasus")

    st.subheader("🕵️ Kasus Hari Ini")
    tampil_svg(svg_kasus(barisan))
    st.write(
        "Sebuah brankas rahasia hanya bisa dibuka dengan kode yang tersusun "
        "dari barisan angka. Kamu hanya mendapat lima kode pertama. "
        "Untuk membuka brankas, kamu harus menemukan **rumus** yang bisa "
        "menghasilkan kode ke berapa pun."
    )

    st.subheader("🎯 Tujuan Pembelajaran")
    st.markdown(
        """
        Setelah mengerjakan LKPD ini, kamu diharapkan mampu:

        1. Menentukan **suku pertama (a)** dan **beda (b)** barisan aritmatika.
        2. Menyusun dan menyederhanakan **rumus suku ke-n**.
        3. Menggunakan rumus untuk menghitung suku tertentu.
        4. Menalar apakah suatu bilangan **termasuk** suku barisan atau tidak.
        """
    )

    st.subheader("📋 Petunjuk Pengerjaan")
    kartu(
        "1. Kerjakan <b>satu langkah per halaman</b>, berurutan dari Langkah 1 sampai 8.<br>"
        "2. Tekan <b>Kirim Jawaban</b>. Jawabanmu tersimpan, benar maupun salah, "
        "dan kamu boleh lanjut ke langkah berikutnya.<br>"
        "3. Kamu boleh mengubah jawaban sebelum lanjut, lalu kirim lagi.<br>"
        "4. Gunakan <b>Minta Petunjuk</b> jika kesulitan.<br>"
        "5. <b>Benar atau salahnya dibahas di bagian Refleksi</b> pada akhir LKPD: "
        "kamu akan diberi tahu di mana letak kesalahanmu.<br>"
        f"6. Skor maksimal tiap misi: <b>{SKOR_MAKS_MISI} poin</b>."
    )

    st.markdown("**Barisan kasusmu:**")
    kotak_barisan(barisan)

    navigasi(1, 3, True, label_kembali="🏠 Kembali",
             label_lanjut="➡️ Mulai Langkah 1")

# =========================================================
# HALAMAN 3 - LANGKAH 1: SUKU PERTAMA
# =========================================================

elif halaman == 3:
    judul_langkah("LANGKAH 1 DARI 8", "🟦 Menentukan Suku Pertama (a)")

    tampil_svg(svg_tangga(barisan))

    st.markdown("**Tabel pengamatan:**")
    baris_n = " | ".join(str(i + 1) for i in range(len(barisan)))
    baris_u = " | ".join(str(v) for v in barisan)
    st.markdown(
        f"| n | {baris_n} |\n|---|{'---|' * len(barisan)}\n| Uₙ | {baris_u} |"
    )

    st.write("**Pertanyaan:** berapakah nilai suku pertama $a$?")
    st.latex("a = U_1")

    jawaban = st.number_input(
        "Masukkan nilai a:", min_value=-1000, max_value=1000,
        value=awal("jawab_a", "a"), step=1, key="in_a",
    )

    if st.button("📨 Kirim Jawaban", use_container_width=True, key="kirim_a"):
        catat(
            "jawab_a",
            [item("Suku pertama (a)", jawaban, a, jawaban == a, cat_a(jawaban, a, b))],
            {"a": jawaban},
        )

    info_terkirim("jawab_a")

    tombol_petunjuk("hint_a", "jawab_a")
    if st.session_state.hint_a and not st.session_state.jawab_a:
        st.info("Petunjuk: lihat batang emas atau angka yang paling awal pada barisan.")

    navigasi(2, 4, st.session_state.jawab_a)

# =========================================================
# HALAMAN 4 - LANGKAH 2: BEDA
# =========================================================

elif halaman == 4:
    judul_langkah("LANGKAH 2 DARI 8", "🟩 Menentukan Beda (b)")

    tampil_svg(svg_loncatan(barisan, None))

    st.write(
        "Perhatikan 'loncatan' dari satu suku ke suku berikutnya. "
        "Besar loncatan itu selalu sama dan disebut **beda**."
    )
    st.latex("b = U_2 - U_1")

    jawaban = st.number_input(
        "Masukkan nilai beda b:", min_value=-1000, max_value=1000,
        value=awal("jawab_b", "b"), step=1, key="in_b",
    )

    if st.button("📨 Kirim Jawaban", use_container_width=True, key="kirim_b"):
        catat(
            "jawab_b",
            [item("Beda (b)", jawaban, b, jawaban == b, cat_b(jawaban, a, b))],
            {"b": jawaban},
        )

    info_terkirim("jawab_b")

    tombol_petunjuk("hint_b", "jawab_b")
    if st.session_state.hint_b and not st.session_state.jawab_b:
        st.info(f"Petunjuk: hitung {barisan[1]} − {barisan[0]}.")

    navigasi(3, 5, st.session_state.jawab_b)

# =========================================================
# HALAMAN 5 - LANGKAH 3: RUMUS
# =========================================================

elif halaman == 5:
    judul_langkah("LANGKAH 3 DARI 8", "🟨 Menyusun Rumus Suku ke-n")

    tampil_svg(svg_mesin("a + (n−1)b"))

    a_s, b_s = ab_siswa()
    kol1, kol2 = st.columns(2)
    kol1.metric("a yang kamu kirim", a_s)
    kol2.metric("b yang kamu kirim", b_s)

    st.write("Rumus umum barisan aritmatika:")
    st.latex("U_n = a + (n-1)b")
    st.write(f"Substitusikan nilai $a = {a_s}$ dan $b = {b_s}$ yang kamu temukan:")
    st.latex(f"U_n = {a_s} + (n-1)({b_s})")
    st.write("Sekarang sederhanakan bentuk tersebut.")

    st.markdown("### ✏️ Masukkan hasil penyederhanaan")
    kol1, kol2 = st.columns(2)
    with kol1:
        koefisien = st.number_input(
            "Koefisien n:", min_value=-1000, max_value=1000,
            value=awal("jawab_rumus", "koef"), step=1, key="in_koef",
        )
    with kol2:
        konstanta_input = st.number_input(
            "Konstanta:", min_value=-1000, max_value=1000,
            value=awal("jawab_rumus", "konst"), step=1, key="in_konst",
        )
    st.latex(r"U_n = (\text{koefisien})\,n + \text{konstanta}")

    if st.button("📨 Kirim Jawaban", use_container_width=True, key="kirim_rumus"):
        c_koef = cat_koef(koefisien, a, b)
        c_konst = cat_konst(konstanta_input, a, b)
        konsisten = koefisien == b_s and konstanta_input == a_s - b_s
        if konsisten and not (koefisien == b and konstanta_input == konstanta):
            tambah = (" Rumusmu sudah konsisten dengan a dan b yang kamu kirim di "
                      "Langkah 1 dan 2, jadi kesalahan berasal dari nilai a atau b tersebut.")
            if koefisien != b:
                c_koef += tambah
            if konstanta_input != konstanta:
                c_konst += tambah
        catat(
            "jawab_rumus",
            [
                item("Koefisien n", koefisien, b, koefisien == b, c_koef),
                item("Konstanta", konstanta_input, konstanta,
                     konstanta_input == konstanta, c_konst),
            ],
            {"koef": koefisien, "konst": konstanta_input},
        )

    info_terkirim("jawab_rumus")

    tombol_petunjuk("hint_rumus", "jawab_rumus", "💡 Minta Petunjuk Rumus")
    if st.session_state.hint_rumus and not st.session_state.jawab_rumus:
        st.info(
            f"Gunakan $U_n = {a_s} + (n-1)({b_s})$. "
            "Kembangkan tanda kurung, lalu gabungkan suku yang sejenis."
        )

    navigasi(4, 6, st.session_state.jawab_rumus)

# =========================================================
# HALAMAN 6 - LANGKAH 4: HITUNG SUKU KE-N
# =========================================================

elif halaman == 6:
    judul_langkah("LANGKAH 4 DARI 8", "🟥 Menggunakan Rumus")

    tampil_svg(svg_grafik(a, b))

    k1, k0 = rumus_siswa()
    st.write("Rumus yang kamu susun pada Langkah 3:")
    st.latex(rumus_latex(k1 + k0, k1))

    st.write(
        "Sekarang gunakan rumusmu. "
        "Pilih sebuah nilai $n$, kemudian tentukan nilai $U_n$."
    )

    n = st.number_input(
        "Tentukan nilai n:", min_value=1, max_value=100,
        value=max(1, awal("jawab_suku", "n", 10)), step=1, key="in_n",
    )
    jawaban = st.number_input(
        f"Berapa nilai suku ke-{n}?", min_value=-10000, max_value=10000,
        value=awal("jawab_suku", "un"), step=1, key="in_suku",
    )

    if st.button("📨 Kirim Jawaban", use_container_width=True, key="kirim_suku"):
        hasil_benar = b * n + konstanta
        c_un = cat_un(jawaban, a, b, n)
        if jawaban != hasil_benar and jawaban == k1 * n + k0:
            c_un += (" Hitunganmu sudah sesuai rumus yang kamu susun pada "
                     "Langkah 3, tetapi rumus itu sendiri belum tepat.")
        catat(
            "jawab_suku",
            [item(f"Nilai suku ke-{n}", jawaban, hasil_benar, jawaban == hasil_benar, c_un)],
            {"n": int(n), "un": jawaban},
        )

    info_terkirim("jawab_suku")

    navigasi(5, 7, st.session_state.jawab_suku)

# =========================================================
# HALAMAN 7 - LANGKAH 5: PENALARAN KRITIS
# =========================================================

elif halaman == 7:
    judul_langkah("LANGKAH 5 DARI 8", "🟪 Penalaran Kritis")

    if st.session_state.uji is None:
        nt = random.randint(12, 30)
        n1 = a + (nt - 1) * b
        n2 = n1 + random.randint(1, max(1, b - 1))  # pasti bukan suku (b >= 2)
        st.session_state.uji = {"n": nt, "N1": n1, "N2": n2}
    u = st.session_state.uji

    tampil_svg(svg_lup(u["N1"], u["N2"]))

    k1, k0 = rumus_siswa()
    st.write("Rumus yang kamu susun pada Langkah 3:")
    st.latex(rumus_latex(k1 + k0, k1))

    st.markdown(f"**A.** Suku ke berapakah bilangan **{u['N1']}**?")
    jawab_a_uji = st.number_input(
        "Nilai n:", min_value=1, max_value=1000,
        value=max(1, awal("jawab_uji", "a", 1)), step=1, key="in_uji_a",
    )

    st.markdown(f"**B.** Apakah bilangan **{u['N2']}** termasuk suku barisan ini?")
    opsi = ["— pilih —", "Ya, termasuk suku barisan", "Tidak termasuk suku barisan"]
    pilihan_b = st.selectbox(
        "Pilih jawabanmu:", opsi,
        index=opsi.index(awal("jawab_uji", "b", "— pilih —")),
        key="in_uji_b",
    )

    if st.button("📨 Kirim Jawaban", use_container_width=True, key="kirim_uji"):
        c_a = cat_n(jawab_a_uji, a, b, u["n"])
        if (jawab_a_uji != u["n"] and k1 != 0 and (u["N1"] - k0) % k1 == 0
                and (u["N1"] - k0) // k1 == jawab_a_uji):
            c_a += (" Hitunganmu sesuai rumus yang kamu susun pada Langkah 3, "
                    "tetapi rumus itu sendiri belum tepat.")
        n_pecah = (u["N2"] - konstanta) / b
        c_b = ""
        if pilihan_b == "— pilih —":
            c_b = "Kamu belum memilih jawaban. "
        elif pilihan_b.startswith("Ya"):
            c_b = "Kamu menjawab Ya, padahal bilangan itu bukan suku barisan. "
        c_b += (f"Hitung n = ({u['N2']} − ({konstanta})) ÷ {b} = {n_pecah:.2f}. "
                f"Karena n bukan bilangan bulat, {u['N2']} bukan suku barisan.")
        benar_b = "Tidak termasuk suku barisan"
        catat(
            "jawab_uji",
            [
                item(f"A. Suku ke berapa {u['N1']}?", jawab_a_uji, u["n"],
                     jawab_a_uji == u["n"], c_a),
                item(f"B. Apakah {u['N2']} suku barisan?", pilihan_b, benar_b,
                     pilihan_b == benar_b, c_b),
            ],
            {"a": jawab_a_uji, "b": pilihan_b},
        )

    info_terkirim("jawab_uji")

    tombol_petunjuk("hint_uji", "jawab_uji")
    if st.session_state.hint_uji and not st.session_state.jawab_uji:
        st.info(
            f"Petunjuk: tulis $U_n = {u['N1']}$ sehingga rumusmu sama dengan "
            f"{u['N1']}, lalu cari $n$. Nomor suku harus bilangan bulat positif."
        )

    navigasi(6, 8, st.session_state.jawab_uji)

# =========================================================
# HALAMAN 8 - LANGKAH 6: KURSI BIOSKOP
# =========================================================

elif halaman == 8:
    c = ambil_konteks()["kursi"]
    nilai_k = c["a"] + (c["n_cari"] - 1) * c["b"]
    halaman_masalah(
        kunci="kursi",
        tag="LANGKAH 6 DARI 8",
        judul="🎬 Masalah Nyata: Kursi Bioskop",
        svg=svg_bioskop(c["a"], c["b"]),
        cerita=(
            f"Sebuah bioskop menata kursi penonton dalam <b>{c['n_tanya']} baris</b>. "
            f"Baris paling depan (baris ke-1) berisi <b>{c['a']} kursi</b>. "
            f"Baris-baris di belakangnya selalu memiliki <b>{c['b']} kursi lebih banyak</b> "
            "daripada baris tepat di depannya."
        ),
        c=c,
        fmt=lambda x: f"{x} kursi",
        tanya_un=f"Berapa banyak kursi pada baris paling belakang (baris ke-{c['n_tanya']})?",
        tanya_n=f"Pada baris ke berapakah terdapat {nilai_k} kursi?",
        sebelum=7,
        sesudah=9,
    )

# =========================================================
# HALAMAN 9 - LANGKAH 7: MENABUNG MANDIRI (Un)
# =========================================================

elif halaman == 9:
    c = ambil_konteks()["tabung"]
    nilai_t = c["a"] + (c["n_cari"] - 1) * c["b"]

    halaman_masalah(
        kunci="tabung",
        tag="LANGKAH 7 DARI 8",
        judul="🐷 Masalah Nyata: Menabung Mandiri",
        svg=svg_tabungan(c["a"], c["b"]),
        cerita=(
            "Dina ingin membiasakan diri menabung secara mandiri setiap minggu. "
            f"Pada minggu pertama ia menabung <b>{rupiah(c['a'])}</b>. "
            f"Setiap minggu berikutnya, tabungannya <b>{rupiah(c['b'])} lebih banyak</b> "
            "daripada minggu sebelumnya."
        ),
        c=c,
        fmt=rupiah,
        step=500,
        tanya_un=f"Berapa rupiah yang Dina tabung pada minggu ke-{c['n_tanya']}?",
        tanya_n=f"Pada minggu ke berapakah Dina menabung sebesar {rupiah(nilai_t)}?",
        sebelum=8,
        sesudah=10,
    )

# =========================================================
# HALAMAN 10 - LANGKAH 8: TOTAL TABUNGAN (Sn)
# =========================================================

elif halaman == 10:
    c = ambil_konteks()["tabung"]
    a_, b_ = c["a"], c["b"]
    n_s = c["n_tanya"] + 4                      # 12 - 16 minggu
    u6 = a_ + 5 * b_
    un_s = a_ + (n_s - 1) * b_
    sn_s = n_s * (a_ + un_s) // 2               # selalu bilangan bulat
    tercapai = c["n_cari"] % 2 == 1             # variasi: tercapai / belum
    target = sn_s - 3 * b_ if tercapai else sn_s + 3 * b_
    pilihan_benar = "Ya, target tercapai" if tercapai else "Tidak, target belum tercapai"
    batas = 100_000_000

    def _hitung_misi():
        if not st.session_state.misi_dihitung:
            st.session_state.misi_selesai += 1
            st.session_state.misi_dihitung = True

    judul_langkah("LANGKAH 8 DARI 8", "💰 Total Tabungan: Jumlah n Suku Pertama (Sₙ)")
    tampil_svg(svg_pasangan(a_, b_))

    kartu(
        "Dina sudah tahu berapa yang ia tabung tiap minggu "
        f"(minggu pertama <b>{rupiah(a_)}</b>, naik <b>{rupiah(b_)}</b> tiap minggu). "
        "Sekarang ia ingin tahu <b>total uang yang terkumpul</b>. "
        "Jumlah n suku pertama sebuah barisan disebut <b>Sₙ</b>."
    )

    st.markdown("### 🔍 Bagian A - Temukan trik pasangan")
    st.write(
        "Perhatikan 6 minggu pertama pada gambar. Setiap pasangan "
        "(garis berwarna) punya jumlah yang sama."
    )

    st.markdown("**1.** Berapa $U_1 + U_6$ (dalam rupiah)?")
    ip = st.number_input("Jawabanmu:", -batas, batas, awal("jawab_sn", "p"), 500, key="in_sn_p")

    st.markdown("**2.** Ada berapa pasangan yang terbentuk dari 6 minggu?")
    iq = st.number_input("Banyak pasangan:", 0, 100, awal("jawab_sn", "q"), 1, key="in_sn_q")

    st.markdown("**3.** Berapa total tabungan 6 minggu pertama ($S_6$)?")
    is6 = st.number_input("Jawabanmu:", -batas, batas, awal("jawab_sn", "s6"), 500, key="in_sn_s6")

    st.markdown("---")
    st.markdown("### 🧮 Bagian B - Terapkan pada target Dina")
    kartu(
        f"Dina menabung selama <b>{n_s} minggu</b> dan menargetkan total tabungan "
        f"sebesar <b>{rupiah(target)}</b>."
    )

    st.markdown(f"**4.** Berapa rupiah yang Dina tabung pada minggu ke-{n_s} ($U_{{{n_s}}}$)?")
    iun = st.number_input("Jawabanmu:", -batas, batas, awal("jawab_sn", "un"), 500, key="in_sn_un")

    st.markdown(f"**5.** Berapa total tabungan selama {n_s} minggu ($S_{{{n_s}}}$)?")
    isn = st.number_input("Jawabanmu:", -batas, batas, awal("jawab_sn", "sn"), 500, key="in_sn_sn")

    st.markdown("**6.** Apakah target Dina tercapai?")
    opsi_tc = ["— pilih —", "Ya, target tercapai", "Tidak, target belum tercapai"]
    ipil = st.selectbox(
        "Pilih kesimpulanmu:", opsi_tc,
        index=opsi_tc.index(awal("jawab_sn", "tc", "— pilih —")),
        key="in_sn_tc",
    )

    if st.button("📨 Kirim Jawaban", use_container_width=True, key="kirim_sn"):
        pasangan = a_ + u6
        # nomor 1
        c1 = f"U₁ + U₆ = {rupiah(a_)} + {rupiah(u6)} = {rupiah(pasangan)}."
        if ip == 0:
            c1 = "Bagian ini belum kamu isi. " + c1
        elif ip == u6:
            c1 = "Kamu hanya menulis U₆, belum menjumlahkannya dengan U₁. " + c1
        # nomor 2
        c2 = "Enam suku dipasangkan dua-dua, jadi ada 6 ÷ 2 = 3 pasangan."
        if iq == 6:
            c2 = "Kamu menulis banyak suku (6), bukan banyak pasangan. " + c2
        # nomor 3
        c3 = (f"S₆ = banyak pasangan × jumlah satu pasangan = 3 × {rupiah(pasangan)} "
              f"= {rupiah(3 * pasangan)}.")
        if is6 == pasangan:
            c3 = "Kamu baru menghitung satu pasangan. " + c3
        # nomor 5
        c5 = (f"S{sub(n_s)} = n/2 × (a + U{sub(n_s)}) = {n_s}/2 × ({a_} + {un_s}) "
              f"= {rupiah(sn_s)}.")
        if isn == n_s * (a_ + un_s):
            c5 = "Kamu lupa membagi dua (÷ 2) pada rumus Sₙ. " + c5
        elif isn == un_s:
            c5 = "Kamu menulis suku terakhir, bukan jumlah seluruh suku. " + c5
        # nomor 6
        if ipil == "— pilih —":
            c6 = "Kamu belum memilih jawaban. "
        elif ipil != pilihan_benar:
            c6 = "Kesimpulanmu terbalik. "
        else:
            c6 = ""
        c6 += (f"Bandingkan S{sub(n_s)} = {rupiah(sn_s)} dengan target {rupiah(target)}: "
               + ("total tabungan lebih dari atau sama dengan target, jadi tercapai."
                  if tercapai else "total tabungan kurang dari target, jadi belum tercapai."))
        catat(
            "jawab_sn",
            [
                item("1. U₁ + U₆", ip, pasangan, ip == pasangan, c1, rupiah),
                item("2. Banyak pasangan", iq, 3, iq == 3, c2),
                item("3. S₆", is6, 3 * pasangan, is6 == 3 * pasangan, c3, rupiah),
                item(f"4. U{sub(n_s)}", iun, un_s, iun == un_s,
                     cat_un(iun, a_, b_, n_s, rupiah), rupiah),
                item(f"5. S{sub(n_s)}", isn, sn_s, isn == sn_s, c5, rupiah),
                item("6. Kesimpulan target", ipil, pilihan_benar, ipil == pilihan_benar, c6),
            ],
            {"p": ip, "q": iq, "s6": is6, "un": iun, "sn": isn, "tc": ipil},
        )

    info_terkirim("jawab_sn")

    tombol_petunjuk("hint_sn", "jawab_sn")
    if st.session_state.hint_sn and not st.session_state.jawab_sn:
        st.info(
            "Petunjuk: jumlah tiap pasangan sama dengan $U_1 + U_6$. "
            "$S_n$ = banyak pasangan $\\times$ jumlah satu pasangan, atau "
            "$S_n = \\frac{n}{2}(a + U_n)$. Untuk nomor 6, bandingkan "
            "$S_n$ dengan target."
        )

    navigasi(9, 11, st.session_state.jawab_sn,
             label_lanjut="🏆 Lihat Hasil", aksi_lanjut=_hitung_misi)

# =========================================================
# HALAMAN 11 - HASIL, REFLEKSI & PEMBAHASAN KESALAHAN
# =========================================================

elif halaman == 11:
    tampil_svg(svg_piala())

    st.success(
        f"Selamat, Detektif {st.session_state.nama}! "
        "Kamu sudah mengirimkan seluruh jawaban dan menyelesaikan semua tahapan."
    )

    st.subheader("📚 Kesimpulan")
    st.write(
        "Rumus suku ke-n barisan aritmatika dapat ditemukan menggunakan "
        "suku pertama dan beda. Jumlah n suku pertamanya dihitung dengan "
        "memasangkan suku dari kedua ujung."
    )
    st.latex("U_n = a + (n-1)b")
    st.latex(r"S_n = \frac{n}{2}\,(a + U_n)")
    st.markdown(
        """
        dengan:

        - **a** = suku pertama
        - **b** = beda
        - **n** = banyak suku / nomor suku
        """
    )

    st.markdown("---")
    st.subheader("💭 Refleksi")
    st.write(
        "Tuliskan refleksimu lebih dulu. Setelah disimpan, kamu akan "
        "melihat **pembahasan: di mana letak kesalahanmu**."
    )
    refleksi = st.text_area(
        "Menurutmu, bagaimana cara menemukan rumus suku ke-n dan jumlah n suku pertama?",
        value=st.session_state.refleksi,
        height=150,
    )
    if st.button("💾 Simpan Refleksi & Lihat Pembahasan", use_container_width=True):
        if refleksi.strip():
            st.session_state.refleksi = refleksi.strip()
            st.session_state.refleksi_selesai = True
        else:
            st.warning("Tuliskan refleksimu terlebih dahulu.")

    if st.session_state.refleksi_selesai:
        st.markdown("---")
        st.subheader("🔍 Pembahasan: Di Mana Letak Kesalahanmu?")

        kol1, kol2, kol3 = st.columns(3)
        kol1.metric("⭐ Skor Misi", f"{st.session_state.skor_misi} / {SKOR_MAKS_MISI}")
        kol2.metric("🏅 Skor Total", st.session_state.skor_total)
        kol3.metric("🎯 Misi Selesai", st.session_state.misi_selesai)

        ada_salah = tampil_pembahasan()

        st.markdown("**Rumus yang benar untuk barisan kasusmu:**")
        st.latex(f"U_n = {a} + (n-1)({b})")
        st.latex(rumus_latex(a, b))

        st.subheader("🛠️ Rencana Perbaikan")
        perbaikan = st.text_area(
            "Dari pembahasan di atas, bagian mana yang masih keliru dan "
            "bagaimana kamu akan memperbaikinya?"
            if ada_salah else
            "Bagian mana yang menurutmu paling menantang, dan apa yang membantumu?",
            value=st.session_state.perbaikan,
            height=120,
        )
        if st.button("💾 Simpan Rencana Perbaikan", use_container_width=True):
            if perbaikan.strip():
                st.session_state.perbaikan = perbaikan.strip()
                st.success("Rencana perbaikan berhasil disimpan!")
            else:
                st.warning("Tuliskan rencana perbaikanmu terlebih dahulu.")

        st.download_button(
            "📥 Unduh Lembar Hasil LKPD (HTML / cetak PDF)",
            data=buat_lkpd_html(),
            file_name=f"LKPD_{st.session_state.nama or 'siswa'}.html",
            mime="text/html",
            use_container_width=True,
        )
        st.caption("Buka file hasil unduhan di browser, lalu tekan Ctrl+P untuk menyimpannya sebagai PDF.")

    st.markdown("---")
    st.subheader("🔄 Misi Berikutnya")
    if st.button("🎲 Coba Barisan Lain", use_container_width=True):
        kandidat = [i for i in range(len(SOAL)) if i != st.session_state.soal_index]
        st.session_state.soal_index = random.choice(kandidat)
        reset_misi()
        pindah_halaman(2)

    if st.button("🏠 Kembali ke Awal", use_container_width=True):
        reset_misi()
        st.session_state.skor_total = 0
        st.session_state.misi_selesai = 0
        pindah_halaman(1)