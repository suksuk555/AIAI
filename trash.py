import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image

data_dir = "dataset-resized"


train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = train_datagen.flow_from_directory(
    data_dir, target_size=(224,224), batch_size=32, class_mode="categorical", subset="training"
)
val_data = train_datagen.flow_from_directory(
    data_dir, target_size=(224,224), batch_size=32, class_mode="categorical", subset="validation"
)

# โหลด MobileNetV2
base_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, input_shape=(224,224,3))
base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(7, activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# เทรนโมเดล
history = model.fit(train_data, validation_data=val_data, epochs=15)
# บันทึกโมเดลไว้ใช้ใน Streamlit
model.save("model/trash_model.h5")

'''

# ทดสอบโมเดล
class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# ---- ใส่ path ของรูปภาพที่ต้องการทำนาย ----
img_path = "imageForProject\paper1.jpg"

# โหลดและเตรียมภาพ
img = Image.open(img_path).convert('RGB')
img = img.resize((224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x /= 255.0

# ทำนาย
preds = model.predict(x)
predicted_class = class_names[np.argmax(preds)]
confidence = np.max(preds) * 100

print(f"ภาพนี้น่าจะเป็น: {predicted_class} ({confidence:.2f}%)")

'''



