"""CLI demo - Track E3, nhom DTMD."""

import os
import sys

for stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        stream.reconfigure(
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        pass

sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)),
)


def main() -> int:

    try:
        import tracing
        from agent import create_session, run_agent

    except Exception as exc:
        print(
            "Khong nap duoc codebase:",
            type(exc).__name__,
            str(exc),
        )
        return 1

    session = create_session()

    print("=" * 60)
    print("DTMD - VI AN TOAN")
    print("Track E3 - AI Product Hackathon")
    print("=" * 60)
    print("Moi truong mo phong, khong giao dich tien that.")
    print("/reset : Bat dau tinh huong moi")
    print("/exit  : Thoat chuong trinh")
    print("=" * 60)

    blank = 0

    while True:

        try:
            text = input("\nBan: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nDa ket thuc phien.")
            return 0

        if not text:
            blank += 1

            if blank >= 2:
                return 0

            continue

        blank = 0

        if text.lower() == "/exit":
            return 0

        if text.lower() == "/reset":
            session = create_session()
            print("Da bat dau tinh huong moi.")
            continue

        tracing.begin("app")

        try:
            result = run_agent(text, session)

        except Exception as exc:
            tracing.end()
            print(
                "[Loi xu ly]",
                type(exc).__name__,
            )
            continue

        stats, events = tracing.end()

        print("\nAgent:", result.get("output", ""))

        print(
            "\n[TRACE]"
            f"\nClassification: {result.get('classification')}"
            f"\nAction: {result.get('action')}"
            f"\nPriority: {result.get('priority')}"
            f"\nQuestions: {session['question_count']}"
            f"\nModel: {', '.join(stats['models']) or '-'}"
            f"\nModel calls: {stats['model_calls']}"
            f"\nTool calls: {stats['tool_calls']}"
            f"\nTokens in: {stats['tokens_in']}"
            f"\nTokens out: {stats['tokens_out']}"
        )


if __name__ == "__main__":
    sys.exit(main())
