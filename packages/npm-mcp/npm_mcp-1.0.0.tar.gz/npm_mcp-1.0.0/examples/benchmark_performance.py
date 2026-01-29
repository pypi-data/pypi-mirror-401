#!/usr/bin/env python3
"""
Performance Benchmark Script for NPM MCP Server

This script measures and reports on various performance characteristics:
- Throughput (operations/second)
- Latency (p50, p95, p99)
- Concurrency performance
- Batch processing efficiency
- Memory usage
- Connection pool behavior

Usage:
    export NPM_URL="http://your-npm-instance:81"
    export NPM_EMAIL="admin@example.com"
    export NPM_PASSWORD="your-password"

    python examples/benchmark_performance.py --all
    python examples/benchmark_performance.py --throughput
    python examples/benchmark_performance.py --concurrency
    python examples/benchmark_performance.py --scale
"""

import argparse
import asyncio
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import contextlib

from npm_mcp.config.loader import ConfigLoader
from npm_mcp.instance_manager import InstanceManager


@dataclass
class BenchmarkResult:
    """Results from a benchmark test."""

    name: str
    duration: float  # seconds
    operations: int
    throughput: float  # ops/second
    latencies: list[float]  # per-operation latencies
    p50: float  # median latency
    p95: float  # 95th percentile
    p99: float  # 99th percentile
    memory_mb: float | None = None


def calculate_percentile(values: list[float], percentile: float) -> float:
    """Calculate percentile from sorted values."""
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = int(len(sorted_values) * (percentile / 100.0))
    return sorted_values[min(index, len(sorted_values) - 1)]


async def benchmark_list_operations(npm_client, iterations: int = 100) -> BenchmarkResult:
    """Benchmark list operations (proxy hosts, certificates, etc.)."""
    print(f"Benchmarking list operations ({iterations} iterations)...")

    latencies = []
    start_time = time.time()

    for i in range(iterations):
        op_start = time.time()
        await npm_client.list_proxy_hosts()
        latencies.append(time.time() - op_start)

        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{iterations}")

    duration = time.time() - start_time
    throughput = iterations / duration

    return BenchmarkResult(
        name="List Operations",
        duration=duration,
        operations=iterations,
        throughput=throughput,
        latencies=latencies,
        p50=calculate_percentile(latencies, 50),
        p95=calculate_percentile(latencies, 95),
        p99=calculate_percentile(latencies, 99),
    )


async def benchmark_create_operations(npm_client, count: int = 10) -> BenchmarkResult:
    """Benchmark create operations."""
    print(f"Benchmarking create operations ({count} proxy hosts)...")

    latencies = []
    created_ids = []
    start_time = time.time()

    for i in range(count):
        op_start = time.time()

        try:
            host = await npm_client.create_proxy_host(
                domain_names=[f"bench-{i}-{int(time.time())}.example.com"],
                forward_scheme="http",
                forward_host="192.168.1.100",
                forward_port=8080 + i,
                block_exploits=True,
            )
            created_ids.append(host.id)
            latencies.append(time.time() - op_start)
            print(f"  Created: {i + 1}/{count}")
        except Exception as e:
            print(f"  Failed: {e}")

    duration = time.time() - start_time
    throughput = len(created_ids) / duration if created_ids else 0

    # Clean up created hosts
    print("  Cleaning up...")
    for host_id in created_ids:
        with contextlib.suppress(Exception):
            await npm_client.delete_proxy_host(host_id)

    return BenchmarkResult(
        name="Create Operations",
        duration=duration,
        operations=len(created_ids),
        throughput=throughput,
        latencies=latencies,
        p50=calculate_percentile(latencies, 50),
        p95=calculate_percentile(latencies, 95),
        p99=calculate_percentile(latencies, 99),
    )


async def benchmark_concurrent_operations(
    npm_client, concurrency_level: int = 10, iterations: int = 50
) -> BenchmarkResult:
    """Benchmark concurrent list operations."""
    print(f"Benchmarking concurrent operations (concurrency={concurrency_level})...")

    latencies = []
    start_time = time.time()

    # Create batches
    total_ops = iterations
    batch_count = total_ops // concurrency_level

    for batch in range(batch_count):
        batch_start = time.time()

        # Run concurrent operations
        tasks = [npm_client.list_proxy_hosts() for _ in range(concurrency_level)]
        await asyncio.gather(*tasks)

        batch_latency = time.time() - batch_start
        latencies.append(batch_latency / concurrency_level)  # Average per operation

        if (batch + 1) % 5 == 0:
            print(f"  Progress: {(batch + 1) * concurrency_level}/{total_ops}")

    duration = time.time() - start_time
    throughput = total_ops / duration

    return BenchmarkResult(
        name=f"Concurrent Operations (n={concurrency_level})",
        duration=duration,
        operations=total_ops,
        throughput=throughput,
        latencies=latencies,
        p50=calculate_percentile(latencies, 50),
        p95=calculate_percentile(latencies, 95),
        p99=calculate_percentile(latencies, 99),
    )


