import streamlit as st

# ページのタイトルとアイコン設定
st.set_page_config(
    page_title="YouTube KPI Dashboard", 
    page_icon="📊",
    layout="centered"
)

# --- 💡 カスタムCSS ---
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important; }
        h1, h2, h3, p, span, label, .stMarkdown { color: #F8FAFC !important; }
        div[data-testid="stTabs"] button {
            background-color: #1E293B !important; color: #64748B !important; font-size: 16px !important;
            font-weight: bold !important; padding: 12px 24px !important; border-radius: 8px 8px 0px 0px !important; 
            margin-right: 6px !important; border: 1px solid #334155 !important; border-bottom: none !important;
            transition: all 0.2s ease;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background-color: #FF0000 !important; color: #FFFFFF !important;            
            border: 1px solid #FF3B30 !important; border-bottom: none !important;
            box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.4); 
        }
        div[data-testid="stTabs"] [data-baseweb="tab-highlight-bar"] { background-color: #FF0000 !important; height: 4px !important; }
        
        /* 📦 通常のコンテナスタイル */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #1E293B !important; border: 2px solid #38BDF8 !important; padding: 15px !important;
            border-radius: 12px !important; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2) !important; margin-bottom: 20px !important;
        }
        
        /* 🛠️ 総合配信ステータス・目標戦略ボックス */
        .status-highlight-box {
            background-color: #2A3A52 !important;
            border: 2px solid #60A5FA !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin-top: 10px !important;
            margin-bottom: 25px !important;
            box-shadow: 0px 6px 25px rgba(56, 189, 248, 0.15) !important;
        }
        .status-highlight-box p, .status-highlight-box div {
            color: #F8FAFC !important;
        }
        
        /* 🚨 データ矛盾エラー専用の警告ボックス */
        .error-highlight-box {
            background-color: #451A03 !important;
            border: 2px solid #EF4444 !important;
            border-radius: 12px !important;
            padding: 25px !important;
            margin-top: 10px !important;
            margin-bottom: 25px !important;
            box-shadow: 0px 6px 25px rgba(239, 68, 68, 0.2) !important;
        }
        .error-highlight-box h3, .error-highlight-box p, .error-highlight-box li {
            color: #FEE2E2 !important;
        }
        
        .stNumberInput input { background-color: #FFFFFF !important; color: #0F172A !important; font-weight: bold !important; font-size: 16px !important; border-radius: 6px !important; }
        div[data-testid="stSlider"] { background-color: #334155 !important; padding: 15px 25px 20px 25px !important; border-radius: 8px !important; border: 1px solid #475569 !important; }
        
        b { color: #F472B6 !important; }
        
        .section-heading {
            font-size: 18px !important;
            font-weight: bold !important;
            color: #0F172A !important;
            background-color: #F1F5F9 !important;
            padding: 12px 16px !important;
            margin-top: 45px !important;
            margin-bottom: 18px !important;
            border-left: 6px solid #475569 !important;
            border-radius: 4px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }
        
        .status-badge {
            padding: 10px 14px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
            display: inline-block;
            margin-top: 5px !important;
            margin-bottom: 20px !important;
            margin-left: 24px !important;
            width: calc(100% - 24px) !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
            box-shadow: 0px 3px 10px rgba(0,0,0,0.3);
            box-sizing: border-box !important;
        }
        .bg-red { background-color: #EF4444 !important; color: #FFFFFF !important; border-left: 5px solid #991B1B; }
        .bg-yellow { background-color: #F59E0B !important; color: #FFFFFF !important; border-left: 5px solid #92400E; }
        .bg-green { background-color: #10B981 !important; color: #FFFFFF !important; border-left: 5px solid #065F46; }
        .bg-dark { background-color: #6B7280 !important; color: #FFFFFF !important; border-left: 5px solid #374151; }
        
        .advice-text {
            font-size: 15px !important;
            line-height: 1.9 !important;
            color: #F1F5F9 !important;
            margin-top: 5px !important;
            margin-bottom: 50px !important;
            margin-left: 24px !important;
            margin-right: 15px !important;
        }
        
        .alert-highlight {
            background-color: rgba(239, 68, 68, 0.15) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            padding: 12px 15px !important;
            border-radius: 6px !important;
            margin: 15px 0 !important;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# メインタイトル
st.markdown("<h1 style='text-align: center; color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56,189,248,0.4);'>🤖 AI-MV配信分析システム</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8 !important;'>新規チャンネル運用実習用 PDCAシミュレーター</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 1. 投稿前：目標逆算（Plan）", "🔍 2. 投稿後：実績分析（Check & Action）"])

# ==========================================
# --- 🎯 タブ1：投稿前：目標逆算（Plan） ---
# ==========================================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h3 style='color: #38BDF8 !important; margin-top:0;'>⚙️ シミュレーション設定</h3>", unsafe_allow_html=True)
        target_views = st.number_input("目指す視聴回数（回）", min_value=50, value=100, step=50)
        target_ctr = st.slider("狙うクリック率（CTR %）", min_value=1.0, max_value=20.0, value=5.0, step=0.1)
    
    required_imp = target_views / (target_ctr / 100)
    
    with st.container(border=True):
        st.markdown("<h3 style='color: #FF3B30 !important; margin-top:0;'>💡 算出された必要データ</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.metric(label="■ 目標MV視聴回数", value=f"{target_views:,} 回")
        with col2: st.metric(label="■ 必要な総インプレッション数", value=f"{int(required_imp):,} 回")

    # 🛠️ 設定された目標数値（CTR ＆ 視聴回数）に対する複合戦略カルテ
    st.markdown(f"""
    <div class="status-highlight-box">
        <h3 style='color: #60A5FA !important; margin-top:0; margin-bottom:15px;'>📊 設定された目標に対する戦略カルテ</h3>
    """, unsafe_allow_html=True)
    
    # ① クリック率（CTR）への言及
    if target_ctr >= 7.0:
        st.markdown(f"""
            <p>🎯 <b>【CTR設定：{target_ctr}%】ハイレベル目標（天才デザイナー級）</b><br>
            YouTubeの音楽ジャンル平均（4%〜5%）を大きく超える強気な目標です。これを達成するには、スマホの小さな画面でも一瞬で目を引く<b>「圧倒的な視覚的インパクト」</b>が必須。イラストの構図、キャラクターの表情の強さ、文字フォントや配色に一切の妥協を許さない『神サムネ』を制作してください！</p>
        """, unsafe_allow_html=True)
    elif target_ctr >= 4.0:
        st.markdown(f"""
            <p>🎯 <b>【CTR設定：{target_ctr}%】スタンダード目標（合格ライン）</b><br>
            新規チャンネルが目指すべき美しく現実的な数値です。クリアのためには、チーム内の他のメンバーの作品と見比べたときに「自分のサムネイルが埋もれていないか」を横並びでチェックし、デザインの『基本の打率』を徹底的に高めていきましょう。</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <p>🎯 <b>【CTR設定：{target_ctr}%】セーフティ目標（要引き上げ）</b><br>
            少し安全圏を狙いすぎな設定です。音楽MVは視覚的な美しさが命となるため、初期チャンネルであっても4.0%以上を狙うのが実習の醍醐味！デザインを「派手にする」「文字を太くする」など工夫して、目標を引き上げてみませんか？</p>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)

    # ② 目標視聴回数（Views）への言及
    if target_views >= 1000:
        st.markdown(f"""
            <p>🔥 <b>【視聴回数設定：{target_views:,}回】総力戦フェーズ（メガヒット目標）</b><br>
            新設チャンネルとしては非常に大きな、挑戦的な大目標です！身内やチーム内の再生だけでこの大台に届くことは絶対にありません。YouTubeの検索・おすすめアルゴリズムを味方につけるのはもちろん、<b>外部SNS（XやTikTok等）でインフルエンサーを巻き込んだり、メンバー全員のリポスト協力を借りて『初期アクセスのお祭り感』を組織的に作り出すマーケティング戦略</b>が不可欠になります。</p>
        """, unsafe_allow_html=True)
    elif target_views >= 300:
        st.markdown(f"""
            <p>🚀 <b>【視聴回数設定：{target_views:,}回】コミュニティ拡張フェーズ（スマッシュヒット目標）</b><br>
            「実習生個人の熱量」に加え、「見知らぬ第3者（一般のボカロファン・AI音楽ファン）」を最低でも数十人以上呼び込み、さらにリピート再生してもらう必要がある絶妙な目標値です。概要欄にフル歌詞を記載してYouTubeの検索に引っかかりやすくするSEO対策や、15秒のショート動画を本編と同時に投稿して認知の網を広げる多角的なアプローチを準備しましょう。</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <p>🌱 <b>【視聴回数設定：{target_views:,}回】ファーストフォロワー獲得フェーズ（手堅い初動目標）</b><br>
            まずは確実に達成可能な、手堅く現実的なファーストステップです。このフェーズで最も重要なのは、<b>『チーム全員でお互いのMVを最初から最後まで熱心に視聴し合うこと』</b>です。初動の視聴維持率（動画をどこまで長く見てくれたか）を高めることで、YouTube AIに「これは新設だけど非常に質の高い動画だ」と認知させ、次の動画へのインプレッション（露出）拡大に繋げるベースを作りましょう。</p>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

    # 📋 投稿前チェックリスト
    st.markdown("### 📋 投稿前チェックリスト（成功確率を上げる事前準備）")
    st.markdown("<hr style='border-color: #334155; margin-top:0; margin-bottom:10px;'>", unsafe_allow_html=True)
    
    # 📝 項目A：タイトルとサムネイル
    st.markdown('<div class="section-heading">📝 A. サムネイルとタイトルの同時最適化</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge bg-green">🟩 【投稿前チェック】スマホ画面での視認性を必ず確認してください</div>', unsafe_allow_html=True)
    st.markdown('<div class="advice-text">'
                'YouTube視聴者の7割以上はスマホです。作成したサムネイルをPCの大画面だけで見て満足してはいけません。<br>'
                '1. <b>スマホサイズでの確認</b>：画像をスマホの画面サイズ（またはPC画面上で10%程度に縮小）まで小さくしたとき、中央のイラストや文字がボヤけずに判別できるか確認してください。<br>'
                '2. <b>右下の「時間表示（シャク）」トラップ</b>：YouTubeの仕様上、動画の右下には再生時間が黒い四角で強制表示されます。<b>サムネイルの右下隅に重要な文字やキャラクターの顔を配置すると、この時間表示に被って完全に隠れてしまいます。</b> デザインの重要要素は必ず中央〜左側に寄せましょう。'
                '</div>', unsafe_allow_html=True)

    # 🏷️ 項目B：ハッシュタグとSEO
    st.markdown('<div class="section-heading">🏷️ B. ハッシュタグとメタデータの仕込み（全角禁止令）</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge bg-yellow">🟨 【ミス多発注意】概要欄に記載するハッシュタグの「＃」は100%半角に！</div>', unsafe_allow_html=True)
    st.markdown('<div class="advice-text">'
                '新規チャンネルがYouTube AIに見つけてもらうための唯一の命綱が、概要欄のテキスト情報です。<br>'
                '<span class="alert-highlight">'
                ' ⚠️ <b>【実習生全員でトリプルチェックしてください】</b><br>'
                ' 概要欄のハッシュタグが全角の「＃ボカロ」になっているケースが多発しています。<b>全角だとYouTubeのシステムに青いリンクのタグとして認識されず、ただの文字列になってしまい、検索や関連フィードに1ミリも載らなくなります。</b> 必ず <b>#SunoAI #ボカロ #作業用BGM</b> のように、シャープを半角の「#」に統一してください。'
                '</span><br>'
                'また、作詞・作曲（SunoAIなど）、動画編集のクレジットに加え、<b>曲のフル歌詞を概要欄にすべて書き起こして記載</b>してください。歌詞の言葉すべてが検索キーワード（SEO）となり、AIが動画のジャンルを特定する強力な手助けになります。'
                '</div>', unsafe_allow_html=True)

    # 📱 項目C：ショート動画の準備
    st.markdown('<div class="section-heading">📱 C. 初動ブースト用のショート動画切り出し</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge bg-dark">⬛ 【準備必須】本編の投稿と同時にショート動画を1本以上用意すること</div>', unsafe_allow_html=True)
    st.markdown('<div class="advice-text">'
                '新設アカウントの場合、数分ある本編MVをいきなり見つけてもらうのは至難の業です。そのため、投稿後すぐに連動ショート動画を出す準備をあらかじめ完了させておいてください。<br>'
                '1. <b>最も盛り上がる15秒の選定</b>：イントロではなく、曲の中で一番キャッチーな「サビの15秒間」を縦型（9:16）で切り出します。<br>'
                '2. <b>常時テロップの配置</b>：ショート動画の画面上部などに、「AIで神曲MV作ってみた」「最後まで聴いて」といったスクロールを止めるためのキャッチコピー（固定テロップ）をあらかじめ動画ファイル内に合成しておいてください。視聴維持率が劇的に向上します。'
                '</div>', unsafe_allow_html=True)


# =========================================================
# --- 🔍 タブ2：投稿後：実績分析（Check & Action） ---
# =========================================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h3 style='color: #38BDF8 !important; margin-top:0;'>📈 アナリティクス実績数値の入力</h3>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #38BDF8 !important; font-weight: bold; margin-bottom: 5px;'>🎬 対象MV本体の実績データ（アナリティクス表示順）</p>", unsafe_allow_html=True)
        
        # 🛠️ 入力順序をアナリティクス標準（視聴回数 → インプレッション → クリック率）に並び替え
        act_total_views = st.number_input("① 実際の視聴回数（回）", min_value=0, value=45, step=5)
        
        col_in1, col_in2 = st.columns(2)
        with col_in1: act_imp = st.number_input("② 実際のインプレッション数（回）", min_value=0, value=1000, step=50)
        with col_in2: act_ctr = st.number_input("③ 実際のインプレッションのクリック率（CTR %）", min_value=0.0, max_value=100.0, value=4.5, step=0.1)
        
        st.markdown("<hr style='border-color: #334155; margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FF3B30 !important; font-weight: bold; margin-bottom: 5px;'>📱 連動ショート動画の実績（※未投稿は0でOK）</p>", unsafe_allow_html=True)
        act_short_views = st.number_input("このMVから切り出したショート動画の最高視聴回数（回）", min_value=0, value=0, step=50)
        
    # 🧮 計算ロジック
    yt_internal_views = int(act_imp * (act_ctr / 100))
    
    # 🚨 データ矛盾エラー検知フラグ
    is_data_error = act_total_views < yt_internal_views

    if is_data_error:
        # ❌ 【エラー表示】矛盾がある場合のアラート画面
        st.markdown(f"""
        <div class="error-highlight-box">
            <h3 style='margin-top:0;'>⚠️ 入力エラー：データの整合性が取れません</h3>
            <p>入力された「① 実際の視聴回数（<b>{act_total_views:,} 回</b>）」が、YouTube内の推定視聴数（<b>{yt_internal_views:,} 回</b>）を下回っています。以下の原因が考えられます。確認して修正してください：</p>
            <ul>
                <li><b>原因① データのタイムラグ</b>：アナリティクスの「インプレッション数」や「クリック率」はリアルタイムに近いですが、「視聴回数」の確定反映には最大1〜2日の遅れが発生することがあります。</li>
                <li><b>原因② アナリティクスの見間違い</b>：「インプレッション数」の桁数を一桁多く間違えて入力していないか、別の動画の数値を混ぜていないか確認してください。</li>
                <li><b>原因③ 計算上の数値</b>：インプレッション({act_imp:,}回) × クリック率({act_ctr}%) = {yt_internal_views:,}回 の視聴がYouTube内で確実に生まれているはずです。総視聴回数は必ずこの数値以上になります。</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        act_external_views = 0
        external_ratio = 0
    else:
        # ⭕ 正常処理：外部流入数と割合を算出
        act_external_views = act_total_views - yt_internal_views
        external_ratio = (act_external_views / act_total_views * 100) if act_total_views > 0 else 0
        
        if act_ctr >= 10.0: ctr_status = "👑 神レベル！"
        elif act_ctr >= 4.0: ctr_status = "🔥 素晴らしい！"
        else: ctr_status = "⚠️ 低めです"
        
        if act_short_views == 0: short_status = "未検証"
        elif act_short_views < 500: short_status = "低（要改善）"
        else: short_status = "高（牽引中！）"

        # 🌟 総合配信ステータス
        st.markdown(f"""
        <div class="status-highlight-box">
            <h3 style='color: #60A5FA !important; margin-top:0; margin-bottom:15px;'>📝 現在の総合配信ステータス</h3>
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
                <div style="flex: 1; min-width: 250px; line-height: 1.8;">
                    🎬 <b>実際の総視聴回数: {act_total_views:,} 回</b><br>
                    <span style="font-size: 13px; color: #94A3B8 !important;">
                        └ 📥 YouTube内のおすすめ・検索等: {yt_internal_views:,} 回<br>
                        └ 🌐 外部SNS・その他からの流入: {act_external_views:,} 回 (比率: <b>{external_ratio:.1f}%</b>)
                    </span>
                </div>
                <div style="flex: 1; min-width: 250px; line-height: 1.8;">
                    📊 対象MVのクリック率: <b>{act_ctr}%</b> ({ctr_status})<br>
                    📱 ショート最高視聴数: <b>{act_short_views:,} 回</b> ({short_status})
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # --- カルテの出力エリア ---
    st.markdown("### 🛠️ 項目別・実習アドバイス（総合診断カルテ）")
    st.markdown("<hr style='border-color: #334155; margin-top:0; margin-bottom:10px;'>", unsafe_allow_html=True)
    
    # 🎬 1. インプレッション
    st.markdown('<div class="section-heading">🎬 1. インプレッション（YouTube AIからの露出評価）</div>', unsafe_allow_html=True)
    if act_imp < 1000:
        st.markdown('<div class="status-badge bg-yellow">🟨 【インプレッション：低め】新規チャンネルの壁に当たっています。検索（SEO）と公式回遊機能の2軸で露出を増やしましょう</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    'YouTubeのシステムが動画のジャンルを十分に把握できておらず、おすすめ表示（ブラウジング）が少なめです。AIに頼るだけでなく、「検索から能動的なユーザーを呼び込む対策」と「公式のYouTube導線機能」をフル活用してチャンネル内のトラフィックを循環させてください。<br><br>'
                    '<b>* 解決アクション①（概要欄・タイトルのリニューアル【YouTube SEO対策】）</b>：<br>'
                    'YouTubeの検索AIに動画の内容を正しく伝えるため、動画のテキスト情報を充実させます。<br>'
                    '1. <b>キーワードの追加</b>：タイトルや概要欄の冒頭に、音楽ファンが検索しそうな言葉（例：「作業用BGM」「ボカロ」「SunoAI」など）を自然な文章で盛り込んでください。<br>'
                    '2. <b>クレジットと歌詞の掲載</b>：概要欄に、作詞・作曲、動画編集の担当者名や、曲のフル歌詞をすべてテキストで記載してください。歌詞のフレーズそのものが検索キーワードになり、検索からのインプレッションを引き上げます。<br>'
                    '3. <b>ハッシュタグの精査</b>：概要欄の最後に、チーム共通のタグやジャンルタグを3〜5個設置してください。<br>'
                    '<span class="alert-highlight">'
                    ' ⚠️ 【最重要チェック！】間違えて全角の「＃」を使っていませんか？<br>'
                    ' <b>全角の「＃」だとただの普通の文字として扱われ、タグ機能が完全に無効化されます。必ず半角の「#」になっているかメンバー全員で確認してください。</b>'
                    '</span><br>'
                    '<b>* 解決アクション②（YouTube Studio内での「終了画面」と「カード」の実装）</b>：<br>'
                    '動画編集画面の右側メニューにある公式の回遊機能を設定し、視聴者をチームの他動画へ流します。<br>'
                    '1. <b>終了画面（ラスト5〜20秒の導線）</b>：動画の最後に「メンバー全員のMVが入った公式プレイリスト」と、チャンネル登録を促す「登録ボタン」の2つの要素を必ず画面内に配置してください。<br>'
                    '2. <b>カード（動画の途中で出すおすすめ情報）</b>：動画の途中で視聴者が離脱しやすいタイミングをアナリティクスで特定し、その瞬間に「カード」を設定してください。離脱しそうなユーザーをチャンネル内に引き留めることができます。'
                    '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge bg-green">🟩 【インプレッション：順調】AIが動画のジャンルを認識し、音楽ファンへのお勧めを開始しています</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    '新設チャンネルとしては十分な露出が獲得できています。AIの評価は良好です。<br><br>'
                    '<b>* 解決アクション（終了画面機能による回遊）</b>：この勢いを活かし、動画の最後（終了画面機能）に、メンバーが作った「他のMVのサムネイルリンク」や「グループの公式プレイリスト」を直接設置してください。自分の動画を見終わった視聴者をそのままチャンネル内の別動画へ誘導し、チーム全体のファン（チャンネル登録者）になってもらう動線を強化しましょう。'
                    '</div>', unsafe_allow_html=True)

    # 📊 2. CTR・クリック率
    st.markdown('<div class="section-heading">📊 2. CTR・クリック率（人間からのデザイン評価）</div>', unsafe_allow_html=True)
    if act_ctr >= 10.0:
        st.markdown('<div class="status-badge bg-green">👑 【CTR：神レベル】10%突破！プロも驚く超天才的な快挙・歴史的傑作サムネイルです</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    'サムネイルとタイトルの組み合わせが、音楽ファンの心を完全に射抜いています。<br><br>'
                    '<b>* 解決アクション（神デザインの言語化）</b>：なぜ自分のサムネイルがここまで人を惹きつけたのか（イラストの構図、キャラクターの表情、文字の色使い、余白など）をチーム内で徹底的に言語化し、共有してください。このノウハウはグループ全体の最大の資産になります。他のメンバーの伸び悩んでいるMVのサムネイルを、このデザインの法則を真似して修正してあげましょう！'
                    '</div>', unsafe_allow_html=True)
    elif act_ctr >= 4.0:
        st.markdown('<div class="status-badge bg-green">🟩 【CTR：合格】音楽ファンの心を掴んでいます！サムネイルのデザインセンスはバッチリです</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    '一般的な音楽ジャンルの平均値（4%〜7%）をクリアしています。自信を持ってください！<br><br>'
                    '<b>* 解決アクション（要素の維持）</b>：今回の大胆な文字の目立ち方や、映像の世界観の出し方は大正解です。この動画をグループの「成功事例」として、今後サムネイルを調整する際のベース基準に設定しましょう。'
                    '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge bg-red">🟥 【CTR：要改善】クリック率が低めです。他のメンバーの動画と比較してみましょう</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    'AIが画面に表示してくれているものの、多くの視聴者にスルーされてしまっています。<br><br>'
                    '<b>* 解決アクション（デザインの横比較とリニューアル）</b>：同じチャンネル内にある「他のメンバーが作ったMV」や「過去一番CTRが高かった動画」のサムネイルと自分のものを見比べてみてください。文字の太さ、イラストの明暗、キャラクターの表情や大きさにどんな違いがありますか？伸びているメンバーの要素を参考にして、今すぐこの動画の<b>サムネイル画像をブラッシュアップ（差し替え）</b>してみましょう。タイトルに「【生成AI MV】」などの共通のフックを足すのも有効です。'
                    '</div>', unsafe_allow_html=True)

    # 📱 3. ショート動画連動
    st.markdown('<div class="section-heading">📱 3. ショート動画連動（新規ファン獲得の呼び水評価）</div>', unsafe_allow_html=True)
    if act_short_views == 0:
        st.markdown('<div class="status-badge bg-yellow">🟨 【ショート：未着手】ロング動画だけでの運用です。今すぐショートを解禁しましょう！</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    '新規チャンネルにおいて、通常のロング動画（MV本体）だけで認知を広げるのは非常に時間がかかります。ショート動画は最大の無料広告チラシです。<br><br>'
                    '<b>* 解決アクション（最初の1本の切り出し）</b>：自分の担当MVのサビの部分（一番盛り上がるところ）を15秒切り抜き、投稿してください。<br>'
                    '<span class="alert-highlight">'
                    ' ⚠️ 【重要ハッシュタグチェック！】<br>'
                    ' <b>ショート動画のタイトルに入れるタグが、全角の「＃」になっていないか必ず確認してください（必ず半角の「#」を使うこと）。全角のままだと関連動画フィードに載らなくなります。</b>'
                    '</span>'
                    '</div>', unsafe_allow_html=True)
    elif act_short_views < 500:
        st.markdown('<div class="status-badge bg-dark">⬛ 【ショート：伸び悩み】初動不足です。動画を改善して『再投稿』しましょう</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    'YouTubeショートはアルゴリズム上、一度再生の波が止まった過去動画の設定を後から直しても視聴数は戻りません。<br><br>'
                    '<b>* 解決アクション（動画クリエイティブを修正して新しく再投稿する）</b>：<br>'
                    '同じMVの素材を使う場合でも、以下の『3大編集ハック』を取り入れて動画を新しく作り直し、<b>別動画として改めて投稿</b>してください。<br>'
                    '1. <b>フックの強化</b>：開始1秒目から「最も映像が派手で、メロディが盛り上がるサビの瞬間」をぶつける。<br>'
                    '2. <b>視覚情報の追加</b>：画面上部にキャッチコピー（テロップ）を常時固定表示する。<br>'
                    '3. <b>テンポの調整</b>：15秒の中でカットの切り替わるスピードを少し早めにする。'
                    '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge bg-green">🟩 【ショート：順調】アクセスを集めて認知を広げる武器として機能しています</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    'ショート動画で新規ファンを引きつけられています。波が来ているうちに、固定コメント欄に本編MVのURLを貼り、ピン留めして動線をさらに強固にしてください。'
                    '</div>', unsafe_allow_html=True)

    # 🌐 4. 外部SNS・コミュニティ連携
    st.markdown('<div class="section-heading">🌐 4. 外部SNS・コミュニティ連携（アルゴリズムに頼らない自力集客評価）</div>', unsafe_allow_html=True)
    
    if is_data_error:
        st.markdown('<div class="status-badge bg-dark">⬛ データエラーのためアドバイスを表示できません。</div>', unsafe_allow_html=True)
    
    elif external_ratio == 0:
        st.markdown('<div class="status-badge bg-red">🟥 【外部流入：0%】YouTube外からの動線が皆無です。AI頼みを脱却し、最初の50視聴を自力で呼び込みましょう</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    '現在、YouTube内のおすすめ機能や検索だけで視聴が回っています。新設チャンネルの初期フェーズでは、YouTube AIの評価が下がる（おすすめが止まる）と視聴数がピタッとゼロになってしまうリスクがあります。他SNSを活用して「自力集客のパイプ」を今すぐ作りましょう。<br><br>'
                    '<b>🔥 【最優先のX（Twitter）対策アクション】</b><br>'
                    '1. <b>「動画付き」告知ポストの徹底</b>：単にYouTubeのリンクだけを貼ったポストは、Xの仕様上インプレッションが極端に下げられます。<b>必ずMVのサビなど15〜20秒の動画ファイルを直接ポストに添付し、そのリプライ欄（またはポストの最後）にYouTubeリンクを貼る形</b>で投稿してください。<br>'
                    '2. <b>ハッシュタグは半角で3つまで</b>：ポスト文に `#SunoAI` `#ボカロ` などのジャンルタグを添えます。全角の「＃」は機能しないので必ず半角にしてください。<br>'
                    '3. <b>TikTokへの同時マルチ投稿</b>：ショート用に作った縦型動画をそのままTikTokにも投稿し、プロフィールにチャンネルのリンクを載せて網を広げてください。'
                    '</div>', unsafe_allow_html=True)
                    
    elif external_ratio < 30.0:
        st.markdown(f'<div class="status-badge bg-yellow">🟨 【外部流入：初動推進】他SNSの成果が「比率 {external_ratio:.1f}%」出ています！チームの横連携でさらにブーストをかけましょう</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    '素晴らしい！アナリティクスには隠れていますが、計算上、確実にあなたのSNS発信や口コミから視聴者がやってきています。この「外部からの熱量の高いアクセス」が、YouTube AIに「初動が良い動画だ」と判断させる強力なスパイスになります。ここからさらに比率を引き上げる対策を行います。<br><br>'
                    '<b>🤝 【グループ全員で行う拡散ブースト・アクション】</b><br>'
                    '1. <b>引用リポストで「お祭り感」を自演する</b>：メンバーがXでMV告知をしたら、他の全員がただのリポストではなく「引用リポスト」で曲の感想や推しポイントを熱く語って拡散してください。タイムライン上でグループ全体の熱気が外部ユーザーに伝わり、クリック率が跳ね上がります。<br>'
                    '2. <b>インプレッションの相互乗り入れ</b>：メンバー個人のSNSアカウントのプロフィールや固定ポストに、自分の動画だけでなく「グループの最新MVプレイリスト」のURLを掲載し、チーム全体でトラフィックを回し合ってください。'
                    '</div>', unsafe_allow_html=True)
                    
    else:
        st.markdown(f'<div class="status-badge bg-green">🟩 【外部流入：最強！】総視聴の {external_ratio:.1f}% が外部動線！SNSマーケティングの天才的な成功事例です</div>', unsafe_allow_html=True)
        st.markdown('<div class="advice-text">'
                    '驚異的な数値です！YouTubeのアルゴリズムだけに依存せず、自分たちの手で爆発的なアクセスを呼び込むことに成功しています。この自力ブーストによって、今後YouTube側のおすすめインプレッションも二次関数的に伸びていく可能性が非常に高い状態です。今の熱量を固定ファン化しましょう。<br><br>'
                    '<b>👑 【ファンを完全に定着させるコミュニティ化・アクション】</b><br>'
                    '1. <b>コメント欄の100%ハート＆リプライハック</b>：SNSからYouTubeにわざわざ移動してコメントを残してくれたユーザーは、超高熱量なコアファン候補です。あなたの言葉で感謝の返信を書き、コメントの最上部に「固定コメント」として次回の活動予告や他SNSのリンクをピン留めしてください。<br>'
                    '2. <b>Xでの「第2波」ポスト（時間差攻撃）</b>：1回の告知で終わらせず、数日後に「制作秘話」や「AI生成時のプロンプト（呪文）のこだわり」などを画像付きでポストし、まだ見ていなかったSNSフォロワーを再度YouTubeへ誘導する第2の導線を作ってください。'
                    '</div>', unsafe_allow_html=True)