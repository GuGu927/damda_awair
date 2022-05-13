# 담다 어웨어

Damda Awair Component

![HACS][hacs-shield]
![Version v1.4][version-shield]

문의 : 네이버 [HomeAssistant카페](https://cafe.naver.com/koreassistant)

## 담다 어웨어가 도움이 되셨나요?

<a href="https://qr.kakaopay.com/281006011000098177846177" target="_blank"><img src="https://github.com/GuGu927/damda_pad/blob/main/images/kakao.png" alt="KaKao"></a>

카카오페이 : https://qr.kakaopay.com/281006011000098177846177

<a href="https://paypal.me/rangee927" target="_blank"><img src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_150x38.png" alt="PayPal"></a>

## 버전 기록정보

| 버전   | 날짜       | 내용                                        |
| ------ | ---------- | ------------------------------------------- |
| v1.0.0 | 2021.11.22 | 게시                                        |
| v1.1.0 | 2021.12.06 | 상태 업데이트 시간 30초로 변경<br>버그 수정 |
| v1.2.0 | 2021.12.07 | 버그 수정                                   |
| v1.2.1 | 2021.12.08 | 모델명 등 표시방법 수정                     |
| v1.2.2 | 2021.12.11 | 히스토리 그래프 관련 수정                   |
| v1.2.3 | 2021.12.12 | 2021.12 업데이트 대응                       |
| v1.2.4 | 2021.12.15 | 2021.12 업데이트 대응2                      |
| v1.2.5 | 2021.12.23 | 통계그래프 가능하게끔 수정                  |
| v1.2.6 | 2022.01.04 | 오류 수정                                   |
| v1.2.7 | 2022.05.12 | 2022.06 대응                                |

<br/>

## 준비물

- HomeAssistant `최신버전`(**2021.12.0 이상**)
- HomeAssistant OS, Core, Container 등 아무런 상관이 없습니다.

<br/>

## 사용자 구성요소를 HA에 설치하는 방법

### HACS

- HACS > Integrations > 우측상단 메뉴 > `Custom repositories` 선택
- `Add custom repository URL`에 `https://github.com/GuGu927/damda_awair` 입력
- Category는 `Integration` 선택 후 `ADD` 클릭
- HACS > Integrations 에서 `Damda Awair` 찾아서 설치
- HomeAssistant 재시작

<br/>

### 수동설치

- `https://github.com/GuGu927/damda_awair` 페이지에서 `Code/Download ZIP` 을 눌러 파일을 다운로드, 내부의 `damda_awair` 폴더 확인
- HomeAssistant 설정폴더인 `/config` 내부에 `custom_components` 폴더를 생성(이미 있으면 다음 단계)<br/>설정폴더는 `configuration.yaml` 파일이 있는 폴더를 의미합니다.<br>
- `/config/custom_components`에 위에서 다운받은 `damda_awair` 폴더를 넣기<br>
- HomeAssistant 재시작

<br/>

## 담다어웨어를 discovery로 추가하는 방법(**권장**)

### Discovery

- HomeAssistant 사이드패널 > 설정 > 통합 구성요소 > 발견된 `담다 어웨어` 구성하기<br>
- 완료!

## 담다어웨어를 통합구성요소로 설치하는 방법

### 통합구성요소

- HomeAssistant 사이드패널 > 설정 > 통합 구성요소 > 통합 구성요소 추가<br>
- 검색창에서 `담다 어웨어` 입력 후 선택<br>
- IP에 추가할 `어웨어 장치의 IP주소`를 입력.

[version-shield]: https://img.shields.io/badge/version-v1.2.7-orange.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
