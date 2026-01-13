import typer
from rich.console import Console
from rich.table import Table
import time
import os
import random
import string
import shutil
from hvpdb.utils import connect_db
app = typer.Typer(help='Performance Benchmarking Tool')
console = Console()

def generate_random_doc(size_kb: int):
    chars = string.ascii_letters + string.digits
    payload = ''.join(random.choices(chars, k=size_kb * 1024))
    return {'timestamp': time.time(), 'type': 'benchmark', 'payload': payload, 'tags': ['bench', 'test', 'speed']}

@app.command(name='run')
def run_benchmark(target: str=typer.Argument('bench.hvp', help='Target DB path (will be created/wiped)'), ops: int=typer.Option(1000, help='Number of operations'), size: int=typer.Option(1, help='Document size in KB'), verify: bool=typer.Option(False, help='Verify reads after write')):
    if os.path.exists(target):
        try:
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
            if os.path.exists(target + '.wal'):
                os.remove(target + '.wal')
        except:
            pass
    console.print(f'[bold]Starting Benchmark[/bold]')
    console.print(f'Target: {target}')
    console.print(f'Operations: {ops}')
    console.print(f'Doc Size: {size} KB')
    console.print('-' * 40)
    db = connect_db(target)
    grp = db.group('bench_group')
    console.print('[yellow]Running WRITE test...[/yellow]')
    start_time = time.perf_counter()
    doc_ids = []
    sample_doc = generate_random_doc(size)
    for i in range(ops):
        d = sample_doc.copy()
        d['_id'] = f'doc_{i}'
        grp.insert(d)
        doc_ids.append(d['_id'])
    db.commit()
    end_time = time.perf_counter()
    write_duration = end_time - start_time
    write_ops_sec = ops / write_duration
    console.print(f'Write Time: {write_duration:.4f}s')
    console.print(f'Write Throughput: [bold green]{write_ops_sec:.2f} ops/sec[/bold green]')
    console.print('\n[yellow]Running READ test (Random Access)...[/yellow]')
    start_time = time.perf_counter()
    random.shuffle(doc_ids)
    hits = 0
    for doc_id in doc_ids:
        doc = grp.find_one({'_id': doc_id})
        if doc:
            hits += 1
    end_time = time.perf_counter()
    read_duration = end_time - start_time
    read_ops_sec = ops / read_duration
    console.print(f'Read Time: {read_duration:.4f}s')
    console.print(f'Read Throughput: [bold green]{read_ops_sec:.2f} ops/sec[/bold green]')
    console.print(f'Hit Rate: {hits}/{ops}')
    db.storage.close()
    console.print('\n[dim]Benchmark Complete.[/dim]')

@app.command(name='latency')
def measure_latency(target: str=typer.Argument('bench.hvp', help='Target DB'), iter: int=typer.Option(100, help='Iterations')):
    import statistics
    db = connect_db(target)
    grp = db.group('latency_test')
    latencies = []
    for i in range(iter):
        t0 = time.perf_counter_ns()
        grp.insert({'data': 'test'})
        db.commit()
        t1 = time.perf_counter_ns()
        latencies.append((t1 - t0) / 1000000)
    avg = statistics.mean(latencies)
    p95 = sorted(latencies)[int(iter * 0.95)]
    p99 = sorted(latencies)[int(iter * 0.99)]
    console.print(f'Avg Latency: {avg:.2f} ms')
    console.print(f'P95 Latency: {p95:.2f} ms')
    console.print(f'P99 Latency: {p99:.2f} ms')