import streamlit as st
import html

st.set_page_config(
    page_title="AI-MV PDCA Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
:root {
    --bg: #020617;
    --panel: rgba(15, 23, 42, 0.90);
    --panel2: rgba(30, 41, 59, 0.82);
    --border: rgba(148, 163, 184, 0.22);
    --text: #F8FAFC;
    --muted: #CBD5E1;
    --blue: #38BDF8;
    --red: #EF4444;
    --youtube: #FF0033;
    --green: #22C55E;
    --yellow: #F59E0B;
    --pink: #F472B6;
    --white: #FFFFFF;
    --ink: #020617;
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(56,189,248,0.22), transparent 30%),
        radial-gradient(circle at 94% 4%, rgba(255,0,51,0.20), transparent 31%),
        linear-gradient(135deg, #020617 0%, #0F172A 50%, #111827 100%) !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4, p, span, label, .stMarkdown, li {
    color: var(--text) !important;
}

p, li {
    line-height: 1.85;
}

b, strong {
    color: var(--pink) !important;
}

/* =========================
   Streamlit basic widgets
   ========================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 22px !important;
    padding: 22px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.32) !important;
}

.stNumberInput input, .stTextInput input, .stTextArea textarea {
    background-color: #F8FAFC !important;
    color: #020617 !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 700 !important;
}

.stTextArea textarea {
    min-height: 92px;
}

/* Selectbox / popover visibility fix */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div {
    background: #F8FAFC !important;
    color: #020617 !important;
    border: 1px solid rgba(148,163,184,0.45) !important;
    border-radius: 12px !important;
    min-height: 46px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
div[data-baseweb="select"] *,
div[data-baseweb="popover"] *,
ul[role="listbox"] *,
li[role="option"] * {
    color: #020617 !important;
    fill: #020617 !important;
}

div[data-baseweb="popover"],
ul[role="listbox"],
li[role="option"] {
    background: #F8FAFC !important;
    color: #020617 !important;
}

li[role="option"] {
    white-space: normal !important;
    line-height: 1.55 !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}

/* Multiselect tags are not used, but keep this just in case */
.stMultiSelect [data-baseweb="tag"] {
    height: auto !important;
    min-height: 36px !important;
    max-width: 100% !important;
    white-space: normal !important;
    align-items: flex-start !important;
    border-radius: 10px !important;
    padding: 7px 10px !important;
    margin: 4px 6px 4px 0 !important;
}
.stMultiSelect [data-baseweb="tag"] span {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.45 !important;
    color: #020617 !important;
}

div[data-testid="stSlider"] {
    background: rgba(15,23,42,0.68) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 16px 22px 22px !important;
}

button[kind="secondary"], .stDownloadButton button {
    border-radius: 999px !important;
    font-weight: 900 !important;
}

/* Checkbox / radio: long label wrapping */
.stCheckbox label,
.stRadio label {
    align-items: flex-start !important;
}
.stCheckbox label p,
.stRadio label p {
    color: #F8FAFC !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.65 !important;
    font-size: 15px !important;
}
.stCheckbox, .stRadio {
    margin-bottom: 4px !important;
}

/* =========================
   Tabs: straight lower corners + aligned underline
   ========================= */
div[data-testid="stTabs"] [role="tablist"] {
    display: flex !important;
    align-items: flex-end !important;
    gap: 0 !important;
    border-bottom: 2px solid rgba(148, 163, 184, 0.28) !important;
    margin-bottom: 22px !important;
}

div[data-testid="stTabs"] button,
div[data-testid="stTabs"] [role="tab"] {
    background: rgba(15, 23, 42, 0.72) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    border-bottom: 0 !important;
    border-radius: 14px 14px 0 0 !important; /* lower corners are straight */
    padding: 12px 20px !important;
    margin: 0 6px 0 0 !important;
    font-weight: 900 !important;
    box-shadow: none !important;
}

div[data-testid="stTabs"] button[aria-selected="true"],
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #FF0033, #FF5A5F) !important;
    color: white !important;
    border-color: rgba(255,255,255,0.20) !important;
    border-bottom: 2px solid #FF5A5F !important;
    margin-bottom: -2px !important;
    box-shadow: 0 10px 32px rgba(255, 0, 51, 0.28) !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-highlight-bar"] {
    display: none !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(56,189,248,0.16), rgba(255,255,255,0.04));
    border: 1px solid rgba(56,189,248,0.25);
    padding: 18px;
    border-radius: 18px;
}
div[data-testid="stMetricLabel"] p { color: var(--muted) !important; }
div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }

/* =========================
   Original UI components
   ========================= */
