import typer
from rich.console import Console
from rich.live import Live
from rich.table import Table
import time
import os
import datetime
from typing import Optional
app = typer.Typer(help='HVPDB Observability Tools')
console = Console()

@app.command(name='top')
def show_metrics(target: str=typer.Argument(..., help='Database Path')):
    if not target.startswith('hvp://') and (not target.endswith('.hvp')) and (not target.endswith('.hvdb')):
        target += '.hvp'

    def generate_table():
        table = Table(title=f'HVPDB Metrics: {os.path.basename(target)}')
        table.add_column('Metric', style='cyan')
        table.add_column('Value', style='green')
        if os.path.exists(target):
            size = os.path.getsize(target)
            mtime = os.path.getmtime(target)
            last_modified = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            table.add_row('Size', f'{size / 1024:.2f} KB')
            table.add_row('Last Modified', last_modified)
            table.add_row('Status', 'Active')
        else:
            table.add_row('Status', '[red]Not Found[/red]')
        return table
    with Live(generate_table(), refresh_per_second=1) as live:
        try:
            while True:
                time.sleep(1)
                live.update(generate_table())
        except KeyboardInterrupt:
            pass

@app.command(name='audit')
def show_audit_log(target: str=typer.Argument(..., help='Database Path'), group_name: Optional[str]=typer.Argument(None, help='Group Name (Optional)')):
    try:
        db = connect_db(target)
        table = Table(title='Audit Log (WAL)')
        table.add_column('Timestamp', style='dim')
        table.add_column('Group', style='blue')
        table.add_column('Operation', style='yellow')
        table.add_column('Doc ID', style='cyan')
        groups = [group_name] if group_name else db.get_all_groups()
        for g_name in groups:
            grp = db.group(g_name)
            logs = grp.get_audit_trail(limit=10)
            for log in logs:
                ts = log.get('timestamp', 0)
                dt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                table.add_row(dt, log.get('group', g_name), log.get('op', 'unknown'), log.get('doc_id', 'N/A'))
        console.print(table)
    except Exception as e:
        console.print(f'[red]Error reading audit log: {e}[/red]')