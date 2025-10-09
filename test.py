import os
import pickle
import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



# โหลดโมเดลที่บันทึกไว้
with open("model/pet_model.pkl", "rb") as f:
    clf, label_encoders, acc_score = pickle.load(f)
 
st.set_page_config(page_title="Pet Recommender", page_icon="🐾", layout="centered")

# -------------------------------
# Cleancing data
# -------------------------------

df_data = pd.read_csv('data/pet_dataset_final.csv')
df_data["Budget"] = pd.cut(
    df_data["Budget"],
    bins=[-1, 1000, 3000, float("inf")],    
    labels=["Less than 1000", "Between 1000 and 3000", "Greater than 3000"]
)
df_data["PreferQuietPet"] = df_data["PreferQuietPet"].replace(1, "Yes")
df_data["PreferQuietPet"] = df_data["PreferQuietPet"].replace(0, "No")
df_data["Allergies"] = df_data["Allergies"].replace(1, "Yes")
df_data["Allergies"] = df_data["Allergies"].replace(0, "No")

df_data.to_csv("data_ready/dataset1.csv", index=False, encoding="utf-8-sig")

# New Cleancing data

df_data_forms = pd.read_csv('data/pet_dataset_form.csv')
df_data_forms = df_data_forms.drop(["ประทับเวลา", "คะแนน"], axis=1)
df_data_forms.rename(columns={"สัตว์เลี้ยงที่เลี้ยงอยู่คืออะไร": "PetChoice",
                   "เพศ":"Gender",
                   "งบประมาณในการเลี้ยงสัตว์(ต่อเดือน)":"Budget",
                   "เวลาว่างเฉลี่ยต่อวัน (24 ชั่วโมง)":"FreeTime",
                   "เวลาอยู่บ้านเฉลี่ยต่อวัน (24 ชั่วโมง)":"TimeAtHome",
                   "ที่อยู่อาศัย": "Living",
                   "สัตว์เลี้ยงเงียบหรือไม่":"PreferQuietPet",
                   "เป็นภูมแพ้หรือไม่":"Allergies",
                    },inplace=True)

# แยกคอลัมน์ PetChoice ออกมา
pet_choice = df_data_forms.pop('PetChoice')

# แทรกกลับเข้าไปหลัง Allergies
df_data_forms.insert(df_data_forms.columns.get_loc('Allergies') + 1, 'PetChoice', pet_choice)
df_data_forms['Gender'] = df_data_forms['Gender'].replace({'ชาย': 'Male', 'หญิง': 'Female'})
df_data_forms['PetChoice'] = df_data_forms['PetChoice'].replace({
    'ปลา': 'Fish',
    'สุนัข': 'Dog',
    'แมว': 'Cat',
    'แฮมเตอร์': 'Hamster',
    'งู': 'Snake',
    'ไม่เลี้ยงสัตว์': 'No pet'
})

def extract_numeric(val):
    try:
        return int(''.join(filter(str.isdigit, str(val))))
    except:
        return None

df_data_forms['FreeTime'] = df_data_forms['FreeTime'].apply(extract_numeric)
df_data_forms['TimeAtHome'] = df_data_forms['TimeAtHome'].apply(extract_numeric)

df = df_data_forms[(df_data_forms['FreeTime'] <= 24) & (df_data_forms['TimeAtHome'] <= 24)]
def extract_budget(val):
    try:
        return int(''.join(filter(str.isdigit, str(val))))
    except:
        return None

# สร้างคอลัมน์ชั่วคราวเพื่อใช้กรอง
df_data_forms['__budget_numeric'] = df_data_forms['Budget'].apply(extract_budget)
# ลบแถวที่งบประมาณเกิน 100000
df_data_forms = df_data_forms[df_data_forms['__budget_numeric'] <= 100000]
# แทนค่าในคอลัมน์ Budget เดิมด้วยช่วงที่ต้องการ
def categorize_budget(num):
    if num is None:
        return 'Unknown'
    elif num < 1000:
        return 'Less than 1000'
    elif 1000 <= num <= 3000:
        return 'Between 1000 and 3000'
    else:
        return 'Greater than 3000'

df_data_forms['Budget'] = df_data_forms['__budget_numeric'].apply(categorize_budget)
# ลบคอลัมน์ชั่วคราว
df_data_forms.drop(columns=['__budget_numeric'], inplace=True)
df_data_forms.to_csv("data_ready/dataset2.csv", index=False, encoding="utf-8-sig")

# -------------------------------
# Load datasets Used data 

