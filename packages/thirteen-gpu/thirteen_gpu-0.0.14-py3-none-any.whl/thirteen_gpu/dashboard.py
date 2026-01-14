import datetime
import json
import os
import re
import shlex
import subprocess
import multiprocessing
import threading  # multiprocessing 임포트
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from typing import List

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Request, Body, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

from thirteen_gpu.main import connect_worker, execute_by_threads
from thirteen_gpu.worker import Worker
from thirteen_gpu.vast_sdk import (
    create_vast_instances_from_offers,
    destroy_vast_instances,
    list_vast_instances,
    stop_vast_instances,
    start_vast_instances,
    reboot_vast_instances,
    search_vast_offers,
)


app = FastAPI()

# 짧은 TTL 캐시: Job Logs 모달 초기 로딩 체감 개선
_PROJECT_JOBS_CACHE: dict[tuple[str, str], dict] = {}
_PROJECT_JOBS_CACHE_TS: dict[tuple[str, str], float] = {}
_PROJECT_JOBS_CACHE_TTL_SEC = 5.0


class WorkerData(BaseModel):
    user_id: str
    vast_ids: str


@app.post(
    "/add_worker"
)  # 기존의 @app.get("/add_worker")를 @app.post("/add_worker")로 변경
def add_worker(data: WorkerData):
    print(f"User ID: {data.user_id}, Vast IDs: {data.vast_ids}")

    try:
        for vast_id in data.vast_ids.split():
            result = subprocess.run(
                f"python thirteen_gpu/add_new_worker.py --vast_id {vast_id} --user {data.user_id}",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"Worker {vast_id} added successfully")

        subprocess.run("pkill -f run_scheduler.py", shell=True)
        return {"message": "Worker가 성공적으로 추가되었습니다."}
    except subprocess.CalledProcessError as e:
        error_msg = f"Worker 추가 실패: {e.stderr if e.stderr else str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"Worker 추가 중 오류 발생: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/get_workers")
def get_workers(active_only: bool = False):
    """
    workers.json 내용을 반환
    active_only=True 이면 worker_pool_names.txt 에 있는 worker들만 반환
    """
    try:
        workers = json.loads(open("thirteen_gpu/workers.json").read())
    except Exception:
        workers = {}

    if active_only:
        try:
            pool_data = json.loads(open("thirteen_gpu/worker_pool_names.txt").read())
            active_ids = set()
            for user_workers in pool_data.values():
                if isinstance(user_workers, list):
                    active_ids.update(user_workers)
            
            workers = {k: v for k, v in workers.items() if k in active_ids}
        except Exception as e:
            print(f"worker_pool_names.txt 읽기 실패: {e}")
            # 실패 시 빈 딕셔너리 혹은 전체 반환? 
            # active_only 요청했는데 실패하면 필터링 실패 사실을 알리는게 맞지만,
            # 여기서는 편의상 빈 딕셔너리 반환하거나 에러 처리.
            # 일단 전체 worker 반환보다는 필터링 로직 에러이므로 그냥 진행
            pass

    return workers


@app.get("/vast_unadded_instances")
def vast_unadded_instances():
    """
    worker로 아직 등록되지 않은 Vast 인스턴스만 반환.
    기준: workers.json의 (ip, port) 쌍과 Vast instance의 (ssh_host, ssh_port) 비교.
    """
    try:
        workers = json.loads(open("thirteen_gpu/workers.json").read())
    except Exception:
        workers = {}

    existing = set()
    for w in workers.values():
        ip = w.get("ip")
        port = w.get("port")
        try:
            port = int(port) if port is not None else None
        except Exception:
            port = None
        if ip and port is not None:
            existing.add((ip, port))

    try:
        instances = list_vast_instances()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast 인스턴스 조회 실패: {e}")

    items = []
    for inst in instances:
        if not isinstance(inst, dict):
            continue
        ssh_host = inst.get("ssh_host")
        ssh_port = inst.get("ssh_port")
        try:
            ssh_port_i = int(ssh_port) if ssh_port is not None else None
        except Exception:
            ssh_port_i = None
        if not ssh_host or ssh_port_i is None:
            continue
        if (ssh_host, ssh_port_i) in existing:
            continue
        items.append(
            {
                "id": inst.get("id"),
                "label": inst.get("label"),
                "actual_status": inst.get("actual_status") or inst.get("status"),
                "gpu_name": inst.get("gpu_name"),
                "num_gpus": inst.get("num_gpus"),
                "dph_total": inst.get("dph_total"),
                "ssh_host": ssh_host,
                "ssh_port": ssh_port_i,
            }
        )

    return {"count": len(items), "instances": items}


class OwnerData(BaseModel):
    owner_id: str
    worker_id: str


@app.post("/set_owner")
def set_owner(data: OwnerData):
    try:
        print(f"{data=}")
        owner = data.owner_id
        worker_ids = data.worker_id.split()

        workers = json.loads(open("thirteen_gpu/workers.json").read())
        for worker_id in worker_ids:
            if worker_id in workers:
                workers[worker_id]["owner"] = owner
            else:
                raise HTTPException(
                    status_code=404, detail=f"Worker ID {worker_id} not found"
                )

        with open("thirteen_gpu/workers.json", "w") as f:
            json.dump(workers, f, indent=4)

        # owner 변경 이력을 디스크에 저장
        with open("thirteen_gpu/owner_change_log.txt", "a") as log_file:
            log_file.write(
                f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Owner 변경: {worker_ids} -> {owner}\n"
            )

        os.system("pkill -f run_scheduler.py")
        return {"message": "Owner 가 성공적으로 설정되었습니다."}
    except Exception as e:
        print(f"{e=}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/show_owner_change_log")
def show_owner_change_log():
    if not os.path.exists("thirteen_gpu/owner_change_log.txt"):
        return "No owner change log"

    with open("thirteen_gpu/owner_change_log.txt", "r") as log_file:
        log_lines = log_file.readlines()
        log_lines.reverse()
        log_content = "<br>".join(line.replace('"', "") for line in log_lines)
        log_content = log_content.replace("\n", "")
        log_content = log_content.replace("seilna", '<span style="color:red;">seilna</span>')
        log_content = log_content.replace("forybm", '<span style="color:green;">forybm</span>')
        log_content = log_content.replace("joohong", '<span style="color:blue;">joohong</span>')
        log_content = log_content.replace("lynch", '<span style="color:purple;">lynch</span>')
    return log_content


@app.post("/vast_on")
def vast_on(data: dict = Body(...)):
    user = data.get("user", "all")

    workers = json.loads(open("thirteen_gpu/workers.json").read())
    instances = json.loads(subprocess.check_output("vast show instances --raw", shell=True))

    if user == "all":
        target_workers = {k: v for k, v in workers.items() if k.startswith("v")}
    else:
        target_workers = {k: v for k, v in workers.items() if k.startswith("v") and v.get("owner") == user}

    started_instances = []
    for instance in instances:
        if instance["actual_status"] == "exited":
            ssh_host = instance.get("ssh_host")
            ssh_port = instance.get("ssh_port")

            for worker_name, worker_info in target_workers.items():
                if worker_info["ip"] == ssh_host and worker_info["port"] == ssh_port:
                    os.system(f"vast start instance {instance['id']}")
                    started_instances.append(f"{worker_name} (id: {instance['id']})")
                    print(f"Starting instance {instance['id']} ({worker_name}) for user {user}")
                    break

    if started_instances:
        return {
            "message": f"{user} 사용자의 {len(started_instances)}개 인스턴스 시작 완료: {', '.join(started_instances)}"
        }
    else:
        return {"message": f"{user} 사용자의 중지된 Vast 인스턴스가 없습니다."}


