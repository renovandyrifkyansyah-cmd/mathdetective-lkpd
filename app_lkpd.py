"""
🔎 MATH DETECTIVE — LKPD Interaktif
Menemukan Rumus Suku ke-n Barisan Aritmatika
=================================================================

Cara menjalankan:
    pip install streamlit
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
    Halaman 10  Hasil, Kesimpulan & Refleksi
"""

import base64
import html
import os
import random
from datetime import datetime

import streamlit as st

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="LKPD Math Detective - Barisan Aritmatika",
    page_icon="🔎",
    layout="centered",
)

st.markdown(
    """
<style>
.block-container { max-width: 950px; padding-top: 1.5rem; padding-bottom: 3rem; }

.main-title { text-align: center; font-size: 34px; font-weight: 800; margin-bottom: 2px; }
.subtitle   { text-align: center; font-size: 16px; margin-bottom: 14px; opacity: .85; }

.lkpd-tag {
    display: inline-block; padding: 4px 14px; border-radius: 999px;
    background: #6d28d9; color: #fff; font-size: 13px; font-weight: 700;
    letter-spacing: .5px; margin-bottom: 6px;
}
.sequence-box {
    padding: 22px; border-radius: 16px; text-align: center;
    font-size: 30px; font-weight: 700; margin: 14px 0;
    border: 2px solid #2d6cdf; background: rgba(45,108,223,.08);
}
.kartu {
    padding: 16px 20px; border-radius: 14px; margin: 12px 0;
    border-left: 6px solid #f59e0b; background: rgba(245,158,11,.10);
}
.progress-text { text-align: center; font-size: 14px; margin-bottom: 4px; }

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
        f'style="width:100%;max-width:{maks}px;border-radius:18px;"></div>',
        unsafe_allow_html=True,
    )


# =========================================================
# ILUSTRASI (SVG dibuat langsung dari Python, tanpa file gambar)
# =========================================================

def svg_sampul():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 260" font-family="Arial, sans-serif">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#1e3a8a"/><stop offset="1" stop-color="#6d28d9"/></linearGradient></defs>
<rect width="800" height="260" rx="22" fill="url(#g)"/>
<g fill="#fff" opacity="0.16" font-size="48" font-weight="700">
<text x="30" y="70">3</text><text x="120" y="215">6</text><text x="270" y="55">9</text>
<text x="400" y="235">12</text><text x="690" y="60">15</text><text x="520" y="40">18</text></g>
<g fill="#fbbf24"><text x="470" y="40" font-size="26">★</text><text x="745" y="170" font-size="22">★</text>
<text x="40" y="240" font-size="20">★</text></g>
<text x="40" y="95" font-size="20" fill="#fde68a" font-weight="700" letter-spacing="3">LKPD • KELAS VIII</text>
<text x="40" y="150" font-size="46" fill="#fff" font-weight="800">MATH DETECTIVE</text>
<text x="40" y="190" font-size="22" fill="#e0e7ff">Pecahkan misteri rumus suku ke-n</text>
<text x="40" y="222" font-size="18" fill="#c7d2fe">Barisan Aritmatika</text>
<circle cx="640" cy="125" r="72" fill="#dbeafe" fill-opacity="0.22" stroke="#fbbf24" stroke-width="14"/>
<line x1="692" y1="178" x2="752" y2="238" stroke="#fbbf24" stroke-width="18" stroke-linecap="round"/>
<text x="640" y="118" text-anchor="middle" fill="#fff" font-size="19" font-weight="700">a + (n−1)b</text>
<text x="640" y="148" text-anchor="middle" fill="#fde68a" font-size="30" font-weight="800">Uₙ = ?</text>
</svg>"""


def svg_kasus(urutan):
    kotak = ""
    for i, v in enumerate(urutan):
        x = 372 + i * 68
        kotak += (
            f'<rect x="{x}" y="82" width="58" height="58" rx="10" fill="#1d4ed8" stroke="#93c5fd" stroke-width="2"/>'
            f'<text x="{x + 29}" y="119" text-anchor="middle" font-size="22" font-weight="700" fill="#fff">{v}</text>'
        )
    x = 372 + len(urutan) * 68
    kotak += (
        f'<rect x="{x}" y="82" width="58" height="58" rx="10" fill="#dc2626" stroke="#fecaca" stroke-width="2"/>'
        f'<text x="{x + 29}" y="123" text-anchor="middle" font-size="32" font-weight="800" fill="#fff">?</text>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Arial, sans-serif">
<rect width="800" height="300" rx="22" fill="#0f172a"/>
<rect x="40" y="40" width="300" height="220" rx="18" fill="#475569" stroke="#cbd5e1" stroke-width="4"/>
<rect x="60" y="60" width="260" height="180" rx="12" fill="#334155"/>
<circle cx="190" cy="150" r="58" fill="#1e293b" stroke="#fbbf24" stroke-width="6"/>
<circle cx="190" cy="150" r="14" fill="#fbbf24"/>
<rect x="184" y="98" width="12" height="38" rx="5" fill="#fbbf24"/>
<g fill="#94a3b8"><rect x="52" y="85" width="12" height="30" rx="4"/><rect x="52" y="185" width="12" height="30" rx="4"/></g>
<text x="190" y="52" text-anchor="middle" font-size="14" fill="#e2e8f0" font-weight="700">BRANKAS RAHASIA</text>
<text x="372" y="62" font-size="18" fill="#fde68a" font-weight="700">KODE PETUNJUK:</text>
{kotak}
<text x="372" y="190" font-size="17" fill="#e2e8f0">Kode berikutnya mengikuti pola tertentu.</text>
<text x="372" y="222" font-size="17" fill="#e2e8f0">Tugasmu: temukan rumus kode ke-n!</text>
<text x="372" y="252" font-size="15" fill="#94a3b8">Detektif, brankas menunggumu... 🔎</text>
</svg>"""


def svg_tangga(urutan):
    m = max(urutan)
    isi = ""
    for i, v in enumerate(urutan):
        h = 190 * v / m
        x = 50 + i * 145
        y = 250 - h
        warna = "#f59e0b" if i == 0 else "#3b82f6"
        label = f"U{sub(i + 1)}" + (" = a" if i == 0 else "")
        isi += (
            f'<rect x="{x}" y="{y:.1f}" width="100" height="{h:.1f}" rx="8" fill="{warna}"/>'
            f'<text x="{x + 50}" y="{y - 8:.1f}" text-anchor="middle" font-size="24" font-weight="700" fill="#0f172a">{v}</text>'
            f'<text x="{x + 50}" y="276" text-anchor="middle" font-size="18" font-weight="700" fill="#334155">{label}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Arial, sans-serif">
<rect width="800" height="300" rx="22" fill="#f1f5f9"/>
<line x1="30" y1="250" x2="770" y2="250" stroke="#64748b" stroke-width="3"/>
{isi}
<text x="400" y="26" text-anchor="middle" font-size="16" fill="#475569">Tinggi tiap batang = nilai suku. Batang emas adalah suku pertama.</text>
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
            f'stroke="#f59e0b" stroke-width="5" marker-end="url(#pa)"/>'
            f'<rect x="{mid - 34}" y="{y - 112}" width="68" height="30" rx="15" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>'
            f'<text x="{mid}" y="{y - 91}" text-anchor="middle" font-size="18" font-weight="800" fill="#b45309">{label}</text>'
        )
    for i, (x, v) in enumerate(zip(xs, urutan)):
        warna = "#f59e0b" if i == 0 else "#10b981"
        isi += (
            f'<circle cx="{x}" cy="{y}" r="36" fill="{warna}" stroke="#fff" stroke-width="4"/>'
            f'<text x="{x}" y="{y + 9}" text-anchor="middle" font-size="26" font-weight="800" fill="#fff">{v}</text>'
            f'<text x="{x}" y="{y + 66}" text-anchor="middle" font-size="17" font-weight="700" fill="#065f46">U{sub(i + 1)}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" font-family="Arial, sans-serif">
<defs><marker id="pa" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#f59e0b"/></marker></defs>
<rect width="800" height="300" rx="22" fill="#ecfdf5"/>
{isi}
</svg>"""


def svg_mesin(rhs, masukan="n", keluaran="Uₙ"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 260" font-family="Arial, sans-serif">
<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker></defs>
<rect width="800" height="260" rx="22" fill="#fefce8"/>
<text x="100" y="78" text-anchor="middle" font-size="16" fill="#475569" font-weight="700">MASUKAN</text>
<rect x="40" y="92" width="120" height="80" rx="16" fill="#3b82f6"/>
<text x="100" y="146" text-anchor="middle" font-size="38" font-weight="800" fill="#fff">{masukan}</text>
<line x1="165" y1="132" x2="255" y2="132" stroke="#475569" stroke-width="5" marker-end="url(#ar)"/>
<rect x="260" y="40" width="280" height="180" rx="22" fill="#7c3aed"/>
<circle cx="290" cy="70" r="12" fill="#c4b5fd"/><circle cx="510" cy="70" r="12" fill="#c4b5fd"/>
<text x="400" y="84" text-anchor="middle" font-size="16" fill="#ddd6fe" font-weight="700" letter-spacing="2">MESIN RUMUS</text>
<rect x="290" y="105" width="220" height="60" rx="12" fill="#5b21b6"/>
<text x="400" y="146" text-anchor="middle" font-size="26" font-weight="800" fill="#fde68a">{rhs}</text>
<text x="400" y="200" text-anchor="middle" font-size="14" fill="#ddd6fe">nomor suku masuk, nilai suku keluar</text>
<line x1="545" y1="132" x2="635" y2="132" stroke="#475569" stroke-width="5" marker-end="url(#ar)"/>
<text x="700" y="78" text-anchor="middle" font-size="16" fill="#475569" font-weight="700">KELUARAN</text>
<rect x="640" y="92" width="120" height="80" rx="16" fill="#10b981"/>
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
        warna = "#f59e0b" if n == 1 else "#2563eb"
        isi += (
            f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y:.1f}" stroke="#fdba74" stroke-width="1.5" stroke-dasharray="4 4"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{warna}" stroke="#fff" stroke-width="3"/>'
            f'<text x="{x:.1f}" y="{y - 16:.1f}" text-anchor="middle" font-size="16" font-weight="700" fill="#9a3412">{v}</text>'
            f'<text x="{x:.1f}" y="{y0 + 24}" text-anchor="middle" font-size="16" fill="#475569">{n}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 340" font-family="Arial, sans-serif">
<rect width="800" height="340" rx="22" fill="#fff7ed"/>
<line x1="{x0}" y1="{y0}" x2="775" y2="{y0}" stroke="#475569" stroke-width="3"/>
<line x1="{x0}" y1="{y0}" x2="{x0}" y2="30" stroke="#475569" stroke-width="3"/>
<text x="775" y="{y0 + 24}" font-size="18" font-weight="700" fill="#475569">n</text>
<text x="{x0 + 8}" y="30" font-size="18" font-weight="700" fill="#475569">Uₙ</text>
<polyline points="{garis}" fill="none" stroke="#2563eb" stroke-width="3"/>
{isi}
<text x="400" y="334" text-anchor="middle" font-size="15" fill="#9a3412">Titik-titik suku barisan aritmatika selalu naik secara teratur (garis lurus).</text>
</svg>"""


def svg_lup(n1, n2):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 220" font-family="Arial, sans-serif">
<defs><linearGradient id="g2" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#fef9c3"/><stop offset="1" stop-color="#fed7aa"/></linearGradient></defs>
<rect width="800" height="220" rx="22" fill="url(#g2)"/>
<circle cx="120" cy="100" r="56" fill="#fff" fill-opacity="0.6" stroke="#b45309" stroke-width="12"/>
<line x1="160" y1="142" x2="205" y2="187" stroke="#b45309" stroke-width="16" stroke-linecap="round"/>
<text x="120" y="118" text-anchor="middle" font-size="52" font-weight="800" fill="#b45309">?</text>
<text x="500" y="62" text-anchor="middle" font-size="20" fill="#78350f" font-weight="700">Dua angka mencurigakan:</text>
<rect x="290" y="82" width="170" height="70" rx="16" fill="#1d4ed8"/>
<text x="375" y="130" text-anchor="middle" font-size="40" font-weight="800" fill="#fff">{n1}</text>
<rect x="520" y="82" width="170" height="70" rx="16" fill="#7c3aed"/>
<text x="605" y="130" text-anchor="middle" font-size="40" font-weight="800" fill="#fff">{n2}</text>
<text x="500" y="190" text-anchor="middle" font-size="18" fill="#78350f">Mana yang benar-benar suku barisan?</text>
</svg>"""


def svg_piala():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 260" font-family="Arial, sans-serif">
<defs><linearGradient id="g3" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#065f46"/><stop offset="1" stop-color="#10b981"/></linearGradient></defs>
<rect width="800" height="260" rx="22" fill="url(#g3)"/>
<g fill="#fde68a"><rect x="90" y="40" width="10" height="22" rx="3" transform="rotate(25 95 51)"/>
<rect x="190" y="150" width="10" height="22" rx="3" transform="rotate(-30 195 161)"/>
<rect x="620" y="50" width="10" height="22" rx="3" transform="rotate(-20 625 61)"/>
<rect x="700" y="140" width="10" height="22" rx="3" transform="rotate(35 705 151)"/>
<circle cx="150" cy="95" r="6"/><circle cx="650" cy="110" r="6"/><circle cx="260" cy="40" r="5"/><circle cx="560" cy="35" r="5"/></g>
<path d="M340 50 H460 V110 C460 150 430 170 400 170 C370 170 340 150 340 110 Z" fill="#fbbf24" stroke="#f59e0b" stroke-width="4"/>
<path d="M340 68 H312 C300 68 300 122 346 126" fill="none" stroke="#fbbf24" stroke-width="10" stroke-linecap="round"/>
<path d="M460 68 H488 C500 68 500 122 454 126" fill="none" stroke="#fbbf24" stroke-width="10" stroke-linecap="round"/>
<rect x="388" y="170" width="24" height="26" fill="#f59e0b"/>
<rect x="346" y="196" width="108" height="18" rx="6" fill="#d97706"/>
<text x="400" y="122" text-anchor="middle" font-size="44" fill="#fff">★</text>
<text x="400" y="244" text-anchor="middle" font-size="22" font-weight="800" fill="#fff" letter-spacing="3">MISI SELESAI!</text>
</svg>"""


# =========================================================
# STATE & LOGIKA
# =========================================================

def pindah_halaman(nomor):
    st.session_state.halaman = nomor
    st.rerun()


def beri_skor(kunci):
    """Menambah skor hanya sekali per misi untuk tiap tahap."""
    if not st.session_state[kunci]:
        st.session_state.skor_misi += POIN[kunci]
        st.session_state.skor_total += POIN[kunci]
    st.session_state[kunci] = True


def reset_misi():
    for kunci in POIN:
        st.session_state[kunci] = False
    for kunci in ("hint_a", "hint_b", "hint_rumus", "hint_uji",
                  "hint_kursi", "hint_tabung", "hint_sn"):
        st.session_state[kunci] = False
    st.session_state.skor_misi = 0
    st.session_state.bukti_n = None
    st.session_state.uji = None
    st.session_state.konteks = None
    st.session_state.misi_dihitung = False
    for kunci in ("in_a", "in_b", "in_koef", "in_konst", "in_n", "in_suku",
                  "in_uji_a", "in_uji_b"):
        st.session_state.pop(kunci, None)
    for kasus in ("kursi", "tabung"):
        for item in ("a", "b", "koef", "konst", "un", "n"):
            st.session_state.pop(f"in_{kasus}_{item}", None)
    for item in ("p", "q", "s6", "un", "sn", "tc"):
        st.session_state.pop(f"in_sn_{item}", None)


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
    """Satu halaman soal cerita barisan aritmatika (dipakai kursi & tabungan).

    c = {"a", "b", "n_tanya", "n_cari"}; fmt = fungsi penampil nilai.
    """
    flag = f"jawab_{kunci}"
    a_, b_ = c["a"], c["b"]
    k_ = a_ - b_
    n_tanya, n_cari = c["n_tanya"], c["n_cari"]
    un_tanya = a_ + (n_tanya - 1) * b_
    nilai_cari = a_ + (n_cari - 1) * b_
    batas = 100_000_000

    judul_langkah(tag, judul)
    tampil_svg(svg)
    kartu(cerita)

    st.markdown("### ✏️ Lembar Jawaban")

    st.markdown("**1. Kenali polanya**")
    k1, k2 = st.columns(2)
    ia = k1.number_input("Suku pertama (a):", -batas, batas, 0, step, key=f"in_{kunci}_a")
    ib = k2.number_input("Beda (b):", -batas, batas, 0, step, key=f"in_{kunci}_b")

    st.markdown("**2. Susun rumus** dalam bentuk $U_n = bn + k$")
    k3, k4 = st.columns(2)
    ik = k3.number_input("Koefisien n (b):", -batas, batas, 0, step, key=f"in_{kunci}_koef")
    ikon = k4.number_input("Konstanta (k):", -batas, batas, 0, step, key=f"in_{kunci}_konst")

    st.markdown(f"**3.** {tanya_un}")
    iun = st.number_input("Jawabanmu:", -batas, batas, 0, step, key=f"in_{kunci}_un")

    st.markdown(f"**4.** {tanya_n}")
    iN = st.number_input("Nilai n:", 0, 1000, 0, 1, key=f"in_{kunci}_n")

    if st.button("🔎 Periksa Jawaban", use_container_width=True, key=f"cek_{kunci}"):
        cek = {
            "suku pertama (a)": ia == a_,
            "beda (b)": ib == b_,
            "koefisien n": ik == b_,
            "konstanta": ikon == k_,
            "jawaban nomor 3": iun == un_tanya,
            "jawaban nomor 4": iN == n_cari,
        }
        salah = [nama for nama, ok in cek.items() if not ok]
        if not salah:
            beri_skor(flag)
        else:
            st.error(
                "❌ Masih ada yang belum tepat: " + ", ".join(salah)
                + ". Baca ceritanya sekali lagi."
            )

    if st.session_state[flag]:
        st.success("🎉 Hebat! Semua jawabanmu benar.")
        st.markdown("**Pembahasan**")
        st.latex(f"U_n = {a_} + (n-1)({b_})")
        st.latex(rumus_latex(a_, b_))
        st.latex(f"U_{{{n_tanya}}} = {b_}({n_tanya}) + ({k_}) = {un_tanya}")
        st.latex(rf"n = \frac{{{nilai_cari - k_}}}{{{b_}}} = {n_cari}")
        st.info(
            f"Jadi, pada urutan ke-{n_tanya} nilainya {fmt(un_tanya)}, "
            f"dan {fmt(nilai_cari)} berada pada urutan ke-{n_cari}."
        )

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


@st.cache_resource
def muat_backsound():
    """Membaca backsound.mp3 (atau .wav) yang diletakkan sefolder dengan app_lkpd.py."""
    folder = os.path.dirname(os.path.abspath(__file__))
    for nama, mime in (("backsound.mp3", "audio/mpeg"), ("backsound.wav", "audio/wav")):
        jalur = os.path.join(folder, nama)
        if os.path.exists(jalur):
            with open(jalur, "rb") as f:
                return f.read(), mime
    return None, None


def putar_backsound():
    data, mime = muat_backsound()
    if data is None:
        st.caption("⚠️ File backsound.mp3 belum ada di folder aplikasi.")
        return
    st.caption("🎧 Backsound")
    try:
        st.audio(data, format=mime, loop=True, autoplay=True)
    except TypeError:  # Streamlit versi lama belum mengenal loop/autoplay
        st.audio(data, format=mime)


def buat_lkpd_html():
    """Lembar hasil LKPD yang bisa dicetak / disimpan sebagai PDF dari browser."""
    s = st.session_state
    e = html.escape
    d = SOAL[s.soal_index]
    a_, b_ = d["a"], d["b"]
    uji = s.uji or {}
    baris_tahap = "".join(
        f"<tr><td>{e(LABEL_TAHAP[k])}</td><td>{'✅ Benar' if s[k] else '❌ Belum'}</td>"
        f"<td>{POIN[k] if s[k] else 0} / {POIN[k]}</td></tr>"
        for k in POIN
    )
    refleksi = e(s.refleksi).replace("\n", "<br>") or "<i>(belum diisi)</i>"
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"><title>LKPD Math Detective - {e(s.nama)}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 760px; margin: 30px auto; color: #0f172a; }}
h1 {{ color: #4c1d95; margin-bottom: 0; }}
h2 {{ color: #1e3a8a; border-bottom: 2px solid #c7d2fe; padding-bottom: 4px; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid #94a3b8; padding: 8px; text-align: left; }}
th {{ background: #e0e7ff; }}
.kotak {{ background: #eef2ff; padding: 12px 16px; border-radius: 10px; font-size: 20px; }}
</style></head><body>
<h1>🔎 LKPD Math Detective</h1>
<p>Menemukan Rumus Suku ke-n Barisan Aritmatika</p>
<table>
<tr><th>Nama</th><td>{e(s.nama)}</td><th>Kelas</th><td>{e(s.kelas)}</td></tr>
<tr><th>Tanggal</th><td>{datetime.now().strftime('%d-%m-%Y %H:%M')}</td><th>Barisan</th><td>{e(d['nama'])}</td></tr>
</table>
<h2>Barisan yang diselidiki</h2>
<div class="kotak">{', '.join(map(str, buat_barisan(a_, b_)))}, ...</div>
<p>Suku pertama (a) = <b>{a_}</b> &nbsp;|&nbsp; Beda (b) = <b>{b_}</b></p>
<h2>Rumus yang ditemukan</h2>
<div class="kotak">Uₙ = a + (n − 1)b = {a_} + (n − 1)({b_})<br><b>{e(rumus_teks(a_, b_))}</b></div>
<h2>Penalaran kritis</h2>
<p>Suku ke berapakah {uji.get('N1', '-')}? Jawaban benar: n = {uji.get('n', '-')}.<br>
Apakah {uji.get('N2', '-')} suku barisan? Jawaban benar: tidak, karena n bukan bilangan bulat.</p>
<h2>Rekap skor</h2>
<table><tr><th>Tahap</th><th>Status</th><th>Poin</th></tr>{baris_tahap}
<tr><th>Total misi</th><th></th><th>{s.skor_misi} / {SKOR_MAKS_MISI}</th></tr></table>
<h2>Refleksi</h2>
<p>{refleksi}</p>
</body></html>""".encode("utf-8")


DEFAULTS = {
    "halaman": 1, "nama": "", "kelas": "", "soal_index": 0,
    "skor_misi": 0, "skor_total": 0, "misi_selesai": 0, "misi_dihitung": False,
    "jawab_a": False, "jawab_b": False, "jawab_rumus": False,
    "jawab_suku": False, "jawab_uji": False,
    "jawab_kursi": False, "jawab_tabung": False, "jawab_sn": False,
    "hint_a": False, "hint_b": False, "hint_rumus": False, "hint_uji": False,
    "hint_kursi": False, "hint_tabung": False, "hint_sn": False,
    "bukti_n": None, "uji": None, "konteks": None, "refleksi": "",
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
    st.checkbox("🎵 Backsound", value=True, key="musik_aktif")
    if st.session_state.musik_aktif:
        if 2 <= halaman <= TOTAL_HALAMAN - 1:
            putar_backsound()
        elif halaman == 1:
            st.caption("🎧 Backsound menyala otomatis saat misi dimulai.")
    st.markdown("---")
    st.title("🔎 Math Detective")
    st.markdown("---")
    if st.session_state.nama:
        st.write(f"👤 **{st.session_state.nama}**")
    if st.session_state.kelas:
        st.write(f"🏫 **{st.session_state.kelas}**")
    st.markdown("---")
    st.metric("⭐ Skor Total", st.session_state.skor_total)
    st.metric("🎯 Misi Selesai", st.session_state.misi_selesai)
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
        "2. Tekan <b>Periksa</b> untuk mengecek jawabanmu.<br>"
        "3. Gunakan <b>Minta Petunjuk</b> jika kesulitan.<br>"
        "4. Langkah berikutnya terbuka setelah jawabanmu benar.<br>"
        f"5. Skor maksimal tiap misi: <b>{SKOR_MAKS_MISI} poin</b>."
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
        value=0, step=1, key="in_a",
    )

    if st.button("🔎 Periksa Jawaban", use_container_width=True, key="cek_a"):
        if jawaban == a:
            beri_skor("jawab_a")
        else:
            st.error("❌ Belum tepat. Perhatikan angka pertama pada barisan.")

    if st.session_state.jawab_a:
        st.success(f"🎉 Benar! Suku pertama adalah a = {a}.")

    tombol_petunjuk("hint_a", "jawab_a")
    if st.session_state.hint_a and not st.session_state.jawab_a:
        st.info("Petunjuk: lihat batang emas atau angka yang paling awal pada barisan.")

    navigasi(2, 4, st.session_state.jawab_a)

# =========================================================
# HALAMAN 4 - LANGKAH 2: BEDA
# =========================================================

elif halaman == 4:
    judul_langkah("LANGKAH 2 DARI 8", "🟩 Menentukan Beda (b)")

    tampil_svg(svg_loncatan(barisan, b if st.session_state.jawab_b else None))

    st.write(
        "Perhatikan 'loncatan' dari satu suku ke suku berikutnya. "
        "Besar loncatan itu selalu sama dan disebut **beda**."
    )
    st.latex("b = U_2 - U_1")

    jawaban = st.number_input(
        "Masukkan nilai beda b:", min_value=-1000, max_value=1000,
        value=0, step=1, key="in_b",
    )

    if st.button("🔎 Periksa Beda", use_container_width=True, key="cek_b"):
        if jawaban == b:
            beri_skor("jawab_b")
            st.rerun()  # agar ilustrasi menampilkan nilai beda
        else:
            st.error("❌ Belum tepat. Hitung selisih antara dua suku berurutan.")

    if st.session_state.jawab_b:
        st.success(f"🎉 Benar! Beda barisan adalah b = {b}.")
        st.info(f"Kita memperoleh:  **a = {a}**  dan  **b = {b}**")

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

    kol1, kol2 = st.columns(2)
    kol1.metric("Suku pertama (a)", a)
    kol2.metric("Beda (b)", b)

    st.write("Rumus umum barisan aritmatika:")
    st.latex("U_n = a + (n-1)b")
    st.write(f"Substitusikan $a = {a}$ dan $b = {b}$:")
    st.latex(f"U_n = {a} + (n-1)({b})")
    st.write("Sekarang sederhanakan bentuk tersebut.")

    st.markdown("### ✏️ Masukkan hasil penyederhanaan")
    kol1, kol2 = st.columns(2)
    with kol1:
        koefisien = st.number_input(
            "Koefisien n:", min_value=-1000, max_value=1000,
            value=0, step=1, key="in_koef",
        )
    with kol2:
        konstanta_input = st.number_input(
            "Konstanta:", min_value=-1000, max_value=1000,
            value=0, step=1, key="in_konst",
        )
    st.latex(r"U_n = (\text{koefisien})\,n + \text{konstanta}")

    if st.button("🔎 Periksa Rumus", use_container_width=True, key="cek_rumus"):
        if koefisien == b and konstanta_input == konstanta:
            beri_skor("jawab_rumus")
        else:
            st.error("❌ Rumus belum tepat. Coba sederhanakan kembali.")

    if st.session_state.jawab_rumus:
        st.success("🎉 Luar biasa! Kamu berhasil menemukan rumus.")
        st.markdown("### 🔐 Rumus yang kamu temukan:")
        st.latex(rumus_latex(a, b))
        tampil_svg(svg_mesin(rumus_ruas_kanan(a, b)), maks=640)

    tombol_petunjuk("hint_rumus", "jawab_rumus", "💡 Minta Petunjuk Rumus")
    if st.session_state.hint_rumus and not st.session_state.jawab_rumus:
        st.info(
            f"Gunakan $U_n = {a} + (n-1)({b})$. "
            "Kembangkan tanda kurung, lalu gabungkan suku yang sejenis."
        )

    navigasi(4, 6, st.session_state.jawab_rumus)

# =========================================================
# HALAMAN 6 - LANGKAH 4: HITUNG SUKU KE-N
# =========================================================

elif halaman == 6:
    judul_langkah("LANGKAH 4 DARI 8", "🟥 Menggunakan Rumus")

    tampil_svg(svg_grafik(a, b))

    st.success("Rumus yang berhasil kamu temukan:")
    st.latex(rumus_latex(a, b))

    st.write(
        "Sekarang buktikan bahwa rumusmu benar. "
        "Pilih sebuah nilai $n$, kemudian tentukan nilai $U_n$."
    )

    n = st.number_input(
        "Tentukan nilai n:", min_value=1, max_value=100,
        value=10, step=1, key="in_n",
    )
    jawaban = st.number_input(
        f"Berapa nilai suku ke-{n}?", min_value=-10000, max_value=10000,
        value=0, step=1, key="in_suku",
    )

    if st.button("🚀 Periksa Hasil", use_container_width=True, key="cek_suku"):
        if jawaban == b * n + konstanta:
            beri_skor("jawab_suku")
            st.session_state.bukti_n = int(n)
        else:
            st.error("❌ Belum tepat. Masukkan nilai n ke dalam rumus.")

    if st.session_state.jawab_suku and st.session_state.bukti_n is not None:
        nb = st.session_state.bukti_n
        hasil = b * nb + konstanta
        st.success(f"🎉 Benar! Suku ke-{nb} adalah {hasil}.")
        st.markdown("### 🧮 Pembuktian")
        st.latex(f"U_{{{nb}}} = {b}({nb}) + ({konstanta})")
        st.latex(f"U_{{{nb}}} = {hasil}")

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

    st.write("Rumus barisanmu:")
    st.latex(rumus_latex(a, b))

    st.markdown(f"**A.** Suku ke berapakah bilangan **{u['N1']}**?")
    jawab_a_uji = st.number_input(
        "Nilai n:", min_value=1, max_value=1000, value=1, step=1, key="in_uji_a",
    )

    st.markdown(f"**B.** Apakah bilangan **{u['N2']}** termasuk suku barisan ini?")
    pilihan_b = st.selectbox(
        "Pilih jawabanmu:",
        ["— pilih —", "Ya, termasuk suku barisan", "Tidak termasuk suku barisan"],
        key="in_uji_b",
    )

    if st.button("🔎 Periksa Jawaban", use_container_width=True, key="cek_uji"):
        benar_a = jawab_a_uji == u["n"]
        benar_b = pilihan_b == "Tidak termasuk suku barisan"
        if benar_a and benar_b:
            beri_skor("jawab_uji")
        else:
            if not benar_a:
                st.error("❌ Soal A belum tepat. Selesaikan persamaan $U_n$ = bilangan tersebut.")
            if not benar_b:
                st.error("❌ Soal B belum tepat. Coba cari $n$ dan lihat apakah bilangan bulat.")

    if st.session_state.jawab_uji:
        st.success("🎉 Hebat! Penalaranmu tepat.")
        st.markdown("**Pembahasan A**")
        st.latex(f"{b}n + ({konstanta}) = {u['N1']}")
        st.latex(rf"n = \frac{{{u['N1'] - konstanta}}}{{{b}}} = {u['n']}")
        st.markdown("**Pembahasan B**")
        st.latex(
            rf"n = \frac{{{u['N2'] - konstanta}}}{{{b}}} = {(u['N2'] - konstanta) / b:.2f}"
        )
        st.write(
            f"Karena $n$ bukan bilangan bulat, {u['N2']} **bukan** suku barisan ini."
        )

    tombol_petunjuk("hint_uji", "jawab_uji")
    if st.session_state.hint_uji and not st.session_state.jawab_uji:
        st.info(
            f"Petunjuk: tulis $U_n = {u['N1']}$ sehingga ${b}n + ({konstanta}) = {u['N1']}$, "
            "lalu cari $n$. Nomor suku harus bilangan bulat positif."
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
    ip = st.number_input("Jawabanmu:", -batas, batas, 0, 500, key="in_sn_p")

    st.markdown("**2.** Ada berapa pasangan yang terbentuk dari 6 minggu?")
    iq = st.number_input("Banyak pasangan:", 0, 100, 0, 1, key="in_sn_q")

    st.markdown("**3.** Berapa total tabungan 6 minggu pertama ($S_6$)?")
    is6 = st.number_input("Jawabanmu:", -batas, batas, 0, 500, key="in_sn_s6")

    st.markdown("---")
    st.markdown("### 🧮 Bagian B - Terapkan pada target Dina")
    kartu(
        f"Dina menabung selama <b>{n_s} minggu</b> dan menargetkan total tabungan "
        f"sebesar <b>{rupiah(target)}</b>."
    )

    st.markdown(f"**4.** Berapa rupiah yang Dina tabung pada minggu ke-{n_s} ($U_{{{n_s}}}$)?")
    iun = st.number_input("Jawabanmu:", -batas, batas, 0, 500, key="in_sn_un")

    st.markdown(f"**5.** Berapa total tabungan selama {n_s} minggu ($S_{{{n_s}}}$)?")
    isn = st.number_input("Jawabanmu:", -batas, batas, 0, 500, key="in_sn_sn")

    st.markdown("**6.** Apakah target Dina tercapai?")
    ipil = st.selectbox(
        "Pilih kesimpulanmu:",
        ["— pilih —", "Ya, target tercapai", "Tidak, target belum tercapai"],
        key="in_sn_tc",
    )

    if st.button("🔎 Periksa Jawaban", use_container_width=True, key="cek_sn"):
        cek = {
            "nomor 1 (U₁ + U₆)": ip == a_ + u6,
            "nomor 2 (banyak pasangan)": iq == 3,
            "nomor 3 (S₆)": is6 == 3 * (a_ + u6),
            f"nomor 4 (U{sub(n_s)})": iun == un_s,
            f"nomor 5 (S{sub(n_s)})": isn == sn_s,
            "nomor 6 (kesimpulan target)": ipil == pilihan_benar,
        }
        salah = [nama for nama, ok in cek.items() if not ok]
        if not salah:
            beri_skor("jawab_sn")
        else:
            st.error("❌ Masih ada yang belum tepat: " + ", ".join(salah) + ".")

    if st.session_state.jawab_sn:
        st.success("🎉 Luar biasa! Kamu menemukan cara menghitung total tabungan.")
        st.markdown("**Pembahasan**")
        st.latex(rf"S_6 = 3 \times (U_1 + U_6) = 3 \times {a_ + u6} = {3 * (a_ + u6)}")
        st.markdown("Trik pasangan ini menghasilkan **rumus jumlah n suku pertama**:")
        st.latex(r"S_n = \frac{n}{2}\,(a + U_n)")
        st.latex(r"S_n = \frac{n}{2}\,\big(2a + (n-1)b\big)")
        st.latex(rf"U_{{{n_s}}} = {a_} + ({n_s}-1)({b_}) = {un_s}")
        st.latex(rf"S_{{{n_s}}} = \frac{{{n_s}}}{{2}}\,({a_} + {un_s}) = {sn_s}")
        st.info(
            f"Total tabungan {n_s} minggu: {rupiah(sn_s)}. "
            f"Target {rupiah(target)} "
            + ("sudah tercapai." if tercapai else "belum tercapai.")
        )

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
# HALAMAN 11 - HASIL, KESIMPULAN & REFLEKSI
# =========================================================

elif halaman == 11:
    tampil_svg(svg_piala())

    st.success(
        f"Selamat, Detektif {st.session_state.nama}! "
        "Kamu telah memecahkan seluruh tahapan kasus barisan aritmatika."
    )

    st.subheader("📊 Hasil Belajar")
    kol1, kol2, kol3 = st.columns(3)
    kol1.metric("⭐ Skor Misi", f"{st.session_state.skor_misi} / {SKOR_MAKS_MISI}")
    kol2.metric("🏅 Skor Total", st.session_state.skor_total)
    kol3.metric("🎯 Misi Selesai", st.session_state.misi_selesai)

    with st.expander("Lihat rincian tiap langkah"):
        for k in POIN:
            tanda = "✅" if st.session_state[k] else "❌"
            st.write(f"{tanda} {LABEL_TAHAP[k]} — {POIN[k] if st.session_state[k] else 0}/{POIN[k]}")

    st.markdown("---")
    st.subheader("🧠 Rumus yang Ditemukan")
    st.latex(f"U_n = {a} + (n-1)({b})")
    st.latex(rumus_latex(a, b))

    st.subheader("📚 Kesimpulan")
    st.write(
        "Rumus suku ke-n barisan aritmatika dapat ditemukan menggunakan "
        "suku pertama dan beda:"
    )
    st.latex("U_n = a + (n-1)b")
    st.markdown(
        """
        dengan:

        - **a** = suku pertama
        - **b** = beda
        - **n** = nomor suku
        """
    )

    st.markdown("---")
    st.subheader("💭 Refleksi")
    refleksi = st.text_area(
        "Menurutmu, bagaimana cara menemukan rumus suku ke-n?",
        value=st.session_state.refleksi,
        height=150,
    )
    if st.button("💾 Simpan Refleksi", use_container_width=True):
        if refleksi.strip():
            st.session_state.refleksi = refleksi.strip()
            st.success("Refleksi berhasil disimpan!")
        else:
            st.warning("Tuliskan refleksimu terlebih dahulu.")

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
        st.session_state.refleksi = ""
        pindah_halaman(1)
