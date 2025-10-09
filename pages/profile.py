import streamlit as st




# ------------------------------
# ตั้งค่าหน้าเว็บ
# ------------------------------


st.set_page_config(
    page_title="My Profile Page",
    page_icon="📊",
    layout="wide"
)


# ------------------------------
# CSS ตกแต่ง
# ------------------------------
st.markdown("""
    <style>
        .profile-pic {
            border-radius: 50%;
            width: 180px;
            height: 180px;
            object-fit: cover;
            border: 4px solid #4CAF50;
            margin-bottom: 10px;
        }
        .card {
            background-color: #f9f9f9;
            padding: 20px 25px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section-title {
            color: #2E86C1;
            font-weight: bold;
            font-size: 22px;
            margin-bottom: 10px;
        }
            .gradient-card {
            background: linear-gradient(135deg, #f8fbff 0%, #eef7ff 100%);
            padding: 24px 28px;
            border-radius: 18px;
            box-shadow: 0 10px 24px rgba(46, 134, 193, 0.12);
            border: 1px solid rgba(46, 134, 193, 0.15);
            margin-bottom: 22px;
        }
        /* ป้ายคำ (tags/pills) */
        .pill {
            display: inline-block;
            padding: 6px 12px;
            margin: 4px 6px 0 0;
            border-radius: 999px;
            background: #E8F4FD;
            color: #2E86C1;
            font-size: 13px;
            border: 1px solid #D6ECFF;
            white-space: nowrap;
        }
        /* หัวข้อย่อยดูเด่นขึ้น */
        .subhead {
            font-weight: 700;
            color: #1B4F72;
            margin: 10px 0 6px 0;
            font-size: 16px;
        }
        /* เส้นคั่นแบบ soft */
        .soft-divider {
            height: 1px;
            background: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(46,134,193,.25) 50%, rgba(0,0,0,0) 100%);
            margin: 10px 0 14px 0;
        }
            .block-container{ max-width: 1100px; padding-top:1rem; padding-bottom:3rem; }
            .section-title{ color:#2E86C1; font-weight:800; font-size:24px; margin:4px 0 14px 0; }
            .card{
            background:#fff; padding:22px 26px; border-radius:16px;
            border:1px solid #eef3f7; box-shadow:0 8px 20px rgba(0,0,0,.06); margin-bottom:16px;
            }
            .muted{ color:#6c7a89; }
            .soft-divider{ height:1px;
            background:linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(46,134,193,.25) 50%, rgba(0,0,0,0) 100%);
            margin:10px 0 16px 0;
            }
            .badge{
            display:inline-block; padding:4px 10px; margin:0 6px 6px 0; font-size:12px; border-radius:999px;
            background:#f3f7fb; border:1px solid #eef3f7;
            }
            .meta{ font-size:13px; color:#5f6b7a; }
            h3{ margin-bottom:.4rem; }
            .badge {
    display: inline-block;
    padding: 6px 12px;
    margin: 0 6px 6px 0;
    font-size: 13px;
    font-weight: 600;
    border-radius: 999px;
    background: rgba(46,134,193,0.15);   /* พื้นหลังฟ้าใส */
    color: #A8D8FF;                      /* ตัวอักษรสีฟ้าอ่อน */
    border: 1px solid rgba(46,134,193,0.4);
    transition: all 0.2s ease-in-out;
}
.badge:hover {
    background: rgba(46,134,193,0.35);   /* สีเข้มขึ้นเล็กน้อยตอน hover */
    color: #ffffff;                      /* ตัวอักษรขาวตอน hover */
    border-color: rgba(46,134,193,0.6);
    transform: translateY(-2px);
}

            
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# ส่วนหัวโปรไฟล์
# ------------------------------
st.title("👤 My Profile Page")
st.write("---")

col1, col2 = st.columns([0.5, 2])

with col1:
    st.image(
        "img/myPic/pic1.jpg",
        width=180,
        output_format="PNG"
    )

with col2:
    st.markdown("### 📌 ข้อมูลส่วนตัว")
    st.write("""
    **ชื่อ–สกุล:** สุทธิชัย มุกโชควัฒนา  
    **รหัสนักศึกษา:** 2213111178  
    **สาขา:** เทคโนโลยีสารสนเทศ (IT)  
    **มหาวิทยาลัย:** สถาบันเทคโนโลยีไทย-ญี่ปุ่น (TNI)  
    **อีเมล:** Suk.suthichai@gmail.com  
    **เบอร์โทรศัพท์:** 0616048252
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# ความสนใจ
# ------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🎯 ความสนใจด้าน Data Science / Data Mining</div>", unsafe_allow_html=True)

# แถวบน: วิสัยทัศน์ + แท็กความสนใจ

st.markdown("""
Data Science และ Data Mining เป็นสาขาที่ได้รับความนิยมมากในยุคดิจิทัล เนื่องจากข้อมูล (Data)
    กลายเป็นทรัพยากรที่มีค่าสูงสุดในการตัดสินใจขององค์กร ไม่ว่าจะเป็นธุรกิจ การตลาด หรือเทคโนโลยี
""")


st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)

