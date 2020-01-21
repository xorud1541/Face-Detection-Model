# Face-Detection-Model

## Google-images-Crawler 사용법
- 실행인자
	- keyword : 크롤링할 검색어
	- max_num : 수집할 이미지 개수

- 예시
	<pre><code>
	$ pip install icrawler
	$ python Google-images-Crawler.py "keyword" 1000
	</code></pre>
	
## MakeFaceData 사용법
- 실행인자
	- inputdir : 얼굴 영역을 추출할 이미지들
	
- 예시
	<pre><code>
	$ python MakeFaceData.py inputdir
	</code></pre>