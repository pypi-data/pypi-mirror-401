import typer
from rich.console import Console
import os
import msgpack
app = typer.Typer(help='Developer Tools & Debugging')
console = Console()

@app.command(name='wal-decode')
def wal_decode(target: str=typer.Argument(..., help='Database Path'), limit: int=typer.Option(20, help='Max entries to show')):
    wal_path = target + '.wal'
    if not os.path.exists(wal_path):
        console.print(f'[red]WAL file {wal_path} not found.[/red]')
        return
    console.print(f'[bold]Decoding WAL: {wal_path}[/bold]')
    try:
        with open(wal_path, 'rb') as f:
            header = f.read(32)
            console.print(f'Header (Raw): {header.hex()}')
            unpacker = msgpack.Unpacker(f)
            count = 0
            for entry in unpacker:
                console.print(entry)
                count += 1
                if count >= limit:
                    console.print('[dim]... limit reached ...[/dim]')
                    break
    except Exception as e:
        console.print(f'[red]Error decoding WAL: {e}[/red]')

@app.command(name='schema-stats')
def schema_stats(target: str=typer.Argument(..., help='Database Path')):
    from hvpdb.utils import connect_db
    try:
        db = connect_db(target)
        stats = {}
        for group_name in db.get_all_groups():
            grp = db.group(group_name)
            docs = grp.get_all()
            g_stats = {'count': len(docs), 'keys': {}}
            for doc in docs:
                for k, v in doc.items():
                    type_name = type(v).__name__
                    if k not in g_stats['keys']:
                        g_stats['keys'][k] = {'types': set(), 'count': 0}
                    g_stats['keys'][k]['types'].add(type_name)
                    g_stats['keys'][k]['count'] += 1
            for k in g_stats['keys']:
                g_stats['keys'][k]['types'] = list(g_stats['keys'][k]['types'])
            stats[group_name] = g_stats
        console.print_json(data=stats)
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')
from .bench import app as bench_app
app.add_typer(bench_app, name='bench', help='Performance Benchmarking')