#!/bin/bash
# scripts/local_capture_macos.sh
#
# macOS에서 OpenSim GUI를 실행해 스크린샷을 자동 수집합니다.
# 본 저장소 루트에서 실행하세요:
#     bash scripts/local_capture_macos.sh                # 가이드 모드
#     bash scripts/local_capture_macos.sh --auto         # 자동 모드
#
# 사전 준비:
#   1. OpenSim 4.5 (또는 4.6) GUI 설치
#   2. 자동 모드는 "시스템 설정 → 개인정보 보호 및 보안 → 손쉬운 사용"에서
#      터미널(Terminal.app)에 권한을 부여해야 합니다.
#
# 결과: docs/images/local-*.png 로 저장됨

set -e

# ───────────────────────────── 설정 ─────────────────────────────
APP_NAME_DEFAULT="OpenSim 4.5"
ARM26_DEFAULT="$(pwd)/demo_runs/arm26.osim"
OUT_DIR="$(pwd)/docs/images"

# 인자 파싱
MODE="guided"
[[ "$1" == "--auto" ]] && MODE="auto"

# OpenSim 앱 찾기
APP_PATH=""
for p in "/Applications/${APP_NAME_DEFAULT}.app" \
         "/Applications/OpenSim 4.6.app" \
         "/Applications/OpenSim.app"; do
    [[ -d "$p" ]] && APP_PATH="$p" && break
done

if [[ -z "$APP_PATH" ]]; then
    echo "❌ OpenSim 앱을 /Applications에서 찾지 못했습니다."
    echo "   경로를 직접 입력하세요 (예: /Applications/OpenSim 4.5.app):"
    read -r APP_PATH
    [[ ! -d "$APP_PATH" ]] && { echo "경로가 존재하지 않습니다."; exit 1; }
fi

APP_NAME="$(basename "$APP_PATH" .app)"
mkdir -p "$OUT_DIR"

# Arm26 확인
if [[ ! -f "$ARM26_DEFAULT" ]]; then
    echo "⚠️  $ARM26_DEFAULT 가 없습니다."
    echo "   demo_runs/ 폴더에 arm26.osim을 두거나, 경로를 입력하세요:"
    read -r ARM26_DEFAULT
fi

echo "──────────────────────────────────────────────"
echo "  App : $APP_NAME"
echo "  Model: $ARM26_DEFAULT"
echo "  Mode : $MODE"
echo "  Out  : $OUT_DIR"
echo "──────────────────────────────────────────────"

# ───────────────────────────── 헬퍼 ─────────────────────────────
shot() {
    local name="$1"
    local desc="$2"
    local file="$OUT_DIR/local-$(printf '%02d' "$STEP")-$name.png"
    # OpenSim 창만 캡처 (-l <window_id>로 특정 창 캡처가 가능)
    # 가장 단순한 방법: 활성 창을 캡처 (-W는 인터랙티브 선택)
    # 여기서는 OpenSim을 활성화한 후 메인 디스플레이 캡처를 사용
    osascript -e "tell application \"$APP_NAME\" to activate" 2>/dev/null || true
    sleep 0.5
    screencapture -x -o "$file"
    echo "  📸 $file  ($desc)"
    STEP=$((STEP + 1))
}

wait_user() {
    local msg="$1"
    echo ""
    echo "  ▶ $msg"
    echo -n "    완료하면 Enter (또는 's'로 이 단계 스킵): "
    read -r ans
    [[ "$ans" == "s" ]] && return 1
    return 0
}

count_down() {
    local n="$1"
    for i in $(seq "$n" -1 1); do
        printf "\r  자동 캡처까지 %d초..." "$i"; sleep 1
    done
    printf "\r                          \r"
}

# ───────────────────────────── 실행 ─────────────────────────────
STEP=1

echo ""
echo "1/5. OpenSim 실행"
open -a "$APP_NAME"
echo "  앱이 뜨고 메인 창이 보일 때까지 잠시 기다립니다..."
sleep 6
shot "startup" "빈 메인 창"

echo ""
echo "2/5. 모델 열기 (File → Open Model)"
if [[ "$MODE" == "auto" ]]; then
    osascript <<APPLESCRIPT
tell application "$APP_NAME" to activate
delay 1
tell application "System Events"
    tell process "$APP_NAME"
        keystroke "o" using {command down}
    end tell
end tell
delay 1.5
tell application "System Events"
    keystroke "g" using {command down, shift down}   -- 경로 직접 입력 다이얼로그
    delay 0.5
    keystroke "$ARM26_DEFAULT"
    delay 0.3
    keystroke return
    delay 0.5
    keystroke return                                  -- 'Open' 확정
end tell
APPLESCRIPT
    sleep 3
else
    wait_user "메뉴에서 File → Open Model... 을 선택하고, $ARM26_DEFAULT 를 여세요." \
        || true
fi
shot "arm26-loaded" "Arm26 모델이 로드된 상태"

echo ""
echo "3/5. 시점 변경 — Side View"
if [[ "$MODE" == "auto" ]]; then
    # View 메뉴는 OpenSim 버전마다 다름. 자동 시도.
    osascript <<APPLESCRIPT
tell application "System Events"
    tell process "$APP_NAME"
        try
            click menu item "Side" of menu 1 of menu item "Camera" of menu 1 of menu bar item "View" of menu bar 1
        end try
    end tell
end tell
APPLESCRIPT
    sleep 1
else
    wait_user "View → Camera → Side 등으로 시점을 측면으로 바꿔보세요." \
        || true
fi
shot "side-view" "측면 시점"

echo ""
echo "4/5. Coordinates 슬라이더 — 팔꿈치 굴곡"
wait_user "우측 Coordinates 패널의 r_elbow_flex 슬라이더를 80~90°까지 끌어보세요." \
    || true
shot "elbow-flexed" "팔꿈치가 굴곡된 자세"

echo ""
echo "5/5. Forward Dynamics 다이얼로그"
if [[ "$MODE" == "auto" ]]; then
    osascript <<APPLESCRIPT
tell application "System Events"
    tell process "$APP_NAME"
        try
            click menu item "Forward Dynamics..." of menu 1 of menu bar item "Tools" of menu bar 1
        end try
    end tell
end tell
APPLESCRIPT
    sleep 2
else
    wait_user "Tools → Forward Dynamics... 메뉴를 여세요 (다이얼로그 캡처용)." \
        || true
fi
shot "fd-dialog" "Forward Dynamics 설정 다이얼로그"

echo ""
echo "──────────────────────────────────────────────"
echo " 완료! $OUT_DIR 의 local-*.png 확인"
ls -1 "$OUT_DIR"/local-*.png 2>/dev/null
echo ""
echo " 다음 단계: 저장소에 커밋"
echo "   git add docs/images/local-*.png"
echo "   git commit -m 'docs: add local OpenSim GUI screenshots (macOS)'"
echo "   git push"
echo "──────────────────────────────────────────────"
