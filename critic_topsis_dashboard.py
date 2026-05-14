"""
CRITIC-TOPSIS Tıbbi Malzeme Tedarikçi Karar Destek Sistemi
===========================================================
Üretim kalitesinde, tek dosya Streamlit uygulaması.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64
from datetime import datetime

# ──────────────────────────────────────────────────────────
# SAYFA YAPILANDIRMASI
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CRITIC-TOPSIS Karar Destek Sistemi",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────
# CSS - MODERN AKADEMİK TEMA
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F0F4F8;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B3E 0%, #122B6A 60%, #1A3A8A 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * {
    color: #E8EDF8 !important;
}
[data-testid="stSidebar"] .stSlider label {
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #A8BFFF !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
    background: #4A90D9 !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
}

/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, #0D1B3E 0%, #1E3A8A 50%, #1D4ED8 100%);
    border-radius: 16px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(13,27,62,0.25);
}
.main-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.main-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 200px;
    width: 160px; height: 160px;
    background: rgba(74,144,217,0.12);
    border-radius: 50%;
}
.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.1rem;
    color: #FFFFFF;
    margin: 0 0 0.3rem 0;
    line-height: 1.15;
    letter-spacing: -0.01em;
}
.main-subtitle {
    font-size: 0.95rem;
    color: #93C5FD;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.02em;
}
.header-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #BFDBFE;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.9rem;
}

/* ── Metric / KPI Cards ── */
.kpi-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px rgba(13,27,62,0.08);
    border: 1px solid rgba(30,58,138,0.06);
    transition: box-shadow 0.25s ease, transform 0.2s ease;
    height: 100%;
}
.kpi-card:hover {
    box-shadow: 0 6px 24px rgba(30,58,138,0.14);
    transform: translateY(-2px);
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #374151;
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #0D1B3E;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.kpi-delta {
    font-size: 0.8rem;
    color: #1E40AF;
    font-weight: 500;
}

/* ── Winner Card ── */
.winner-card {
    background: linear-gradient(135deg, #052E16 0%, #14532D 100%);
    border: 1px solid #16A34A;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 4px 20px rgba(22,163,74,0.2);
    position: relative;
    overflow: hidden;
}
.winner-card::after {
    content: '★';
    position: absolute;
    right: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 3.5rem;
    color: rgba(74,222,128,0.12);
}
.winner-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4ADE80;
    margin-bottom: 0.3rem;
}
.winner-name {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #F0FDF4;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.winner-score {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    color: #86EFAC;
}
.winner-desc {
    font-size: 0.85rem;
    color: #BBF7D0;
    margin-top: 0.5rem;
    line-height: 1.5;
}

/* ── Section Cards ── */
.section-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    box-shadow: 0 2px 12px rgba(13,27,62,0.08);
    border: 1px solid rgba(30,58,138,0.06);
    margin-bottom: 1.2rem;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: #0D1B3E;
    margin-bottom: 0.25rem;
}
.section-subtitle {
    font-size: 0.78rem;
    color: #475569;
    letter-spacing: 0.03em;
    margin-bottom: 1rem;
}

/* ── Table ── */
.dataframe {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.87rem !important;
}
thead tr th {
    background: #0D1B3E !important;
    color: #E8EDF8 !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
}
tbody tr:nth-child(even) {
    background: #F8FAFC !important;
}
tbody tr:hover {
    background: #EFF6FF !important;
}

/* ── Scenario Buttons ── */
.stButton button {
    background: linear-gradient(135deg, #1E3A8A, #1D4ED8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(29,78,216,0.3) !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
    box-shadow: 0 4px 16px rgba(29,78,216,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Sidebar Weights Display ── */
.weight-display {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #93C5FD !important;
}
.weight-total {
    font-weight: 700;
    color: #4ADE80 !important;
}

/* ── Info Box ── */
.info-box {
    background: #EFF6FF;
    border-left: 4px solid #1D4ED8;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    margin: 0.8rem 0;
    font-size: 0.84rem;
    color: #1E3A8A;
    line-height: 1.6;
}

/* ── Academic Comment ── */
.academic-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    font-size: 0.84rem;
    color: #334155;
    line-height: 1.7;
}
.academic-box strong {
    color: #0D1B3E;
}

/* ── Ranking Badge ── */
.rank-1 { color: #D97706; font-weight: 700; }
.rank-2 { color: #64748B; font-weight: 600; }
.rank-3 { color: #92400E; font-weight: 600; }

/* ── Divider ── */
.section-divider {
    height: 2px;
    background: linear-gradient(90deg, #1E3A8A, transparent);
    border-radius: 1px;
    margin: 0.5rem 0 1rem 0;
    opacity: 0.25;
}

/* ── Download buttons ── */
.download-btn {
    display: inline-block;
    background: linear-gradient(135deg, #0D1B3E, #1E3A8A);
    color: white;
    text-decoration: none;
    padding: 0.5rem 1.2rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0.3rem 0.3rem 0.3rem 0;
    transition: all 0.2s;
}
.download-btn:hover {
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    text-decoration: none;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer { visibility: hidden; }
header [data-testid="stToolbar"] { visibility: hidden; }

/* ── Sidebar: ALWAYS visible, cannot be collapsed ── */
[data-testid="stSidebar"] {
    transform: none !important;
    min-width: 280px !important;
    max-width: 320px !important;
}
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="headerNoPadding"] {
    display: none !important;
    visibility: hidden !important;
}
section[data-testid="stSidebar"] > div {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# JavaScript: force sidebar open on every load
st.markdown("""
<script>
(function() {
    try {
        const keys = Object.keys(localStorage);
        keys.forEach(k => {
            if (k.includes('sidebar') || k.includes('Sidebar')) {
                localStorage.removeItem(k);
            }
        });
    } catch(e) {}
})();
</script>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# VERİ SETİ
# ──────────────────────────────────────────────────────────
SUPPLIERS = ["Tedarikçi A", "Tedarikçi B", "Tedarikçi C", "Tedarikçi D"]
CRITERIA  = ["Maliyet", "Kalite", "Teslim Süresi", "Güvenilirlik", "Sterilite"]
BENEFIT_CRITERIA = [False, True, True, True, True]  # Maliyet = maliyet kriteri (küçük iyi)

