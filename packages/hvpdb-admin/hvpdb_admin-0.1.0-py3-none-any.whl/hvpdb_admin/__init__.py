import typer
from rich.console import Console
from rich.table import Table
import os
import json
import time
app = typer.Typer(help='Admin & Audit Tools')
console = Console()

@app.command(name='audit')
def audit_log(target: str=typer.Argument(..., help='Database Path'), limit: int=typer.Option(50, help='Number of entries to show')):
    console.print(f'[bold]Audit Log for {target}[/bold]')
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('Timestamp', style='dim')
    table.add_column('User', style='cyan')
    table.add_column('Action', style='green')
    table.add_column('Details', style='white')
    wal_path = target + '.wal'
    if os.path.exists(wal_path):
        pass
    console.print('[dim]Note: Audit logging is currently minimal.[/dim]')

@app.command(name='policy')
def set_policy(target: str=typer.Argument(..., help='Database Path'), min_length: int=typer.Option(8, help='Minimum password length'), require_special: bool=typer.Option(True, help='Require special chars')):
    from hvpdb.utils import connect_db
    try:
        db = connect_db(target)
        if 'meta' not in db.storage.data:
            db.storage.data['meta'] = {}
        policy = {'min_length': min_length, 'require_special': require_special, 'updated_at': time.time()}
        db.storage.data['meta']['security_policy'] = policy
        db.commit()
        console.print(f'[green]Security policy updated for {target}[/green]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@app.command(name='rotate-logs')
def rotate_logs(target: str=typer.Argument(..., help='Database Path')):
    console.print('[yellow]Rotating logs...[/yellow]')
    wal_path = target + '.wal'
    if os.path.exists(wal_path):
        ts = int(time.time())
        new_name = f'{wal_path}.{ts}.bak'
        import shutil
        shutil.copy2(wal_path, new_name)
        console.print(f'[green]Archived WAL to {new_name}[/green]')
        console.print("Run 'hvpdb compact' to safely truncate active WAL.")