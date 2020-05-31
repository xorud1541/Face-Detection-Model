# Face-Detection-Model

## 정리해야 할 내용들(블로그에 기록)
- 학습모델 저장포맷 유형별 정리
- 모델 구조 설명
- Tensorflow 2.0의 dataset 사용법
- 학습모델의 compile이란?
- numpy와 tensor의 차이
- numpy 학습

## Todo(~ v2.0)
- 모델의 예측이 틀렸을 때, 새로 레이블링 해줄 위젯(라디오버튼) 추가
- 재학습 고도화
- 이미지 뷰어 UI개선

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

* epoch이란?
전체 훈련데이터를 이용하여 한 번 돌며 학습하는 것을 epoch이라고 한다.

* step이란?
weight와 bias를 1회 업데이트하는 것을 step 이라고 한다.

### Tensorflow 2.0 사용한 문법 정리

* tf.data.dataset
tf.data.datast API는 효율적으로 입력 파이프라인을 지원한다. 또한, 스트리밍 형식으로 데이터를 입력할 수 있기에 메모리에 딱 맞지 않아도 된다.
	- tf.data.dataset.list_files
		<pre><code>
		@staticmethod
		list_files(
			file_pattern,
			shuffle=None,
			seed=Node
		)
		</code></pre>

		glob 패턴과 일치하는 모든 파일들을 모은다.

		Returns:
		+ dataset: 파일이름들에 대응하는 문자열 dataset을 반환한다.

		+ example
		<pre><code>
		// data_dir에 해당하는 모든 파일들을 데이터세트로 묶는다.
		train_list_ds = tf.dats.Dataset.list_files(str(data_dir/'*/*'))
		</code></pre>

	- tf.data.dataset.map
		<pre><code>
		map(
			map_func,
			num_parallel_calls=None
			)
		</code></pre>

		dataset들의 각각의 요소들이 map_func 함수를 통해서 전처리 작업을 할 수 있다.
		그리고 변형된 각가의 요소들이 새로운 dataset으로 반환되어진다.

		num_parallel_calls?
		병렬처리의 개수를 지정할 수 있다.
		num_parallel_calls = tf.data.experimental.AUTOTUNE 이라 설정하면 이용가능한 CPU에 맞게 동적으로 지정 가능하다.

  - tf.data.dataset.shuffle
		<pre><code>
		shuffle(
			buffer_size,
			seed=None,
			reshuffle_each_iteration=None
			)
		</code></pre>

		dataset에 data들을 랜덤하게 섞는다.
		buffer_size 만큼의 data들을 섞는다.

	- tf.data.dataset.repeat
	- tf.data.dataset.batch
	- tf.data.dataset.prefetch
