from core.orchestrator import Orchestrator

def main():
    orch = Orchestrator()
    topic = input("Enter a research topic: ")
    result = orch.run(topic)

    print("\n--- RESULT ---")
    print(result)

if __name__ == "__main__":
    main()
