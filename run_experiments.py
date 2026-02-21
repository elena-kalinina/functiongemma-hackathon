#!/usr/bin/env python3
"""
Run benchmark experiments with different strategies.
Usage: python run_experiments.py
"""


import re

STRATEGIES = ["always_local", "baseline", "complexity", "complexity_plus", "semantic", "validation", "combined", "smart_validation","complexity_semantic_plus"]

def set_strategy(strategy):
    """Update ACTIVE_STRATEGY in main.py"""
    with open("main.py", "r") as f:
        content = f.read()
    
    # Replace the ACTIVE_STRATEGY line
    content = re.sub(
        r'ACTIVE_STRATEGY = "[^"]*"',
        f'ACTIVE_STRATEGY = "{strategy}"',
        content
    )
    
    with open("main.py", "w") as f:
        f.write(content)

def run_benchmark():
    """Run benchmark and capture output"""

    pass

def extract_score(output):
    """Extract the total score from benchmark output"""
    match = re.search(r'TOTAL SCORE:\s*([\d.]+)%', output)
    if match:
        return float(match.group(1))
    return None

def extract_stats(output):
    """Extract on-device vs cloud stats"""
    match = re.search(r'on-device=(\d+)/(\d+).*cloud=(\d+)/(\d+)', output)
    if match:
        return {
            "on_device": int(match.group(1)),
            "total": int(match.group(2)),
            "cloud": int(match.group(3)),
        }
    return None

def main():
    print("=" * 60)
    print("STRATEGY COMPARISON EXPERIMENT")
    print("=" * 60)
    print()
    
    results = []
    
    for strategy in STRATEGIES:
        print(f"Testing strategy: {strategy}...")
        set_strategy(strategy)
        
        output = run_benchmark()
        score = extract_score(output)
        stats = extract_stats(output)
        
        results.append({
            "strategy": strategy,
            "score": score,
            "stats": stats,
        })
        
        if score:
            on_device_pct = (stats["on_device"] / stats["total"] * 100) if stats else 0
            print(f"  Score: {score:.1f}%  |  On-device: {on_device_pct:.0f}%")
        else:
            print(f"  Failed to extract score")
        print()
    
    # Summary table
    print()
    print("=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"{'Strategy':<15} {'Score':>10} {'On-Device':>12} {'Cloud':>10}")
    print("-" * 60)
    
    for r in results:
        if r["score"] and r["stats"]:
            on_device_pct = r["stats"]["on_device"] / r["stats"]["total"] * 100
            cloud_pct = r["stats"]["cloud"] / r["stats"]["total"] * 100
            print(f"{r['strategy']:<15} {r['score']:>9.1f}% {on_device_pct:>11.0f}% {cloud_pct:>9.0f}%")
    
    print("-" * 60)
    
    # Find best strategy
    best = max(results, key=lambda x: x["score"] or 0)
    print(f"\n🏆 Best strategy: {best['strategy']} with {best['score']:.1f}%")
    
    # Set back to best strategy
    set_strategy(best["strategy"])
    print(f"\n✓ Set ACTIVE_STRATEGY to '{best['strategy']}'")

if __name__ == "__main__":
    main()
