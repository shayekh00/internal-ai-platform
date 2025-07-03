# observability.py

import json
from pathlib import Path
from typing import List, Dict
from statistics import mean
import datetime

def load_logs(agent_name: str) -> List[Dict]:
    log_path = Path.cwd() / agent_name / "logs.jsonl"
    if not log_path.exists():
        raise FileNotFoundError(f"No logs found for agent '{agent_name}'")

    logs = []
    with open(log_path, "r") as f:
        for line in f:
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return logs

def summarize_logs(logs: List[Dict]) -> Dict:
    latencies = [log["latency"] for log in logs]
    failures = [log for log in logs if "I don't know" in log["response"] or "not sure" in log["response"].lower()]
    return {
        "total_logs": len(logs),
        "avg_latency": round(mean(latencies), 2) if latencies else 0.0,
        "max_latency": max(latencies) if latencies else 0.0,
        "num_failures": len(failures),
        "last_5_prompts": logs[-5:] if logs else []
    }

def print_summary(summary: Dict):
    print(f"\n📊 Observability Summary")
    print(f"Total calls:     {summary['total_logs']}")
    print(f"Average latency: {summary['avg_latency']}s")
    print(f"Max latency:     {summary['max_latency']}s")
    print(f"Failures:        {summary['num_failures']}")
    print(f"Recent prompts:")
    for log in summary["last_5_prompts"]:
        ts = datetime.datetime.fromtimestamp(log["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        print(f" - [{ts}] {log['prompt'][:60]} → {log['response'][:60]}")
