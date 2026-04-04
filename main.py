import sys
from agent import run_agent

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <job_url>")
        sys.exit(1)

    job_url = sys.argv[1]
    report = run_agent(job_url)
    print(report)

if __name__ == "__main__":
    main()