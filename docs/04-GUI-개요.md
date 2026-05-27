# 4장. GUI 개요

OpenSim GUI는 NetBeans 플랫폼 기반의 도킹형 인터페이스를 사용한다.
각 패널은 분리·재배치·플로팅이 가능하며, **Window** 메뉴에서 표시·숨김을 제어한다.

## 4.1 메인 창 구성

```
┌─────────────────────────────────────────────────────────────────────┐
│ ① 메뉴바: File  Edit  View  Tools  Window  Help                     │
├─────────────────────────────────────────────────────────────────────┤
│ ② 툴바: 모션 재생 컨트롤 │ 분석 도구 단축 │ 시각화 옵션              │
├──────────────┬──────────────────────────────────┬───────────────────┤
│              │                                  │                   │
│ ③ Navigator  │     ④ 3D Visualizer (Model)     │  ⑤ Coordinates    │
│              │                                  │                   │
│              │                                  │                   │
├──────────────┤                                  ├───────────────────┤
│              │                                  │                   │
│ ⑥ Properties │                                  │  ⑦ Motion Slider  │
│              │                                  │                   │
├──────────────┴──────────────────────────────────┴───────────────────┤
│ ⑧ Messages / Output                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## 4.2 메뉴바

### 4.2.1 File 메뉴

| 항목 | 설명 |
| ---- | ---- |
| New Model... | 빈 모델 생성 |
| Open Model... | `.osim` 파일 열기 |
| Save Model / Save Model As | 모델 저장 |
| Load Motion... | `.mot` / `.sto` 모션 파일 로드 |
| Save Motion As... | 현재 모션 저장 |
| Print... | 현재 3D 뷰를 인쇄 |
| Recent Files | 최근 작업 파일 목록 |
| Exit | 프로그램 종료 |

### 4.2.2 Edit 메뉴

- **Undo / Redo** — 모델 편집 되돌리기
- **Preferences...** — GUI 환경 설정 (그래픽 품질, 메모리 한도, 단위 등)

### 4.2.3 View 메뉴

- **Camera Reset / Top / Front / Side / Iso** — 미리 정의된 카메라 각도
- **Show/Hide Markers, Muscles, Wrapping Surfaces, Forces** — 모델 요소 표시 토글
- **Background Color** — 배경색 변경
- **Take Snapshot** — PNG 캡처

### 4.2.4 Tools 메뉴

가장 많이 사용하는 메뉴이다. 각 도구의 상세 사용법은 [6장](06-주요-도구.md) 참고.

| 도구 | 약어 | 입력 | 출력 |
| ---- | ---- | ---- | ---- |
| Scale | — | 정적 마커, 측정치 | 스케일된 모델, 모델별 마커셋 |
| Inverse Kinematics | IK | 마커 궤적(.trc) | 관절 각도(.mot) |
| Inverse Dynamics | ID | 관절 각도, 외력 | 관절 모멘트(.sto) |
| Static Optimization | SO | 관절 각도, 외력 | 근육 활성도/힘(.sto) |
| Computed Muscle Control | CMC | 관절 각도, 외력 | 근육 활성도(.sto) |
| Forward Dynamics | FD | 컨트롤 신호 | 운동 결과(.sto) |
| Analyze | — | 운동 결과 | 다양한 분석 출력 |
| Plot... | — | `.sto` / `.mot` | 그래프 |

### 4.2.5 Window 메뉴

각 도킹 윈도우를 표시/숨김 한다.
- Navigator, Coordinates, Properties, Messages, Motion Slider 등을 토글 가능.
- **Reset Windows** 로 기본 레이아웃 복구.

### 4.2.6 Help 메뉴

- About — 빌드 버전 확인
- Online Documentation — 공식 Confluence 위키 링크
- License — Apache 2.0 라이선스

## 4.3 툴바

상단 툴바에는 자주 사용하는 기능이 아이콘으로 배치되어 있다.

| 아이콘 | 기능 |
| ------ | ---- |
| ▶ | 모션 재생 |
| ◼ | 정지 |
| ⟲ | 반복 재생 토글 |
| ◀◀ / ▶▶ | 처음/끝 프레임으로 이동 |
| 슬라이더 | 재생 속도 (0.1× ~ 5×) |
| Scale / IK / ID / SO / CMC / FD | 도구 바로 실행 |
| Plot | 결과 시각화 |
| Camera | 시점 변경 |

## 4.4 Navigator 패널 (좌측)

- 현재 열린 **모델**, **모션**, **분석 결과**가 트리 형태로 표시된다.
- 한 GUI 세션에서 **여러 모델**을 동시에 열 수 있다. 현재 작업 모델은 **굵게** 표시.
- 우클릭 메뉴로 모델 닫기, 다른 이름으로 저장, 컬러 변경 등의 기능 제공.

### 모델 트리 주요 항목

- **Bodies / Joints / Constraints** — 기구학 요소
- **Forces** — 근육, 외력, 스프링 등
- **Markers** — 모션 캡처 마커
- **Controllers** — 컨트롤 신호 정의
- **ContactGeometries** — 접촉 모델
- **Probes / Reporters** — 출력 수집

## 4.5 3D Visualizer (중앙)

- 모델의 3D 뷰. 마우스 조작은 [3.3.1](03-시작하기.md#331-3d-뷰어-조작) 참고.
- **Wrapping Surfaces** (근육 경로 우회를 위한 표면)를 표시할 수 있다.
- **Marker Experimental Data** 가 로드되면 실제 마커와 모델 마커를 함께 표시한다.
- **View → Show Forces** 로 외력 벡터(GRF)를 화살표로 표시.

### 시각화 옵션 단축키

| 단축키 | 동작 |
| ------ | ---- |
| `M` | 근육 표시 토글 |
| `B` | Body 표시 토글 |
| `K` | 마커 표시 토글 |
| `W` | Wrapping surface 토글 |
| `F` | 외력 표시 토글 |

## 4.6 Coordinates 패널 (우측 상단)

- 모든 자유도(Coordinate)의 슬라이더 표시
- 각 자유도마다 다음을 설정 가능:
  - **값(value)** — 현재 각도/변위
  - **Lock** — IK 등에서 고정
  - **Default** — 기본값으로 리셋
  - **Clamped/Unclamped** — 한계 적용 여부

## 4.7 Properties 윈도우

- Navigator에서 선택한 컴포넌트의 모든 속성을 표시.
- 예: 근육 선택 시 `max_isometric_force`, `optimal_fiber_length`, `tendon_slack_length`,
  `pennation_angle_at_optimal` 등을 직접 편집 가능.
- 변경 후 **Apply** 버튼을 눌러야 모델에 반영된다.

> 모델을 편집한 경우 반드시 **File → Save Model As...** 로 새 파일로 저장하라.
> 원본 예제 모델을 덮어쓰지 않는 것이 좋다.

## 4.8 Motion Slider

- 로드된 모션의 타임라인을 표시.
- 슬라이더 드래그로 임의의 프레임으로 이동 가능.
- 우클릭으로 **북마크** 추가 가능.

## 4.9 Messages / Output 패널

- OpenSim 라이브러리의 로그 메시지(정보·경고·오류)가 출력된다.
- 도구 실행 시 진행 상황·잔차·반복 횟수가 표시된다.
- 우클릭 → *Save Log...* 으로 텍스트 파일로 저장 가능 (디버깅 시 유용).

## 4.10 작업공간 / 레이아웃 저장

- 각 패널을 드래그하여 위치를 변경할 수 있다.
- **Window → Save Layout As...** 로 사용자 레이아웃 저장.
- **Window → Reset Windows** 로 기본 레이아웃 복구.

## 4.11 다음 장 안내

다음 장에서는 [모델 트리·자유도·속성 윈도우](05-모델-탐색.md)를 활용한
모델 탐색·편집을 자세히 다룬다.
