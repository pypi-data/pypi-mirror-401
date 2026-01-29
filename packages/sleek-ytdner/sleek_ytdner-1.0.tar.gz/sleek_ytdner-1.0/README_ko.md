# Sleek YTDner (슬릭 YTDner)

<p align="center">
  <img src="sleek_ytdner/static/images/logo.png" alt="Sleek 로고" width="150" height="auto">
</p>

<p align="center">
  <strong>Pure. Potent. Permanent.</strong><br>
  타협하지 않는 완벽주의자를 위해 설계된 마지막 미디어 아카이버.
</p>

<p align="center">
  <a href="LICENSE_ko.md"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="라이선스"></a>
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue" alt="Python 버전">
  <img src="https://img.shields.io/badge/Flask-3.0%2B-lightgrey" alt="Flask">
</p>

---
[English](README.md) | [한국어](README_ko.md)
---

## 📖 소개

**Sleek YTDner**는 현대적이고 미니멀한 유튜브 다운로더이자 미디어 아카이버입니다. **Flask**를 기반으로 강력한 **yt-dlp** 엔진을 활용하며, 이 모든 기능을 아름다운 고성능 글래스모피즘(Glassmorphism) UI로 감쌌습니다.

Sleek은 **심미성**, **프라이버시**, 그리고 **통제권**을 중요시하는 분들을 위해 디자인되었습니다.

### ✨ 주요 기능

- **💎 글래스모피즘 디자인**: 시스템 테마와 자연스럽게 어우러지는 아름다운 반투명 사용자 인터페이스.
- **🌗 적응형 테마**: 시스템의 라이트/다크 모드와 자동으로 동기화되며, 수동 전환도 가능합니다.
- **🚀 8K 지원**: 최대 8K HDR 비디오와 무손실 오디오 추출을 지원합니다.
- **🔒 프라이버시 우선**: 모든 처리는 로컬에서 이루어집니다. 외부 서버 통신이나 추적이 없으며, 데이터 주권은 오직 당신에게 있습니다.
- **📂 스마트 자동화**: 선호하는 다운로드 경로를 기억하고 최적의 파일 포맷을 자동으로 감지합니다.
- **⚡ 비동기 처리**: 반응성 높은 경험을 위해 다운로드 스트림을 비동기로 처리합니다.

## 🛠️ 기술 스택

- **백엔드**: Python 3.12+, Flask
- **코어 엔진**: yt-dlp
- **프론트엔드**: HTML5, Vanilla JS, CSS3 (Variables, Flexbox/Grid, Backdrop Filter)
- **라이선스**: MIT

## 🚀 시작하기

### 필수 조건

- **Python 3.8+**: 호환되는 버전이 설치되어 있어야 합니다.
- **FFmpeg**: 고품질 비디오 및 오디오 병합을 위해 필요합니다.
  - *Ubuntu/Debian*: `sudo apt install ffmpeg`
  - *macOS*: `brew install ffmpeg`
  - *Windows*: [FFmpeg.org](https://ffmpeg.org/)에서 다운로드하여 PATH에 추가하세요.

### 설치 방법

Sleek YTDner는 표준 Python 패키지로 배포됩니다. 소스에서 직접 설치할 수 있습니다.

1. **저장소 클론하기**
   ```bash
   git clone https://github.com/hslcrb/pypack_sleek_a-ytdownloader-pkg.git
   cd pypack_sleek_a-ytdownloader-pkg
   ```

2. **pip로 설치하기**
   시스템을 깨끗하게 유지하기 위해 가상 환경 사용을 권장합니다.
   ```bash
   # 가상 환경 생성 및 활성화 (선택 사항이지만 권장됨)
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

   # 패키지 설치
   pip install .
   ```

   코드를 수정하려는 개발자의 경우:
   ```bash
   pip install -e .
   ```

## 💻 사용 방법

설치가 완료되면, **Sleek YTDner**를 시스템 어디에서나 명령어로 실행할 수 있습니다.

1. **서버 실행**
   설정 파일과 다운로드 폴더를 저장할 디렉토리로 이동한 후 실행하세요:
   ```bash
   sleek-downloader
   ```

2. **인터페이스 접속**
   웹 브라우저를 열고 다음 주소로 이동하세요:
   ```
   http://localhost:5000
   ```
   
   별도의 설정이 없다면 애플리케이션은 현재 작업 디렉토리에 `config.json`과 `downloads` 폴더를 자동으로 생성합니다.

## 🤝 기여하기

기여는 언제나 환영합니다! 풀 리퀘스트(PR) 제출 절차와 행동 강령에 대한 자세한 내용은 [CONTRIBUTING_ko.md](CONTRIBUTING_ko.md)를 참고해주세요.

## 📄 라이선스

이 프로젝트는 MIT License 하에 배포됩니다. 자세한 내용은 [LICENSE_ko.md](LICENSE_ko.md) 파일을 참조하세요.

---
<p align="center">
  © 2008-2026 Rheehose (Rhee Creative). 열정으로 제작되었습니다.<br>
  <em>최종 업데이트: 2026년 1월 17일 (KST)</em>
</p>
