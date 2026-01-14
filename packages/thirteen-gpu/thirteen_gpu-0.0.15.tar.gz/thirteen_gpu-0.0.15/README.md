# Thirteen GPU Scheduler

분산 GPU 클러스터에서 머신러닝 작업을 자동으로 스케줄링하고 관리하는 시스템입니다.

## Features

- **자동 작업 분배**: 사용 가능한 GPU를 자동으로 감지하고 작업을 분배
- **멀티 워커 지원**: 여러 GPU 서버를 동시에 관리
- **실시간 대시보드**: 작업 상태 및 GPU 사용량 모니터링
- **Vast.ai 통합**: 클라우드 GPU 인스턴스 자동 관리
- **Slack 알림**: 작업 완료 시 알림 지원

## Installation

```bash
pip install thirteen_gpu
```

Vast.ai 지원이 필요한 경우:
```bash
pip install thirteen_gpu[vast]
```

## Usage

### Job Submit

```bash
submit --user [USERNAME] --project [PROJECT_NAME] --path /path/to/project
```

예시:
```bash
submit --user seilna --project my_project_test1 --path ~/Desktop/neural-quant
```

**옵션:**
- `--user`: 사용자 이름
- `--project`: 프로젝트 이름 (중복 불가)
- `--path`: 프로젝트 경로 (`config/runs/*.json` 형태의 설정 파일 필요)
- `--alarm`: 완료 시 Slack 알림 활성화

### Job Delete

```bash
delete --user [USERNAME] --project [PROJECT_NAME]
```

## Dashboard

웹 대시보드를 통해 작업 상태를 실시간으로 모니터링할 수 있습니다.

## Architecture

```
thirteen_gpu/
├── main.py          # 메인 스케줄러 루프
├── worker.py        # GPU 워커 관리
├── project.py       # 프로젝트 관리
├── job.py           # 작업 관리
├── ssh.py           # SSH 연결 관리
├── dashboard.py     # 웹 대시보드
├── submit.py        # 작업 제출 CLI
├── delete.py        # 작업 삭제 CLI
└── vast.py          # Vast.ai 통합
```

## Requirements

- Python >= 3.x
- fastapi
- paramiko
- uvicorn
- vastai-sdk (optional)