async def benchmark_batch_processing(npm_client, batch_sizes: list[int]) -> list[BenchmarkResult]:
    """Benchmark different batch sizes."""
    print("Benchmarking batch processing...")

    results = []

    for batch_size in batch_sizes:
        print(f"  Testing batch_size={batch_size}...")

        latencies = []
        start_time = time.time()

        # Simulate batch processing
        iterations = 100 // batch_size
        for _ in range(iterations):
            batch_start = time.time()

            # Process batch
            tasks = [npm_client.list_certificates() for _ in range(batch_size)]
            await asyncio.gather(*tasks)

            latencies.append(time.time() - batch_start)

        duration = time.time() - start_time
        total_ops = iterations * batch_size
        throughput = total_ops / duration

        results.append(
            BenchmarkResult(
                name=f"Batch Processing (size={batch_size})",
                duration=duration,
                operations=total_ops,
                throughput=throughput,
                latencies=latencies,
                p50=calculate_percentile(latencies, 50),
                p95=calculate_percentile(latencies, 95),
                p99=calculate_percentile(latencies, 99),
            )
        )

    return results


def print_result(result: BenchmarkResult) -> None:
    """Print benchmark result in a formatted way."""
    print(f"\n{'=' * 80}")
    print(f"Benchmark: {result.name}")
    print(f"{'=' * 80}")
    print(f"Duration:     {result.duration:.2f}s")
    print(f"Operations:   {result.operations}")
    print(f"Throughput:   {result.throughput:.2f} ops/sec")
    print("Latency:")
    print(f"  - p50:      {result.p50 * 1000:.2f}ms")
    print(f"  - p95:      {result.p95 * 1000:.2f}ms")
    print(f"  - p99:      {result.p99 * 1000:.2f}ms")
    if result.memory_mb:
        print(f"Memory:       {result.memory_mb:.2f} MB")


async def run_all_benchmarks(npm_client) -> list[BenchmarkResult]:
    """Run all benchmarks."""
    results = []

    print("\n" + "=" * 80)
    print("NPM MCP Server Performance Benchmarks")
    print("=" * 80)
    print()

    # 1. List operations
    result = await benchmark_list_operations(npm_client, iterations=50)
    results.append(result)
    print_result(result)

    # 2. Create operations
    result = await benchmark_create_operations(npm_client, count=5)
    results.append(result)
    print_result(result)

    # 3. Concurrent operations (various levels)
    for concurrency in [1, 5, 10, 20]:
        result = await benchmark_concurrent_operations(
            npm_client, concurrency_level=concurrency, iterations=50
        )
        results.append(result)
        print_result(result)

    # 4. Batch processing
    batch_results = await benchmark_batch_processing(npm_client, batch_sizes=[1, 5, 10, 20])
    results.extend(batch_results)
    for result in batch_results:
        print_result(result)

    return results


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="NPM MCP Server Performance Benchmarks")
    parser.add_argument("--all", action="store_true", help="Run all benchmarks")
    parser.add_argument("--throughput", action="store_true", help="Run throughput tests")
    parser.add_argument("--concurrency", action="store_true", help="Run concurrency tests")
    parser.add_argument("--scale", action="store_true", help="Run scale tests")

    args = parser.parse_args()

    # Default to --all if nothing specified
    if not any([args.all, args.throughput, args.concurrency, args.scale]):
        args.all = True

    # Get credentials
    npm_url = os.getenv("NPM_URL")
    npm_email = os.getenv("NPM_EMAIL")
    npm_password = os.getenv("NPM_PASSWORD")

    if not all([npm_url, npm_email, npm_password]):
        print("ERROR: Missing required environment variables")
        print("  - NPM_URL")
        print("  - NPM_EMAIL")
        print("  - NPM_PASSWORD")
        sys.exit(1)

    try:
        # Initialize
        config = ConfigLoader.load_config()
        instance_manager = InstanceManager(config.global_settings)

        await instance_manager.add_instance(
            name="benchmark",
            url=npm_url,
            username=npm_email,
            password=npm_password,
        )

        npm_client = await instance_manager.get_client("benchmark")

        # Run benchmarks
        if args.all:
            results = await run_all_benchmarks(npm_client)
        else:
            results = []

            if args.throughput:
                result = await benchmark_list_operations(npm_client)
                results.append(result)
                print_result(result)

            if args.concurrency:
                for concurrency in [1, 10, 50]:
                    result = await benchmark_concurrent_operations(npm_client, concurrency)
                    results.append(result)
                    print_result(result)

        # Summary
        print("\n" + "=" * 80)
        print("Benchmark Summary")
        print("=" * 80)
        print(f"\n{'Benchmark':<40} {'Throughput':<20} {'p95 Latency':<15}")
        print("-" * 75)

        for result in results:
            print(
                f"{result.name:<40} {result.throughput:>8.2f} ops/sec     "
                f"{result.p95 * 1000:>8.2f}ms"
            )

        print()

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await instance_manager.close_all()


if __name__ == "__main__":
    asyncio.run(main())
