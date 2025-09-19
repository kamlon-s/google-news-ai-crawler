from gnews import GNews
import time
from upload_to_supabase import upload_news_to_supabase # Supabase 업로드 함수 임포트

def crawl_google_news(query, num_articles=10, lang='ko', country='KR'):
    google_news = GNews(language=lang, country=country, max_results=num_articles)
    
    print(f"'{query}'에 대한 구글 뉴스 검색 시작...")
    articles_list = google_news.get_news(query)
    
    if not articles_list:
        print(f"'{query}'에 대한 뉴스를 찾을 수 없습니다.")
        return

    print(f"총 {len(articles_list)}개의 기사를 찾았습니다. 상위 {min(num_articles, len(articles_list))}개 기사의 메타데이터를 가져옵니다.")
    
    crawled_data = []
    for i, article_data in enumerate(articles_list[:num_articles]):
        print(f"--- {i+1}/{min(num_articles, len(articles_list))}번째 기사 정보 처리 중 ---")
        try:
            crawled_data.append({
                'title': article_data.get('title', '제목 없음'),
                'url': article_data.get('url', 'URL 없음'),
                'publisher': article_data.get('publisher', {}).get('title', 'N/A'),
                'published_date': article_data.get('published date', 'N/A') # 키 수정
            })
            print(f"제목: {article_data.get('title', '제목 없음')}")
            print(f"URL: {article_data.get('url', 'URL 없음')}")
            print("-" * 50)
            time.sleep(0.5) # 서버 부하를 줄이기 위해 잠시 대기
        except Exception as e:
            print(f"기사 정보 처리 중 오류 발생: {article_data.get('url', 'URL 없음')} - {e}")
            print("-" * 50)
            continue
            
    return crawled_data

if __name__ == "__main__":
    search_query = "ai"
    top_articles = crawl_google_news(search_query, num_articles=10)
    
    if top_articles:
        print("\n=== 크롤링 완료된 기사 메타데이터 목록 ===")
        for i, article in enumerate(top_articles):
            print(f"\n--- 기사 {i+1} ---")
            print(f"제목: {article['title']}")
            print(f"출처: {article['publisher']}")
            print(f"발행일: {article['published_date']}")
            print(f"Google News URL: {article['url']}")
        print("\n참고: Google News RSS 링크의 복잡한 리디렉션 메커니즘으로 인해 기사 본문 전체를 안정적으로 추출하는 것은 현재 도구로는 어렵습니다. 위 목록은 기사의 제목, 출처, 발행일 및 Google News 링크를 제공합니다.")
        
        # Supabase에 크롤링된 데이터 업로드
        print("\n=== Supabase에 데이터 업로드 시작 ===")
        upload_news_to_supabase(top_articles)
    else:
        print("크롤링된 기사 메타데이터가 없습니다.")