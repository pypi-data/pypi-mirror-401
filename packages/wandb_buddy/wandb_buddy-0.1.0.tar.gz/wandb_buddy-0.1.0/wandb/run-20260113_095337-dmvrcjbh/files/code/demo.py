"""
Demo script to test wandb_buddy with dummy W&B runs.

Usage:
    python demo.py

This will:
1. Create several dummy runs in a test project with various tags/configs
2. Use load_runs() to retrieve and display them
"""

import wandb
import random
import time

# Configuration
ENTITY = wandb.api.default_entity  # Uses your default entity
PROJECT = "wandb_buddy_test"

def create_dummy_runs():
    """Create a few dummy runs with different configurations."""
    
    experiments = [
        {
            "tags": ["experiment-v1", "baseline"],
            "config": {"lr": 0.001, "batch_size": 32, "model": "resnet18"},
            "metrics": {"accuracy": 0.85, "loss": 0.42},
        },
        {
            "tags": ["experiment-v1", "improved"],
            "config": {"lr": 0.0005, "batch_size": 64, "model": "resnet34"},
            "metrics": {"accuracy": 0.89, "loss": 0.31},
        },
        {
            "tags": ["experiment-v1", "improved"],
            "config": {"lr": 0.0001, "batch_size": 128, "model": "resnet50"},
            "metrics": {"accuracy": 0.91, "loss": 0.25},
        },
        {
            "tags": ["experiment-v2", "debug"],
            "config": {"lr": 0.01, "batch_size": 16, "model": "resnet18"},
            "metrics": {"accuracy": 0.72, "loss": 0.65},
        },
        {
            "tags": ["experiment-v2"],
            "config": {"lr": 0.001, "batch_size": 32, "model": "resnet34"},
            "metrics": {"accuracy": 0.88, "loss": 0.33},
        },
    ]
    
    print(f"Creating {len(experiments)} dummy runs in {ENTITY}/{PROJECT}...")
    print("-" * 50)
    
    for i, exp in enumerate(experiments):
        run = wandb.init(
            entity=ENTITY,
            project=PROJECT,
            tags=exp["tags"],
            config=exp["config"],
            name=f"demo_run_{i+1}",
            reinit=True,
        )
        
        # Simulate some training steps
        for step in range(5):
            noise = random.uniform(-0.02, 0.02)
            wandb.log({
                "accuracy": exp["metrics"]["accuracy"] + noise,
                "loss": exp["metrics"]["loss"] - noise,
                "step": step,
            })
            time.sleep(0.1)
        
        # Log final metrics to summary
        wandb.summary["final_accuracy"] = exp["metrics"]["accuracy"]
        wandb.summary["final_loss"] = exp["metrics"]["loss"]
        
        run.finish()
        print(f"  Created: {run.name} with tags {exp['tags']}")
    
    print("-" * 50)
    print("All runs created!\n")


def test_load_runs():
    """Test the load_runs function with various queries."""
    from wandb_buddy import load_runs
    
    print("=" * 60)
    print("Testing load_runs()")
    print("=" * 60)
    
    # Test 1: Load all experiment-v1 runs
    print("\n1. Load runs with tag 'experiment-v1':")
    df = load_runs(ENTITY, PROJECT, tags=["experiment-v1"])
    print(f"   Found {len(df)} runs")
    if len(df) > 0:
        print(df[["name", "tags", "lr", "model", "final_accuracy"]].to_string(index=False))
    
    # Test 2: Load experiment-v1 but exclude debug
    print("\n2. Load 'experiment-v1' excluding 'debug':")
    df = load_runs(ENTITY, PROJECT, tags=["experiment-v1"], exclude_tags=["debug"])
    print(f"   Found {len(df)} runs")
    if len(df) > 0:
        print(df[["name", "tags", "lr", "model"]].to_string(index=False))
    
    # Test 3: Use raw filters
    print("\n3. Load runs with batch_size >= 64 (raw filter):")
    df = load_runs(ENTITY, PROJECT, filters={"config.batch_size": {"$gte": 64}})
    print(f"   Found {len(df)} runs")
    if len(df) > 0:
        print(df[["name", "batch_size", "model"]].to_string(index=False))
    
    # Test 4: Combined tags + raw filters
    print("\n4. Load 'experiment-v1' with lr <= 0.0005:")
    df = load_runs(
        ENTITY, PROJECT,
        tags=["experiment-v1"],
        filters={"config.lr": {"$lte": 0.0005}}
    )
    print(f"   Found {len(df)} runs")
    if len(df) > 0:
        print(df[["name", "lr", "final_accuracy"]].to_string(index=False))
    
    # Test 5: Load all runs (no filter)
    print("\n5. Load ALL runs from project:")
    df = load_runs(ENTITY, PROJECT, state="all")
    print(f"   Found {len(df)} total runs")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print(f"View your runs at: https://wandb.ai/{ENTITY}/{PROJECT}")
    print("=" * 60)


if __name__ == "__main__":
    print(f"W&B Entity: {ENTITY}")
    print(f"W&B Project: {PROJECT}\n")
    
    # Step 1: Create dummy runs
    create_dummy_runs()
    
    # Small delay to ensure runs are indexed
    print("Waiting a few seconds for W&B to index runs...")
    time.sleep(3)
    
    # Step 2: Test load_runs
    test_load_runs()
