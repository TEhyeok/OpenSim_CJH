# OpenSim 한국어 사용 설명서

스탠퍼드 대학교 NCSRR(National Center for Simulation in Rehabilitation Research)에서 개발한
오픈소스 근골격계 모델링·동역학 시뮬레이션 소프트웨어 **OpenSim**의 한국어 사용 설명서입니다.

> 본 문서의 기준 버전은 **OpenSim 4.5.2** (2025-04-22 릴리스)이며, 연구자 및 대학원생을 대상으로
> 설치부터 GUI 사용법까지 다룹니다.

![OpenSim 표준 분석 워크플로](docs/images/workflow.png)

*그림: 실험 데이터로부터 결과 분석까지 이어지는 OpenSim 표준 워크플로*

---

## 목차

| 장 | 제목 | 주요 내용 |
| -- | ---- | --------- |
| 1 | [OpenSim 소개](docs/01-소개.md) | 소프트웨어 개요, 적용 분야, 핵심 개념 |
| 2 | [설치 가이드](docs/02-설치.md) | Windows / macOS / Linux 설치, 시스템 요구사항 |
| 3 | [시작하기](docs/03-시작하기.md) | 첫 실행, 예제 모델 로드, 워크플로 개요 |
| 4 | [GUI 개요](docs/04-GUI-개요.md) | 메인 창, 메뉴, 툴바, 도킹 윈도우 구조 |
| 5 | [모델 탐색과 조작](docs/05-모델-탐색.md) | Navigator, Coordinates, Properties Window |
| 6 | [주요 분석 도구](docs/06-주요-도구.md) | Scale, IK, ID, SO, CMC, Forward, Moco |
| 7 | [시각화와 결과 분석](docs/07-시각화-결과분석.md) | Visualizer, Plotter, 결과 파일 해석 |
| 8 | [문제 해결과 참고 자료](docs/08-문제해결-참고자료.md) | 자주 발생하는 오류, 커뮤니티, 추가 학습 자료 |

---

## 빠른 시작

1. **다운로드** — <https://simtk.org/projects/opensim> 에서 OpenSim 4.5 GUI 인스톨러를 받는다.
2. **설치** — Windows는 `.exe`, macOS는 `.dmg`를 실행하여 설치한다. ([2장 참고](docs/02-설치.md))
3. **첫 실행** — `File → Open Model`에서 `Models/Arm26/arm26.osim` 예제를 연다. ([3장 참고](docs/03-시작하기.md))
4. **분석** — `Tools` 메뉴에서 원하는 도구(Scale, IK 등)를 실행한다. ([6장 참고](docs/06-주요-도구.md))

## 시각 자료

본 설명서의 모든 그림은 `docs/images/` 하위에 PNG로 보관되며,
일부 흐름도는 GitHub-flavored Markdown의 **Mermaid** 문법으로 인라인 렌더링됩니다.
PNG는 `scripts/make_figures.py` 한 번 실행으로 모두 재생성됩니다.

```bash
pip install matplotlib
python3 scripts/make_figures.py
```

## 라이선스

본 사용 설명서는 학습 목적으로 작성되었습니다.
OpenSim 소프트웨어 자체는 Apache License 2.0으로 배포됩니다.
공식 자료 출처: <https://opensim.stanford.edu> · <https://github.com/opensim-org/opensim-core>
