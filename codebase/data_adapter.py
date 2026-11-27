
"""Data Adapter — Track E3, nhóm DTMD.

Chuẩn hóa dữ liệu JSONL từ Data Pipeline sang
contract hiện tại của AI Core.

Không thay đổi dữ liệu gốc.
Không sử dụng nhãn scenario để quyết định hành động.
Không tính lại điểm rủi ro.
"""

import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

TRANSACTION_RULE_IDS = (
    "T01",
    "T02",
    "T03",
    "T04",
)


def read_jsonl(path: Path) -> list:
    """Đọc danh sách bản ghi từ file JSONL."""

    records = []

    with path.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            record = json.loads(line)

            if not isinstance(record, dict):
                raise ValueError(
                    f"Invalid record at line {line_number}"
                )

            records.append(record)

    return records


def read_json(path: Path) -> list:
    """Đọc JSON dạng danh sách, hỗ trợ fixture cũ."""

    with path.open("r", encoding="utf-8-sig") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError(
            f"{path.name} must contain a JSON list"
        )

    return records


def normalize_transaction(record: dict) -> dict:
    """Chuyển schema giao dịch JSONL sang schema AI Core."""

    raw_flags = record.get("trigger_flags")

    if isinstance(raw_flags, list):
        flags = {
            rule_id: (
                "MATCHED"
                if rule_id in raw_flags
                else "UNKNOWN"
            )
            for rule_id in TRANSACTION_RULE_IDS
        }
    else:
        flags = {
            rule_id: "UNKNOWN"
            for rule_id in TRANSACTION_RULE_IDS
        }

    face_status = record.get("face_auth_status")

    if face_status == "SUCCESS":
        face_verified = True
    elif face_status == "FAILED":
        face_verified = False
    else:
        face_verified = None

    return {
        "tx_id": record["tx_id"],
        "user_id": record["user_id"],
        "amount": record.get("amount_vnd"),
        "currency": "VND",
        "recipient": record.get("recipient"),
        "status": record.get("transaction_status"),
        "face_id_verified": face_verified,
        "memo": "",
        "transaction_flags": flags,
        "data_source": record.get("data_source"),
    }


def normalize_scam_case(record: dict) -> dict:
    """Chuẩn hóa ca lừa đảo tương đồng."""

    return {
        "case_id": record["case_id"],
        "rule_ids": record.get("related_rule_ids", []),
        "title": record.get("pattern", ""),
        "description": record.get("description", ""),
        "source": None,
        "is_synthetic": (
            record.get("data_source") == "SYNTHETIC"
            or record.get("source_type") == "SYNTHETIC"
        ),
        "verified_status": record.get("verified_status"),
    }


def load_transactions(data_dir: Path = DATA_DIR) -> list:
    """Đọc giao dịch từ pipeline hoặc fixture kiểm thử."""

    data_dir = Path(data_dir)

    jsonl_path = (
        data_dir
        / "data"
        / "interim"
        / "normalized_transactions.jsonl"
    )

    if jsonl_path.is_file():
        return [
            normalize_transaction(record)
            for record in read_jsonl(jsonl_path)
        ]

    fixture_path = data_dir / "transactions.json"

    if fixture_path.is_file():
        return read_json(fixture_path)

    raise FileNotFoundError(
        "Transaction dataset not available"
    )


def load_scam_cases(data_dir: Path = DATA_DIR) -> list:
    """Đọc dữ liệu retrieval từ pipeline hoặc fixture."""

    data_dir = Path(data_dir)

    jsonl_path = (
        data_dir
        / "data"
        / "interim"
        / "normalized_scam_cases.jsonl"
    )

    if jsonl_path.is_file():
        return [
            normalize_scam_case(record)
            for record in read_jsonl(jsonl_path)
        ]

    fixture_path = data_dir / "scam_cases.json"

    if fixture_path.is_file():
        return read_json(fixture_path)

    raise FileNotFoundError(
        "Scam case dataset not available"
    )