RAW_DATA = np.array([
    [3, 3, 5, 5, 3],   # A: dengeli, en iyi teslim+güvenilirlik → Baz kazananı
    [1, 2, 3, 3, 2],   # B: en ucuz ama kalite/sterilite düşük → Maliyet kazananı
    [5, 5, 2, 3, 5],   # C: en pahalı ama kalite/sterilite lider → Kalite kazananı
    [4, 3, 4, 4, 3],   # D: orta düzey, hiçbir senaryoda birinci değil
], dtype=float)

# ──────────────────────────────────────────────────────────
# SENARYO TANIMLARI
# ──────────────────────────────────────────────────────────
SCENARIOS = {
    "Baz Senaryo":      [0.20, 0.20, 0.20, 0.20, 0.20],
    "Maliyet Odaklı":   [0.40, 0.15, 0.15, 0.15, 0.15],
    "Kalite Odaklı":    [0.10, 0.30, 0.15, 0.15, 0.30],
}

# ──────────────────────────────────────────────────────────
# MATEMATİKSEL FONKSİYONLAR
# ──────────────────────────────────────────────────────────

def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """Vektör normalizasyonu (Euclidean)."""
    norms = np.sqrt((matrix ** 2).sum(axis=0))
    norms[norms == 0] = 1e-10
    return matrix / norms


def calculate_critic_weights(matrix: np.ndarray) -> np.ndarray:
    """
    CRITIC yöntemi:
    1. Normalize et
    2. Standart sapma hesapla
    3. Korelasyon matrisinden bilgi miktarını hesapla
    4. Ağırlıkları normalize et
    """
    norm = normalize_matrix(matrix)
    std_dev = norm.std(axis=0)
    corr_matrix = np.corrcoef(norm.T)
    conflict = np.sum(1 - corr_matrix, axis=0)
    info = std_dev * conflict
    weights = info / info.sum()
    return weights


def calculate_spearman(ranks1: np.ndarray, ranks2: np.ndarray) -> float:
    n = len(ranks1)
    if n < 2: return 1.0
    d = np.array(ranks1) - np.array(ranks2)
    return 1 - (6 * np.sum(d**2)) / (n * (n**2 - 1))


def calculate_topsis(
    matrix: np.ndarray,
    weights: np.ndarray,
    benefit_criteria: list[bool],
) -> dict:
    """
    TOPSIS Algoritması:
    1. Normalize matris
    2. Ağırlıklı normalize matris
    3. Pozitif (A+) ve Negatif (A-) ideal çözüm
    4. Uzaklıklar (d+, d-)
    5. Yakınlık katsayısı (CC)
    """
    # Adım 1: Normalize
    norm = normalize_matrix(matrix)

    # Adım 2: Ağırlıklı normalize
    weighted = norm * weights

    # Adım 3: İdeal çözümler
    pis = np.array([
        weighted[:, j].max() if benefit_criteria[j] else weighted[:, j].min()
        for j in range(weighted.shape[1])
    ])
    nis = np.array([
        weighted[:, j].min() if benefit_criteria[j] else weighted[:, j].max()
        for j in range(weighted.shape[1])
    ])

    # Adım 4: Uzaklıklar
    d_pos = np.sqrt(((weighted - pis) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - nis) ** 2).sum(axis=1))

    # Adım 5: Yakınlık katsayısı
    cc = d_neg / (d_pos + d_neg + 1e-10)

    return {
        "normalized_matrix": norm,
        "weighted_matrix": weighted,
        "pis": pis,
        "nis": nis,
        "d_pos": d_pos,
        "d_neg": d_neg,
        "cc": cc,
    }


def calculate_ranking(cc: np.ndarray, supplier_names: list[str]) -> pd.DataFrame:
    """Yakınlık katsayısına göre sırala."""
    ranks = cc.argsort()[::-1].argsort() + 1
    df = pd.DataFrame({
        "Tedarikçi": supplier_names,
        "Yakınlık Katsayısı (CC)": cc.round(4),
        "D⁺ (PIS Uzaklığı)": None,
        "D⁻ (NIS Uzaklığı)": None,
        "Sıralama": ranks,
    })
    df = df.sort_values("Sıralama").reset_index(drop=True)
    return df


def scenario_analysis(
    matrix: np.ndarray,
    benefit_criteria: list[bool],
    scenarios: dict,
    supplier_names: list[str],
) -> pd.DataFrame:
    """Her senaryo için TOPSIS sonuçlarını hesapla."""
    rows = []
    for scen_name, weights in scenarios.items():
        w = np.array(weights)
        w = w / w.sum()
        res = calculate_topsis(matrix, w, benefit_criteria)
        for i, sup in enumerate(supplier_names):
            rows.append({
                "Senaryo": scen_name,
                "Tedarikçi": sup,
                "CC Skoru": round(res["cc"][i], 4),
            })
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ──────────────────────────────────────────────────────────

def df_to_csv_link(df: pd.DataFrame, filename: str) -> str:
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-btn">⬇ CSV İndir</a>'


