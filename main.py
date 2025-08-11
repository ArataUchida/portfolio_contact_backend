from fastapi import FastAPI, Form, HTTPException
import smtplib
from email.message import EmailMessage
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では限定する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send_mail/")
async def send_mail(
    name: str = Form(...),
    email: str = Form(...),
    comment: str = Form(...)
):
    msg = EmailMessage()
    msg["Subject"] = f"お問い合わせ from {name}"
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER
    msg.set_content(f"Name: {name}\nEmail: {email}\n\n{comment}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # 暗号化された接続に切り替えるためのコマンド
            server.login(SMTP_USER, SMTP_PASSWORD)# ログイン
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"メール送信失敗: {e}")

    return {"message": "メール送信成功"}