# แถวกลาง: ด้านที่สนใจเชิงลึก (3 คอลัมน์)

st.markdown("<div class='subhead'>เหตุผลที่หลายคนสนใจสาขานี้</div>", unsafe_allow_html=True)
st.write("- ข้อมูลคือพลังในการตัดสินใจ การใช้ข้อมูลช่วยให้การตัดสินใจขององค์กรแม่นยำและมีประสิทธิภาพมากขึ้น")
st.write("- ผสมผสานหลายศาสตร์ ทั้งคณิตศาสตร์ สถิติ การเขียนโปรแกรม และความรู้เฉพาะทาง (Domain Knowledge)")
st.write("- ได้ใช้ความคิดเชิงวิเคราะห์ (Analytical Thinking) และสร้างสรรค์ในการแก้ปัญหา")



st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)

# แถวล่าง: โฟกัสงานถัดไป + ตัวอย่างการประยุกต์
c6, c7 = st.columns([1, 1])
with c6:
    st.markdown("<div class='subhead'>🔍 Data Science (วิทยาศาสตร์ข้อมูล) </div>", unsafe_allow_html=True)
    st.write("""
- ต้องการ วิเคราะห์พฤติกรรมของผู้บริโภค เพื่อคาดการณ์แนวโน้มในอนาคต เช่น การทำนายยอดขายหรือความต้องการของตลาด  
- สนใจการใช้ สถิติ, การเขียนโปรแกรม
- ต้องการพัฒนา โมเดลการคาดการณ์ (Predictive Model) หรือ ระบบแนะนำ (Recommendation System)  
- มีความอยากรู้อยากเห็นในการตั้งคำถาม
    """)
with c7:
    st.markdown("<div class='subhead'>⛏️ Data Mining (การทำเหมืองข้อมูล) </div>", unsafe_allow_html=True)
    st.write("""
- ความสนใจใน Data Mining มักเกิดจากความอยากค้นพบ "รูปแบบ (Patterns)" และ "ความสัมพันธ์ (Relationships)" ในข้อมูลจำนวนมหาศาล 
- ทำนายว่าโพสต์ประเภทใดควรโปรโมต (เช่น คลิปสั้น vs ยาว)  
- วาง Data Pipeline ง่าย ๆ สำหรับเก็บสถิติคอนเทนต์และอัปเดตโมเดลรายสัปดาห์
    """)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# ประสบการณ์
# ------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>💡 โปรเจกต์ที่เคยทำ</div>", unsafe_allow_html=True)

# ---------------- Project 1 ----------------
# ------------------------------
# Tabs ของโปรเจกต์
# ------------------------------
tabs = st.tabs([
    "📂 Expense App",
    "🤖 Maintenance Chatbot",
    "🛠️ Smart Clothline",
    "📊 Python Stock"
])

# ========== Project 1 ==========
with tabs[0]:
    st.markdown("<div class='section-title'>📂 Expense Management System</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        st.image(r"img\pro1\pic2.png", use_container_width=True,
                 caption="สรุปรายรับ–รายจ่ายแบบกราฟ (ตัวอย่างจากแอป)")
    with col2:
        st.markdown("**บทบาท:** Scrum Project Manager & Developer")
        st.markdown("**เทคโนโลยี:** Android Studio, Flutter, Firebase")
        st.markdown("""**ไฮไลต์งาน:**  
- บันทึกรายรับ–รายจ่ายพร้อมหมวดหมู่  
- สรุปรายงานแบบกราฟรายเดือน  
- ซิงก์ข้อมูลบนคลาวด์ผ่าน Firebase  
- บริหารงานแบบ Agile ในรายวิชา INT-303
        """)
        st.link_button("▶️ ดูวิดีโอโปรเจกต์", 
                       "https://drive.google.com/file/d/1KGXYmo1lSRtex1KiDezLxh8QtYBk9LRT/view",
                       type="primary")
        st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>Flutter</span><span class='badge'>Firebase</span><span class='badge'>Agile</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ========== Project 2 ==========