df1 = pd.read_csv("data_ready/dataset2.csv").head(60)  
df2 = pd.read_csv("data_ready/dataset1.csv") 
df_combined = pd.concat([df1, df2], ignore_index=True)
output_folder = "data_ready"
os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(output_folder, "pet_dataset_merged.csv")
df_combined.to_csv(output_path, index=False)


# -------------------------------
# STEP 1: Load and Train Model
# -------------------------------

@st.cache_resource

def train_pet_model():
    df = pd.read_csv("data_ready/pet_dataset_merged.csv")

    features = ['Gender', 'Budget', 'FreeTime', 'TimeAtHome', 'Living', 'PreferQuietPet', 'Allergies']
    target = 'PetChoice'

    label_encoders = {}
    df_encoded = df.copy()
    for col in features + [target]:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col])
        label_encoders[col] = le

    X = df_encoded[features]
    y = df_encoded[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc_score = accuracy_score(y_test, y_pred)
    with open("model/pet_model.pkl", "wb") as f:
        pickle.dump((clf, label_encoders, acc_score), f)


    return clf, label_encoders, acc_score

clf, label_encoders, acc_score = train_pet_model()
# -------------------------------
# STEP 2: Streamlit UI
# -------------------------------
st.markdown(
    """
    <div style="
        text-align: center; 
        background: linear-gradient(90deg, #4CAF50, #2E8B57); 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        white-space: nowrap;
    ">
        <h1 style="color: white; font-size: 36px; margin: 0; line-height: 1.2;">
             ระบบแนะนำสัตว์เลี้ยงที่เหมาะกับคุณ 🐱
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")
with st.expander("ℹ️ วิธีการใช้งาน"):
    st.markdown("""
    1. กรอกข้อมูลพฤติกรรมและลักษณะของคุณ  
    2. กดปุ่ม **"ทำนายสัตว์เลี้ยงที่เหมาะกับคุณ"**  
    3. ระบบจะแสดงสัตว์เลี้ยงที่เหมาะกับคุณ 3 อันดับแรก พร้อมความแม่นยำของโมเดล  

    ⚠️ หมายเหตุ: ผลลัพธ์เป็นเพียงการแนะนำเบื้องต้น ควรพิจารณาปัจจัยอื่นๆ ร่วมด้วย
    """)

st.markdown("### ✍️ กรอกข้อมูลของคุณ")

# Input Section
user_input = {}
col1, col2 = st.columns(2)

for i, col in enumerate(['Gender', 'Budget', 'Living', 'PreferQuietPet', 'Allergies']):
    with (col1 if i % 2 == 0 else col2):
        user_input[col] = st.selectbox(f"{col}", label_encoders[col].classes_)

with col1:
    user_input['FreeTime'] = st.slider("🕒 เวลาว่างต่อวัน (ชั่วโมง)", min_value=0, max_value=24, value=4)

with col2:
    user_input['TimeAtHome'] = st.slider("🏠 เวลาที่อยู่บ้านต่อวัน (ชั่วโมง)", min_value=0, max_value=24, value=8)

# -------------------------------
# STEP 3: Prediction
# -------------------------------

if st.button("🔍 ทำนายสัตว์เลี้ยงที่เหมาะกับคุณ"):
    input_df = pd.DataFrame([user_input])
    for col in input_df.columns:
        if col in ['FreeTime', 'TimeAtHome']:
            continue
        input_df[col] = label_encoders[col].transform(input_df[col])

    input_df = input_df[clf.feature_names_in_]

    probs = clf.predict_proba(input_df)[0]
    top3_idx = probs.argsort()[-3:][::-1]
    top3_pets = [label_encoders['PetChoice'].inverse_transform([i])[0] for i in top3_idx]

    # Show accuracy
    st.metric("📊 ความแม่นยำของโมเดล", f"{acc_score*100:.2f}%")
    # Show results in cards
    st.success("🐾 ผลการทำนาย: สัตว์เลี้ยงที่เหมาะกับคุณ 3 อันดับแรก")
    for i, pet in enumerate(top3_pets, 1):
        st.markdown(
    f"""
    <div style="
        background-color:#2E2E2E; 
        padding:15px; 
        margin:10px 0; 
        border-radius:12px; 
        border-left:6px solid #4CAF50;
        color:#FFFFFF;">
        <h4 style="margin:0;">{i}. {pet}</h4>
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown("---")

with st.sidebar:
    st.header("ℹ️ วิธีการใช้งานแบบละเอียด")

    with st.expander("วิธีการใช้งานแบบละเอียด"):
        st.write("""
    1. กรอกข้อมูลพฤติกรรมและลักษณะของคุณ \n
        -Gender(เพศ) : เพศของผู้เลี้ยงสัตว์เลี้ยง \n
        -Budget(งบประมาณ) : งบประมาณที่มีต่อการเลี้ยงสัตว์เลี้ยงต่อเดือน  \n
        -Living(ที่อยู่อาศัย) : ประเภทที่อยู่อาศัย เช่น อพาร์ตเมนต์ คอนโด บ้าน \n
        -PreferQuietPet(ชอบสัตว์เลี้ยงที่เงียบไหม) : ความชอบส่วนตัวเกี่ยวกับเสียงของสัตว์เลี้ยง \n
        -Allergies(แพ้ขนสัตว์ไหม) : ข้อมูลเกี่ยวกับการแพ้ขนสัตว์ ซึ่งมีผลต่อการเลือกประเภทสัตว์เลี้ยง \n
        -FreeTime(เวลาว่างต่อวัน) : เวลาว่างที่มีต่อการดูแลสัตว์เลี้ยงต่อวัน \n
        -TimeAtHome(เวลาที่อยู่บ้านต่อวัน) : เวลาที่อยู่บ้านต่อวัน ซึ่งมีผลต่อการดูแลสัตว์เลี้ยง \n
    2. กดปุ่ม "ทำนายสัตว์เลี้ยงที่เหมาะกับคุณ" \n
    3. ระบบจะแสดงสัตว์เลี้ยงที่เหมาะกับคุณ 3 อันดับแรก พร้อมความแม่นยำของโมเดล   \n
    หมายเหตุ: ผลลัพธ์ที่ได้เป็นเพียงการแนะนำเบื้องต้น ควรพิจารณาปัจจัยอื่นๆ ร่วมด้วยก่อนตัดสินใจเลี้ยงสัตว์
            
    
    """)

    st.header("📖 คู่มือการเลี้ยงสัตว์")

    with st.expander("🐶 การเลี้ยงสุนัข (Dog)"):
        st.write("**1.เรื่องอาหาร**\n"
        "- ให้อาหารสุนัขวันละ 1–2 มื้อ (ขึ้นอยู่กับอายุและขนาด)\n"
        "- เลือกอาหารเม็ดหรืออาหารปรุงเองที่เหมาะกับสายพันธุ์และวัย\n"
        "- ห้ามให้ของหวาน ช็อกโกแลต องุ่น หัวหอม กระเทียม เพราะเป็นพิษกับสุนัข\n" 
        "- ควรมีน้ำสะอาดให้ตลอดเวลา\n" 

        "\n**2. การดูแลสุขภาพ**\n"
        "- พาไปฉีดวัคซีนและถ่ายพยาธิตามกำหนด\n"
        "- หมั่นดูแลเรื่องหมัด เห็บ และพาไปพบสัตวแพทย์เมื่อมีอาการผิดปกติ\n" \
        
        "\n**3. การออกกำลังกายและกิจกรรม**\n"
        "- พาออกไปเดินเล่นหรือวิ่งเล่นทุกวัน เล่นกับน้องหมาเพื่อให้เขาไม่เครียดและผูกพันกับเจ้าของ\n"
        
        "\n**4. การเลี้ยงดูด้านจิตใจ**\n" 
        "- ให้ความรัก เอาใจใส่ และฝึกวินัย ไม่ใช้ความรุนแรง ควรใช้วิธี ให้รางวัล เมื่อทำถูกต้อง\n" 
        "\n**5. ที่อยู่อาศัย**\n" 
        "- จัดที่นอนสะอาด แห้ง และอากาศถ่ายเท\n" 
        "- ไม่ควรผูกโซ่นานเกินไป ควรมีพื้นที่ให้วิ่งเล่น\n"

        "")
    with st.expander("🐱 การเลี้ยงแมว (Cat)"):
        st.write("**1. เรื่องอาหาร**\n"
        "- ให้อาหารแมววันละ 2–3 มื้อ หรือเลือกให้อาหารเม็ดแบบ แบ่งปริมาณไว้ทั้งวัน\n"
        "- ห้ามให้ ช็อกโกแลต หัวหอม กระเทียม องุ่น นมวัว เพราะเป็นพิษต่อแมว\n"
        "- แมวบางตัวชอบน้ำไหล ควรมี น้ำพุแมว เพื่อกระตุ้นให้ดื่มมากขึ้น\n" 

        "\n**2. การดูแลสุขภาพ**\n"
        "- ฉีดวัคซีนและถ่ายพยาธิตามกำหนด\n"
        "- ทำความสะอาด กระบะทราย ทุกวัน และเปลี่ยนทรายอย่างน้อยสัปดาห์ละครั้ง\n" 
        
        "\n**3. การเลี้ยงดูด้านจิตใจ**\n" 
        "- เล่นกับแมววันละ 15–30 นาที ด้วยของเล่น เช่น ไม้ล่อแมว ลูกบอล"
        "- ให้ความรักและเอาใจใส่ แต่ก็เคารพความเป็นส่วนตัวของแมว (เพราะแมวชอบมีโลกส่วนตัว)" 
        
        "\n**4. ที่อยู่อาศัย**\n" 
        "- แมวชอบพื้นที่สงบ ควรมีที่นอนและที่ซ่อน\n" 
        "- จัดมุมปีนป่าย เช่น คอนโดแมว หรือชั้นวางของสูง ๆ\n"
        "- บ้านควรปลอดภัย ไม่ควรให้วิ่งเล่นนอกบ้านเพราะเสี่ยงอุบัติเหตุและโรค\n"

        "")
    with st.expander("🐠 การเลี้ยงปลา (Fish)"):
        st.write("**1. การเตรียมตู้ปลา**\n"
        "- เลือกตู้ให้เหมาะกับชนิดและจำนวนปลา\n"
        "- ใส่ กรวด หิน พืชน้ำ หรือของตกแต่ง ให้ปลาได้หลบซ่อน\n"
        "- ต้องมี เครื่องกรองน้ำ เพื่อรักษาความสะอาด และ ปั๊มอากาศ เพื่อเพิ่มออกซิเจน\n" 

        "\n**2. น้ำและสิ่งแวดล้อม**\n"
        "- ใช้น้ำที่ปราศจากคลอรีน (พักน้ำอย่างน้อย 24 ชม. หรือใช้น้ำยาลดคลอรีน)\n"
        "- เปลี่ยนน้ำบางส่วน 20–30% ทุกสัปดาห์ ไม่ควรเปลี่ยนทั้งหมดทีเดียว\n" 
        
        "\n**3. อาหาร**\n" 
        "- ให้อาหารเม็ดหรืออาหารสดที่เหมาะกับสายพันธุ์ปลา ให้ในปริมาณที่กินหมดภายใน 2–3 นาที วันละ 1–2 ครั้ง"
        "- ไม่ควรให้อาหารมากเกินไปเพราะจะทำให้น้ำเสีย" 
        
        "\n**4. การดูแลสุขภาพปลา**\n" 
        "- สังเกตอาการผิดปกติ เช่น ว่ายน้ำไม่ปกติ ตัวซีด มีจุดขาว (อาจติดเชื้อ)\n" 
        "- แยกปลาป่วยออกมาต่างหากเพื่อป้องกันการแพร่โรค\n"
        "- รักษาคุณภาพน้ำให้ดีเสมอ เพราะสุขภาพปลาขึ้นอยู่กับน้ำ\n"

        "\n**5. การเลี้ยงที่เหมาะสม**\n" 
        "- ไม่ควรเลี้ยงปลาหลายชนิดที่ดุร้ายรวมกัน เพราะอาจกัดกันได้\n" 
       

        "")
    with st.expander("🐹 การเลี้ยงแฮมสเตอร์ (Hamster)"):
        st.write("**1. กรงและที่อยู่อาศัย**\n"
        "- เลือกกรงที่มี พื้นโปร่ง ระบายอากาศได้ดี ไม่ควรเป็นตู้ปิดทึบ\n"
        "- ปูรองพื้นด้วย ขี้เลื่อยไม้เนื้ออ่อน (ห้ามใช้ไม้สน/ซีดาร์ เพราะมีสารระเหยอันตราย)\n"
        "- ควรมี ล้อวิ่ง สำหรับออกกำลังกาย\n" 

        "\n**2. อาหาร**\n"
        "- อาหารหลักคือ อาหารเม็ดสำหรับแฮมสเตอร์ และสามารถเสริมด้วย ผักสด ผลไม้ (เช่น แครอท แอปเปิ้ล) แต่ต้องให้ในปริมาณน้อย\n"
        "- ห้ามให้ ช็อกโกแลต ของหวาน ของเค็ม เพราะเป็นอันตราย \n" 
        
        "\n**3. สุขภาพและการดูแล**\n" 
        "- ทำความสะอาดกรงสัปดาห์ละ 1–2 ครั้ง\n"
        "- ไม่ควรอาบน้ำด้วยน้ำจริง แต่ใช้ ทรายอาบแห้งสำหรับแฮมสเตอร์ ให้เขากลิ้งเล่นเพื่อทำความสะอาดตัวเอง\n" 
        "- สังเกตพฤติกรรม หากซึม ไม่กินอาหาร หรือมีอาการผิดปกติ ควรพาไปพบสัตวแพทย์\n" 

        
        "\n**4. พฤติกรรมและการเล่น**\n" 
        "- แฮมสเตอร์ส่วนใหญ่เป็นสัตว์หวงถิ่น ควรเลี้ยงเดี่ยว 1 กรงต่อ 1 ตัว\n" 
        "- เล่นกับเขาเบา ๆ อย่าจับแรง เพราะตัวเล็กและกระดูกเปราะ\n"
        "- ควรฝึกให้คุ้นมือเจ้าของด้วยการค่อย ๆ ยื่นอาหารให้\n"

        "")
    with st.expander("🐍 การเลี้ยงงู (Snake)"):
        st.write("**1. ที่อยู่อาศัย**\n"
        "- ใช้ตู้กระจกหรือกล่องเลี้ยงงูที่ปิดมิดชิด ป้องกันงูเลื้อยออกมาได้\n"
        "- ควรมีพื้นที่ให้หลบซ่อน เช่น กล่องหรือหินจำลอง\n"
        "- รักษาอุณหภูมิที่เหมาะสม (ส่วนใหญ่ 25–30°C) และมีโคมไฟ/แผ่นความร้อนช่วย\n"
        "- ปูพื้นด้วยวัสดุ เช่น ขี้เลื่อย กระดาษ หรือทราย (แล้วแต่ชนิดงู)\n"

        "\n**2. อาหาร**\n"
        "- อาหารหลักคือ หนูแช่แข็ง/สัตว์ฟันแทะที่เหมาะสมกับขนาดงู\n"
        "- ให้อาหารทุก 1–2 สัปดาห์ ขึ้นอยู่กับอายุและขนาด\n"
        "- ไม่ควรจับหรือลูบคลำหลังให้อาหารทันที เพราะงูอาจตื่นตกใจและสำรอกได้\n"

        "\n**3. สุขภาพและการดูแล**\n"
        "- คอยสังเกตอาการผิดปกติ เช่น ไม่กินอาหาร ผิวซีด มีรอยโรค หรือหายใจเสียงดัง\n"
        "- ทำความสะอาดตู้และเปลี่ยนน้ำอย่างน้อยสัปดาห์ละครั้ง\n"
        "- ช่วงลอกคราบควรรักษาความชื้นให้เพียงพอ\n"

        "\n**4. ความปลอดภัย**\n"
        "- ควรศึกษาสายพันธุ์ก่อนเลี้ยง บางชนิดดุร้าย ไม่เหมาะกับมือใหม่\n"
        "- ห้ามเลี้ยงงูพิษถ้าไม่มีประสบการณ์และอุปกรณ์พร้อม\n"
        "- เวลาจับควรใช้ที่คีบหรือตะขอช่วย และจับด้วยความระมัดระวัง\n"

        "")
    with st.expander("ไม่ควรเลี้ยงสัตว์ (No Pet)"):
            st.write("**ไม่ควรเลี้ยงสัตว์เนื่องจากคุณสมบัติไม่พร้อม**\n")


# ------------------------------------------------------------
# 1) Business Understanding
# ------------------------------------------------------------
with st.popover("1) Business & Project Motivation", use_container_width=True, help="ความเป็นมาและคุณค่าทางธุรกิจของโครงการ"):
    st.subheader("Business Understanding และความน่าสนใจของโปรเจกต์")
    st.markdown("""
- ผู้ใช้จำนวนมากอยากเลี้ยงสัตว์แต่ไม่แน่ใจว่า **สัตว์ชนิดใดเหมาะกับไลฟ์สไตล์** ของตน (ข้อจำกัดด้านเสียง, เวลา, งบประมาณ, ภูมิแพ้)
- เป้าหมายโครงการ: **พัฒนาโมเดล Classification** เพื่อแนะนำประเภทสัตว์เลี้ยงที่เหมาะสมที่สุดให้ผู้ใช้รายบุคคล

**คุณค่าทางธุรกิจ (Business Value)**
- ใช้เป็น **ฟีเจอร์แนะนำ (Recommendation)** ในเว็บไซต์/แอปของร้านขายสัตว์เลี้ยงหรือ Adoption Platform
- ช่วยทีมการตลาดทำ **Personalized Marketing**/Cross-sell อุปกรณ์อาหาร/บริการที่สอดคล้องกับสัตว์ที่เหมาะ
- ลดความเสี่ยงการเลี้ยงไม่เหมาะสม → เพิ่มความพึงพอใจและความรับผิดชอบต่อสัตว์เลี้ยง
""")

# ------------------------------------------------------------
# 2) Data Source
# ------------------------------------------------------------
with st.popover("2) Data Source", use_container_width=True, help="แหล่งข้อมูลและคำอธิบายฟีเจอร์"):
    st.subheader("แหล่งที่มาของข้อมูล (Data Source)")
    st.markdown("""
ข้อมูลเป็น **Supervised Dataset** สำหรับงานจำแนกประเภท (Classification) โดยฟีเจอร์หลักมี:
- `Gender` (เพศ)
- `Residence` (ลักษณะที่อยู่อาศัย: บ้าน/คอนโด/หอพัก/ฯลฯ)
- `FreeTime_hr` (เวลาว่างเฉลี่ยต่อวัน, ชั่วโมง)
- `Budget` (งบประมาณรายเดือนสำหรับสัตว์เลี้ยง, บาท)
- `Allergy` (มีภูมิแพ้สัตว์หรือไม่: Yes/No)
- `QuietPreference` (ต้องการสัตว์ที่เงียบหรือไม่: Yes/No)
- `StayHome_hr` (เวลาที่อยู่บ้านต่อวัน, ชั่วโมง)

**Target (ชนิดผลลัพธ์):** `สุนัข`, `แมว`, `ปลา`, `หนูแฮมสเตอร์`, `งู`, `ไม่ควรเลี้ยงสัตว์`
                
**แหล่งที่มาของDataset**
> Kaggle,
> Google Forms (แบบสอบถามจากผู้ใช้จริง)
""")

# ------------------------------------------------------------
# 3) Data Preprocessing
# ------------------------------------------------------------
with st.popover("3) Data Preprocessing", use_container_width=True, help="ขั้นตอนการเตรียมข้อมูลก่อนเทรนโมเดล"):
    st.subheader("🔧 ขั้นตอนการเตรียมข้อมูล (Data Preprocessing)")

    st.markdown("""
**ขั้นตอนหลักในการทำความสะอาดและเตรียมข้อมูลก่อนเทรนโมเดล**

1️⃣ **โหลดข้อมูลต้นฉบับ**  
   - ใช้ชุดข้อมูล 2 แหล่ง:  
     • `pet_dataset_final.csv` (ข้อมูลหลักที่จัดเตรียมไว้แล้ว)  
     • `pet_dataset_form.csv` (ข้อมูลจากแบบฟอร์ม Google Form)

2️⃣ **ทำความสะอาดข้อมูล (Cleaning)**   
   - เปลี่ยนชื่อคอลัมน์ภาษาไทย → อังกฤษ (เช่น `เพศ` → `Gender`, `สัตว์เลี้ยงที่เลี้ยงอยู่คืออะไร` → `PetChoice`)  
   - ปรับค่าภาษาไทยให้เป็นภาษาอังกฤษ เช่น `ชาย`→`Male`, `หญิง`→`Female`

3️⃣ **จัดหมวดหมู่งบประมาณ (Budget Binning)**  
   - แปลงตัวเลขงบประมาณให้อยู่ใน 3 ช่วง:  
     • `< 1000` → `"Less than 1000"`  
     • `1000–3000` → `"Between 1000 and 3000"`  
     • `> 3000` → `"Greater than 3000"`

4️⃣ **แปลงค่าตรรกะ (Boolean Mapping)**  
   - `PreferQuietPet`: 1→`Yes`, 0→`No`  
   - `Allergies`: 1→`Yes`, 0→`No`

5️⃣ **แปลงเวลาที่เป็นข้อความให้เป็นตัวเลข (Extract Numeric Time)**  
   - ดึงตัวเลขจากข้อความ เช่น `"8 ชั่วโมง"` → `8`  
   - กรองข้อมูลให้ไม่เกิน 24 ชั่วโมงทั้ง `FreeTime` และ `TimeAtHome`

6️⃣ **กรองและจัดกลุ่มงบประมาณเพิ่มเติม**  
   - ดึงตัวเลขออกจากข้อความ  
   - กรองค่าสูงเกินจริง (≤ 100,000 บาท)  
   - แปลงกลับเป็นช่วงงบประมาณตามข้อ 3

7️⃣ **รวมข้อมูลสองชุดเข้าด้วยกัน**  
   - รวม (`concat`) `dataset1.csv` และ `dataset2.csv`  
   - บันทึกเป็น `pet_dataset_merged.csv` ซึ่งใช้สำหรับเทรนโมเดล

8️⃣ **เข้ารหัสข้อมูล (Label Encoding)**  
   - ใช้ `LabelEncoder` แปลงข้อมูลเชิงหมวดหมู่ทุกคอลัมน์ (รวมทั้ง Target `PetChoice`)  
   - เก็บ `label_encoders` สำหรับใช้ตอนทำนายผล

9️⃣ **แบ่งข้อมูล Train/Test**  
   - ใช้ `train_test_split()` แบ่งข้อมูล 80% สำหรับเทรน, 20% สำหรับทดสอบ  

✅ **ผลลัพธ์สุดท้าย:**  
ไฟล์ `data_ready/pet_dataset_merged.csv` คือชุดข้อมูลที่พร้อมสำหรับใช้เทรน Decision Tree Model ในขั้นตอนถัดไป
""")

# ------------------------------------------------------------
# 4) Model Training
# ------------------------------------------------------------
with st.popover("4) Model Training", use_container_width=True, help="โมเดลที่ลองและพารามิเตอร์หลัก"):
    st.subheader("โมเดลที่ใช้และการฝึกสอน")
    st.markdown("""
ได้ทดลองโมเดลพื้นฐานหลายแบบและปรับจูนเบื้องต้น:
- **Logistic Regression**
- **K-Nearest Neighbors** 
- **Decision Tree** ← *ผลลัพธ์ดีที่สุด*
""")








# -------------------------------
# Popover: Evaluation (สรุปผลการประเมินโมเดล)
# -------------------------------
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    precision_recall_fscore_support, roc_auc_score, roc_curve, auc
)
from sklearn.model_selection import train_test_split

def _encode_with_saved_encoders(df, cols, label_encoders):
    df = df.copy()
    for c in cols:
        le = label_encoders.get(c)
        if le is None:
            continue
        # map unseen labels -> -1 แล้วกรองออกภายหลัง
        df[c] = df[c].map(lambda x: x if x in le.classes_ else None)
    # กรองค่าที่เป็น None (unseen) ออก
    for c in cols:
        if c in df.columns:
            df = df[df[c].notna()]
    # แปลงเป็นตัวเลขด้วย encoders ที่บันทึกไว้
    for c in cols:
        le = label_encoders.get(c)
        if le is None:
            continue
        df[c] = le.transform(df[c])
    return df

with st.popover("5) Evaluation", use_container_width=True, help="ตัวชี้วัดและกราฟประเมินผลโมเดล"):
    st.subheader("📏 การประเมินผลโมเดล (Evaluation)")
    st.markdown("""
เมตริกที่รายงาน:
- **Accuracy** — สัดส่วนที่ทำนายถูกทั้งหมด  
- **Precision / Recall / F1-score** — รายคลาส + macro/weighted average  
- **Confusion Matrix** — เปรียบเทียบค่าจริงกับค่าทำนาย  
- **ROC-AUC (One-vs-Rest, Macro)** — วัดความสามารถแยกคลาสโดยรวม

> อิงชุดข้อมูล: `data_ready/pet_dataset_merged.csv`  
> อิงโมเดลที่โหลด: `clf`, `label_encoders`
""")

    if st.button("🧪 คำนวณ Evaluation"):
        try:
            # เตรียมข้อมูลทดสอบให้ตรงกับที่ใช้เทรน
            df_eval = pd.read_csv("data_ready/pet_dataset_merged.csv")
            features = ['Gender', 'Budget', 'FreeTime', 'TimeAtHome', 'Living', 'PreferQuietPet', 'Allergies']
            target = 'PetChoice'

            df_encoded = _encode_with_saved_encoders(df_eval, features + [target], label_encoders)

            X = df_encoded[features]
            y = df_encoded[target]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # พยากรณ์
            y_pred = clf.predict(X_test)

            # ---------------- Metrics (ตัวเลขสรุป) ----------------
            acc = accuracy_score(y_test, y_pred)
            prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(
                y_test, y_pred, average='macro', zero_division=0
            )
            prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(
                y_test, y_pred, average='weighted', zero_division=0
            )

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Accuracy", f"{acc*100:.2f}%")
            m2.metric("Macro F1", f"{f1_macro:.3f}")
            m3.metric("Macro Precision", f"{prec_macro:.3f}")
            m4.metric("Macro Recall", f"{rec_macro:.3f}")

            # ---------------- Classification report (ข้อความ) ----------------
            class_names = list(label_encoders[target].classes_)
            st.markdown("#### 📃 Classification Report")
            st.text(classification_report(y_test, y_pred, target_names=class_names, zero_division=0))

            # ---------------- Confusion Matrix (กราฟ) ----------------
            st.markdown("#### 🔁 Confusion Matrix")
            cm = confusion_matrix(y_test, y_pred, labels=range(len(class_names)))

            fig_cm = plt.figure(figsize=(6, 5))
            plt.imshow(cm, interpolation='nearest')
            plt.title("Confusion Matrix")
            plt.xlabel("Predicted")
            plt.ylabel("True")
            plt.xticks(ticks=np.arange(len(class_names)), labels=class_names, rotation=45, ha='right')
            plt.yticks(ticks=np.arange(len(class_names)), labels=class_names)
            # ใส่ตัวเลขในช่อง
            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    plt.text(j, i, cm[i, j], ha="center", va="center")
            plt.tight_layout()
            st.pyplot(fig_cm)

            # ---------------- ROC-AUC (macro OVR) + เส้น ROC ----------------
            st.markdown("#### 📈 ROC Curves (One-vs-Rest) & Macro AUC")
            if hasattr(clf, "predict_proba"):
                y_proba = clf.predict_proba(X_test)  # (n_samples, n_classes)
                # สร้าง one-vs-rest labels
                n_classes = len(class_names)
                y_test_bin = np.zeros((y_test.shape[0], n_classes), dtype=int)
                for i, yi in enumerate(y_test):
                    y_test_bin[i, yi] = 1

                # macro AUC
                macro_auc = roc_auc_score(y_test_bin, y_proba, average='macro', multi_class='ovr')
                st.metric("Macro ROC-AUC (OVR)", f"{macro_auc:.3f}")

                # วาด ROC ต่อคลาส
                fig_roc = plt.figure(figsize=(6, 5))
                for i in range(n_classes):
                    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
                    roc_auc = auc(fpr, tpr)
                    plt.plot(fpr, tpr, label=f"{class_names[i]} (AUC={roc_auc:.2f})")
                # เส้นอ้างอิง
                plt.plot([0, 1], [0, 1], linestyle="--")
                plt.xlabel("False Positive Rate")
                plt.ylabel("True Positive Rate")
                plt.title("ROC Curves (One-vs-Rest)")
                plt.legend(loc="lower right")
                plt.tight_layout()
                st.pyplot(fig_roc)
            else:
                st.info("โมเดลนี้ไม่รองรับ predict_proba จึงไม่สามารถคำนวณ ROC-AUC/วาด ROC ได้")

            st.success("ประเมินผลสำเร็จ ✅")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดระหว่างประเมินผล: {e}")


# ------------------------------------------------------------
# 6) Results & Recommendations
# ------------------------------------------------------------
with st.popover("6) ข้อเสนอแนะ (Recommendations)", use_container_width=True, help="แนวทางปรับปรุงและพัฒนาโมเดลในอนาคต"):
    st.subheader("💡 ข้อเสนอแนะในอนาคต")

    st.markdown("""
**1️⃣ เพิ่มคุณภาพของข้อมูล (Data Quality Improvement)**  
- เก็บข้อมูลจริงจากผู้ใช้เพิ่มเติม เพื่อให้โมเดลเรียนรู้จากพฤติกรรมจริงมากขึ้น  
- เพิ่มจำนวนตัวอย่างของคลาสที่มีน้อย เช่น “งู” หรือ “ไม่เลี้ยงสัตว์” เพื่อแก้ปัญหา class imbalance  
- ตรวจสอบความถูกต้องของข้อมูลแบบฟอร์ม เช่น เวลาและงบประมาณที่ไม่สมเหตุสมผล  

---

**2️⃣ ปรับปรุงฟีเจอร์ (Feature Engineering)**  
- เพิ่มฟีเจอร์ที่สะท้อนพฤติกรรมและนิสัย เช่น “ชอบทำกิจกรรมกลางแจ้งไหม” หรือ “จำนวนสมาชิกในบ้าน”  
- สร้างฟีเจอร์เชิงอนุพันธ์ (เช่น อัตราส่วนเวลาว่างต่อเวลาอยู่บ้าน) เพื่อให้โมเดลเข้าใจ lifestyle ของผู้ใช้ได้ดีขึ้น  

---

**3️⃣ ปรับปรุงและเปรียบเทียบโมเดล (Model Optimization)**  
- ลองใช้โมเดลอื่น ๆ เช่น **Random Forest**, **XGBoost**, หรือ **Support Vector Machine**  
- ใช้เทคนิค **Hyperparameter Tuning** (GridSearchCV / RandomizedSearchCV) เพื่อหาค่าพารามิเตอร์ที่เหมาะสมที่สุด  
- ทดลองใช้เทคนิค **Cross Validation** เพื่อให้ผลการวัดมีความเสถียรมากขึ้น  

---

🎯 **สรุป:**  
ระบบแนะนำสัตว์เลี้ยงนี้สามารถต่อยอดได้อีกมาก ทั้งด้านความแม่นยำของโมเดลและการออกแบบ UX/UI  
หากมีข้อมูลจริงและการปรับจูนเพิ่มเติม โมเดลจะสามารถช่วยให้ผู้ใช้เลือกสัตว์เลี้ยงที่เหมาะสมกับชีวิตจริงได้อย่างแม่นยำมากขึ้น 🐶🐱🐠
""")

st.divider()