.hero {
    text-align: center;
    padding: 36px 22px 30px;
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(255,0,51,0.18), rgba(56,189,248,0.12));
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 24px 80px rgba(0,0,0,0.35);
    margin-bottom: 28px;
}
.hero-kicker {
    font-size: 13px;
    color: var(--muted) !important;
    font-weight: 900;
    letter-spacing: 0.16em;
}
.hero h1 {
    margin: 8px 0 8px;
    font-size: 2.5rem;
    letter-spacing: -0.04em;
}
.hero p { color: #CBD5E1 !important; margin-bottom: 0; }

.section-heading {
    position: relative;
    font-size: 20px !important;
    font-weight: 900 !important;
    letter-spacing: -0.01em;
    background:
        linear-gradient(135deg, rgba(56,189,248,0.18), rgba(255,0,51,0.08)),
        rgba(15,23,42,0.72) !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    border-left: 0 !important;
    padding: 15px 18px 15px 22px !important;
    margin-top: 24px !important;
    margin-bottom: 14px !important;
    border-radius: 18px !important;
    box-shadow: 0 14px 36px rgba(0,0,0,0.24);
    overflow: hidden;
}
.section-heading::before {
    content: "";
    position: absolute;
    left: 0;
    top: 10px;
    bottom: 10px;
    width: 6px;
    border-radius: 999px;
    background: linear-gradient(180deg, var(--blue), var(--youtube));
}
.section-heading::after {
    content: "";
    position: absolute;
    right: -40px;
    top: -40px;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: rgba(56,189,248,0.08);
}

.advice-card {
    background: var(--panel);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    padding: 24px;
    margin: 24px 0;
    box-shadow: 0 18px 50px rgba(0,0,0,0.32);
    overflow: visible !important;
}
.advice-kicker {
    color: var(--blue) !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 0.14em;
    margin-bottom: 6px;
}
.advice-card h3 { margin: 0 0 16px 0; }

.result-badge {
    padding: 14px 16px;
    border-radius: 15px;
    font-weight: 900;
    margin: 14px 0 20px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.28);
    overflow-wrap: anywhere;
}
.success { background: linear-gradient(135deg, #22C55E, #047857); }
.warning { background: linear-gradient(135deg, #F59E0B, #B45309); }
.danger { background: linear-gradient(135deg, #EF4444, #991B1B); }
.neutral { background: linear-gradient(135deg, #64748B, #334155); }
.legendary { background: linear-gradient(135deg, #A855F7, #FF0033); }

.diagnosis-section {
    margin-top: 18px;
    padding: 2px 0 2px 16px;
    border-left: 4px solid rgba(56,189,248,0.78);
}
.section-label {
    display: inline-block;
    color: var(--pink) !important;
    font-weight: 900;
    margin-bottom: 6px;
}
.diagnosis-section ul,
ul.clean-list {
    margin: 8px 0 0 0 !important;
    padding-left: 22px !important;
    list-style-position: outside !important;
}
.diagnosis-section li,
ul.clean-list li {
    margin-bottom: 8px !important;
    overflow-wrap: break-word !important;
}

.alert-highlight {
    background: rgba(239, 68, 68, 0.14) !important;
    border: 1px solid rgba(239, 68, 68, 0.45) !important;
    border-radius: 14px !important;
    padding: 14px 16px !important;
    color: #FEE2E2 !important;
    font-weight: 800;
    margin-top: 18px;
}

.mission-box {
    background: linear-gradient(135deg, rgba(56,189,248,0.16), rgba(255,0,51,0.10));
    border: 1px solid rgba(56,189,248,0.30);
    border-radius: 22px;
    padding: 22px;
    margin: 22px 0;
    overflow: visible !important;
}

/* Stylish status dashboard cards */
.status-panel {
    position: relative;
    background:
        linear-gradient(135deg, rgba(56,189,248,0.10), rgba(255,0,51,0.07)),
        rgba(15,23,42,0.76);
    border: 1px solid rgba(148,163,184,0.24);
    border-radius: 10px;
    padding: 16px;
    margin: 16px 0 22px;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    overflow: visible !important;
    box-shadow: 0 16px 44px rgba(0,0,0,0.24), 0 0 0 1px rgba(255,255,255,0.03) inset;
}
.status-panel-header {
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 2px 2px 4px;
}
.status-panel-title {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 900;
    font-size: 15px;
    letter-spacing: 0.03em;
    color: #FFFFFF !important;
}
.status-panel-title::before {
    content: "";
    width: 9px;
    height: 9px;
    background: linear-gradient(135deg, var(--blue), var(--youtube));
    border-radius: 2px;
    box-shadow: 0 0 16px rgba(56,189,248,0.55);
}
.status-panel-subtitle {
    color: var(--muted) !important;
    font-size: 12px;
    font-weight: 800;
    white-space: nowrap;
}
.status-item {
    position: relative;
    background:
        linear-gradient(135deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035)),
        rgba(15,23,42,0.55);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 8px;
    padding: 15px 15px 14px;
    min-width: 0;
    width: 100%;
    box-sizing: border-box;
    overflow: hidden !important;
    display: grid;
    grid-template-columns: 38px minmax(0, 1fr);
    gap: 12px;
    align-items: start;
}
.status-item::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--blue);
    opacity: 0.95;
}
.status-item::after {
    content: "";
    position: absolute;
    right: -26px;
    top: -26px;
    width: 72px;
    height: 72px;
    background: rgba(255,255,255,0.045);
    transform: rotate(18deg);
}
.status-icon {
    position: relative;
    z-index: 1;
    width: 34px;
    height: 34px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 7px;
    font-size: 18px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
}
.status-content {
    position: relative;
    z-index: 1;
    min-width: 0;
}
.status-label {
    color: var(--muted) !important;
    font-weight: 900;
    font-size: 12px;
    letter-spacing: 0.08em;
    margin-bottom: 5px;
    text-transform: uppercase;
}
.status-value {
    color: #FFFFFF !important;
    font-weight: 900;
    font-size: 18px;
    line-height: 1.55;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
    max-width: 100%;
}
.status-item-small .status-value {
    font-size: 17px;
}
.status-item-problem {
    grid-column: 1 / -1;
    border: 1px solid rgba(255,0,51,0.32);
    background:
        linear-gradient(135deg, rgba(255,0,51,0.16), rgba(56,189,248,0.07)),
        rgba(15,23,42,0.68);
}
.status-item-problem::before {
    background: linear-gradient(180deg, var(--youtube), var(--yellow));
}
.status-item-problem .status-value {
    font-size: 16px;
    line-height: 1.75;
    font-weight: 800;
}
.status-youtube::before { background: #FF0033; }
.status-external::before { background: #38BDF8; }
.status-ctr::before { background: #F472B6; }
.status-retention::before { background: #A855F7; }
.status-views::before { background: #22C55E; }
.status-warning::before { background: #F59E0B; }

.action-list-box {
    background:
        linear-gradient(135deg, rgba(34,197,94,0.18), rgba(56,189,248,0.10)),
        rgba(15,23,42,0.82);
    border: 1px solid rgba(34,197,94,0.35);
    border-left: 6px solid var(--green);
    border-radius: 20px;
    padding: 18px 20px;
    margin-top: 16px;
    margin-bottom: 10px;
    box-shadow: 0 16px 42px rgba(0,0,0,0.26), 0 0 0 1px rgba(255,255,255,0.03) inset;
    overflow: visible !important;
}
.action-list-title {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #FFFFFF !important;
    font-weight: 900;
    font-size: 15px;
    letter-spacing: 0.02em;
    background: rgba(34,197,94,0.18);
    border: 1px solid rgba(34,197,94,0.36);
    border-radius: 999px;
    padding: 7px 12px;
    margin-bottom: 12px;
}
.action-list-box ul {
    margin: 8px 0 0 0 !important;
    padding-left: 0 !important;
    list-style: none !important;
}
.action-list-box li {
    position: relative;
    margin-bottom: 9px;
    padding: 10px 12px 10px 38px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    white-space: normal !important;
    overflow-wrap: break-word !important;
    line-height: 1.65;
}
.action-list-box li::before {
    content: "✓";
    position: absolute;
    left: 13px;
    top: 10px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--green);
    color: #052E16;
    font-size: 12px;
    font-weight: 900;
}
.small-note {
    color: var(--muted) !important;
    font-size: 13px;
    margin: 10px 0 0 !important;
}

@media (max-width: 720px) {
    .status-panel {
        padding: 14px;
        gap: 10px;
    }
    .status-item {
        padding: 13px 14px;
    }
    .hero h1 { font-size: 2rem; }
}

/* =========================
   V6: subtle radius tuning
   角丸を控えめにし、section-headingは下角を直線化
   ========================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 10px !important;
}

.stNumberInput input,
.stTextInput input,
.stTextArea textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div {
    border-radius: 7px !important;
}

.stMultiSelect [data-baseweb="tag"] {
    border-radius: 6px !important;
}

div[data-testid="stSlider"] {
    border-radius: 10px !important;
}

button[kind="secondary"],
.stDownloadButton button {
    border-radius: 8px !important;
}

div[data-testid="stTabs"] button,
div[data-testid="stTabs"] [role="tab"] {
    border-radius: 8px 8px 0 0 !important;
}

div[data-testid="stMetric"] {
    border-radius: 10px !important;
}

.hero {
    border-radius: 14px !important;
}

.section-heading {
    border-radius: 10px 10px 0 0 !important;
    margin-top: 18px !important;
    margin-bottom: -1px !important;
    padding: 14px 18px 14px 22px !important;
    border-bottom: 0 !important;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18) !important;
    z-index: 2;
}

.section-heading::before {
    top: 0 !important;
    bottom: 0 !important;
    border-radius: 0 !important;
}

.section-heading::after {
    width: 86px !important;
    height: 86px !important;
    border-radius: 0 !important;
    opacity: 0.55;
}

.advice-card,
.mission-box,
.status-panel,
.action-list-box {
    border-radius: 10px !important;
}

.status-item,
.result-badge,
.alert-highlight,
.action-list-box li {
    border-radius: 8px !important;
}

.action-list-title {
    border-radius: 8px !important;
}

.action-list-box li::before {
    border-radius: 4px !important;
}

/* V8: status panel responsive polish */
@media (max-width: 820px) {
    .status-panel {
        grid-template-columns: 1fr !important;
    }
    .status-panel-header {
        flex-direction: column;
        align-items: flex-start;
    }
    .status-panel-subtitle {
        white-space: normal;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# Helper functions
# =========================
def badge_class(level: str) -> str:
    return {
        "success": "success",
        "warning": "warning",
        "danger": "danger",
        "neutral": "neutral",
        "legendary": "legendary",
    }.get(level, "neutral")


def render_card(kicker, title, badge, level, status, reason, actions, alert=None, mission=None):
    """診断カードを安全に組み立てて表示する。

    以前の版ではHTMLテンプレート内の差し込み用変数が、そのまま文字として
    表示される環境があったため、ここでは大きなf文字列にまとめず、
    HTMLパーツをリストで組み立てます。
    """
    action_items = "".join([f"<li>{item}</li>" for item in actions])

    card_parts = [
        '<div class="advice-card">',
        f'<div class="advice-kicker">{kicker}</div>',
        f'<h3>{title}</h3>',
        f'<div class="result-badge {badge_class(level)}">{badge}</div>',
        '<div class="diagnosis-section">',
        '<span class="section-label">🎮 今の状態</span>',
        f'<p>{status}</p>',
        '</div>',
        '<div class="diagnosis-section">',
        '<span class="section-label">🧠 原因の見立て</span>',
        f'<p>{reason}</p>',
        '</div>',
        '<div class="diagnosis-section">',
        '<span class="section-label">🔥 次の一手</span>',
        f'<ul class="clean-list">{action_items}</ul>',
        '</div>',
    ]

    if mission:
        mission_items = "".join([f"<li>{item}</li>" for item in mission])
        card_parts.extend([
            '<div class="diagnosis-section mission-section">',
            '<span class="section-label">🎯 今日のミッション</span>',
            f'<ul class="clean-list">{mission_items}</ul>',
            '</div>',
        ])

    if alert:
        card_parts.append(f'<div class="alert-highlight">{alert}</div>')

    card_parts.append('</div>')
    st.markdown("\n".join(card_parts), unsafe_allow_html=True)


def ctr_rank(ctr):
    if ctr >= 10:
        return "👑 伝説級クリエイター", "legendary"
    if ctr >= 7:
        return "🔥 人気クリエイター", "success"
    if ctr >= 4:
        return "⚔️ 注目クリエイター", "success"
    return "👶 駆け出しクリエイター", "warning"


def retention_rank(retention):
    if retention >= 55:
        return "👑 沼らせ成功", "legendary"
    if retention >= 40:
        return "🔥 しっかり聴かれている", "success"
    if retention >= 25:
        return "🟨 途中離脱あり", "warning"
    return "🟥 見せ方・導線の改善が必要", "danger"


def choose_main_problem(imp, ctr, retention, short_views, external_ratio):
    if imp < 1000:
        return "露出不足", "YouTubeに表示される回数が少ないため、SEO・ショート・外部SNSで入口を増やすのが最優先です。"
    if ctr < 4:
        return "クリック不足", "表示はされているのに押されていない状態です。サムネイルとタイトルの改善が最優先です。"
    if retention < 30:
        return "視聴維持不足", "クリックは取れていますが、途中離脱が多い可能性があります。既存MVを作り直すのではなく、離脱ポイントを確認し、固定コメント・概要欄・ショートの切り出し・告知文で期待値を整えましょう。"
    if short_views == 0:
        return "ショート未活用", "本編MVだけでは新規チャンネルの拡散力が足りません。既存MVから魅力的な場面を切り出し、ショートを無料広告として使いましょう。"
    if external_ratio < 15:
        return "外部流入不足", "YouTube内の評価だけに依存しています。SNS告知とチーム拡散で初動を作りましょう。"
    return "総合的に良好", "大きな弱点は少ない状態です。成功要因を言語化し、次回の投稿で再現しましょう。"


def render_status_panel(rows):
    """総合ステータスをミニKPIカード風に表示する。"""
    def status_meta(label):
        label_str = str(label)
        if "総視聴" in label_str:
            return "🎬", "status-views"
        if "YouTube" in label_str:
            return "📥", "status-youtube"
        if "外部" in label_str or "SNS" in label_str:
            return "🌐", "status-external"
        if "CTR" in label_str:
            return "📊", "status-ctr"
        if "維持" in label_str:
            return "🎧", "status-retention"
        if "課題" in label_str or "最大" in label_str:
            return "🚨", "status-item-problem"
        return "✨", "status-warning"

    panel_parts = [
        '<div class="status-panel">',
        '<div class="status-panel-header">',
        '<div class="status-panel-title">現在の総合ステータス</div>',
        '<div class="status-panel-subtitle">KPI SNAPSHOT</div>',
        '</div>',
    ]

    for label, value in rows:
        icon, class_name = status_meta(label)
        label_text = html.escape(str(label), quote=True)
        value_text = html.escape(str(value), quote=True).replace("\n", "<br>")
        small_class = " status-item-small" if len(str(value)) > 14 else ""
        panel_parts.extend([
            f'<div class="status-item {class_name}{small_class}">',
            f'<div class="status-icon">{icon}</div>',
            '<div class="status-content">',
            f'<div class="status-label">{label_text}</div>',
            f'<div class="status-value">{value_text}</div>',
            '</div>',
            '</div>',
        ])

    panel_parts.append('</div>')
    st.markdown("\n".join(panel_parts), unsafe_allow_html=True)


def render_selected_list(title, items):
    safe_title = html.escape(str(title), quote=True)
    if not items:
        st.markdown(
            f"""
            <div class="action-list-box">
                <div class="action-list-title">✅ {safe_title}</div>
                <p class="small-note">まだ選択されていません。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    selected_html = "".join([f"<li>{html.escape(str(item), quote=True)}</li>" for item in items])
    st.markdown(
        f"""
        <div class="action-list-box">
            <div class="action-list-title">✅ {safe_title}</div>
            <ul>{selected_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def checkbox_group(label, options, default_selected=None, key_prefix="check", columns=1):
    default_selected = default_selected or []
    st.markdown(f"**{label}**")
    selected = []
    if columns <= 1:
        for i, option in enumerate(options):
            if st.checkbox(option, value=option in default_selected, key=f"{key_prefix}_{i}"):
                selected.append(option)
    else:
        cols = st.columns(columns)
        for i, option in enumerate(options):
            with cols[i % columns]:
                if st.checkbox(option, value=option in default_selected, key=f"{key_prefix}_{i}"):
                    selected.append(option)
    return selected


def make_report(student_name, video_title, hypothesis, target_audience, planned_actions, target_views, target_ctr,
                act_views, act_imp, act_ctr, retention, likes, comments, subs, short_views,
                external_views, external_ratio, main_problem, next_actions, next_kpi, next_goal, reflection, next_hypothesis):
    name_part = f"{student_name}さんの" if student_name else "今回の"
    action_part = "、".join(planned_actions) if planned_actions else "未設定"
    next_action_part = "、".join(next_actions) if next_actions else "未設定"
    return f"""【AI-MV YouTube運用 PDCAレポート】

■ 対象作品
{name_part}MV「{video_title or '未入力'}」について、投稿前には「{hypothesis or '未入力'}」という仮説を立て、主なターゲットを「{target_audience or '未入力'}」に設定した。投稿前の目標は、視聴回数 {target_views:,} 回、CTR {target_ctr:.1f}% であり、実施施策は「{action_part}」である。

■ 実績確認（Check）
投稿後の実績は、視聴回数 {act_views:,} 回、インプレッション {act_imp:,} 回、CTR {act_ctr:.1f}%、平均視聴維持率 {retention:.1f}% となった。高評価数は {likes:,} 件、コメント数は {comments:,} 件、チャンネル登録者増加は {subs:,} 人、連動ショートの最高視聴回数は {short_views:,} 回である。計算上、YouTube外部・その他からの流入は約 {external_views:,} 回、外部流入比率は {external_ratio:.1f}% と考えられる。

■ 診断
今回の最大課題は「{main_problem}」である。{choose_main_problem(act_imp, act_ctr, retention, short_views, external_ratio)[1]}

■ 次回の改善（Action）
次回は「{next_action_part}」を重点施策として実行する。検証するKPIは「{next_kpi}」、次回目標は「{next_goal or '未入力'}」とする。

■ 振り返り
今回わかったこと：{reflection or '未入力'}
次回の仮説：{next_hypothesis or '未入力'}
"""

# =========================
# Header
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-kicker">AI MUSIC VIDEO / YOUTUBE PDCA DASHBOARD</div>
    <h1>🎬 AI-MV配信分析システム</h1>
    <p>生成AI音楽 × MV制作 × YouTube運用を、仮説・実行・分析・改善まで一気通貫で学ぶ実習ツール</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Tabs
# =========================
tab1, tab2, tab3 = st.tabs([
    "🎯 1. 投稿前 Plan",
    "📊 2. 投稿後 Check",
    "📝 3. 改善 Action & レポート"
])

# =========================
# PLAN
# =========================
with tab1:
    st.markdown('<div class="section-heading">🎯 投稿前：仮説とKPIを決める</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        with st.container(border=True):
            st.markdown("### 🎵 作品情報")
            student_name = st.text_input("学生名・チーム名（任意）", placeholder="例：NVCチームA")
            video_title = st.text_input("MVタイトル", placeholder="例：電波の向こうへ")
            target_audience = st.text_area("狙うターゲット", placeholder="例：ボカロ好き、AI音楽に興味がある高校生、作業用BGMを探している人")
            hypothesis = st.text_area("今回の仮説", placeholder="例：サムネを明るくし、タイトルにSunoAIとボカロを入れればCTRが上がるはず")
    with col_b:
        with st.container(border=True):
            st.markdown("### 📈 目標KPI")
            target_views = st.number_input("目標視聴回数（回）", min_value=50, value=300, step=50)
            target_ctr = st.slider("目標CTR（%）", min_value=1.0, max_value=20.0, value=5.0, step=0.1)
            target_retention = st.slider("目標平均視聴維持率（%）", min_value=5.0, max_value=100.0, value=35.0, step=1.0)
            required_imp = target_views / (target_ctr / 100)
            st.metric("必要インプレッション目安", f"{int(required_imp):,} 回")

    with st.container(border=True):
        st.markdown("### 🚀 実施予定の施策")
        plan_options = [
            "サムネイルをスマホサイズで確認する",
            "タイトルに検索キーワードを入れる",
            "概要欄にフル歌詞を書く",
            "概要欄に制作クレジットを書く",
            "半角#のハッシュタグを3〜5個入れる",
            "本編MVからショート動画を切り出して投稿する",
            "Xに動画付き告知を投稿する",
            "Instagramストーリーズで告知する",
            "TikTokにもショートを流用する",
            "終了画面・カード・再生リストを設定する",
            "チーム内で相互視聴・コメントを行う",
        ]
        planned_actions = checkbox_group(
            "投稿前に仕込む施策を選んでください（全文表示されるチェックボックス形式）",
            plan_options,
            default_selected=[
                "サムネイルをスマホサイズで確認する",
                "概要欄にフル歌詞を書く",
                "本編MVからショート動画を切り出して投稿する",
            ],
            key_prefix="plan_action",
            columns=1,
        )
        render_selected_list("選択中の施策", planned_actions)

    ctr_label, ctr_level = ctr_rank(target_ctr)
    if target_views >= 1000:
        view_badge = "🔥 総力戦フェーズ：メガヒットを狙うラスボス級ミッション！"
        view_level = "legendary"
        view_status = "新規チャンネルとしてはかなり挑戦的な目標です。チーム内再生だけでは届きにくく、外部SNSとショートの総動員が必要です。"
    elif target_views >= 300:
        view_badge = "🚀 スマッシュヒットフェーズ：一般視聴者を巻き込む拡張ミッション！"
        view_level = "success"
        view_status = "身内だけではなく、ボカロ・AI音楽・作業用BGMなどに興味がある第三者へ届ける設計が必要です。"
    else:
        view_badge = "🌱 ファーストフォロワー獲得フェーズ：初動づくりの基礎ミッション！"
        view_level = "warning"
        view_status = "まずは初期視聴と視聴維持を作り、YouTubeに『この動画は見られている』と伝える段階です。"

    render_card(
        "PLAN STRATEGY",
        "投稿前 戦略カルテ",
        view_badge,
        view_level,
        view_status,
        f"CTR目標は <b>{target_ctr:.1f}%</b>。ランクは <b>{ctr_label}</b> です。MVでは音と映像の世界観がクリック前に伝わるかが勝負です。",
        [
            "サムネイルはPCではなくスマホサイズで確認する",
            "タイトルは世界観だけでなく検索語も入れる",
            "概要欄に歌詞・制作クレジット・半角#タグを入れてYouTube AIに内容を伝える",
            "本編だけで勝負せず、ショートとSNS告知で入口を増やす",
        ],
        alert="⚠️ ハッシュタグは全角の『＃』ではなく、必ず半角の『#』にしてください。地味ですが超重要です。",
        mission=["投稿前チェックリストを全員で確認", "既存MVからショート用15秒を切り出す", "概要欄テンプレを完成させる"]
    )

# =========================
# CHECK
# =========================
with tab2:
    st.markdown('<div class="section-heading">📊 投稿後：YouTubeアナリティクスを入力する</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🎬 MV本体の実績")
        c1, c2, c3 = st.columns(3)
        with c1:
            act_views = st.number_input("視聴回数（回）", min_value=0, value=300, step=10)
            likes = st.number_input("高評価数", min_value=0, value=12, step=1)
        with c2:
            act_imp = st.number_input("インプレッション数（回）", min_value=0, value=6000, step=100)
            comments = st.number_input("コメント数", min_value=0, value=2, step=1)
        with c3:
            act_ctr = st.number_input("CTR（%）", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
            subs = st.number_input("登録者増加数", min_value=0, value=1, step=1)
        retention = st.slider("平均視聴維持率（%）", min_value=0.0, max_value=100.0, value=35.0, step=1.0)

    with st.container(border=True):
        st.markdown("### 📱 ショート・外部導線")
        c4, c5 = st.columns(2)
        with c4:
            short_views = st.number_input("連動ショートの最高視聴回数", min_value=0, value=500, step=50)
        with c5:
            sns_posts = st.number_input("SNS告知投稿数", min_value=0, value=2, step=1)

    yt_internal_views = int(act_imp * (act_ctr / 100))
    is_data_error = act_views < yt_internal_views
    external_views = 0 if is_data_error else max(act_views - yt_internal_views, 0)
    external_ratio = 0 if act_views == 0 or is_data_error else external_views / act_views * 100

    if is_data_error:
        st.markdown(f"""
        <div class="advice-card">
            <div class="advice-kicker">DATA CHECK</div>
            <h3>⚠️ 入力データに矛盾があります</h3>
            <div class="result-badge danger">総視聴回数より、計算上のYouTube内視聴数が大きくなっています</div>
            <p>インプレッション <b>{act_imp:,}</b> × CTR <b>{act_ctr:.1f}%</b> = 推定 <b>{yt_internal_views:,}</b> 回です。総視聴回数 <b>{act_views:,}</b> 回より大きいため、桁数・期間・別動画の数値混在を確認してください。</p>
        </div>
        """, unsafe_allow_html=True)
        main_problem = "入力データ確認"
    else:
        ctr_label, ctr_level = ctr_rank(act_ctr)
        ret_label, ret_level = retention_rank(retention)
        main_problem, main_reason = choose_main_problem(act_imp, act_ctr, retention, short_views, external_ratio)
        st.markdown('<div class="section-heading">🧪 総合ステータス</div>', unsafe_allow_html=True)
        render_status_panel([
            ("総視聴回数", f"{act_views:,} 回"),
            ("YouTube内の推定視聴", f"{yt_internal_views:,} 回"),
            ("外部SNS・その他の推定流入", f"{external_views:,} 回（外部流入比率：{external_ratio:.1f}%）"),
            ("CTRランク", ctr_label),
            ("維持率ランク", ret_label),
            ("最大課題", f"{main_problem}：{main_reason}"),
        ])

        # Impression card
        if act_imp < 1000:
            render_card(
                "IMPRESSION CHECK", "1. インプレッション診断",
                "🟨 新規チャンネルの壁、出現中！まずは表示回数を増やすミッションです", "warning",
                "動画の魅力以前に、まだYouTube上で十分に表示されていない状態です。",
                "YouTube AIが動画ジャンルを学習しきれていない、または初期導線が弱く露出チャンスが少ない可能性があります。",
                ["タイトルと概要欄に検索される言葉を追加する", "概要欄にフル歌詞と制作クレジットを書く", "ショート・SNS・再生リストから入口を増やす", "終了画面とカードでチャンネル内回遊を作る"],
                "⚠️ 半角#タグ、歌詞、クレジットはYouTube AIへの名刺です。ここを空欄にすると、AIに自己紹介しないまま戦場に出る感じです。",
                ["概要欄を修正", "既存MVからショートを1本投稿", "終了画面を設定"]
            )
        else:
            render_card(
                "IMPRESSION CHECK", "1. インプレッション診断",
                "🟩 露出は順調！YouTube AIが少しずつ味方になっています", "success",
                "表示回数は新規チャンネルとして十分に取れています。次はクリックと視聴維持の勝負です。",
                "タイトル・概要欄・初動の反応により、YouTube側が動画を出す価値ありと判断し始めています。",
                ["CTRが低ければサムネイル改善", "視聴維持率が低ければショートの切り出し位置や固定コメントを改善", "関連動画・プレイリストで回遊を伸ばす"],
                mission=["成功した流入元を確認", "次回のタイトル・タグ設計に反映"]
            )

        # CTR card
        if act_ctr >= 10:
            render_card(
                "CTR CHECK", "2. CTR診断",
                "👑 CTR神レベル！サムネとタイトルが視聴者の親指を止めています", "legendary",
                "クリック率は非常に高く、サムネイル・タイトルの組み合わせが強力に機能しています。",
                "映像の世界観、文字の見やすさ、タイトルの引きがうまく噛み合っています。これはチームの成功事例です。",
                ["なぜクリックされたのかを言語化する", "他メンバーのサムネ改善に横展開する", "このデザイン法則を次回のテンプレにする"],
                mission=["成功サムネの共通点を3つ書く", "チーム内で共有"]
            )
        elif act_ctr >= 4:
            render_card(
                "CTR CHECK", "2. CTR診断",
                "🔥 CTR合格！音楽ファンの入口はしっかり作れています", "success",
                "表示された人のうち、一定数がクリックしています。サムネとタイトルは最低ラインを突破しています。",
                "デザインの視認性やタイトルの魅力が機能しています。次は視聴維持率やコメントなど、見た後の反応を伸ばす段階です。",
                ["良かったサムネ要素を維持する", "タイトルのキーワードを微調整する", "維持率が低ければショートの切り出し位置や固定コメントを改善する"],
                mission=["成功要素を1つ残す", "改善要素を1つだけ変える"]
            )
        else:
            render_card(
                "CTR CHECK", "2. CTR診断",
                "🟥 CTR要改善！表示されているのにスルーされています", "danger",
                "YouTubeは動画を見せてくれていますが、視聴者がクリックする理由が弱い状態です。",
                "サムネイルの文字が小さい、世界観が伝わりにくい、タイトルの引きが弱い、右下の時間表示に重要要素が被っている可能性があります。",
                ["サムネイルの文字を太く・短くする", "人物・キャラ・象徴的な絵を大きく配置する", "タイトル冒頭に強いキーワードを入れる", "伸びているメンバーのサムネと横比較する"],
                "⚠️ サムネの右下は再生時間表示に隠れます。重要な顔・文字・ロゴは中央〜左寄せがおすすめです。",
                ["サムネイルを差し替え", "タイトルを1案改善", "スマホサイズで再確認"]
            )

        # Retention card
        if retention >= 40:
            render_card(
                "RETENTION CHECK", "3. 視聴維持率診断",
                f"{ret_label}！押した後もしっかり聴かれています", ret_level,
                "クリック後の離脱が少なく、曲やMVの構成が視聴者を引き留めています。",
                "MVそのものの見せ方や曲の世界観が、視聴者の期待と合っている可能性があります。",
                ["離脱が少ない場面を分析する", "サビ前後の演出をショートに切り出す", "成功した見せ方を次回MVにも応用する"],
                mission=["維持率が高い場面をメモ", "ショート化する候補を選ぶ"]
            )
        else:
            render_card(
                "RETENTION CHECK", "3. 視聴維持率診断",
                f"{ret_label}。既存MVの見せ方・導線を整えるミッションです", ret_level,
                "サムネで興味を持たれても、視聴者の期待と動画内容にズレがある可能性があります。",
                "ここではMVを作り直すのではなく、アナリティクスで離脱ポイントを確認し、固定コメント・概要欄・ショート切り出し・SNS告知文で魅力の伝え方を調整します。",
                ["視聴維持率グラフで離脱が大きい場面を確認する", "ショートではサビや強いフレーズを中心に切り出す", "固定コメントで本編の見どころや聴きどころを補足する", "タイトル・概要欄で曲の魅力が伝わる説明を足す"],
                mission=["離脱ポイントを1つ確認", "ショートで使うサビ部分を選ぶ", "固定コメントで見どころを補足"]
            )

        # Shorts and SNS card
        if short_views == 0:
            render_card(
                "SHORTS CHECK", "4. ショート・SNS導線診断",
                "🟨 ショート未着手！無料広告チラシをまだ配っていません", "warning",
                "本編MVだけで新規チャンネルを伸ばすのは難易度高めです。ショートは認知の入口になります。",
                "YouTubeショート、TikTok、Instagramリールに既存MVの魅力的な部分を切り出すことで、まだチャンネルを知らない人に届く可能性が上がります。",
                ["サビなど印象的な15秒を縦型に切り出す", "固定テロップで『AIでMV作ってみた』などのフックを入れる", "固定コメントや概要欄から本編へ誘導する"],
                mission=["既存MVからサビ15秒を切り出す", "縦型9:16で書き出す", "本編リンクを固定コメントに入れる"]
            )
        elif external_ratio < 15:
            render_card(
                "SNS CHECK", "4. 外部流入診断",
                "🟨 外部流入が弱め。YouTube AI頼みから脱出するタイミングです", "warning",
                "視聴の多くがYouTube内に偏っており、SNSからの初動ブーストが弱い状態です。",
                "XやInstagramでリンクだけを貼ると流れにくいため、動画付き投稿・制作裏話・引用リポストなどの工夫が必要です。",
                ["XにはYouTubeリンクだけでなく動画ファイルも添付する", "チーム全員で引用リポストしてお祭り感を作る", "制作秘話やプロンプト紹介で第2波投稿をする"],
                mission=["動画付き告知を1本投稿", "メンバー同士で引用リポスト", "本編URLをプロフィールか固定投稿に設置"]
            )
        else:
            render_card(
                "SNS CHECK", "4. 外部流入診断",
                "👑 外部流入が効いています！自力集客の導線が動き始めています", "legendary",
                "SNSや口コミから視聴者を呼び込めています。これはアルゴリズムに頼りすぎない強い状態です。",
                "外部から来た視聴者がコメントや高評価を残すと、YouTube内の評価にも良い影響が出る可能性があります。",
                ["コメントには必ず返信する", "第2波投稿で制作裏話を出す", "次回予告を固定コメントに置く"],
                mission=["コメント返信", "制作裏話をSNS投稿", "次回投稿への導線を作る"]
            )

# =========================
# ACTION & REPORT
# =========================
with tab3:
    st.markdown('<div class="section-heading">📝 改善アクションとPDCAレポート</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🔧 次に実行する改善アクション")
        action_options = [
            "サムネイルを変更する",
            "タイトルを変更する",
            "概要欄・タグ・歌詞を修正する",
            "既存MVからショート動画を切り出して新しく投稿する",
            "X / Instagram / TikTokで告知する",
            "終了画面・カード・再生リストを設定する",
            "コメント返信・固定コメントでファン化する",
            "チーム内で相互視聴・コメント・引用リポストを行う",
        ]
        next_actions = checkbox_group(
            "次に実行する改善アクションを複数選んでください（複数選択対応）",
            action_options,
            default_selected=["概要欄・タグ・歌詞を修正する", "既存MVからショート動画を切り出して新しく投稿する"],
            key_prefix="next_action",
            columns=1,
        )
        render_selected_list("選択中の改善アクション", next_actions)

        st.markdown("### 📌 次回検証するKPI")
        next_kpi = st.radio(
            "次回、重点的に見るKPIを選んでください",
            ["CTR", "インプレッション", "平均視聴維持率", "視聴回数", "コメント数", "登録者増加数", "外部流入比率", "ショート視聴回数"],
            horizontal=False,
        )
        next_goal = st.text_input("次回目標", placeholder="例：CTR 4.5% → 6.0%")
        reflection = st.text_area("今回わかったこと", placeholder="例：サムネの文字が小さいとスマホで目立たず、CTRが下がるとわかった")
        next_hypothesis = st.text_area("次回の仮説", placeholder="例：サムネの文字を太くして、タイトル冒頭に『AI MV』を入れればCTRが上がるはず")

    try:
        if is_data_error:
            main_problem = "入力データ確認"
        else:
            main_problem, _ = choose_main_problem(act_imp, act_ctr, retention, short_views, external_ratio)
        report_text = make_report(
            student_name, video_title, hypothesis, target_audience, planned_actions, target_views, target_ctr,
            act_views, act_imp, act_ctr, retention, likes, comments, subs, short_views,
            external_views, external_ratio, main_problem, next_actions, next_kpi, next_goal, reflection, next_hypothesis
        )
    except NameError:
        report_text = "先に『投稿前 Plan』と『投稿後 Check』の数値を入力してください。"

    st.markdown('<div class="section-heading">📄 自動生成PDCAレポート</div>', unsafe_allow_html=True)
    st.text_area("コピーして提出用レポートに使えます", value=report_text, height=460)
    st.download_button(
        "📥 PDCAレポートをテキストで保存",
        data=report_text.encode("utf-8"),
        file_name="ai_mv_pdca_report.txt",
        mime="text/plain"
    )
