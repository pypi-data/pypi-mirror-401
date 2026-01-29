from collections import defaultdict


def print_report(timeline):
    if not timeline:
        print("\n✅ No incidents detected in this time window.\n")
        return

    print("\n🚨 INCIDENT SUMMARY")
    print("-" * 18)

    reasons = set()
    pods = set()
    namespaces = set()

    for e in timeline:
        reasons.add(e["reason"])
        pods.add(e["name"])
        namespaces.add(e["namespace"])

    print("Detected Issues:")
    for r in sorted(reasons):
        print(f"  - {r}")

    print(f"\nAffected Pods    : {len(pods)}")
    print(f"Affected Namespaces : {len(namespaces)}")

    print("\n🧠 OPSAUTOPSY INCIDENT TIMELINE\n")

    # Group by namespace → pod
    grouped = defaultdict(lambda: defaultdict(list))

    for e in timeline:
        grouped[e["namespace"]][e["name"]].append(e)

    for namespace, pods in grouped.items():
        print(f"📦 Namespace: {namespace}")
        print("=" * (14 + len(namespace)))

        for pod, events in pods.items():
            print(f"\n🔹 POD::{pod}")
            print("-" * (len(pod) + 8))

            events.sort(key=lambda x: x["time"])

            for e in events:
                ts = e["time"].strftime("%Y-%m-%d %H:%M:%S")
                print(f"{ts} | {e['reason']} | {e['message']}")

    print("\n--- END OF OPSAUTOPSY ---\n")