def generate_pdf_report(results: dict, weights: np.ndarray, best: str) -> str:
    """Basit HTML tabanlı PDF raporu oluştur."""
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    html = f"""
    <html><head><meta charset="utf-8">
    <style>
      body{{font-family:Arial,sans-serif;margin:40px;color:#1a1a2e;}}
      h1{{color:#0D1B3E;border-bottom:2px solid #1D4ED8;padding-bottom:8px;}}
      h2{{color:#1E3A8A;margin-top:24px;}}
      table{{border-collapse:collapse;width:100%;margin-top:12px;}}
      th{{background:#0D1B3E;color:white;padding:8px 12px;text-align:left;font-size:12px;}}
      td{{padding:7px 12px;border-bottom:1px solid #E2E8F0;font-size:12px;}}
      tr:nth-child(even){{background:#F8FAFC;}}
      .winner{{background:#052E16;color:#4ADE80;padding:12px 16px;border-radius:8px;margin:16px 0;}}
      .footer{{margin-top:40px;font-size:10px;color:#94A3B8;border-top:1px solid #E2E8F0;padding-top:8px;}}
    </style></head><body>
    <h1>🏥 CRITIC-TOPSIS Tedarikçi Değerlendirme Raporu</h1>
    <p><strong>Rapor Tarihi:</strong> {now}</p>
    <p><strong>Konu:</strong> Tıbbi Malzeme Tedarikçi Seçimi</p>

    <div class="winner">
      <strong>✅ En İyi Tedarikçi: {best}</strong><br>
      CC Skoru: {results['cc'][SUPPLIERS.index(best)]:.4f}
    </div>

    <h2>Kriter Ağırlıkları</h2>
    <table><tr><th>Kriter</th><th>Ağırlık</th></tr>
    {''.join(f"<tr><td>{c}</td><td>{w:.4f}</td></tr>" for c, w in zip(CRITERIA, weights))}
    </table>

    <h2>TOPSIS Sonuçları</h2>
    <table><tr><th>Tedarikçi</th><th>CC Skoru</th><th>D⁺</th><th>D⁻</th><th>Sıralama</th></tr>
    {''.join(
        f"<tr><td>{SUPPLIERS[i]}</td><td>{results['cc'][i]:.4f}</td>"
        f"<td>{results['d_pos'][i]:.4f}</td><td>{results['d_neg'][i]:.4f}</td>"
        f"<td>{int(results['cc'].argsort()[::-1].argsort()[i])+1}</td></tr>"
        for i in range(len(SUPPLIERS))
    )}
    </table>

    <h2>Akademik Yorum</h2>
    <p>CRITIC-TOPSIS yöntemi kullanılarak gerçekleştirilen bu analizde, belirlenen kriter ağırlıkları
    çerçevesinde <strong>{best}</strong> en yüksek yakınlık katsayısı (CC) değerine ulaşarak birinci sıraya
    yerleşmiştir. CRITIC yöntemi, kriterlerin istatistiksel tutarsızlığı ve korelasyon yapısını dikkate alarak
    nesnel ağırlıklandırma sağlamaktadır. TOPSIS ise alternatifleri hem pozitif hem negatif ideal çözüme
    olan uzaklıklarına göre değerlendirmektedir. Bu çok kriterli yaklaşım, tıbbi malzeme tedarikçi
    seçiminde sistematik ve şeffaf bir karar süreci sunmaktadır.</p>

    <div class="footer">
      CRITIC-TOPSIS Karar Destek Sistemi | Endüstri Mühendisliği Çok Kriterli Karar Verme
    </div>
    </body></html>
    """
    b64 = base64.b64encode(html.encode("utf-8")).decode()
    return f'<a href="data:text/html;base64,{b64}" download="CRITIC_TOPSIS_Raporu.html" class="download-btn">📄 Rapor İndir (HTML)</a>'


# ──────────────────────────────────────────────────────────
# GRAFİK FONKSİYONLARI
# ──────────────────────────────────────────────────────────

COLORS = {
    "A": "#1D4ED8",
    "B": "#0891B2",
    "C": "#16A34A",
    "D": "#9333EA",
}
SUP_COLORS = list(COLORS.values())

PLOTLY_LAYOUT = dict(
    font=dict(family="DM Sans, sans-serif", color="#1E293B"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
)


def bar_chart_topsis(cc: np.ndarray, supplier_names: list[str]) -> go.Figure:
    ranks = cc.argsort()[::-1]
    sorted_names = [supplier_names[i] for i in ranks]
    sorted_cc    = [cc[i] for i in ranks]
    bar_colors   = [SUP_COLORS[i] for i in ranks]

    fig = go.Figure(go.Bar(
        x=sorted_names,
        y=sorted_cc,
        marker=dict(
            color=bar_colors,
            line=dict(color="white", width=1.5),
            cornerradius=6,
        ),
        text=[f"{v:.4f}" for v in sorted_cc],
        textposition="outside",
        textfont=dict(size=13, family="JetBrains Mono, monospace", color="#0D1B3E"),
        hovertemplate="<b>%{x}</b><br>CC Skoru: %{y:.4f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="TOPSIS Yakınlık Katsayısı Sıralaması", font=dict(size=14, color="#0D1B3E"), x=0.02),
        yaxis=dict(title="Yakınlık Katsayısı (CC)", range=[0, max(sorted_cc) * 1.18],
                   showgrid=True, gridcolor="#F1F5F9"),
        xaxis=dict(showgrid=False),
        showlegend=False,
        height=360,
    )
    # En iyi tedarikçiye yıldız
    fig.add_annotation(
        x=sorted_names[0], y=sorted_cc[0] * 1.12,
        text="★ EN İYİ", showarrow=False,
        font=dict(size=11, color="#D97706", family="DM Sans"),
        bgcolor="rgba(255,237,213,0.9)", bordercolor="#D97706",
        borderwidth=1, borderpad=4,
    )
    return fig


def radar_chart(matrix: np.ndarray, supplier_names: list[str], criteria: list[str]) -> go.Figure:
    fig = go.Figure()
    cats = criteria + [criteria[0]]
    for i, sup in enumerate(supplier_names):
        vals = list(matrix[i]) + [matrix[i][0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats,
            fill="toself",
            fillcolor=f"rgba({int(SUP_COLORS[i][1:3],16)},{int(SUP_COLORS[i][3:5],16)},{int(SUP_COLORS[i][5:7],16)},0.13)",
            line=dict(color=SUP_COLORS[i], width=2),
            name=sup,
            hovertemplate=f"<b>{sup}</b><br>%{{theta}}: %{{r}}<extra></extra>",
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Tedarikçi Performans Radar Analizi", font=dict(size=14, color="#0D1B3E"), x=0.02),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5.5], gridcolor="#CBD5E1",
                            tickfont=dict(size=9, color="#475569")),
            angularaxis=dict(gridcolor="#CBD5E1", tickfont=dict(size=11, color="#1E293B")),
            bgcolor="rgba(248,250,252,0.8)",
        ),
        legend=dict(
            orientation="h", y=-0.15, x=0.5, xanchor="center",
            font=dict(size=11),
        ),
        height=400,
    )
    return fig


def pie_chart_weights(weights: np.ndarray, criteria: list[str]) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=criteria,
        values=weights,
        hole=0.42,
        marker=dict(
            colors=["#1D4ED8", "#0891B2", "#16A34A", "#9333EA", "#DC2626"],
            line=dict(color="white", width=2),
        ),
        textinfo="label+percent",
        textfont=dict(size=11, family="DM Sans"),
        hovertemplate="<b>%{label}</b><br>Ağırlık: %{value:.3f}<br>Oran: %{percent}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Kriter Ağırlık Dağılımı", font=dict(size=14, color="#0D1B3E"), x=0.02),
        legend=dict(orientation="v", font=dict(size=10)),
        height=360,
    )
    fig.add_annotation(
        text="Ağırlık<br>Dağılımı", x=0.5, y=0.5,
        showarrow=False, font=dict(size=12, color="#374151", family="DM Serif Display"),
        xref="paper", yref="paper",
    )
    return fig


