import streamlit as st
import json

st.title("選戰局勢即時模擬器 ($S_k$)")

# 建立分頁：切換「AI 快速貼上」與「手動拉桿調整」
tab1, tab2 = st.tabs(["🤖 AI 文字快速輸入", "🎛️ 手動拉桿調整"])

# 預設參數
data = {
    "m1": 50.0, "m2": 50.0, "m3": 50.0, "m4": 50.0,
    "alpha": 0.25, "beta": 0.25, "gamma": 0.25, "delta": 0.25,
    "phi": 1.0, "omega": 0.0, "delta_swan": 0.0
}

with tab1:
    st.subheader("貼上 AI 產出的 JSON 資料")
    ai_input = st.text_area(
        "請將 AI 生成的文字完整貼在下方：", 
        height=220,
        placeholder='{\n  "m1": 75.0, "m2": 60.0, "m3": 80.0, "m4": 55.0,\n  "alpha": 0.25, "beta": 0.25, "gamma": 0.25, "delta": 0.25,\n  "phi": 1.1, "omega": 5.0, "delta_swan": -3.0\n}'
    )
    
    if ai_input.strip():
        try:
            parsed_data = json.loads(ai_input)
            data.update(parsed_data)
            st.success("✅ AI 資料解析成功！已自動套用參數。")
        except Exception as e:
            st.error("❌ 格式不正確，請確認是否貼上完整的 JSON 文字。")

with tab2:
    st.caption("你也可以在這裡手動微調參數：")
    col1, col2 = st.columns(2)
    with col1:
        data["m1"] = st.slider("M1 指標", 0.0, 100.0, float(data["m1"]))
        data["m2"] = st.slider("M2 指標", 0.0, 100.0, float(data["m2"]))
        data["m3"] = st.slider("M3 指標", 0.0, 100.0, float(data["m3"]))
        data["m4"] = st.slider("M4 指標", 0.0, 100.0, float(data["m4"]))
    with col2:
        data["alpha"] = st.number_input("Alpha 權重", value=float(data["alpha"]))
        data["beta"] = st.number_input("Beta 權重", value=float(data["beta"]))
        data["gamma"] = st.number_input("Gamma 權重", value=float(data["gamma"]))
        data["delta"] = st.number_input("Delta 權重", value=float(data["delta"]))
    
    data["phi"] = st.slider("黨內整合係數 (Phi)", 0.5, 1.5, float(data["phi"]))
    data["omega"] = st.number_input("連動催票 (Omega)", value=float(data["omega"]))
    data["delta_swan"] = st.slider("資訊與黑天鵝 (Delta)", -20.0, 20.0, float(data["delta_swan"]))

# 核心數學公式計算
sk = ((data["alpha"] * data["m1"] + 
       data["beta"] * data["m2"] + 
       data["gamma"] * data["m3"] + 
       data["delta"] * data["m4"]) * data["phi"]) + data["omega"] + data["delta_swan"]

st.markdown("---")
st.metric(label="最終綜合指數 ($S_k$)", value=f"{sk:.2f}")

# 顯示當前使用的所有數據預覽
with st.expander("🔍 查看目前套用的詳細數據"):
    st.json(data)