@app.post("/vast_off")
def vast_off(data: dict = Body(...)):
    user = data.get("user", "all")

    workers = json.loads(open("thirteen_gpu/workers.json").read())
    instances = json.loads(subprocess.check_output("vast show instances --raw", shell=True))

    if user == "all":
        target_workers = {k: v for k, v in workers.items() if k.startswith("v")}
    else:
        target_workers = {k: v for k, v in workers.items() if k.startswith("v") and v.get("owner") == user}

    stopped_instances = []
    for instance in instances:
        if instance["actual_status"] == "running":
            ssh_host = instance.get("ssh_host")
            ssh_port = instance.get("ssh_port")

            for worker_name, worker_info in target_workers.items():
                if worker_info["ip"] == ssh_host and worker_info["port"] == ssh_port:
                    os.system(f"vast stop instance {instance['id']}")
                    stopped_instances.append(f"{worker_name} (id: {instance['id']})")
                    print(f"Stopping instance {instance['id']} ({worker_name}) for user {user}")
                    break

    if stopped_instances:
        return {
            "message": f"{user} 사용자의 {len(stopped_instances)}개 인스턴스 중지 완료: {', '.join(stopped_instances)}"
        }
    else:
        return {"message": f"{user} 사용자의 실행 중인 Vast 인스턴스가 없습니다."}


@app.post("/vast_stop_schedule")
async def vast_stop_schedule():
    instances = json.loads(
        subprocess.check_output("vast show instances --raw", shell=True)
    )

    for instance in instances:
        if instance["actual_status"] == "exited":
            os.system(f"vast stop instance {instance['id']}")

            print(f"Stopping instance {instance['id']}")
    return {"message": "Stop Schduling Done"}


class ProjectData(BaseModel):
    project_name: str
    user: str


class VastOfferSearchData(BaseModel):
    n_gpus: int
    cpu_cores_min: int
    cpu_ram_gb_min: int
    dlperf_min: int
    gpu_type: str = "4090"
    limit: int = 200


class VastCreateInstancesData(BaseModel):
    offer_ids: List[int] = Field(default_factory=list)
    disk_gb: int
    user: str


class VastDeleteInstancesData(BaseModel):
    instance_ids: List[int] = Field(default_factory=list)
    confirm: bool = False


class VastStopInstancesData(BaseModel):
    instance_ids: List[int] = Field(default_factory=list)
    confirm: bool = False


class VastRebootInstancesData(BaseModel):
    instance_ids: List[int] = Field(default_factory=list)
    confirm: bool = False


class VastStartInstancesData(BaseModel):
    instance_ids: List[int] = Field(default_factory=list)
    confirm: bool = False


