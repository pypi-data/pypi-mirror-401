# 의약품안전나라 > 의약품등 제품정보 검색 > 엑셀다운로드

```
의약품안전나라 > 의약품등 제품정보 검색 > 엑셀다운로드
    
의약품안전나라 > 의약품등 제품정보 검색:
https://nedrug.mfds.go.kr/searchDrug
엑셀다운로드
https://nedrug.mfds.go.kr/searchDrug/getExcel

1. Excel 파일 다운로드
2. GCS에 업로드
3. Excel 파일에서 약품목록 파싱
4. BigQuery에 로드
5. medicine_list.csv에 저장
```

## Installation

```bash
pip install sayou-healthcare
```

## Usage

#### 의약품안전나라 > 의약품등 제품정보 검색

```python
from sayou.healthcare.nedrug import NedrugCrawler

# Nedrug Crawler 초기화
crawler = NedrugCrawler()

data = crawler.download()
for medicine in data.medicines:
    print(medicine)
```