def scenario_comparison_chart(scen_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for i, sup in enumerate(SUPPLIERS):
        sub = scen_df[scen_df["Tedarikçi"] == sup]
        fig.add_trace(go.Bar(
            name=sup,
            x=sub["Senaryo"],
            y=sub["CC Skoru"],
            marker=dict(color=SUP_COLORS[i], cornerradius=4),
            text=[f"{v:.3f}" for v in sub["CC Skoru"]],
            textposition="outside",
            textfont=dict(size=10, family="JetBrains Mono"),
            hovertemplate=f"<b>{sup}</b><br>Senaryo: %{{x}}<br>CC: %{{y:.4f}}<extra></extra>",
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Senaryo Karşılaştırma Analizi", font=dict(size=14, color="#0D1B3E"), x=0.02),
        barmode="group",
        yaxis=dict(title="CC Skoru", showgrid=True, gridcolor="#F1F5F9"),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
        height=380,
    )
    return fig


def scatter_topsis_map(d_pos: list, d_neg: list, names: list, cc: list) -> go.Figure:
    fig = go.Figure()
    for i, sup in enumerate(names):
        fig.add_trace(go.Scatter(
            x=[d_neg[i]],
            y=[d_pos[i]],
            mode="markers+text",
            name=sup,
            marker=dict(size=22, color=SUP_COLORS[i], line=dict(color='white', width=2), opacity=0.9),
            text=[sup],
            textposition="top center",
            textfont=dict(size=12, color="#0D1B3E", family="JetBrains Mono", weight="bold"),
            hovertemplate=f"<b>{sup}</b><br>D⁻ (Kötüden Uzaklık): %{{x:.4f}}<br>D⁺ (İdeale Uzaklık): %{{y:.4f}}<br>CC Skoru: {cc[i]:.4f}<extra></extra>"
        ))
    
    # İdeal bölge vurgusu (Sağ Alt Köşe)
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.5, y0=0, x1=1, y1=0.5,
                  fillcolor="rgba(16, 185, 129, 0.08)", layer="below", line_width=0)
    fig.add_annotation(x=0.98, y=0.05, xref="paper", yref="paper", text="🌟 İdeal Bölge",
                       showarrow=False, font=dict(color="#10B981", size=13, weight="bold"))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="TOPSIS Uzaklık Haritası (Scatter Map)", font=dict(size=14, color="#0D1B3E"), x=0.02),
        xaxis=dict(title="D⁻ (Negatif Çözüme Uzaklık) ➡️ Daha Büyük İyi", showgrid=True, gridcolor="#E2E8F0"),
        yaxis=dict(title="D⁺ (İdeal Çözüme Uzaklık) ⬇️ Daha Küçük İyi", showgrid=True, gridcolor="#E2E8F0", autorange="reversed"),
        showlegend=False,
        height=380,
    )
    return fig


def heatmap_critic_correlation(matrix: np.ndarray, criteria: list[str]) -> go.Figure:
    norm = normalize_matrix(matrix)
    corr_matrix = np.corrcoef(norm.T)
    fig = go.Figure(go.Heatmap(
        z=corr_matrix,
        x=criteria,
        y=criteria,
        colorscale="RdBu",
        zmin=-1, zmax=1,
        text=np.round(corr_matrix, 2),
        texttemplate="%{text}",
        textfont=dict(size=11, family="JetBrains Mono"),
        hovertemplate="<b>%{y} - %{x}</b><br>Korelasyon: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(title="Korelasyon", thickness=10, len=0.8)
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="CRITIC Kriter Çatışma (Korelasyon) Matrisi", font=dict(size=14, color="#0D1B3E"), x=0.02),
        height=380,
    )
    return fig


def heatmap_weighted(weighted: np.ndarray, supplier_names: list[str], criteria: list[str]) -> go.Figure:
    fig = go.Figure(go.Heatmap(
        z=weighted,
        x=criteria,
        y=supplier_names,
        colorscale=[
            [0.0, "#EFF6FF"],
            [0.5, "#3B82F6"],
            [1.0, "#0D1B3E"],
        ],
        text=np.round(weighted, 4),
        texttemplate="%{text}",
        textfont=dict(size=11, family="JetBrains Mono"),
        hovertemplate="<b>%{y} – %{x}</b><br>Ağırlıklı Değer: %{z:.4f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text="Ağırlık", side="right"),
            thickness=12, len=0.8,
        ),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Ağırlıklı Normalize Karar Matrisi Isı Haritası", font=dict(size=14, color="#0D1B3E"), x=0.02),
        height=280,
    )
    return fig


# ──────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────
if "weights" not in st.session_state:
    st.session_state.weights = [0.20, 0.20, 0.20, 0.20, 0.20]

if "raw_data" not in st.session_state:
    st.session_state.raw_data = pd.DataFrame(
        RAW_DATA,
        columns=CRITERIA,
        index=SUPPLIERS,
    )

# ──────────────────────────────────────────────────────────
# DİNAMİK HİBRİT SENARYO (UZMAN + CRITIC)
# ──────────────────────────────────────────────────────────
try:
    uzman_weights = np.array([0.177, 0.208, 0.198, 0.208, 0.208])
    curr_matrix = st.session_state.raw_data.values.astype(float)
    curr_critic = calculate_critic_weights(curr_matrix)
    hibrit_weights = 0.5 * curr_critic + 0.5 * uzman_weights
    hibrit_weights = hibrit_weights / hibrit_weights.sum()
    SCENARIOS["Hibrit (CRITIC+Uzman)"] = hibrit_weights.tolist()
