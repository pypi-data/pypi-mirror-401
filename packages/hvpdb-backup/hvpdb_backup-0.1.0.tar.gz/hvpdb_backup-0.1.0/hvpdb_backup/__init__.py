import typer
import shutil
import os
import datetime
from typing import Optional
from rich.console import Console
from hvpdb.utils import normalize_target
app = typer.Typer(help='HVPDB Backup Manager')
console = Console()

@app.command(name='create')
def create_backup(target: str=typer.Argument(..., help='Database Path'), name: Optional[str]=typer.Argument(None, help='Backup Name/Tag'), output_dir: str=typer.Argument('./backups', help='Output Directory')):
    target = normalize_target(target)
    if not os.path.exists(target):
        console.print(f"[red]Database '{target}' not found.[/red]")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'{name}_{timestamp}.hvp' if name else f'backup_{timestamp}.hvp'
    dest = os.path.join(output_dir, backup_name)
    try:
        if os.path.isdir(target):
            shutil.copytree(target, dest)
        else:
            shutil.copy2(target, dest)
        console.print(f'[green]Backup created: {dest}[/green]')
    except Exception as e:
        console.print(f'[red]Backup failed: {e}[/red]')

@app.command(name='list')
def list_backups(output_dir: str=typer.Argument('./backups', help='Backup Directory')):
    if not os.path.exists(output_dir):
        console.print('No backup directory found.')
        return
    files = os.listdir(output_dir)
    for f in files:
        console.print(f'- {f}')

@app.command(name='restore')
def restore_backup(backup_file: str=typer.Argument(..., help='Path to backup file'), target: str=typer.Argument(..., help='Restore destination')):
    if not os.path.exists(backup_file):
        console.print(f"[red]Backup file '{backup_file}' not found.[/red]")
        return
    if os.path.exists(target):
        if not typer.confirm(f"Overwrite existing '{target}'?"):
            return
    try:
        if os.path.isdir(backup_file):
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.copytree(backup_file, target)
        else:
            shutil.copy2(backup_file, target)
        console.print(f'[green]Restored to {target}[/green]')
    except Exception as e:
        console.print(f'[red]Restore failed: {e}[/red]')