# 기여 가이드 (Contributing Guide)

이 프로젝트는 안정적인 운영과 자동화된 버전 관리를 위해 엄격한 커밋 메시지 컨벤션 및 배포 프로세스를 따릅니다.

## 커밋 메시지 규약 (Commit Message Convention)

우리는 **Angular 커밋 메시지 규약**을 사용합니다. 이를 통해 [Python Semantic Release](https://python-semantic-release.readthedocs.io/)가 자동으로 버전 번호를 결정하고 변경 로그(Changelog)를 생성합니다.

### 형식 (Format)
모든 커밋 메시지는 **헤더(Header)**, **본문(Body)**, **바닥글(Footer)**로 구성됩니다.

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### 타입 (Types)
- **feat**: 새로운 기능 추가 (**Minor** 버전 업데이트 유발)
- **fix**: 버그 수정 (**Patch** 버전 업데이트 유발)
- **docs**: 문서 수정만 있는 경우
- **style**: 코드 의미에 영향을 주지 않는 수정 (화이트스페이스, 포맷팅 등)
- **refactor**: 버그 수정이나 기능 추가가 없는 코드 변경
- **perf**: 성능 개선을 위한 코드 변경
- **test**: 테스트 추가 또는 수정
- **build**: 빌드 시스템이나 외부 의존성에 영향을 주는 변경
- **ci**: CI 설정 파일 및 스크립트 수정
- **chore**: 소스 코드나 테스트 파일을 수정하지 않는 기타 변경

### 파괴적 변경 (Breaking Changes)
**Major** 버전 업데이트(예: 1.x.x -> 2.0.0)를 유발하려면, 커밋 메시지의 본문이나 바닥글 시작 부분에 `BREAKING CHANGE:` 문구를 포함해야 합니다.

## 릴리스 프로세스 (Release Process)

1. 기능 추가나 버그 수정은 별도의 브랜치(예: `feat/new-endpoint` 또는 `fix/api-error`)에서 작업합니다.
2. `master` 브랜치로 **Pull Request(PR)**를 생성합니다.
3. PR이 `master`에 머지되면 **GitHub Actions Release 워크플로우**가 자동으로 실행됩니다.
4. 워크플로우 수행 내용:
   - 마지막 태그 이후의 커밋 메시지 분석
   - 다음 버전 번호 결정
   - `pyproject.toml` 및 `__init__.py` 버전 업데이트
   - `CHANGELOG.md` 자동 갱신
   - 새로운 Git Tag 및 GitHub Release 생성
   - **PyPI**에 새로운 버전 배포

## 개발 환경 설정

의존성 관리를 위해 [uv](https://github.com/astral-sh/uv) 사용을 권장합니다.

```bash
# 의존성 설치 및 환경 동기화
uv sync

# 테스트 실행
uv run pytest
```