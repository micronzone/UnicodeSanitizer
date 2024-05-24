# UnicodeSanitizer

UnicodeSanitizer는 파일명에 포함된 다양한 형태의 인코딩 문제를 해결하기 위한 Python 스크립트입니다. 한글 파일명 변환, URL 디코딩, 자모 분리 해제 기능 등을 제공합니다. 또한, 유니코드 정규화를 통해 파일명이나 폴더명이 find 명령어 또는 fzf(fuzzy finder)에서 정상적으로 검색되지 않는 문제를 효과적으로 해결합니다.

### 배경

macOS와 Windows에서 한글 처리 방식 차이로 인해 발생하는 문제를 간단히 해결하기 위해 이 스크립트를 만들었습니다.

## 기능

- 한글 파일명을 NFC(Normalization Form C) 형식으로 변환
- URL 인코딩된 파일명을 디코딩
- 자모가 분리된 파일명을 조합하여 올바른 파일명으로 변환
- 모든 옵션을 한 번에 실행하는 스마트 옵션

## 설치 방법

1. 이 리포지토리를 클론합니다:
    ```sh
    git clone https://github.com/yourusername/UnicodeSanitizer.git
    cd UnicodeSanitizer
    ```

2. (선택 사항) 가상 환경을 생성하고 활성화합니다:
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate  # Linux 또는 macOS
    .\myenv\Scripts\activate   # Windows
    ```

## 사용 방법

```sh
python3 sanitizer.py [옵션] [디렉토리 경로]
```

### 옵션

- `-a` : 모든 옵션을 순차적으로 실행
- `-k` : 한글 파일명을 NFC 형식으로 변환
- `-u` : URL 인코딩된 파일명을 디코딩
- `-f` : 자모 분리된 파일명을 올바른 파일명으로 변환
- `--debug` : 디버그 로그 생성

### 예시

디렉토리 내 모든 파일명을 변환하려면:
```sh
python3 sanitizer.py -a ~/Documents
```

특정 옵션을 사용하여 파일명을 변환하려면:
```sh
python3 sanitizer.py -k ~/Documents
python3 sanitizer.py -u ~/Documents
python3 sanitizer.py -f ~/Documents
```

디버그 로그를 생성하려면:
```sh
python3 sanitizer.py -a ~/Documents --debug
python3 sanitizer.py -k ~/Documents --debug
python3 sanitizer.py -u ~/Documents --debug
python3 sanitizer.py -f ~/Documents --debug
```

## 업데이트

UnicodeSanitizer 리포지토리 업데이트를 확인하는 것이 좋습니다!

```sh
cd UnicodeSanitizer
git status
```

변경 사항 가져오기:

```sh
git pull origin main
```

## 기여 방법

기여해주셔서 감사합니다! 이 프로젝트에 기여하시려면 아래 단계를 따라 주세요:

1. 이 리포지토리를 포크하세요
2. 기능 브랜치(micronzone 브랜치)를 생성하세요 (`git checkout -b micronzone/UnicodeSanitizer`)
3. 변경 사항을 커밋하세요 (`git commit -m 'Add some UnicodeSanitizer'`)
4. 브랜치에 푸시하세요 (`git push origin micronzone/UnicodeSanitizer`)
5. 풀 리퀘스트를 여세요

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
