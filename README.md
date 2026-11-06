# Image Converter

แอป desktop สำหรับแปลงและปรับขนาดรูปภาพด้วย Python และ Tkinter รองรับการเลือกหลายไฟล์ การลากไฟล์หรือโฟลเดอร์มาวาง และการแปลงภาพแบบ Batch

## รูปแบบไฟล์

- Input: JPG, JPEG, PNG, WebP, AVIF, BMP, TIF, TIFF, GIF และ ICO
- Output: WebP, AVIF, JPEG, PNG, BMP, TIFF, GIF และ ICO

## ติดตั้งและเรียกใช้

ต้องมี Python 3 พร้อม Tkinter และ pip จากโฟลเดอร์โปรเจกต์ ให้สร้าง virtual environment และติดตั้ง dependencies ดังนี้

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install tkinterdnd2
python3 image_converter_gui.py
```

`tkinterdnd2` ใช้สำหรับ drag and drop และต้องติดตั้งเพิ่มเติม เนื่องจากยังไม่ได้ระบุไว้ใน `requirements.txt`

## วิธีใช้งาน

1. ลากไฟล์หรือโฟลเดอร์มาวางในแอป หรือใช้ปุ่ม **Add Files** และ **Add Folder** การเพิ่มโฟลเดอร์จะค้นหารูปภาพใน subfolders ด้วย
2. เลือก Output format และ Quality ตั้งแต่ 1 ถึง 100 โดย Quality ใช้กับ JPEG, WebP และ AVIF
3. หากต้องการปรับขนาด ให้ระบุ Width และระบุ Height เพิ่มได้ ถ้าไม่ระบุ Height แอปจะใช้ค่า Width แทน เลือก **Keep Aspect Ratio** เพื่อรักษาสัดส่วนภาพ
4. กด **Start Conversion** แล้วดูความคืบหน้า สถิติ และ log ในแท็บ Progress

ไฟล์ผลลัพธ์จะอยู่ในโฟลเดอร์เดียวกับไฟล์ต้นฉบับ หากชื่อปลายทางมีอยู่แล้ว แอปจะเติม `_01`, `_02` และลำดับถัดไปก่อนนามสกุล เช่น `image.avif`, `image_01.avif`, `image_02.avif` โดยเก็บไฟล์เดิมไว้ รวมถึงเมื่อเลือก Output format เดียวกับต้นฉบับ

## ทดสอบ

หลังติดตั้ง dependencies แล้ว รัน tests ด้วยคำสั่ง

```bash
python -m unittest discover -v
```

## Build สำหรับ macOS

ติดตั้ง dependencies ตามขั้นตอนข้างต้น และติดตั้ง `create-dmg` ให้เรียกได้จาก PATH จากนั้นรัน

```bash
./build.sh
```

สคริปต์ใช้ PyInstaller สร้าง `dist/Image Converter.app` แล้วใช้ `create-dmg` สร้าง `Image Converter.dmg` โดยสคริปต์จะลบโฟลเดอร์ `build` และ `dist` เดิมก่อน build

## License

ดูรายละเอียดใน [LICENSE](LICENSE)
