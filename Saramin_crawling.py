import requests
from bs4 import BeautifulSoup
import time
import csv

keyword = "데이터분석"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
num_pages = 5
filename = "saramin_data_analyst_jobs.csv"

with open(filename, "w", encoding="utf-8-sig", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["회사", "제목", "경력", "학력", "고용형태", "근무지",  "링크"])

    for page_num in range(1, num_pages + 1):
        base_url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchword={keyword}&recruitPage={page_num}"

        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            job_list = soup.find_all("div", class_="item_recruit")

            if not job_list:
                print(f"페이지 {page_num}에 채용 정보가 없습니다.")
                continue

            print(f"--- 페이지 {page_num} ---")

            for job in job_list:
                try:
                    company = job.find("div", class_="area_corp")
                    company_text = company.text.strip() if company and company.text else ""

                    title = job.find("h2", class_="job_tit")
                    title_text = title.text.strip() if title and title.text else ""

                    job_conditions = job.find("div", class_="job_condition")
                    job_conditions_text = job_conditions.text.strip() if job_conditions and job_conditions.text else ""
                    # 경력, 학력, 고용형태, 근무지 분리 (정확한 구분은 웹 페이지 구조에 따라 달라질 수 있음)
                    condition_parts = job_conditions_text.split("·")
                    experience = condition_parts[0].strip() if len(condition_parts) > 0 else ""
                    education = condition_parts[1].strip() if len(condition_parts) > 1 else ""
                    employment_type = condition_parts[2].strip() if len(condition_parts) > 2 else ""
                    location = condition_parts[3].strip() if len(condition_parts) > 3 else ""

                    link_tag = job.find("a")
                    link = "https://www.saramin.co.kr" + link_tag["href"] if link_tag and link_tag.has_attr("href") else ""

                    csvwriter.writerow([company_text, title_text, experience, education, employment_type, location, link])

                    print("회사:", company_text)
                    print("제목:", title_text)
                    print("경력:", experience)
                    print("학력:", education)
                    print("고용형태:", employment_type)
                    print("근무지:", location)
                    print("링크:", link)
                    print("-" * 50)

                except Exception as e:
                    print("Error:", e)
                    continue

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print("HTTP 요청 실패:", e)
            break
        except Exception as e:
            print("Error:", e)
            break

print("크롤링 완료! 파일: {} 저장됨".format(filename))