except Exception:
    pass

# ──────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 0.5rem 0;'>
        <div style='font-size:2.4rem;'>🏥</div>
        <div style='font-family:"DM Serif Display",serif;font-size:1.05rem;
                    color:#E8EDF8;margin-top:0.3rem;'>Karar Destek</div>
        <div style='font-size:0.72rem;color:#7BA7E8;letter-spacing:0.1em;
                    text-transform:uppercase;'>CRITIC · TOPSIS</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # ── Senaryo Analizi
    st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;'
                'text-transform:uppercase;color:#7BA7E8;margin-bottom:0.6rem;">⚡ Hızlı Senaryo</div>',
                unsafe_allow_html=True)
    cols_btn = st.columns(1)
    for scen_name, scen_weights in SCENARIOS.items():
        if st.button(scen_name, use_container_width=True):
            st.session_state.weights = scen_weights.copy()
            st.session_state.active_scenario = scen_name
            for i, w in enumerate(scen_weights):
                st.session_state[f"slider_{i}"] = w
            st.rerun()

    if st.session_state.get("active_scenario") == "Hibrit (CRITIC+Uzman)":
        st.markdown("""
        <div style='background:#0F172A; padding:12px; border-radius:8px; margin-top:8px; border:1px solid #1E293B; font-size:0.75rem; color:#CBD5E1; line-height:1.5;'>
        
        <b style='color:#38BDF8; font-size:0.7rem;'>Aldığımız Uzman Görüşleri:</b><br>
        <div style="display:flex; flex-direction:column; border:1px solid #334155; font-size:0.6rem; text-align:center; margin-top:5px; margin-bottom:10px; border-radius:4px; overflow:hidden;">
            <div style="display:flex; background-color:#1E293B; border-bottom:1px solid #334155; font-weight:bold; color:#38BDF8;">
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">Uzman</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155; color:#E2E8F0;">Mal</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155; color:#E2E8F0;">Kal</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155; color:#E2E8F0;">Sür</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155; color:#E2E8F0;">Güv</div>
                <div style="flex:1; padding:4px; color:#E2E8F0;">Ste</div>
            </div>
            <div style="display:flex; background-color:#0F172A; border-bottom:1px solid #334155; color:#E2E8F0;">
                <div style="flex:1; padding:4px; border-right:1px solid #334155; font-weight:bold; color:#93C5FD;">U1</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px;">5</div>
            </div>
            <div style="display:flex; background-color:#0F172A; border-bottom:1px solid #334155; color:#E2E8F0;">
                <div style="flex:1; padding:4px; border-right:1px solid #334155; font-weight:bold; color:#93C5FD;">U2</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">4</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px;">5</div>
            </div>
            <div style="display:flex; background-color:#0F172A; border-bottom:1px solid #334155; color:#E2E8F0;">
                <div style="flex:1; padding:4px; border-right:1px solid #334155; font-weight:bold; color:#93C5FD;">U3</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">4</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px;">5</div>
            </div>
            <div style="display:flex; background-color:#0F172A; color:#E2E8F0;">
                <div style="flex:1; padding:4px; border-right:1px solid #334155; font-weight:bold; color:#93C5FD;">U4</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px; border-right:1px solid #334155;">5</div>
                <div style="flex:1; padding:4px;">5</div>
            </div>
        </div>
        
        <b style='color:#38BDF8;'>Uzman Ortalamaları:</b><br>
        Mal: 4.25 | Kal: 5.0 | Sür: 4.75 | Güv: 5.0 | Ste: 5.0<br><br>
        
        <b style='color:#38BDF8;'>Normalize Ağırlıklar:</b><br>
        Mal: 0.177 | Kal: 0.208 | Sür: 0.198 | Güv: 0.208 | Ste: 0.208<br><br>
        
        <b style='color:#F472B6;'>Neden Hibrit?</b><br>
        Uzman görüşleri kriterlerin sektörel önemini yansıtırken, CRITIC yöntemi performans verilerindeki değişkenlik ve kriterler arası ilişkilere göre nesnel ağırlık üretmektedir. Bu nedenle tutarsızlıkları dengelemek amacıyla hibrit ağırlıklandırma yaklaşımı tercih edilmiştir. Formül:
        <div style='background:#1E293B; padding:5px; text-align:center; font-family:monospace; margin-top:5px; margin-bottom:10px; border-radius:4px;'>
        w_hibrit = 0.5 × CRITIC + 0.5 × Uzman
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background:#1E293B; border-left:3px solid #10B981; padding:8px; border-radius:4px;'>
        <i style='color:#10B981;'>Ekstra Not:</i> Uzman görüşlerinin birbirine çok yakın olması sebebiyle, <b>farklı stratejileri de gözlemleyebilmek adına</b> ek senaryolar oluşturulmuştur.
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Kriter Ağırlıkları
    st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;'
                'text-transform:uppercase;color:#7BA7E8;margin-bottom:0.8rem;">🎛️ Kriter Ağırlıkları</div>',
                unsafe_allow_html=True)

    raw_w = []
    icons = ["💰", "⭐", "🚚", "🛡️", "🧪"]
    for i, (crit, icon) in enumerate(zip(CRITERIA, icons)):
        val = st.slider(
            f"{icon} {crit}",
            min_value=0.0, max_value=1.0,
            value=float(st.session_state.weights[i]),
            step=0.05, key=f"slider_{i}",
        )
        raw_w.append(val)

    total = sum(raw_w)
    norm_w = [w / total if total > 0 else 0.2 for w in raw_w]
    st.session_state.weights = norm_w

    st.divider()
    st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;'
                'text-transform:uppercase;color:#7BA7E8;margin-bottom:0.4rem;">📊 Normalize Ağırlıklar</div>',
                unsafe_allow_html=True)
    for crit, w in zip(CRITERIA, norm_w):
        bar_w = int(w * 100)
        st.markdown(
            f'<div class="weight-display">'
            f'<span style="color:#A8BFFF;">{crit[:8]:<9}</span> '
            f'<span class="weight-total">{w:.3f}</span>'
            f'<div style="margin-top:4px;height:3px;background:rgba(255,255,255,0.1);border-radius:2px;">'
            f'<div style="width:{bar_w}%;height:100%;background:#4A90D9;border-radius:2px;"></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        f'<div style="text-align:right;font-size:0.72rem;color:#4ADE80;'
        f'font-family:JetBrains Mono,monospace;margin-top:4px;">Σ = {sum(norm_w):.3f}</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Tedarikçi Performans Verileri (Düzenlenebilir) ──
    st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;'
                'text-transform:uppercase;color:#7BA7E8;margin-bottom:0.6rem;">📝 Performans Verileri</div>',
                unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.68rem;color:#93C5FD;margin-bottom:0.5rem;line-height:1.4;">'
                'Aşağıdaki tabloda tedarikçi puanlarını değiştirip <b>Enter</b> tuşuna basın. '
                'Analiz otomatik güncellenir.</div>',
                unsafe_allow_html=True)

    edited_data = st.data_editor(
        st.session_state.raw_data,
        use_container_width=True,
        num_rows="fixed",
        key="data_editor",
        column_config={
            crit: st.column_config.NumberColumn(
                crit,
                min_value=1,
                max_value=5,
                step=1,
                format="%d",
            ) for crit in CRITERIA
        },
    )
    st.session_state.raw_data = edited_data

    # Varsayılan verilere sıfırlama butonu
    if st.button("🔄 Varsayılana Sıfırla", use_container_width=True, key="reset_data"):
        st.session_state.raw_data = pd.DataFrame(
            RAW_DATA, columns=CRITERIA, index=SUPPLIERS,
        )
        st.rerun()

    st.divider()
    st.markdown("""
    <div style='font-size:0.7rem;color:#7BA7E8;line-height:1.6;'>
    <strong style='color:#A8BFFF;'>Yöntem:</strong> CRITIC + TOPSIS<br>
    <strong style='color:#A8BFFF;'>Kriter türü:</strong> Maliyet (↓), Diğerleri (↑)<br>
    <strong style='color:#A8BFFF;'>Normalizasyon:</strong> Euclidean Vektör
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HESAPLAMALAR
# ──────────────────────────────────────────────────────────
data_matrix = st.session_state.raw_data.values.astype(float)
weights_arr = np.array(norm_w)
topsis_res  = calculate_topsis(data_matrix, weights_arr, BENEFIT_CRITERIA)
cc          = topsis_res["cc"]
ranks_arr   = cc.argsort()[::-1].argsort() + 1
best_idx    = cc.argmax()
best_sup    = SUPPLIERS[best_idx]

critic_weights = calculate_critic_weights(data_matrix)
scen_df        = scenario_analysis(data_matrix, BENEFIT_CRITERIA, SCENARIOS, SUPPLIERS)

# ──────────────────────────────────────────────────────────
# ANA ALAN – HEADER
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="header-badge">Çok Kriterli Karar Verme · Endüstri Mühendisliği</div>
    <div class="main-title">CRITIC-TOPSIS Tedarikçi Karar Destek Sistemi</div>
    <div class="main-subtitle">Tıbbi Malzeme Tedarikçi Seçimi · Dinamik Ağırlık Analizi</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# KPI KARTLARI
# ──────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpi_data = [
    ("Tedarikçi Sayısı", "4", "A, B, C, D"),
    ("Kriter Sayısı", "5", "Maliyet, Kalite …"),
    ("En Yüksek CC", f"{cc.max():.4f}", best_sup),
    ("En Düşük CC", f"{cc.min():.4f}", SUPPLIERS[cc.argmin()]),
    ("CC Aralığı", f"{(cc.max()-cc.min()):.4f}", "Max − Min"),
]
for col, (label, val, sub) in zip([k1, k2, k3, k4, k5], kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# EN İYİ TEDARİKÇİ KARTI
# ──────────────────────────────────────────────────────────
descriptions = {
    "Tedarikçi A": "Teslim süresi ve güvenilirlikte lider; dengeli profille baz senaryoda öne çıkıyor.",
    "Tedarikçi B": "En düşük maliyetli seçenek; bütçe kısıtı olduğunda ideal. Kalite ve sterilite düşük.",
    "Tedarikçi C": "Kalite ve sterilite lideri; yüksek maliyet dezavantajı kalite odaklı senaryoda tolere edilir.",
    "Tedarikçi D": "Orta düzey profil; tüm kriterlerde makul ama hiçbirinde lider değil.",
}
st.markdown(f"""
<div class="winner-card">
    <div class="winner-title">✅ En Uygun Tedarikçi — Mevcut Ağırlık Konfigürasyonu</div>
    <div class="winner-name">{best_sup}</div>
    <div class="winner-score">Yakınlık Katsayısı (CC) = {cc[best_idx]:.4f}
        &nbsp;|&nbsp; Sıralama: #1 / {len(SUPPLIERS)}</div>
    <div class="winner-desc">{descriptions.get(best_sup, "")}</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HIZLI TEDARİKÇİ ANALİZİ KUTUSU
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card" style="border: 2px solid rgba(29,78,216,0.2); background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);">
    <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.3rem;">
        <span style="font-size:1.4rem;">🔍</span>
        <div class="section-title" style="margin-bottom:0;">Hızlı Tedarikçi Analizi</div>
    </div>
    <div class="section-subtitle">Kendi verilerinizi girin — anlık CRITIC-TOPSIS sonucunu görün</div>
</div>
""", unsafe_allow_html=True)

with st.expander("📋 Tedarikçi Verilerini Girin ve Anında Analiz Edin", expanded=True):
    st.markdown('<div style="font-size:0.82rem;color:#334155;margin-bottom:1rem;line-height:1.6;">'
                'Her tedarikçi için <b>0-10</b> arası puan girin (Örn: 4.5). '
                'Sistem sonucu <b>anında (gerçek zamanlı)</b> hesaplayacaktır!</div>',
                unsafe_allow_html=True)

    # Tedarikçi sayısı seçimi
    qa_sup_count = st.selectbox(
        "Tedarikçi Sayısı", [2, 3, 4, 5, 6],
        index=2,
        key="qa_sup_count",
    )
    qa_sup_names = [f"Tedarikçi {chr(65+i)}" for i in range(qa_sup_count)]

    # Veri giriş tablosu
    qa_cols = st.columns(len(CRITERIA) + 1)
    qa_cols[0].markdown('<div style="font-weight:700;font-size:0.78rem;color:#0D1B3E;padding:0.35rem 0;"></div>',
                        unsafe_allow_html=True)
    for j, crit in enumerate(CRITERIA):
        qa_cols[j+1].markdown(
            f'<div style="font-weight:700;font-size:0.72rem;color:#1D4ED8;padding:0.35rem 0;'
            f'text-align:center;letter-spacing:0.04em;">{crit}</div>',
            unsafe_allow_html=True,
        )

    qa_values = []
    for i in range(qa_sup_count):
        row_cols = st.columns(len(CRITERIA) + 1)
        row_cols[0].markdown(
            f'<div style="font-weight:600;font-size:0.82rem;color:#0D1B3E;'
            f'padding:0.5rem 0;">{qa_sup_names[i]}</div>',
            unsafe_allow_html=True,
        )
        row_vals = []
        for j, crit in enumerate(CRITERIA):
            val = row_cols[j+1].number_input(
                f"{crit}",
                min_value=0.0, max_value=10.0, value=3.0, step=0.5, format="%.1f",
                key=f"qa_{i}_{j}",
                label_visibility="collapsed",
            )
            row_vals.append(val)
        qa_values.append(row_vals)

    # ANLIK HESAPLAMA (Buton kaldırıldı, gerçek zamanlı çalışır)
    qa_matrix = np.array(qa_values, dtype=float)
    qa_weights = np.array(norm_w)
    qa_res = calculate_topsis(qa_matrix, qa_weights, BENEFIT_CRITERIA)
    qa_cc = qa_res["cc"]
    qa_ranks = qa_cc.argsort()[::-1].argsort() + 1
    qa_best_idx = qa_cc.argmax()
    qa_best = qa_sup_names[qa_best_idx]

    # Sonuç kartı
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#052E16,#14532D);border:1px solid #16A34A;
                border-radius:12px;padding:1.2rem 1.5rem;margin-top:0.8rem;">
        <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                    text-transform:uppercase;color:#4ADE80;">⚡ Anlık Analiz Sonucu</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;
                    color:#F0FDF4;margin:0.3rem 0;">{qa_best}</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.9rem;
                    color:#86EFAC;">CC = {qa_cc[qa_best_idx]:.4f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Tüm tedarikçilerin sıralaması
    qa_result_rows = []
    for i in range(qa_sup_count):
        medal = "🥇" if qa_ranks[i] == 1 else ("🥈" if qa_ranks[i] == 2 else
                ("🥉" if qa_ranks[i] == 3 else f"{qa_ranks[i]}."))
        qa_result_rows.append({
            "Sıra": int(qa_ranks[i]),
            "Tedarikçi": qa_sup_names[i],
            "CC Skoru": round(qa_cc[i], 4),
            "D⁺": round(qa_res["d_pos"][i], 4),
            "D⁻": round(qa_res["d_neg"][i], 4),
            "Durum": medal,
        })
    qa_df = pd.DataFrame(qa_result_rows).sort_values("Sıra").reset_index(drop=True)
    st.dataframe(qa_df, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# ANA GRAFİKLER – SATIR 1
# ──────────────────────────────────────────────────────────
col_l, col_r = st.columns([1.1, 1])

with col_l:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">TOPSIS Sıralama Skoru</div>'
                '<div class="section-subtitle">Yakınlık katsayısına göre azalan sıralama</div>',
                unsafe_allow_html=True)
    st.plotly_chart(bar_chart_topsis(cc, SUPPLIERS), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Kriter Ağırlık Dağılımı</div>'
                '<div class="section-subtitle">Kullanıcı tanımlı normalize ağırlıklar</div>',
                unsafe_allow_html=True)
    st.plotly_chart(pie_chart_weights(weights_arr, CRITERIA), use_container_width=True,
                    config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# SATIR 2 – RADAR + SENARYO
# ──────────────────────────────────────────────────────────
col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tedarikçi Performans Profili</div>'
                '<div class="section-subtitle">Ham veri üzerinden radar karşılaştırması</div>',
                unsafe_allow_html=True)
    st.plotly_chart(radar_chart(data_matrix, SUPPLIERS, CRITERIA), use_container_width=True,
                    config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Senaryo Karşılaştırma</div>'
                '<div class="section-subtitle">Farklı ağırlık senaryolarında CC skoru değişimi</div>',
                unsafe_allow_html=True)
    st.plotly_chart(scenario_comparison_chart(scen_df), use_container_width=True,
                    config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# SATIR 3 – AKADEMİK GÖRSELLEŞTİRME (CRITIC ÇATIŞMA MATRİSİ)
# ──────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">CRITIC Çatışma Matrisi</div>'
            '<div class="section-subtitle">Kriterler arası korelasyon (zıtlık) ölçümü</div>',
            unsafe_allow_html=True)
st.plotly_chart(heatmap_critic_correlation(data_matrix, CRITERIA), 
                use_container_width=True, config={"displayModeBar": False})

with st.expander("ℹ️ Bu Değerler Neye Göre Hesaplanıyor?"):
    st.markdown("""
    <div style='font-size:0.82rem; color:#334155; line-height:1.6;'>
    Bu matris, girdiğiniz tedarikçi verilerindeki kriterlerin birbirleriyle olan <b>Pearson Korelasyon Katsayılarını</b> göstermektedir.
    <br><br>
    CRITIC algoritması, ağırlıkları belirlerken kendi içlerindeki rekabeti ve zıtlığı (çatışmayı) kullanır. Formülde <b>(1 - Korelasyon)</b> işlemi ile zıtlık ölçülür.
    <br><br>
    • <b style='color:#3B82F6;'>Mavi Tonlar (Pozitif):</b> Birlikte artan veya azalan kriterlerdir.<br>
    • <b style='color:#EF4444;'>Kırmızı Tonlar (Negatif):</b> Birbiriyle çatışan (biri artarken diğeri azalan) kriterlerdir.
    <br><br>
    <b>Sonuç:</b> Diğer kriterlerle en çok çatışan ve standart sapması en yüksek olan kritere <u>daha fazla ağırlık</u> verilir.
    </div>
    """, unsafe_allow_html=True)
    
st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# ISI HARİTASI
# ──────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Ağırlıklı Normalize Karar Matrisi</div>'
            '<div class="section-subtitle">Her tedarikçinin kriter bazında ağırlıklı normalize değerleri</div>',
            unsafe_allow_html=True)
