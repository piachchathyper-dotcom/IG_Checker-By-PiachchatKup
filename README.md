# IG Follow Checker

เช็กว่าใครไม่ follow back บน Instagram — ใช้ได้กับ **public account เท่านั้น** ไม่ต้อง login

---

## โครงสร้าง

```
ig-checker/
├── frontend/
│   └── index.html        # เว็บหน้าเดียว ไม่ต้อง build
├── backend/
│   ├── main.py           # FastAPI server
│   └── requirements.txt
├── render.yaml           # deploy บน Render
└── README.md
```

---

## Run local

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
แก้ `API_BASE` ใน `frontend/index.html` บรรทัดนี้:
```js
const API_BASE = "http://localhost:8000";
```
แล้วเปิด `index.html` ใน browser ได้เลย

---

## Deploy (Render)

1. Push โค้ดขึ้น GitHub
2. ไปที่ [render.com](https://render.com) → New Web Service → เชื่อม repo
3. Render จะอ่าน `render.yaml` เองอัตโนมัติ
4. เอา URL ของ backend ที่ได้ไปแทนใน `frontend/index.html`:
   ```js
   const API_BASE = "https://your-service.onrender.com";
   ```
5. Deploy frontend บน GitHub Pages หรือ Netlify (drag & drop โฟลเดอร์ frontend)

---

## ข้อจำกัด

- ใช้ได้เฉพาะ **public account** เท่านั้น
- private account จะ error
- ถ้า account ใหญ่มาก (follower หลักหมื่น) อาจช้าหน่อยเพราะ IG rate limit
