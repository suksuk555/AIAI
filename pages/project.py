import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image

# -----------------------------
# ตั้งค่าหน้าเว็บ
# -----------------------------
st.set_page_config(page_title="AI Trash Classification", page_icon="♻️", layout="wide")

st.title("♻️ ระบบจำแนกประเภทขยะด้วย AI")
st.write("สามารถเลือกได้ว่าจะ 'ถ่ายภาพ' หรือ 'อัปโหลดภาพขยะ' เพื่อให้ AI ช่วยจำแนกประเภท")

# -----------------------------
# โหลดโมเดล (cache resource)
# -----------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model/trash_model.h5")

model = load_model()

# -----------------------------
# รายชื่อคลาส
# -----------------------------
class_names = ['cardboard','danger','glass', 'metal', 'paper', 'plastic', 'trash']

# -----------------------------
# Mapping ประเภทขยะ → ถังขยะสี
# -----------------------------
bin_mapping = {
    "cardboard": ("ถังสีเหลือง ♻️ (รีไซเคิล)", "yellow_bin.png"),
    "danger": ("ถังสีแดง ⚠️ (ขยะอันตราย)", "red_bin.png"),
    "glass": ("ถังสีเหลือง ♻️ (รีไซเคิล)", "yellow_bin.png"),
    "metal": ("ถังสีเหลือง ♻️ (รีไซเคิล)", "yellow_bin.png"),
    "paper": ("ถังสีเหลือง ♻️ (รีไซเคิล)", "yellow_bin.png"),
    "plastic": ("ถังสีเหลือง ♻️ (รีไซเคิล)", "yellow_bin.png"),
    "trash": ("ถังสีฟ้า 🗑️ (ขยะทั่วไป)", "blue_bin.png")
}

# -----------------------------
# ส่วนให้ผู้ใช้เลือกว่าจะใช้กล้องหรืออัปโหลด
# -----------------------------
option = st.radio(
    "📷 เลือกวิธีนำเข้าภาพ:",
    ("ถ่ายภาพจากกล้อง", "อัปโหลดไฟล์จากเครื่อง")
)

img_file = None

if option == "ถ่ายภาพจากกล้อง":
    img_file = st.camera_input("กดปุ่มเพื่อถ่ายภาพ")
elif option == "อัปโหลดไฟล์จากเครื่อง":
    img_file = st.file_uploader("📤 อัปโหลดภาพ (.jpg, .png)", type=["jpg", "jpeg", "png"])

# -----------------------------
# ประมวลผลภาพเมื่อมีไฟล์เข้ามา
# -----------------------------
if img_file is not None:
    img = Image.open(img_file).convert("RGB")
    st.image(img, caption="ภาพที่เลือก", use_container_width=True)

    # เตรียมข้อมูลให้เข้ากับโมเดล
    img_resized = img.resize((224, 224))
    x = keras_image.img_to_array(img_resized)
    x = np.expand_dims(x, axis=0) / 255.0

    # ทำนาย
    preds = model.predict(x)
    predicted_class = class_names[np.argmax(preds)]
    confidence = np.max(preds) * 100

    # แสดงผล
    st.subheader(f"📦 ประเภทขยะ: **{predicted_class.capitalize()}**")
    st.write(f"🔍 ความมั่นใจ: **{confidence:.2f}%**")

    bin_name, bin_img = bin_mapping[predicted_class]
    st.success(f"ควรทิ้งใน: {bin_name}")
    st.image(bin_img, caption=bin_name, width=200)

# -----------------------------
# Sidebar แสดงข้อมูลเพิ่มเติม
# -----------------------------
st.sidebar.title("♻️ ประเภทถังขยะ")
with st.sidebar.expander("ถังสีเหลือง ♻️ (รีไซเคิล)"):
    st.write("- ขวดพลาสติก\n- กระดาษ\n- กระป๋องอลูมิเนียม\n- แก้วหรือโลหะที่ไม่ปนเปื้อน")