st.plotly_chart(heatmap_weighted(topsis_res["weighted_matrix"], SUPPLIERS, CRITERIA),
                use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# DETAY TABLOLARI
# ──────────────────────────────────────────────────────────
st.markdown("### 📋 Nihai Sıralama Tablosu")
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

result_rows = []
for i, sup in enumerate(SUPPLIERS):
    result_rows.append({
        "Tedarikçi": sup,
        "CC Skoru": round(cc[i], 4),
        "D⁺ (PIS Uzaklığı)": round(topsis_res["d_pos"][i], 4),
        "D⁻ (NIS Uzaklığı)": round(topsis_res["d_neg"][i], 4),
        "Sıralama": int(ranks_arr[i]),
        "Durum": "🥇 EN İYİ" if ranks_arr[i] == 1 else ("🥈 2." if ranks_arr[i] == 2 else
                  ("🥉 3." if ranks_arr[i] == 3 else "4.")),
    })
result_df = pd.DataFrame(result_rows).sort_values("Sıralama").reset_index(drop=True)
st.dataframe(result_df, use_container_width=True, hide_index=True)

# CRITIC Ağırlıkları tablosu
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.markdown("#### 🔬 CRITIC Nesnel Ağırlıkları")
    critic_df = pd.DataFrame({
        "Kriter": CRITERIA,
        "CRITIC Ağırlığı": critic_weights.round(4),
        "Kullanıcı Ağırlığı": weights_arr.round(4),
        "Fark": (weights_arr - critic_weights).round(4),
    })
    st.dataframe(critic_df, use_container_width=True, hide_index=True)

with col_t2:
    st.markdown("#### 📊 Ham Veri Matrisi")
    raw_df = pd.DataFrame(data_matrix, columns=CRITERIA, index=SUPPLIERS)
    raw_df.index.name = "Tedarikçi"
    st.dataframe(raw_df, use_container_width=True)

# İdeal Çözümler Tablosu
st.markdown("#### 🎯 İdeal Çözüm Referans Değerleri")
ideal_df = pd.DataFrame({
    "Kriter": CRITERIA,
    "Kriter Türü": ["Maliyet (↓)", "Fayda (↑)", "Fayda (↑)", "Fayda (↑)", "Fayda (↑)"],
    "A⁺ (Pozitif İdeal)": topsis_res["pis"].round(4),
    "A⁻ (Negatif İdeal)": topsis_res["nis"].round(4),
})
st.dataframe(ideal_df, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────
# AKADEMİK YORUM
# ──────────────────────────────────────────────────────────
second_best = SUPPLIERS[[i for i in cc.argsort()[::-1]][1]]
cc_diff = cc.max() - sorted(cc)[-2]
st.markdown("### 🎓 Akademik Değerlendirme")
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="academic-box">
<strong>Analiz Özeti:</strong> Bu çalışmada, tıbbi malzeme tedarikçi seçimi problemi CRITIC (Criteria Importance
Through Intercriteria Correlation) ve TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
yöntemlerinin entegrasyonuyla ele alınmıştır. Maliyet, kalite, teslim süresi, güvenilirlik ve sterilite
kriterleri kapsamında dört tedarikçi sistematik biçimde değerlendirilmiştir.
<br><br>
<strong>Bulgular:</strong> Mevcut kriter ağırlıkları [Maliyet: {weights_arr[0]:.3f}, Kalite: {weights_arr[1]:.3f},
Teslim: {weights_arr[2]:.3f}, Güvenilirlik: {weights_arr[3]:.3f}, Sterilite: {weights_arr[4]:.3f}] çerçevesinde
<strong>{best_sup}</strong>, {cc[best_idx]:.4f} yakınlık katsayısıyla birinci sıraya yerleşmiştir.
İkinci sıradaki <strong>{second_best}</strong> ile arasındaki CC farkı {cc_diff:.4f} olup bu oran tercih kararlılığının
{'yüksek' if cc_diff > 0.05 else 'orta düzey'} olduğuna işaret etmektedir.
<br><br>
<strong>Metodolojik Not:</strong> TOPSIS, alternatifleri hem pozitif ideal çözüme (PIS) yakınlığı hem de negatif
ideal çözümden (NIS) uzaklığı açısından değerlendirmekte; böylece tek boyutlu optimizasyon yaklaşımlarına kıyasla
daha kapsamlı bir karar çerçevesi sunmaktadır. Analizin duyarlılık testi niteliğindeki senaryo karşılaştırması,
ağırlık değişimlerine göre sıralama kararlılığının incelenmesine olanak tanımaktadır.
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# İNDİRME BÖLÜMÜ
# ──────────────────────────────────────────────────────────
st.markdown("### ⬇️ Veri Dışa Aktarma")
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

dl_col1, dl_col2, dl_col3 = st.columns(3)
with dl_col1:
    st.markdown(df_to_csv_link(result_df, "TOPSIS_Sonuclar.csv"), unsafe_allow_html=True)
with dl_col2:
    st.markdown(df_to_csv_link(scen_df, "Senaryo_Analizi.csv"), unsafe_allow_html=True)
with dl_col3:
    st.markdown(generate_pdf_report(topsis_res, weights_arr, best_sup), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;font-size:0.72rem;color:#94A3B8;padding:1rem 0;
            border-top:1px solid #E2E8F0;letter-spacing:0.04em;'>
    CRITIC-TOPSIS Karar Destek Sistemi &nbsp;·&nbsp; Endüstri Mühendisliği Çok Kriterli Karar Verme
    &nbsp;·&nbsp; Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
