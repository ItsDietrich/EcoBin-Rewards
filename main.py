from services.db import ensure_schema
from services.workflow import run_cycle

def main():
    ensure_schema()
    while True:
        try:
            run_cycle()
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()