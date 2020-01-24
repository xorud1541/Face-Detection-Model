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

## Detection-Model

### 용어 정리

* batch란?
배치는 한 번에 처리하는 사진(데이터)의 개수를 말한다.

* train(학습)이란?
사전적 의미: 학습이란 경험을 통해 못하던 일을 하게 되거나 하던 일을 더 잘하게 됨을 뜻한다.
딥러닝 세계의 의미: 특정한 응용 영역에서 발생하는 데이터(경험)를 이용하여 높은 성능으로 문제를 해결하는 컴퓨터 프로그램을 만드는 작업이다.

	- Q1. 성능을 높히는 행위, 작업
		+ 성능(Deep learning performance)이란 무엇일까?
		딥러닝 세계에서 성능이란 학습된 시스템의 **정확도** 와 비례한다고 말할 수 있다. 정확도가 높으면 성능이 좋다고 말할 수 있다.

	- Q2. 얼마나 높아야 높은 성능인가?
		+ 95 ~ 99%

* test란?
* label이란?
* model이란?
* epoch이란?
* step이란?

### Tensorflow 2.0 사용한 문법 정리
### 사용한 딥러닝 개념정리
### 딥러닝 모델 설명
