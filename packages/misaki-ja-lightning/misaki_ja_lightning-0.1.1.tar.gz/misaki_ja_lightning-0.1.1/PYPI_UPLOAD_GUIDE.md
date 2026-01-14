# PyPI 업로드 가이드

이 가이드는 `misaki-ja-lightning`을 PyPI에 업로드하는 방법을 설명합니다.

## 1. 사전 준비

### 1.1 PyPI 계정 생성

1. [PyPI](https://pypi.org)에 회원가입
2. [Test PyPI](https://test.pypi.org)에도 회원가입 (테스트용)
3. 이메일 인증 완료

### 1.2 API 토큰 생성

1. PyPI에 로그인 후 [Account Settings](https://pypi.org/manage/account/) 이동
2. "API tokens" 섹션에서 "Add API token" 클릭
3. Token name 입력 (예: "misaki-ja-lightning-upload")
4. Scope를 "Entire account" 또는 프로젝트별로 설정
5. 생성된 토큰을 안전한 곳에 저장 (**다시 볼 수 없음!**)

### 1.3 필요한 도구 설치

```bash
pip install --upgrade pip build twine
```

## 2. 패키지 준비

### 2.1 버전 확인 및 수정

`setup.py`와 `pyproject.toml`, `__init__.py`의 버전이 일치하는지 확인:

```python
# misaki_ja_lightning/__init__.py
__version__ = "0.1.0"

# setup.py
version="0.1.0"

# pyproject.toml
version = "0.1.0"
```

### 2.2 메타데이터 업데이트

`setup.py`와 `pyproject.toml`에서 다음 정보를 업데이트:

- `author` / `author_email`: 본인 정보로 변경
- `url`: GitHub 저장소 URL
- `description`: 프로젝트 설명

## 3. 패키지 빌드

### 3.1 빌드 실행

프로젝트 루트 디렉토리에서:

```bash
cd /Users/lucas/kokoro-ja/misaki-ja-lightning

# 이전 빌드 결과물 삭제 (있다면)
rm -rf dist/ build/ *.egg-info

# 패키지 빌드
python -m build
```

빌드가 성공하면 `dist/` 디렉토리에 다음 파일들이 생성됩니다:
- `misaki_ja_lightning-0.1.0-py3-none-any.whl` (wheel 파일)
- `misaki_ja_lightning-0.1.0.tar.gz` (source distribution)

### 3.2 빌드 결과 확인

```bash
ls -lh dist/
```

## 4. Test PyPI에 업로드 (선택사항)

실제 PyPI에 올리기 전에 Test PyPI에서 테스트하는 것을 권장합니다.

```bash
python -m twine upload --repository testpypi dist/*
```

Username: `__token__`
Password: Test PyPI API 토큰 (pypi-AgE... 형식)

업로드 후 확인:
```bash
# 가상환경 생성 및 테스트
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Test PyPI에서 설치
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ misaki-ja-lightning

# 테스트
python -c "from misaki_ja_lightning import JAG2P; print('Success!')"

deactivate
```

## 5. PyPI에 업로드

### 5.1 업로드 실행

```bash
python -m twine upload dist/*
```

Username: `__token__`
Password: PyPI API 토큰 (pypi-AgE... 형식)

### 5.2 업로드 성공 확인

업로드가 성공하면 다음과 같은 메시지가 표시됩니다:

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading misaki_ja_lightning-0.1.0-py3-none-any.whl
Uploading misaki_ja_lightning-0.1.0.tar.gz

View at:
https://pypi.org/project/misaki-ja-lightning/0.1.0/
```

## 6. 설치 및 테스트

```bash
# 새 가상환경에서 테스트
python -m venv verify_env
source verify_env/bin/activate

# PyPI에서 설치
pip install misaki-ja-lightning

# 테스트
python example.py

deactivate
```

## 7. 문제 해결

### 7.1 일반적인 오류

**오류: "The user '...' isn't allowed to upload to project '...'"**
- 해결: 프로젝트 이름이 이미 존재합니다. `setup.py`에서 다른 이름으로 변경하세요.

**오류: "File already exists"**
- 해결: 이미 같은 버전이 업로드되어 있습니다. 버전을 올리세요 (예: 0.1.0 → 0.1.1).

**오류: "Invalid authentication credentials"**
- 해결: API 토큰이 올바른지 확인하고, username을 `__token__`으로 입력했는지 확인하세요.

### 7.2 .pypirc 설정 (선택사항)

반복적인 업로드를 위해 홈 디렉토리에 `~/.pypirc` 파일을 생성할 수 있습니다:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgE...your-token-here...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgE...your-test-token-here...
```

**보안 주의:** 이 파일에는 민감한 정보가 포함되므로 권한을 제한하세요:
```bash
chmod 600 ~/.pypirc
```

이후 업로드는 더 간단해집니다:
```bash
python -m twine upload dist/*
```

## 8. 버전 업데이트

새 버전을 배포하려면:

1. 코드 수정
2. 버전 업데이트:
   - `misaki_ja_lightning/__init__.py`
   - `setup.py`
   - `pyproject.toml`
3. CHANGELOG 작성 (선택사항)
4. 빌드 및 업로드:
   ```bash
   rm -rf dist/
   python -m build
   python -m twine upload dist/*
   ```

## 9. 추가 리소스

- [PyPI 공식 가이드](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine 문서](https://twine.readthedocs.io/)
- [Python Packaging User Guide](https://packaging.python.org/)

## 10. 체크리스트

업로드 전 최종 확인:

- [ ] 버전 번호가 모든 파일에서 일치하는가?
- [ ] README.md가 잘 작성되어 있는가?
- [ ] LICENSE 파일이 포함되어 있는가?
- [ ] 필수 의존성이 올바르게 명시되어 있는가?
- [ ] example.py가 정상 작동하는가?
- [ ] Test PyPI에서 테스트했는가? (선택사항)
- [ ] .gitignore에 dist/, build/ 등이 포함되어 있는가?

모든 항목을 확인한 후 업로드하세요!
