from supabase import create_client, Client
import os
import requests

# Supabase 자격 증명 (환경 변수 또는 직접 입력)
# 실제 프로젝트에서는 환경 변수를 사용하는 것이 보안상 더 좋습니다.
SUPABASE_URL = os.environ.get("SUPABASE_URL") or "https://iwmyyalggkttnaxfhcpo.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3bXl5YWxnZ2t0dG5heGZoY3BvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyNzQ2MDYsImV4cCI6MjA3Mzg1MDYwNn0.XrybkF7_jvf4aZZs2SHsn-3paEvCmeenqT6KCDrIAUk"
TABLE_NAME = "test" # 테이블 이름을 "test"로 수정

# Telegram 봇 자격 증명 (환경 변수 또는 직접 입력)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("경고: Telegram 봇 토큰 또는 채팅 ID가 설정되지 않아 알림을 보낼 수 없습니다.")
        return

    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML" # HTML 형식 메시지 지원
    }
    try:
        response = requests.post(telegram_api_url, json=payload)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        print("Telegram 메시지 전송 성공.")
    except requests.exceptions.RequestException as e:
        print(f"Telegram 메시지 전송 실패: {e}")


def upload_news_to_supabase(news_data: list[dict]):
    if not SUPABASE_URL or SUPABASE_URL == "YOUR_SUPABASE_URL":
        print("오류: Supabase URL이 설정되지 않았습니다. SUPABASE_URL 환경 변수를 설정하거나 스크립트 내에서 직접 입력해주세요.")
        return
    if not SUPABASE_KEY or SUPABASE_KEY == "YOUR_SUPABASE_KEY":
        print("오류: Supabase Key가 설정되지 않았습니다. SUPABASE_KEY 환경 변수를 설정하거나 스크립트 내에서 직접 입력해주세요.")
        return

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"Supabase에 연결되었습니다. 테이블: {TABLE_NAME}")

        data_to_insert = []
        for item in news_data:
            data_to_insert.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "publisher": item.get("publisher"),
                "publish_date": item.get("published_date")
            })
        
        if not data_to_insert:
            print("업로드할 데이터가 없습니다.")
            return

        response = supabase.table(TABLE_NAME).insert(data_to_insert).execute()
        
        if response.data:
            success_message = f"{len(response.data)}개의 기사 메타데이터가 Supabase에 성공적으로 업로드되었습니다."
            print(success_message)
            send_telegram_message(success_message)
        elif response.error:
            error_message = f"Supabase 업로드 중 오류 발생: {response.error}"
            print(error_message)
            send_telegram_message(error_message)
        else:
            print("Supabase 업로드 응답에 데이터나 오류 정보가 없습니다.")

    except Exception as e:
        exception_message = f"Supabase 연결 또는 업로드 중 예외 발생: {e}"
        print(exception_message)
        send_telegram_message(exception_message)

if __name__ == "__main__":
    test_news_data = [
        {
            "title": "테스트 기사 1",
            "url": "http://test.com/1",
            "publisher": "테스트 출판사",
            "published_date": "2025-09-19 10:00:00 GMT"
        },
        {
            "title": "테스트 기사 2",
            "url": "http://test.com/2",
            "publisher": "테스트 출판사",
            "published_date": "2025-09-19 11:00:00 GMT"
        }
    ]
    print("테스트 데이터로 Supabase 업로드를 시도합니다.")
    upload_news_to_supabase(test_news_data)