with tabs[1]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🤖 Automated Maintenance Request Chatbot</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        # สไลด์ง่าย ๆ (เปลี่ยนภาพได้ด้วยปุ่ม)
        images2 = [
            r"img/pro2/pic3.jpg",
            r"img/pro2/pic1.jpg",
            r"img/pro2/pic2.png",
        ]
        if "idx_pro2" not in st.session_state:
            st.session_state.idx_pro2 = 0
        st.image(images2[st.session_state.idx_pro2], use_container_width=True, caption="ตัวอย่างหน้าจอ Chatbot/Flow")
        cprev, cnext = st.columns(2)
        with cprev:
            if st.button("⬅️ Previous", key="prev_pro2"):
                st.session_state.idx_pro2 = (st.session_state.idx_pro2 - 1) % len(images2)
        with cnext:
            if st.button("Next ➡️", key="next_pro2"):
                st.session_state.idx_pro2 = (st.session_state.idx_pro2 + 1) % len(images2)
    with col2:
        st.markdown("**บทบาท:** ผู้พัฒนาเดี่ยว (รายวิชา RPA)")
        st.markdown("**เทคโนโลยี:** Power Automate, Microsoft Copilot Agent")
        st.markdown("""**ไฮไลต์งาน:**  
- รับคำขอแจ้งซ่อมผ่านแชทบอทแบบอัตโนมัติ  
- ออกแบบ Flow ให้ส่งต่อข้อมูล/แจ้งเตือนอัตโนมัติ  
- ลดภาระงานเอกสารและการตอบซ้ำ
        """)
        st.link_button("▶️ ดูวิดีโอโปรเจกต์", "https://www.youtube.com/watch?v=JEhAFhPJ46I")
        st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>RPA</span><span class='badge'>Power Automate</span><span class='badge'>Copilot</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ========== Project 3 ==========
with tabs[2]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🛠️ Smart Clothline (Arduino)</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        images3 = [
            r"img/pro3/pic1.jpg",
            r"img/pro3/pic2.jpg",
            r"img/pro3/pic3.jpg",
            r"img/pro3/pic4.jpg",
            r"img/pro3/pic5.jpg",
            r"img/pro3/pic6.jpg",
        ]
        if "idx_pro3" not in st.session_state:
            st.session_state.idx_pro3 = 0
        st.image(images3[st.session_state.idx_pro3], use_container_width=True, caption="ภาพจากการพัฒนา/เดโมราวตากผ้าอัจฉริยะ")
        cprev, cnext = st.columns(2)
        with cprev:
            if st.button("⬅️ Previous", key="prev_pro3"):
                st.session_state.idx_pro3 = (st.session_state.idx_pro3 - 1) % len(images3)
        with cnext:
            if st.button("Next ➡️", key="next_pro3"):
                st.session_state.idx_pro3 = (st.session_state.idx_pro3 + 1) % len(images3)
    with col2:
        st.markdown("**ผลงาน:** รางวัลชนะเลิศ TNI Smart Kaizen 2023")
        st.markdown("**เทคโนโลยี:** Arduino Uno R3, Rain Sensor, Motor Control, Arduino IDE")
        st.markdown("""**ไฮไลต์งาน:**  
- ตรวจจับฝนและสั่งงานมอเตอร์เก็บ/ปล่อยผ้าอัตโนมัติ  
- ต้นแบบ IoT เพื่อใช้จริงในบ้าน/หอพัก  
- ถ่ายทอดความรู้ให้รุ่นน้องเพื่อสานต่อโครงงาน
        """)
        st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>Arduino</span><span class='badge'>Sensor</span><span class='badge'>IoT</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ========== Project 4 ==========
with tabs[3]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Python Stock (Python + Streamlit)</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        st.image(r"img/pro4/pic1.png", use_container_width=True,
                 caption="กราฟตัวอย่าง/อินดิเคเตอร์จากโปรเจกต์")
    with col2:
        st.markdown("**ขอบเขต:** ดึงข้อมูลหุ้น SCB ย้อนหลัง 6 เดือน, Cleaning, Preprocessing, Indicators (MACD/RSI)")
        st.markdown("""**ไฮไลต์งาน:**  
- วิเคราะห์แนวโน้มและสัญญาณเทคนิคด้วย Python  
- แสดงผลผ่าน Streamlit Web App  
- สคริปต์พร้อม deploy และปรับใช้กับหุ้นตัวอื่นได้
        """)
        st.link_button("🌐 เปิดหน้าเว็บโปรเจกต์", "https://suthichaindr.streamlit.app/")
        st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>Pandas</span><span class='badge'>Matplotlib</span><span class='badge'>Streamlit</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# Skillset
# ------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🛠️ Skillset ที่เกี่ยวข้อง</div>", unsafe_allow_html=True)

skills = [
    "🐍 Python (Pandas, Numpy, Matplotlib, Scikit-learn)",
    "🗄️ Java (OOP)",
    "🌐 HTML/CSS (Web Development)",
    "☁️ Cloud (Firebase, Power Automate)",
    "🌐 Streamlit (Web App Development)",
    "📊 Data Visualization (Power BI)",
    "🤖 Machine Learning (Classification)",
    "🛠️ Arduino (IoT, Sensor, Motor Control)",
    
]

for skill in skills:
    st.markdown(f"- {skill}")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# Footer
# ------------------------------
st.write("---")
st.success("Tnank You 🚀")










#st.sidebar.title("📌 เมนู")
#menu = st.sidebar.radio(
#    "เลือกหน้า",
#    ["📑 Profile", "🎬 Youtube", "📂 Pet Recommender", "🛠️ Skillset"]
#)

# ------------------------------
# Main Page
# ------------------------------


