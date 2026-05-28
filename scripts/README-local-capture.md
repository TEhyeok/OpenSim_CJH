# 로컬 PC에서 OpenSim GUI 스크린샷 자동 수집 (macOS)

이 가이드는 사용자 본인의 Mac에서 OpenSim GUI를 실제로 띄우고
스크린샷 5장을 자동/반자동으로 수집해 본 저장소에 추가하는 방법을 설명합니다.

> ⚠️ 본 클라우드 세션(Claude Code on the web)에서는 사용자 데스크톱에 직접 접근할 수 없습니다.
> 아래 스크립트는 **반드시 본인의 Mac 터미널에서 직접 실행**해야 합니다.

## 1. 사전 준비

### 1.1 저장소 클론

```bash
git clone <repo-url> OpenSim_CJH
cd OpenSim_CJH
git checkout claude/opensim-korean-guide-CBjfw
```

### 1.2 OpenSim 설치 확인

```bash
ls /Applications | grep -i opensim
# 예: "OpenSim 4.5"
```

설치되어 있지 않다면 [2장 설치 가이드](../docs/02-설치.md#24-macos-설치) 참고.

### 1.3 (자동 모드만) 손쉬운 사용 권한 부여

자동 모드(`--auto`)는 AppleScript로 메뉴를 조작하므로 권한이 필요합니다.

1. **시스템 설정** → **개인정보 보호 및 보안** → **손쉬운 사용**
2. 터미널(Terminal.app) 또는 사용 중인 셸 앱을 추가하고 체크

(가이드 모드는 권한이 필요 없습니다.)

## 2. 실행

저장소 루트에서:

```bash
# 가이드 모드 (권장, 안정적)
bash scripts/local_capture_macos.sh

# 자동 모드 (실험적, 메뉴까지 자동 조작)
bash scripts/local_capture_macos.sh --auto
```

스크립트는 OpenSim 앱을 찾아 실행한 뒤, 다음 5단계를 진행합니다.

| # | 단계 | 캡처 파일 |
| - | ---- | --------- |
| 1 | 빈 메인 창 | `local-01-startup.png` |
| 2 | Arm26 모델 로드 | `local-02-arm26-loaded.png` |
| 3 | 측면 시점 | `local-03-side-view.png` |
| 4 | 팔꿈치 굴곡 자세 | `local-04-elbow-flexed.png` |
| 5 | Forward Dynamics 다이얼로그 | `local-05-fd-dialog.png` |

가이드 모드에서는 각 단계마다:

```
  ▶ 메뉴에서 File → Open Model... 을 선택하고, ... arm26.osim 을 여세요.
    완료하면 Enter (또는 's'로 이 단계 스킵):
```

처럼 안내가 뜹니다. GUI에서 동작을 마치고 Enter만 누르면 스크린샷이 저장됩니다.

## 3. 결과 확인 및 커밋

```bash
ls -1 docs/images/local-*.png
open docs/images/local-02-arm26-loaded.png   # 미리보기로 확인

git add docs/images/local-*.png
git commit -m "docs: add local OpenSim GUI screenshots (macOS)"
git push origin claude/opensim-korean-guide-CBjfw
```

푸시 후 본 저장소의 9장 문서에 그림을 직접 임베드할 수 있습니다.

## 4. 자주 발생하는 문제

### 4.1 자동 모드가 메뉴를 못 찾는다

OpenSim은 Java/NetBeans 기반이라 AppleScript의 menu bar 탐색이
일부 환경에서 동작하지 않습니다. 자동 모드가 실패하면 가이드 모드를 쓰세요.

### 4.2 화면 전체가 캡처된다

`screencapture -x -o file.png`는 메인 디스플레이 전체를 캡처합니다.
OpenSim 창만 캡처하려면:

```bash
# 대화형으로 창 선택
screencapture -W docs/images/local-02-arm26-loaded.png

# 또는 창 ID로 캡처 (osascript로 ID 조회 필요)
```

가이드 모드에서 `-W` 옵션으로 바꾸려면 스크립트 `shot()` 함수의
`screencapture -x -o` 줄을 `screencapture -W -o` 로 변경하세요.

### 4.3 권한 거부 에러

자동 모드에서 `1002:1002: execution error` 같은 메시지가 나오면 1.3절의
손쉬운 사용 권한이 빠진 것입니다.

### 4.4 OpenSim 앱 이름이 다르다

스크립트는 `OpenSim 4.5` → `OpenSim 4.6` → `OpenSim` 순으로 탐색합니다.
다른 이름이면 스크립트 실행 시 직접 경로를 물어보니 입력하면 됩니다.

## 5. 9장 문서에 그림 추가하기

스크린샷이 모두 모이면, 다음 코드 블록을 `docs/09-실전데모.md`의
적절한 위치에 추가해주세요.

```markdown
## 9.X 실제 OpenSim GUI 스크린샷

다음은 macOS에 설치된 OpenSim 4.5/4.6 GUI를 실제로 실행하여 캡처한 화면입니다.

![OpenSim 시작 화면](images/local-01-startup.png)

*그림. OpenSim 첫 실행 직후의 빈 메인 창.*

![Arm26 모델 로드](images/local-02-arm26-loaded.png)

*그림. File → Open Model로 arm26.osim을 불러온 직후. 3D 뷰어에 어깨–팔꿈치
2자유도 모델이 표시되고, 좌측 Navigator에 트리가 생성된다.*

![측면 시점](images/local-03-side-view.png)
![팔꿈치 굴곡](images/local-04-elbow-flexed.png)
![Forward Dynamics 다이얼로그](images/local-05-fd-dialog.png)
```

저장소에 직접 푸시한 뒤 PR이나 이슈로 알려주시면, 본 문서의 그림 위치 등을
추가로 조정해드릴 수 있습니다.
