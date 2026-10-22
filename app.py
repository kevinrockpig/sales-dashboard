import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib

st.set_page_config(page_title="企業營運數據分析儀表板", layout="wide")

def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.subheader("🔒 系統受保護，請輸入存取密碼")
    user_input = st.text_input("輸入密碼", type="password")
    
    if st.button("確認"):
        input_hash = hashlib.sha256(user_input.encode()).hexdigest()
        if input_hash == st.secrets["DEMO_PASSWORD_HASH"]:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("密碼錯誤")
    return False

# 核心防護：未通過驗證前，強制中斷 Python 執行，前端絕對抓不到資料
if not check_password():
    st.stop()

try:

    st.title("📊 企業銷售數據自動化分析工具")
    st.markdown("上傳您的銷售 CSV 檔案，系統將自動進行數據清理、指標計算與視覺化圖表繪製。")

    # 提供示範資料下載功能，方便客戶測試
    st.sidebar.header("測試資料")
    if st.sidebar.button("產生示範數據"):
        sample_data = pd.DataFrame({
            "日期": pd.date_range(start="2026-01-01", periods=10, freq="D"),
            "產品名稱": ["產品A", "產品B", "產品A", "產品C", "產品B", "產品A", "產品C", "產品B", "產品A", "產品C"],
            "銷售數量": [10, 15, 8, 22, 12, 18, 5, 14, 20, 11],
            "銷售金額": [1000, 2250, 800, 4400, 1800, 1800, 1000, 2100, 2000, 2200]
        })
        st.sidebar.download_button("下載範例 CSV", sample_data.to_csv(index=False), "sample_sales.csv", "text/csv")

    # 檔案上傳區
    uploaded_file = st.file_uploader("請上傳銷售數據 CSV 檔", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # KPI 指標區
        st.subheader("💡 關鍵營運指標 (KPI)")
        col1, col2, col3 = st.columns(3)
        col1.metric("總銷售金額", f"${df['銷售金額'].sum():,}")
        col2.metric("總銷售數量", f"{df['銷售數量'].sum():,} 件")
        col3.metric("平均訂單金額", f"${df['銷售金額'].mean():.1f}")

        st.divider()

        # 圖表分析區
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("📈 產品銷售金額佔比")
            fig_pie = px.pie(df, values="銷售金額", names="產品名稱", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_chart2:
            st.subheader("📊 產品銷售數量對比")
            fig_bar = px.bar(df, x="產品名稱", y="銷售數量", color="產品名稱")
            st.plotly_chart(fig_bar, use_container_width=True)

        # 資料預覽與下載
        st.subheader("📋 數據明細預覽")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("👈 請點擊左側「產生示範數據」下載測試檔，或直接上傳您的 CSV 檔案進行體驗。")

except Exception as e:
    # 顯示給終端客戶看的友善訊息 (避免顯示紅色 Traceback)
    st.warning("⚠️ 數據載入暫時發生異常，請稍後再試或聯繫管理員。")
    
    # 將真實錯誤印在伺服器後台，方便你自己 debug (客戶看不到)
    print(f"後端錯誤紀錄: {e}")