import requests
from bs4 import BeautifulSoup
import time
import csv

keyword = "데이터분석"

# User-Agent 설정 (봇으로 인식되는 것을 방지)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# 크롤링할 페이지 수
num_pages = 5

filename = "jobkorea_data_analyst_jobs.csv"
with open(filename, "w", encoding="utf-8-sig", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["회사", "제목", "링크"])  # 헤더 작성

    for page_num in range(1, num_pages + 1):
        base_url = "https://www.jobkorea.co.kr/Search/?stext={}&Page_No={}".format(keyword, page_num)

        try:
            # HTTP 요청
            response = requests.get(base_url, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            job_list = soup.find_all("article", class_="list-item")

            if not job_list:
                print("페이지 {}에 채용 정보가 없습니다.".format(page_num))
                continue  # 채용 정보가 없으면 다음 페이지로 이동

            print(f"--- 페이지 {page_num} ---")  # 페이지 번호 표시

            for job in job_list:
                try:
                    # 회사 이름 추출
                    company = job.find("a", class_="corp-name-link dev-view")
                    company_text = company.text.strip() if company and company.text else ""  # 수정

                    # 채용 제목 추출
                    title = job.find("a", class_="information-title-link dev-view")
                    title_text = title.text.strip() if title and title.text else ""  # 수정

                    # 링크 추출
                    link_tag = job.find("a", class_="information-title-link dev-view")
                    link = "https://www.jobkorea.co.kr" + link_tag["href"] if link_tag and link_tag.has_attr("href") else ""  # 수정

                    # CSV 파일에 채용 정보 저장
                    csvwriter.writerow([company_text, title_text, link])

                    print("회사:", company_text)
                    print("제목:", title_text)
                    print("링크:", link)
                    print("-" * 50)
                except Exception as e:
                    print("Error:", e)
                    continue

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print("HTTP 요청 실패:", e)
            break  # HTTP 요청 실패 시 크롤링 종료
        except Exception as e:
            print("Error:", e)
            break  # 기타 에러 발생 시 크롤링 종료

print("크롤링 완료! 파일: {} 저장됨".format(filename))
