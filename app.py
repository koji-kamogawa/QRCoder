import streamlit as st
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image
import io

# --- アプリ設定 ---
st.set_page_config(page_title="QRコード生成アプリ(Rev2)", layout="centered")

# --- サイドバー: QRコード設定 ---
st.sidebar.header("QRコード設定")

# エラー訂正レベルの選択
error_correction_levels = {
    "L (約7%復元可能)": ERROR_CORRECT_L,
    "M (約15%復元可能)": ERROR_CORRECT_M,
    "Q (約25%復元可能)": ERROR_CORRECT_Q,
    "H (約30%復元可能)": ERROR_CORRECT_H,
}
selected_error_correction_label = st.sidebar.selectbox(
    "エラー訂正レベル:",
    options=list(error_correction_levels.keys()),
    index=1 # デフォルトは M
)
qr_error_correction = error_correction_levels[selected_error_correction_label]

# ボックスサイズ（QRコードの1マスのピクセル数）
qr_box_size = st.sidebar.slider("ボックスサイズ (ピクセル数):", min_value=1, max_value=20, value=10)

# ボーダー（QRコード周囲の余白のマスの数）
qr_border = st.sidebar.slider("ボーダー (余白の幅):", min_value=0, max_value=10, value=4)

# --- メイン画面 ---
st.title("QRコード生成アプリ")
st.caption("入力したテキストのQRコードを生成します。設定はサイドバーで行えます。")

# テキスト入力
text_input = st.text_area("QRコードにするテキストを入力してください:", height=150)

# QRコード生成と表示
if text_input:
    try:
        # QRコードオブジェクトの作成
        qr = qrcode.QRCode(
            version=None, # バージョンは自動で決定
            error_correction=qr_error_correction,
            box_size=qr_box_size,
            border=qr_border,
        )
        # データの追加
        qr.add_data(text_input)
        qr.make(fit=True) # データに合わせて最適なバージョンで生成

        # PILイメージオブジェクトの作成
        img = qr.make_image(fill_color="black", back_color="white") # img は Pillow Image オブジェクト

        # --- 表示用バイトデータ生成 ---
        # Pillow ImageオブジェクトをPNG形式のバイトデータに変換
        buf_display = io.BytesIO()
        img.save(buf_display, format="PNG")
        byte_im_for_display = buf_display.getvalue() # 表示用のバイト列を取得

        st.subheader("生成されたQRコード:")
        # st.image にバイト列を渡す (Pillow Image の代わりに)
        st.image(byte_im_for_display, caption='生成されたQRコード', use_container_width=True)

        # --- ダウンロード処理 ---
        # 表示用に生成したバイトデータをそのままダウンロード用にも使用
        st.download_button(
            label="QRコードをダウンロード (PNG)",
            data=byte_im_for_display,  # バイト列 (bytes) を渡す
            file_name="qrcode.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"QRコードの生成または表示中にエラーが発生しました: {e}")
        # 詳細なエラー情報をアプリ上に表示
        st.exception(e)

else:
    st.info("テキストエリアに何か入力してください。")

st.sidebar.markdown("---")
st.sidebar.info("このアプリはStreamlitとqrcodeライブラリを使用しています。")