@app.post("/delete_project")
def delete_project(data: ProjectData):
    project_path = f"/home/seilna/tmux_workspace/{data.project_name}"

    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail=f"프로젝트 폴더 {data.project_name}가 존재하지 않습니다.")

    try:
        os.system(f"rm -rf {project_path}")
        return {"message": f"프로젝트 {data.project_name} 폴더가 성공적으로 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"폴더 삭제 중 오류가 발생했습니다: {e}")

# 아래 worker에서 파일 삭제 작업을 병렬로 실행하기 위한 별도 함수
def process_worker(args):
    worker_id, project = args
    # worker_id에 따라 홈폴더 경로를 다르게 설정
    if worker_id in ["s1", "s2", "s3"]:
        home_dir = "/home/thirteen"
    elif worker_id.startswith("v"):
        home_dir = "/root"
    else:
        home_dir = "/home/thirteen"  # 기본값

    remote_command = (
        "bash -c '"
        "count=0; "
        'deleted=""; '
        f"for f in {home_dir}/{{project}}/*.status; do "
        'if [ -f "$f" ]; then '
        'if grep -q failed "$f"; then '
        'rm -f "$f"; '
        'deleted="$deleted|$f"; '
        "count=$((count+1)); "
        "fi; "
        "fi; "
        "done; "
        'echo "$count|||$deleted"\''
    ).format(project=project)

    try:
        output = subprocess.check_output(
            ["ssh", "-o", "BatchMode=yes", f"{worker_id}", remote_command],
            stderr=subprocess.STDOUT
        )
        output_str = output.decode().strip()
        output_str = output_str.split("fun!\n")[-1]
        if "|||" in output_str:
            count_part, deleted_part = output_str.split("|||", 1)
        else:
            count_part, deleted_part = output_str, ""
        removed = int(count_part)
        files_deleted = [f for f in deleted_part.split("|") if f.strip() != ""]
        return (worker_id, {"removed": removed, "files": files_deleted})
    except subprocess.CalledProcessError as e:
        error_msg = e.output.decode()
        # 비밀번호가 요구되면 스킵하도록 처리
        if "password" in error_msg.lower() or "permission denied" in error_msg.lower():
            return (worker_id, {"skipped": "비밀번호 요구로 인해 스킵됨"})
        return (worker_id, {"error": error_msg})
    except Exception as e:
        return (worker_id, {"error": str(e)})

@app.post("/rerun_failed_jobs")
def rerun_failed_jobs(data: ProjectData):
    project_name = data.project_name
    user = data.user

    workers = json.loads(open("thirteen_gpu/worker_pool_names.txt").read())
    worker_ids = workers[user]

    total_removed = 0
    details = {}

    # worker id와 프로젝트 이름을 tuple로 구성
    worker_list = [(worker_id, project_name) for worker_id in worker_ids]

    # multiprocessing을 사용해 각 worker에 대해 병렬 실행
    print(f"failed job 의 status 파일 삭제 시작")
    with multiprocessing.Pool() as pool:
        results = pool.map(process_worker, worker_list)

    for worker_id, result in results:
        if "removed" in result:
            total_removed += result["removed"]
            details[worker_id] = result
            print(f"Worker {worker_id}: 삭제된 파일 수 {result['removed']}, 파일 목록: {result.get('files', [])}")
        else:
            details[worker_id] = result
            print(f"Worker {worker_id} 작업 중 오류 발생: {result.get('error')}")

    return {
        "message": f"모든 remote worker에서 실패한 상태 파일 총 {total_removed}개 삭제됨",
        "details": details
    }


_SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def _ensure_safe_name(name: str, field: str) -> str:
    if not name or not isinstance(name, str) or not _SAFE_NAME_RE.match(name):
        raise HTTPException(status_code=400, detail=f"{field} 값이 올바르지 않습니다.")
    return name


def _read_json_file_safely(path: str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def _get_project_user_from_status(project_name: str) -> str | None:
    status = _read_json_file_safely("thirteen_gpu/status.json")
    if not status or project_name not in status:
        return None
    return (status.get(project_name) or {}).get("user")


def _get_active_worker_ids_for_user(user: str) -> list[str]:
    pool = _read_json_file_safely("thirteen_gpu/worker_pool_names.txt")
    if isinstance(pool, dict):
        ids = pool.get(user)
        if isinstance(ids, list) and ids:
            return [str(x) for x in ids]

    workers_info = _read_json_file_safely("thirteen_gpu/workers.json") or {}
    ids = [wid for wid, info in workers_info.items() if (info or {}).get("owner") == user]
    return ids[:50]


def _connect_worker_from_workers_json(worker_id: str) -> Worker:
    workers_info = _read_json_file_safely("thirteen_gpu/workers.json") or {}
    info = workers_info.get(worker_id)
    if not info:
        raise HTTPException(status_code=404, detail=f"Worker ID {worker_id} not found")
    if "owner" not in info:
        info["owner"] = "unknown"
    return Worker(**info)


def _get_local_project_jobs_meta(project_name: str) -> list[dict]:
    """
    로컬 tmux_workspace/{project} 의 config/runs/*.json 을 기준으로 job 메타를 만든다.
    (Project 클래스와 동일한 규칙: job_{project_name}_{config_idx})

    반환:
      [{ job_name, config_idx, exp_name }, ...]
    """
    base = os.path.join(os.path.expanduser("~"), "tmux_workspace", project_name)
    runs_dir = os.path.join(base, "config", "runs")
    if not os.path.isdir(runs_dir):
        return []
    try:
        files = [f for f in os.listdir(runs_dir) if f.endswith(".json")]
    except Exception:
        return []

    items = []
    for fn in sorted(files):
        config_idx = fn.split(".json")[0]
        job_name = f"job_{project_name}_{config_idx}"
        exp_name = None
        try:
            path = os.path.join(runs_dir, fn)
            cfg = json.loads(open(path).read())
            exp_name = (cfg.get("general") or {}).get("exp_name")
        except Exception:
            exp_name = None

        items.append({"job_name": job_name, "config_idx": config_idx, "exp_name": exp_name})
    return items


def _fetch_project_job_statuses_from_worker(worker: Worker, project_name: str) -> list[dict]:
    proj_dir = f"{worker.home}/{project_name}"
    script = (
        f"cd {shlex.quote(proj_dir)} 2>/dev/null || exit 0; "
        "for s in *.status; do "
        "[ -f \"$s\" ] || continue; "
        "j=\"${s%.status}\"; "
        "st=$(tail -n 1 \"$s\" 2>/dev/null | tr -d '\\r'); "
        "m=$(stat -c %Y \"$s\" 2>/dev/null || echo 0); "
        "le=0; [ -f \"$j.log\" ] && le=1; "
        "ls=$(stat -c %s \"$j.log\" 2>/dev/null || echo 0); "
        "echo \"$j|||$st|||$m|||$le|||$ls\"; "
        "done"
    )
    cmd = f"bash -lc {shlex.quote(script)}"
    out = worker.ssh.ssh_exec_command(cmd).strip()
    if not out:
        return []
    rows = []
    for line in out.split("\n"):
        parts = line.split("|||")
        if len(parts) != 5:
            continue
        job_name, st, mtime_s, log_exists_s, log_size_s = parts
        try:
            mtime = int(mtime_s)
        except Exception:
            mtime = 0
        try:
            log_exists = bool(int(log_exists_s))
        except Exception:
            log_exists = False
        try:
            log_size = int(log_size_s)
        except Exception:
            log_size = 0
        rows.append(
            {
                "job_name": job_name,
                "status": (st or "").strip(),
                "status_mtime": mtime,
                "log_exists": log_exists,
                "log_size": log_size,
            }
        )
    return rows


@app.get("/project_jobs")
def project_jobs(
    project_name: str = Query(...),
    user: str | None = Query(default=None),
    force: bool = Query(default=False),
):
    """
    프로젝트의 전체 job 목록 + status 를 반환한다.
    - 로컬 workspace에서 예상 job 목록을 만든 뒤 (가능하면)
    - worker들의 *.status 를 스캔해서 status / log 정보를 덮어쓴다.
    """
    project_name = _ensure_safe_name(project_name, "project_name")
    if user is None:
        user = _get_project_user_from_status(project_name)
    if not user:
        raise HTTPException(status_code=404, detail="프로젝트 user 정보를 찾을 수 없습니다.")

    cache_key = (project_name, user)
    now = time.time()
    if not force:
        ts = _PROJECT_JOBS_CACHE_TS.get(cache_key)
        if ts is not None and (now - ts) < _PROJECT_JOBS_CACHE_TTL_SEC:
            cached = _PROJECT_JOBS_CACHE.get(cache_key)
            if cached:
                return cached

    expected = _get_local_project_jobs_meta(project_name)
    job_map: dict[str, dict] = {}
    for meta in expected:
        jn = meta.get("job_name")
        if not jn:
            continue
        job_map[jn] = {
            "project_name": project_name,
            "job_name": jn,
            "exp_name": meta.get("exp_name"),
            "status": "pending",
            "worker_id": None,
            "status_mtime": 0,
            "log_exists": False,
            "log_size": 0,
        }

    worker_ids = _get_active_worker_ids_for_user(user)
    errors = []

    def fetch_rows(worker_id: str):
        worker = _connect_worker_from_workers_json(worker_id)
        rows = _fetch_project_job_statuses_from_worker(worker, project_name)
        return worker_id, rows

    # SSH 연결/스캔은 병렬화(최대 12개)해서 대기시간 단축
    if worker_ids:
        max_workers = min(12, max(1, len(worker_ids)))
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futs = {ex.submit(fetch_rows, wid): wid for wid in worker_ids}
            for fut in as_completed(futs):
                wid = futs[fut]
                try:
                    worker_id, rows = fut.result()
                except Exception as e:
                    errors.append({"worker_id": wid, "error": str(e)})
                    continue

                for r in rows:
                    jn = r.get("job_name")
                    if not jn:
                        continue
                    if jn not in job_map:
                        job_map[jn] = {
                            "project_name": project_name,
                            "job_name": jn,
                            "exp_name": None,
                            "status": "pending",
                            "worker_id": None,
                            "status_mtime": 0,
                            "log_exists": False,
                            "log_size": 0,
                        }
                    # 가장 최근 mtime 정보를 우선
                    if int(r.get("status_mtime") or 0) >= int(job_map[jn].get("status_mtime") or 0):
                        job_map[jn]["status"] = r.get("status") or job_map[jn]["status"]
                        job_map[jn]["status_mtime"] = int(r.get("status_mtime") or 0)
                        job_map[jn]["worker_id"] = worker_id
                        job_map[jn]["log_exists"] = bool(r.get("log_exists"))
                        job_map[jn]["log_size"] = int(r.get("log_size") or 0)

    items = list(job_map.values())
    items.sort(key=lambda x: (x.get("status") == "pending", -(x.get("status_mtime") or 0), x.get("job_name") or ""))

    # count by status
    counts = {}
    for it in items:
        st = it.get("status") or "unknown"
        counts[st] = counts.get(st, 0) + 1

    resp = {
        "project_name": project_name,
        "user": user,
        "count": len(items),
        "counts": counts,
        "items": items,
        "errors": errors,
    }
    _PROJECT_JOBS_CACHE[cache_key] = resp
    _PROJECT_JOBS_CACHE_TS[cache_key] = now
    return resp


@app.get("/project_failed_jobs")
def project_failed_jobs(
    project_name: str = Query(...),
    user: str | None = Query(default=None),
):
    project_name = _ensure_safe_name(project_name, "project_name")
    if user is None:
        user = _get_project_user_from_status(project_name)
    if not user:
        raise HTTPException(status_code=404, detail="프로젝트 user 정보를 찾을 수 없습니다.")

    worker_ids = _get_active_worker_ids_for_user(user)
    if not worker_ids:
        return {"project_name": project_name, "user": user, "count": 0, "items": [], "errors": []}

    items = []
    errors = []
    for worker_id in worker_ids:
        try:
            worker = _connect_worker_from_workers_json(worker_id)
        except Exception as e:
            errors.append({"worker_id": worker_id, "error": str(e)})
            continue

        proj_dir = f"{worker.home}/{project_name}"
        script = (
            f"cd {shlex.quote(proj_dir)} 2>/dev/null || exit 0; "
            "for s in *.status; do "
            "[ -f \"$s\" ] || continue; "
            "if tail -n 1 \"$s\" | grep -q failed; then "
            "j=\"${s%.status}\"; "
            "m=$(stat -c %Y \"$s\" 2>/dev/null || echo 0); "
            "le=0; [ -f \"$j.log\" ] && le=1; "
            "ls=$(stat -c %s \"$j.log\" 2>/dev/null || echo 0); "
            "echo \"$j|||$m|||$le|||$ls\"; "
            "fi; "
            "done"
        )
        cmd = f"bash -lc {shlex.quote(script)}"
        try:
            out = worker.ssh.ssh_exec_command(cmd).strip()
        except Exception as e:
            errors.append({"worker_id": worker_id, "error": str(e)})
            continue

        if not out:
            continue

        for line in out.split("\n"):
            parts = line.split("|||")
            if len(parts) != 4:
                continue
            job_name, mtime_s, log_exists_s, log_size_s = parts
            try:
                mtime = int(mtime_s)
            except Exception:
                mtime = 0
            try:
                log_exists = bool(int(log_exists_s))
            except Exception:
                log_exists = False
            try:
                log_size = int(log_size_s)
            except Exception:
                log_size = 0
            items.append(
                {
                    "worker_id": worker_id,
                    "project_name": project_name,
                    "job_name": job_name,
                    "status_mtime": mtime,
                    "log_exists": log_exists,
                    "log_size": log_size,
                }
            )

    items.sort(key=lambda x: x.get("status_mtime", 0), reverse=True)
    return {"project_name": project_name, "user": user, "count": len(items), "items": items, "errors": errors}


@app.get("/project_job_log")
def project_job_log(
    project_name: str = Query(...),
    worker_id: str = Query(...),
    job_name: str = Query(...),
    max_bytes: int = Query(default=50_000_000, ge=1, le=50_000_000),
):
    project_name = _ensure_safe_name(project_name, "project_name")
    worker_id = _ensure_safe_name(worker_id, "worker_id")
    job_name = _ensure_safe_name(job_name, "job_name")

    worker = _connect_worker_from_workers_json(worker_id)
    proj_dir = f"{worker.home}/{project_name}"
    log_path = f"{proj_dir}/{job_name}.log"

    size_script = f"stat -c %s {shlex.quote(log_path)} 2>/dev/null || echo -1"
    size_out = worker.ssh.ssh_exec_command(f"bash -lc {shlex.quote(size_script)}").strip()
    try:
        size = int(size_out)
    except Exception:
        size = -1
    if size < 0:
        raise HTTPException(status_code=404, detail="log 파일이 존재하지 않습니다.")
    if size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"log 파일이 너무 큽니다. size={size} bytes (max_bytes={max_bytes})",
        )

    cat_script = f"cat {shlex.quote(log_path)}"
    content = worker.ssh.ssh_exec_command(f"bash -lc {shlex.quote(cat_script)}")
    return PlainTextResponse(content=content or "", media_type="text/plain; charset=utf-8")


@app.get("/get_billing")
def get_billing():
    import subprocess, json
    try:
        instances = json.loads(subprocess.check_output("vast show instances --raw", shell=True))
        vast_price = sum(float(i["dph_total"]) for i in instances if i["actual_status"] == "running")
    except Exception as e:
        return {"price": 0.0, "error": str(e)}
    return {"price": vast_price}


@app.post("/vast_search_offers")
def vast_search_offers(data: VastOfferSearchData):
    allowed_n_gpus = {1, 2, 4, 8}
    allowed_cpu_cores = {64, 96, 128, 192, 256}
    allowed_cpu_ram_gb = {128, 256, 384, 512}
    allowed_dlperf = {200, 250, 300}
    gpu_type_map = {
        "4090": "RTX 4090",
        "5090": "RTX 5090",
        "5090D": "RTX 5090D",
    }

    if data.n_gpus not in allowed_n_gpus:
        raise HTTPException(status_code=400, detail="n_gpus 값이 올바르지 않습니다.")
    if data.cpu_cores_min not in allowed_cpu_cores:
        raise HTTPException(status_code=400, detail="cpu_cores_min 값이 올바르지 않습니다.")
    if data.cpu_ram_gb_min not in allowed_cpu_ram_gb:
        raise HTTPException(status_code=400, detail="cpu_ram_gb_min 값이 올바르지 않습니다.")
    if data.dlperf_min not in allowed_dlperf:
        raise HTTPException(status_code=400, detail="dlperf_min 값이 올바르지 않습니다.")
    if data.gpu_type not in gpu_type_map:
        raise HTTPException(status_code=400, detail="gpu_type 값이 올바르지 않습니다.")

    gpu_name = gpu_type_map[data.gpu_type]
    limit = max(1, min(int(data.limit), 500))

    # Vast query: cpu_ram은 GiB 단위로 동작하는 것으로 보임.
    query = (
        f'gpu_name="{gpu_name}" '
        f"rentable=true "
        f"num_gpus>={data.n_gpus} "
        f"cpu_cores>={data.cpu_cores_min} "
        f"cpu_ram>={data.cpu_ram_gb_min} "
        f"dlperf>={data.dlperf_min}"
    )

    try:
        offers = search_vast_offers(query, limit=limit, order="dph_total")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast 검색 실패: {e}")

    def norm_cpu_ram_gb(v):
        if v is None:
            return None
        try:
            v = float(v)
        except Exception:
            return None
        # offer 응답에서는 MiB처럼 큰 값으로 오기도 함 (예: 128500)
        return v / 1024.0 if v > 4096 else v

    filtered = []
    for o in offers:
        if o.get("gpu_name") != gpu_name:
            continue
        if o.get("num_gpus") != data.n_gpus:
            continue
        cpu_ram_gb = norm_cpu_ram_gb(o.get("cpu_ram"))
        if cpu_ram_gb is None or cpu_ram_gb < data.cpu_ram_gb_min:
            continue
        if (o.get("cpu_cores") or 0) < data.cpu_cores_min:
            continue
        dlperf = o.get("dlperf") or 0
        if dlperf < data.dlperf_min:
            continue

        try:
            dlperf_int = int(round(float(dlperf)))
        except Exception:
            dlperf_int = None

        filtered.append(
            {
                "id": o.get("id"),
                "gpu_name": o.get("gpu_name"),
                "num_gpus": o.get("num_gpus"),
                "dph_total": o.get("dph_total"),
                "dlperf": dlperf_int,
                "cpu_cores": o.get("cpu_cores"),
                "cpu_ram_gb": round(cpu_ram_gb, 1) if cpu_ram_gb is not None else None,
                "inet_up": o.get("inet_up"),
                "inet_down": o.get("inet_down"),
                "reliability2": o.get("reliability2"),
                "geolocation": o.get("geolocation"),
            }
        )

    return {"query": query, "count": len(filtered), "offers": filtered}


@app.post("/vast_create_instances")
def vast_create_instances(data: VastCreateInstancesData):
    allowed_users = {"seil", "forybm", "jh", "joohong"}
    if data.user not in allowed_users:
        raise HTTPException(status_code=400, detail="user 값이 올바르지 않습니다.")
    if not data.offer_ids:
        raise HTTPException(status_code=400, detail="offer_ids가 비어있습니다.")

    disk_gb = int(data.disk_gb)
    if disk_gb < 10 or disk_gb > 2048:
        raise HTTPException(status_code=400, detail="disk_gb 범위가 올바르지 않습니다.")

    try:
        resp = create_vast_instances_from_offers(
            [int(x) for x in data.offer_ids],
            disk_gb=disk_gb,
            user_tag=data.user,
            template_name="thirteen",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast create 실패: {e}")

    return resp


@app.get("/vast_list_instances")
def vast_list_instances(user: str = "all", status: str = "all"):
    allowed_users = {"all", "seil", "forybm", "jh", "joohong"}
    allowed_status = {"all", "running", "not_running"}
    if user not in allowed_users:
        raise HTTPException(status_code=400, detail="user 값이 올바르지 않습니다.")
    if status not in allowed_status:
        raise HTTPException(status_code=400, detail="status 값이 올바르지 않습니다.")

    try:
        instances = list_vast_instances()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast 인스턴스 조회 실패: {e}")

    def norm(inst):
        return {
            "id": inst.get("id"),
            "label": inst.get("label"),
            "owner": None,
            "actual_status": inst.get("actual_status") or inst.get("status"),
            "gpu_name": inst.get("gpu_name"),
            "num_gpus": inst.get("num_gpus"),
            "dph_total": inst.get("dph_total"),
            "ssh_host": inst.get("ssh_host"),
            "ssh_port": inst.get("ssh_port"),
            "worker_id": None,
            "n_running_jobs": None,
            "total_available_n_jobs": None,
        }

    # worker_id 매핑: (ssh_host, ssh_port) -> workers.json key (예: v297)
    try:
        workers_info = json.loads(open("thirteen_gpu/workers.json").read())
    except Exception:
        workers_info = {}

    addr_to_worker_id = {}
    for wid, info in (workers_info or {}).items():
        if not isinstance(info, dict):
            continue
        ip = info.get("ip")
        port = info.get("port")
        try:
            port = int(port) if port is not None else None
        except Exception:
            port = None
        if ip and port is not None:
            addr_to_worker_id[(ip, port)] = wid

    # total_available_n_jobs 계산용: user_setup.json max_jobs_per_gpus
    try:
        user_setup = json.loads(open("thirteen_gpu/user_setup.json").read())
    except Exception:
        user_setup = {}
    max_jobs_per_gpus = (user_setup or {}).get("max_jobs_per_gpus", {}) or {}

    filtered = []
    for inst in instances:
        if not isinstance(inst, dict):
            continue
        label = inst.get("label")
        st = inst.get("actual_status") or inst.get("status")
        if user != "all" and label != user:
            continue
        if status == "running" and st != "running":
            continue
        if status == "not_running" and st == "running":
            continue
        row = norm(inst)

        # worker_id 매핑 + total slot 계산(ssh 없이)
        host = row.get("ssh_host")
        port = row.get("ssh_port")
        try:
            port_i = int(port) if port is not None else None
        except Exception:
            port_i = None

        wid = addr_to_worker_id.get((host, port_i)) if host and port_i is not None else None
        row["worker_id"] = wid

        if wid and wid in workers_info:
            w = workers_info[wid] or {}
            owner = (w.get("owner") or "unknown")
            row["owner"] = owner
            try:
                n_gpus = int(w.get("n_gpus") or 0)
            except Exception:
                n_gpus = 0
            try:
                max_jobs = int(max_jobs_per_gpus.get(owner, 2))
            except Exception:
                max_jobs = 2
            row["total_available_n_jobs"] = max(0, n_gpus * max_jobs)

        filtered.append(row)

    # n_running_jobs: tmux session 기반으로 계산 (gpu* 세션만 카운트)
    running_worker_ids = sorted(
        {
            r.get("worker_id")
            for r in filtered
            if r.get("worker_id") and r.get("actual_status") == "running"
        }
    )

    n_running_by_worker = {}
    job_errors = []

    def _count_tmux_jobs(wid: str):
        info = workers_info.get(wid) or {}
        ip = info.get("ip")
        port = info.get("port")
        user_ = info.get("user")
        if not ip or not port or not user_:
            n_running_by_worker[wid] = None
            return
        try:
            port_i = int(port)
        except Exception:
            n_running_by_worker[wid] = None
            return

        try:
            from thirteen_gpu.ssh import SSH

            ssh = SSH(ip, port_i, user_)
            # tmux 세션명 규칙: gpu{gpu_id}_{job_name}
            # NOTE: bash -lc 인용 문제가 있어서, 원시 세션 목록을 받아서 파이썬에서 카운트한다.
            out = ssh.ssh_exec_command("tmux ls 2>/dev/null | cut -d ':' -f 1").strip()
            sessions = [s.strip() for s in out.split("\n") if s.strip()]
            n = sum(1 for s in sessions if s.startswith("gpu") and "_" in s)
            n_running_by_worker[wid] = n
        except Exception as e:
            n_running_by_worker[wid] = None
            job_errors.append({"worker_id": wid, "error": str(e)})

    threads = []
    for wid in running_worker_ids:
        t = threading.Thread(target=_count_tmux_jobs, args=(wid,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    for r in filtered:
        wid = r.get("worker_id")
        st = r.get("actual_status")
        if not wid:
            r["n_running_jobs"] = None
        elif st != "running":
            r["n_running_jobs"] = 0
        else:
            r["n_running_jobs"] = n_running_by_worker.get(wid)

    return {
        "user": user,
        "status": status,
        "count": len(filtered),
        "instances": filtered,
        "job_count_errors": job_errors,
    }


@app.post("/vast_delete_instances")
def vast_delete_instances(data: VastDeleteInstancesData):
    if not data.confirm:
        raise HTTPException(status_code=400, detail="confirm=true 가 필요합니다.")
    if not data.instance_ids:
        raise HTTPException(status_code=400, detail="instance_ids가 비어있습니다.")

    try:
        resp = destroy_vast_instances([int(x) for x in data.instance_ids])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast 삭제 실패: {e}")
    return resp


@app.post("/vast_stop_instances")
def vast_stop_instances(data: VastStopInstancesData):
    if not data.confirm:
        raise HTTPException(status_code=400, detail="confirm=true 가 필요합니다.")
    if not data.instance_ids:
        raise HTTPException(status_code=400, detail="instance_ids가 비어있습니다.")

    try:
        resp = stop_vast_instances([int(x) for x in data.instance_ids])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast stop 실패: {e}")
    return resp


@app.post("/vast_start_instances")
def vast_start_instances(data: VastStartInstancesData):
    if not data.confirm:
        raise HTTPException(status_code=400, detail="confirm=true 가 필요합니다.")
    if not data.instance_ids:
        raise HTTPException(status_code=400, detail="instance_ids가 비어있습니다.")

    try:
        resp = start_vast_instances([int(x) for x in data.instance_ids])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast start 실패: {e}")
    return resp


@app.post("/vast_reboot_instances")
def vast_reboot_instances(data: VastRebootInstancesData):
    if not data.confirm:
        raise HTTPException(status_code=400, detail="confirm=true 가 필요합니다.")
    if not data.instance_ids:
        raise HTTPException(status_code=400, detail="instance_ids가 비어있습니다.")

    try:
        resp = reboot_vast_instances([int(x) for x in data.instance_ids])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vast reboot 실패: {e}")
    return resp


@app.post("/set_njobs_per_gpu")
def set_njobs_per_gpu(data: dict = Body(...)):
    user = data.get('user')
    n = data.get('n')
    if not user or not isinstance(n, int):
        return {"message": "user와 n을 올바르게 입력하세요."}
    try:
        import json
        path = 'thirteen_gpu/user_setup.json'
        try:
            with open(path) as f:
                user_setup = json.load(f)
        except Exception:
            user_setup = {}
        if 'max_jobs_per_gpus' not in user_setup:
            user_setup['max_jobs_per_gpus'] = {}
        user_setup['max_jobs_per_gpus'][user] = n
        with open(path, 'w') as f:
            json.dump(user_setup, f, indent=2, ensure_ascii=False)
        os.system('pkill -f run_scheduler.py')
        return {"message": f"{user}의 N jobs per GPU가 {n}으로 변경되었습니다."}
    except Exception as e:
        return {"message": f"설정 변경 실패: {e}"}

@app.get("/")
def read_root():

    scheduler_off = False
    worker_pool_names = open("thirteen_gpu/worker_pool_names.txt").read()
    available_job_slots = open("thirteen_gpu/available_job_slots.txt").read().strip()

    # get last update time of `status.json`
    last_update = os.path.getmtime("thirteen_gpu/status.json")
    last_update = datetime.datetime.fromtimestamp(last_update) + datetime.timedelta(
        hours=9
    )

    # if `last_update` not updated for 1 hour, set it to `None`
    if datetime.datetime.now() + datetime.timedelta(
        hours=9
    ) - last_update > datetime.timedelta(minutes=5):
        scheduler_off = True

    last_update_before = (
        datetime.datetime.now() + datetime.timedelta(hours=9) - last_update
    )
    last_update = last_update.strftime("%Y-%m-%d %H:%M:%S")

    status = json.load(open("thirteen_gpu/status.json"))
    text = "<a href='http://54.180.160.135:2014/'>GPU Status</a> <br>"
    text += "<a href='http://54.180.160.135:2015'>Task 현황</a> <br>"
    # Before ss.mm seconds format
    # microseconds
    if scheduler_off:
        text += f"<h3> Scheduler is off, Last Update: Before {last_update_before.seconds}.{str(last_update_before.microseconds)[:2]} seconds </h3>"
    else:
        text += f"<h3> Last Update: Before {last_update_before.seconds}.{str(last_update_before.microseconds)[:2]} seconds </h3>"

    text += f"<h3> Active Workers : {worker_pool_names} </h3>"
    text += f"<h3> Job Slots: {available_job_slots} </h3>"

    projects = []
    for project_name, project_status in status.items():
        user = project_status["user"]
        submit_at = project_status["submit_at"]

        status_info = [(status_name, status_count) for status_name, status_count in project_status["status"].items()]

        projects.append((project_name, user, submit_at, status_info))

    projects = sorted(projects, key=lambda x: x[2], reverse=True)

    # 완료된 프로젝트 목록 미리 로드
    try:
        with open("thirteen_gpu/completed_projects.json", "r") as f:
            completed_projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        completed_projects = []

    text += """
        <style>
            .dashboard-container {
                display: flex;
                gap: 30px;
                align-items: flex-start;
            }
            .projects-section {
                flex: 1;
                min-width: 0;
            }
            .completed-section {
                flex: 1;
                min-width: 0;
            }
            .section-title {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 15px;
                color: #333;
                padding-bottom: 8px;
                border-bottom: 2px solid #1976d2;
            }
            .section-title.completed {
                border-bottom-color: #4CAF50;
            }
            .project-card {
                background: white;
                border: 1px solid #ddd;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 4px;
                padding: 12px 15px;
                margin-bottom: 10px;
            }
            .card-header {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 6px;
                color: #333;
            }
            .card-meta {
                font-size: 0.85em;
                color: #666;
                margin-bottom: 8px;
            }
            .user-badge {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 0.85em;
                font-weight: 500;
                color: white;
                margin-right: 8px;
            }
            .user-seilna { background-color: #29b6f6; }
            .user-forybm { background-color: #fbc02d; color: #333; }
            .user-joohong { background-color: #ff6f00; }
            .user-lynch { background-color: #8e24aa; }
            .card-status {
                margin-bottom: 10px;
                line-height: 1.4;
                font-size: 0.9em;
            }
            .card-footer button {
                margin-right: 6px;
                padding: 5px 10px;
                border: 1px solid #ddd;
                border-radius: 3px;
                cursor: pointer;
                font-size: 0.85em;
                background-color: #f5f5f5;
                color: #666;
            }
            .card-footer button:hover {
                background-color: #e0e0e0;
            }
            .completed-card {
                background: #f9fff9;
                border: 1px solid #c8e6c9;
                box-shadow: 0 2px 4px rgba(0,0,0,0.08);
                border-radius: 4px;
                padding: 12px 15px;
                margin-bottom: 10px;
            }
            .completed-card .card-header {
                font-size: 1.1em;
                font-weight: bold;
                margin-bottom: 6px;
                color: #2e7d32;
            }
            .completed-card .card-meta {
                font-size: 0.85em;
                color: #666;
                margin-bottom: 6px;
            }
            .completed-card .card-status {
                font-size: 0.85em;
                color: #555;
            }
            .completed-badge {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 0.75em;
                background-color: #4CAF50;
                color: white;
                margin-left: 8px;
            }
        </style>
    """

    # 두 섹션을 나란히 배치하는 컨테이너 시작
    text += '<div class="dashboard-container">'
    
    # 왼쪽: 진행 중인 프로젝트 섹션
    text += '<div class="projects-section">'
    text += '<div class="section-title">🚀 진행 중인 프로젝트</div>'

    for project_name, user, submit_at, status_info in projects:
        status_text = ", ".join([f"{status_name}: {status_count}" for status_name, status_count in status_info])

        text += f"""
            <div class="project-card">
                <div class="card-header">{project_name}</div>
                <div class="card-meta">
                    <span class="user-badge user-{user}">{user}</span>
                    <span>Submitted: {submit_at}</span>
                </div>
                <div class="card-status">{status_text}</div>
                <div class="card-footer">
                    <button onclick="deleteProject('{project_name}', '{user}')">Delete</button>
                    <button onclick="rerunFailedJobs('{project_name}', '{user}')">Rerun Failed Jobs</button>
                    <button onclick="viewFailedLogs('{project_name}', '{user}')">Job 로그 조회</button>
                </div>
            </div>
        """

    if len(projects) == 0:
        text += "<div style='padding: 20px; color: #666;'>No projects</div>"
    
    text += '</div>'  # projects-section 닫기

    # 오른쪽: 최근 완료된 프로젝트 섹션
    text += '<div class="completed-section">'
    text += '<div class="section-title completed">📋 최근 완료된 프로젝트</div>'
    
    if len(completed_projects) == 0:
        text += "<div style='padding: 20px; color: #666;'>완료된 프로젝트가 없습니다.</div>"
    else:
        for cp in completed_projects:
            project_name = cp.get("project_name", "Unknown")
            user = cp.get("user", "unknown")
            submit_at = cp.get("submit_at", "")
            completed_at = cp.get("completed_at", "")
            status_info = cp.get("status", {})
            
            status_text = ", ".join([f"{status_name}: {status_count}" for status_name, status_count in status_info.items() if status_count > 0])
            
            text += f"""
                <div class="completed-card">
                    <div class="card-header">
                        {project_name}
                        <span class="completed-badge">완료</span>
                    </div>
                    <div class="card-meta">
                        <span class="user-badge user-{user}">{user}</span>
                        <span>제출: {submit_at}</span>
                        <span style="margin-left: 10px;">완료: {completed_at}</span>
                    </div>
                    <div class="card-status">{status_text if status_text else 'No jobs'}</div>
                </div>
            """
    
    text += '</div>'  # completed-section 닫기
    text += '</div>'  # dashboard-container 닫기

    # JavaScript 함수 구현 (deleteProject와 rerunFailedJobs)
    text += """
        <script>
        function deleteProject(projectName, user) {
            if (confirm(projectName + " 프로젝트를 정말 삭제하시겠습니까?")) {
                fetch('/delete_project', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 'project_name': projectName, 'user': user })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    // 페이지를 새로고침
                    location.reload();
                })
                .catch(error => {
                    alert("삭제 중 오류가 발생했습니다.");
                    console.error(error);
                });
            }
        }
        function rerunFailedJobs(projectName, user) {
            if (confirm(projectName + " 프로젝트의 실패한 작업들을 재실행하시겠습니까?")) {
                fetch('/rerun_failed_jobs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 'project_name': projectName, 'user': user })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    // 페이지를 새로고침
                    location.reload();
                })
                .catch(error => {
                    alert("실패한 작업 재실행 도중 오류가 발생했습니다.");
                    console.error(error);
                });
            }
        }

        function viewFailedLogs(projectName, user) {
            let modalBg = document.createElement('div');
            modalBg.style.position = 'fixed';
            modalBg.style.top = '0';
            modalBg.style.left = '0';
            modalBg.style.width = '100vw';
            modalBg.style.height = '100vh';
            modalBg.style.backgroundColor = 'rgba(0,0,0,0.3)';
            modalBg.style.zIndex = '1000';

            let modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '50%';
            modal.style.left = '50%';
            modal.style.transform = 'translate(-50%, -50%)';
            modal.style.backgroundColor = 'white';
            modal.style.padding = '20px';
            modal.style.borderRadius = '8px';
            modal.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
            modal.style.minWidth = '900px';
            modal.style.maxWidth = '95vw';
            modal.style.maxHeight = '85vh';
            modal.style.overflowY = 'auto';

            let title = document.createElement('h3');
            title.innerText = `Job Logs: ${projectName}`;
            title.style.marginTop = '0';
            modal.appendChild(title);

            let closeBtn = document.createElement('button');
            closeBtn.innerText = '닫기';
            closeBtn.style.marginBottom = '12px';
            closeBtn.style.backgroundColor = '#f44336';
            closeBtn.style.color = 'white';
            closeBtn.style.border = 'none';
            closeBtn.style.padding = '6px 14px';
            closeBtn.style.borderRadius = '4px';
            closeBtn.style.cursor = 'pointer';
            closeBtn.onclick = function () { document.body.removeChild(modalBg); };
            modal.appendChild(closeBtn);

            const status = document.createElement('div');
            status.style.color = '#666';
            status.style.marginBottom = '10px';
            // spinner
            if (!document.getElementById('spinner-style')) {
                const style = document.createElement('style');
                style.id = 'spinner-style';
                style.innerHTML = `
                    @keyframes spin {
                        0% { transform: rotate(0deg);}
                        100% { transform: rotate(360deg);}
                    }
                `;
                document.head.appendChild(style);
            }
            status.innerHTML = `
                <span style="display:inline-flex;align-items:center;">
                    <span class="spinner" style="
                        width:18px; height:18px; border:3px solid #ccc; border-top:3px solid #3498db;
                        border-radius:50%; margin-right:8px; animation:spin 1s linear infinite;
                        display:inline-block;
                    "></span>
                </span>
            `;
            modal.appendChild(status);

            const result = document.createElement('div');
            modal.appendChild(result);

            function fmtTime(ts) {
                if (!ts) return '';
                try {
                    return new Date(ts * 1000).toLocaleString();
                } catch (e) {
                    return '';
                }
            }

            function openLogModal(workerId, jobName, displayName) {
                let bg = document.createElement('div');
                bg.style.position = 'fixed';
                bg.style.top = '0';
                bg.style.left = '0';
                bg.style.width = '100vw';
                bg.style.height = '100vh';
                bg.style.backgroundColor = 'rgba(0,0,0,0.35)';
                bg.style.zIndex = '1100';

                let m = document.createElement('div');
                m.style.position = 'fixed';
                m.style.top = '50%';
                m.style.left = '50%';
                m.style.transform = 'translate(-50%, -50%)';
                m.style.backgroundColor = 'white';
                m.style.padding = '18px';
                m.style.borderRadius = '8px';
                m.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
                m.style.minWidth = '900px';
                m.style.maxWidth = '95vw';
                m.style.maxHeight = '85vh';
                m.style.overflow = 'hidden';

                const h = document.createElement('div');
                h.style.display = 'flex';
                h.style.alignItems = 'center';
                h.style.justifyContent = 'space-between';
                h.style.marginBottom = '10px';

                const t = document.createElement('div');
                const titleText = (displayName && displayName.trim()) ? displayName : jobName;
                t.innerHTML = `<b>${titleText}</b> <span style="color:#666;">(${workerId})</span>`;
                h.appendChild(t);

                const x = document.createElement('button');
                x.innerText = '닫기';
                x.style.backgroundColor = '#f44336';
                x.style.color = 'white';
                x.style.border = 'none';
                x.style.padding = '6px 14px';
                x.style.borderRadius = '4px';
                x.style.cursor = 'pointer';
                x.onclick = function () { document.body.removeChild(bg); };
                h.appendChild(x);

                m.appendChild(h);

                const pre = document.createElement('pre');
                pre.style.whiteSpace = 'pre-wrap';
                pre.style.wordBreak = 'break-word';
                pre.style.fontFamily = 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace';
                pre.style.fontSize = '12px';
                pre.style.border = '1px solid #eee';
                pre.style.padding = '12px';
                pre.style.margin = '0';
                pre.style.height = '70vh';
                pre.style.overflow = 'auto';
                pre.innerHTML = `
                    <span style="display:inline-flex;align-items:center;">
                        <span class="spinner" style="
                            width:18px; height:18px; border:3px solid #ccc; border-top:3px solid #3498db;
                            border-radius:50%; margin-right:8px; animation:spin 1s linear infinite;
                            display:inline-block;
                        "></span>
                        로딩 중...
                    </span>
                `;
                m.appendChild(pre);

                bg.appendChild(m);
                document.body.appendChild(bg);

                fetch(`/project_job_log?project_name=${encodeURIComponent(projectName)}&worker_id=${encodeURIComponent(workerId)}&job_name=${encodeURIComponent(jobName)}`)
                    .then(async r => {
                        const text = await r.text();
                        if (!r.ok) throw new Error(text || 'log 조회 실패');
                        return text;
                    })
                    .then(text => { pre.innerText = text || ''; })
                    .catch(err => { pre.innerText = '오류: ' + (err?.message || err); });
            }

            function render(resp) {
                const items = resp.items || [];
                if (!items.length) {
                    result.innerHTML = `<div style="color:#666;">job 이 없습니다.</div>`;
                    return;
                }
                const counts = resp.counts || {};
                const badge = (label, value, color) => {
                    if (value === undefined) return '';
                    return `<span style="display:inline-block; padding:3px 8px; border-radius:999px; background:${color}; color:white; font-size:12px; margin-right:6px;">${label}: ${value}</span>`;
                };
                let html = `<div style="margin-bottom:10px;">
                    결과: <b>${resp.count ?? items.length}</b>
                    <span style="color:#888; margin-left:8px;">(카드를 클릭하면 로그를 엽니다)</span>
                </div>`;
                html += `<div style="margin-bottom:10px;">` +
                    badge('running', counts.running, '#1976d2') +
                    badge('finished', counts.finished, '#2e7d32') +
                    badge('failed', counts.failed, '#d32f2f') +
                    badge('stopped', counts.stopped, '#6d4c41') +
                    badge('pending', counts.pending, '#616161') +
                    badge('unknown', counts.unknown, '#455a64') +
                    `</div>`;
                html += `<div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 10px;">`;

                items.forEach(it => {
                    const logLabel = it.log_exists ? `${it.log_size ?? ''} bytes` : '없음';
                    const disabled = !it.log_exists;
                    const border = disabled ? '#eee' : '#ddd';
                    const bg = disabled ? '#fafafa' : 'white';
                    const cursor = disabled ? 'not-allowed' : 'pointer';
                    const opacity = disabled ? '0.6' : '1';

                    const st = (it.status || '').toLowerCase();
                    const stColor = st === 'failed' ? '#d32f2f'
                        : st === 'running' ? '#1976d2'
                        : st === 'finished' ? '#2e7d32'
                        : st === 'stopped' ? '#6d4c41'
                        : st === 'pending' ? '#616161'
                        : '#455a64';
                    const stLabel = it.status || 'unknown';

                    html += `
                        <div
                            data-worker-id="${it.worker_id}"
                            data-job-name="${it.job_name}"
                            data-exp-name="${(it.exp_name ?? '').toString().replaceAll('\"', '&quot;')}"
                            data-log-exists="${it.log_exists ? '1' : '0'}"
                            style="
                                border:1px solid ${border};
                                background:${bg};
                                border-radius:8px;
                                padding:12px 12px;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.06);
                                cursor:${cursor};
                                opacity:${opacity};
                            "
                        >
                            <div style="display:flex; justify-content:space-between; gap:10px; align-items:flex-start;">
                                <div style="font-weight:700; color:#333; white-space:normal; word-break:break-word; overflow-wrap:anywhere; flex:1; min-width:0; line-height:1.25;">
                                    ${it.exp_name ?? it.job_name ?? ''}
                                </div>
                                <div style="font-size:12px; color:#666; white-space:nowrap;">
                                    ${it.worker_id ?? ''}
                                </div>
                            </div>
                            <div style="margin-top:6px; font-size:11px; color:#999; white-space:normal; word-break:break-word; overflow-wrap:anywhere;">
                                ${it.job_name ?? ''}
                            </div>
                            <div style="margin-top:8px; font-size:12px; color:#666; line-height:1.4;">
                                <div><b>status</b>: <span style="display:inline-block; padding:2px 8px; border-radius:999px; background:${stColor}; color:white;">${stLabel}</span></div>
                                <div><b>mtime</b>: ${fmtTime(it.status_mtime) || '-'}</div>
                                <div><b>log</b>: ${logLabel}</div>
                            </div>
                        </div>
                    `;
                });

                html += `</div>`;
                result.innerHTML = html;

                Array.from(result.querySelectorAll('div[data-worker-id][data-job-name]')).forEach(card => {
                    card.onclick = function () {
                        const wid = card.getAttribute('data-worker-id');
                        const jn = card.getAttribute('data-job-name');
                        const en = card.getAttribute('data-exp-name');
                        const le = card.getAttribute('data-log-exists') === '1';
                        if (!le) return;
                        openLogModal(wid, jn, en);
                    };
                });
            }

            fetch(`/project_jobs?project_name=${encodeURIComponent(projectName)}&user=${encodeURIComponent(user)}`)
                .then(async r => {
                    const data = await r.json();
                    if (!r.ok) throw new Error(data.detail || '조회 실패');
                    return data;
                })
                .then(data => { status.innerText = ''; render(data); })
                .catch(err => {
                    status.innerText = '';
                    result.innerHTML = `<div style="color:#f44336;">오류: ${err.message}</div>`;
                });

            modalBg.appendChild(modal);
            document.body.appendChild(modalBg);
        }
        </script>
    """

    # contents = html.format(content=text)
    html = open("thirteen_gpu/dashboard.html").read()
    contents = html.replace("PLACEHOLDER", text)

    # return HTML Rendered Page
    return HTMLResponse(content=contents, status_code=200)

@app.get("/get_resource_util")
def get_resource_util():
    # connect_worker 함수 사용
    workers = json.loads(open("thirteen_gpu/workers.json").read())
    worker_objs = {}

    def worker_connect_thread(worker_id, worker_info):
        connect_worker(worker_info, worker_objs)

    threads = []
    for worker_id, worker_info in workers.items():
        t = threading.Thread(target=worker_connect_thread, args=(worker_id, worker_info))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
        
    # 각 worker에 대해 리소스 사용량 커맨드를 실행하고 결과를 받아오는 코드입니다. (스레드로 변경)
    info_dict = {}
    info_lock = threading.Lock()

    def fetch_resource_info(worker_id, worker):
        try:
            worker_info = workers[worker_id]
            host = worker_info.get("host")
            cmd = (
                "CPU=$(top -bn1 | grep \"Cpu(s)\" | awk '{print $2 + $4}');"
                "MEM=$(LANG=C free -m | awk '/Mem:/ {used=$3; total=$2; printf \"%.1f\", used/total*100}');"
                "SWAP=$(LANG=C free -m | awk '/Swap:/ {used=$3; total=$2; if (total==0) print 0; else printf \"%.1f\", used/total*100}');"
                "echo '{\"cpu_pct\": '\"$CPU\"', \"mem_pct\": '\"$MEM\"', \"swap_pct\": '\"$SWAP\"'}'"
            )
            try:
                result_str = worker.ssh.ssh_exec_command(cmd).strip()
                info = json.loads(result_str)
            except Exception as e:
                print(f"리소스 정보 조회 실패(ssh_exec_command): {worker_id}, 에러: {e}")
                info = {"cpu_pct": None, "mem_pct": None, "swap_pct": None}
            info["owner"] = worker_info.get("owner")
            with info_lock:
                info_dict[worker_id] = info
        except Exception as e:
            print(f"리소스 정보 조회 실패(ssh): {worker_id}, 에러: {e}")
            with info_lock:
                info_dict[worker_id] = {"owner": workers[worker_id].get("owner"), "cpu_pct": None, "mem_pct": None, "swap_pct": None}

    threads = []
    for worker_id, worker in worker_objs.items():
        t = threading.Thread(target=fetch_resource_info, args=(worker_id, worker))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    print(f"{info_dict=}")
    return info_dict