with st.sidebar.expander("ถังสีแดง ⚠️ (ขยะอันตราย)"):
    st.write("- หลอดไฟ\n- แบตเตอรี่\n- สเปรย์\n- ยาหมดอายุ")
with st.sidebar.expander("ถังสีฟ้า 🗑️ (ขยะทั่วไป)"):
    st.write("- ถุงพลาสติกมันเยิ้ม\n- โฟมเปื้อนอาหาร\n- กระดาษทิชชู่")

# -----------------------------
# ป๊อปอัปเพิ่มเติม
# -----------------------------
with st.popover("📖 ดูรายละเอียดโครงงานเพิ่มเติม"):
    st.subheader("ระบบจำแนกประเภทขยะด้วย AI")

    
    st.write("""
**🧠 แนวคิดของโปรเจกต์**\n
    โปรเจกต์นี้ใช้เทคโนโลยี Image Classification (การจำแนกภาพด้วย AI)
    โดยระบบจะรับภาพจากผู้ใช้ เช่น ภาพขวดพลาสติก ถุงขยะ หรือกระป๋อง แล้วใช้โมเดล 
    Machine Learning วิเคราะห์ว่าเป็นขยะประเภทใด เช่น\n
    ♻️ ขยะรีไซเคิล (ถังสีเหลือง)
    ⚠️ ขยะอันตราย (ถังสีแดง)
    🗑️ ขยะทั่วไป (ถังสีฟ้า)
    จากนั้นจะแนะนำผู้ใช้ว่าควรทิ้งขยะลงถังสีใดจึงเหมาะสม\n
             
   
             
**🌍 การประยุกต์ใช้ในงานจริง**\n
    เทคโนโลยีนี้สามารถนำไปใช้ได้จริงในหลายสถานการณ์ เช่น:
    🏫 โรงเรียน / มหาวิทยาลัย
    → ติดตั้งระบบกล้องหรือหน้าจอ AI ช่วยแนะนำให้นักเรียนทิ้งขยะให้ถูกถัง\n
    🏢 สำนักงาน / อาคาร Smart Building
    → ช่วยตรวจสอบความถูกต้องของการแยกขยะก่อนเก็บ\n
    🏙️ เมืองอัจฉริยะ (Smart City)
    → ผสานกับระบบถังขยะอัจฉริยะ (Smart Bin) เพื่อเก็บข้อมูลการทิ้งขยะและจัดการขยะอัตโนมัติ\n
    🛒 ห้างสรรพสินค้า / จุดคัดแยกขยะ
    → ใช้เป็นจุดให้ลูกค้าทิ้งขยะพร้อมแสดงผล AI วิเคราะห์ประเภทขยะแบบ real-time\n
        

        
    """)
    st.markdown("""
**🔧 เทคโนโลยีที่ใช้**\n
- Streamlit – ใช้สร้าง Web Application ให้ผู้ใช้สามารถ upload รูปภาพ และดูผลลัพธ์แบบเรียลไทม์
- TensorFlow / Keras / PIL – สำหรับสร้างโมเดลจำแนกประเภทภาพขยะ
- Python – ภาษาหลักในการพัฒนาและเชื่อมต่อทุกส่วน
    
    
    
**💚 ประโยชน์ของระบบ**\n
    ✅ ลดปัญหาการทิ้งขยะผิดประเภท ทำให้สามารถรีไซเคิลได้มากขึ้น
    ✅ ลดภาระเจ้าหน้าที่เก็บขยะ เพราะระบบช่วยคัดแยกเบื้องต้น
    ✅ ส่งเสริมพฤติกรรมรักษ์สิ่งแวดล้อม ด้วยการให้ feedback แบบเรียลไทม์
    ✅ เก็บข้อมูลเพื่อวิเคราะห์ปริมาณขยะ แต่ละประเภทในอนาคต
    ✅ สามารถต่อยอดกับ IoT / Robotics เพื่อสร้างระบบจัดการขยะอัตโนมัติ
                
                """)


