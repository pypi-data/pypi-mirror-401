import typer
import os
import json
import time
from rich.console import Console
from rich.table import Table
app = typer.Typer(help='HVPDB Migration Tool')
console = Console()
MIGRATION_DIR = './migrations'

@app.command(name='init')
def init_migration():
    if not os.path.exists(MIGRATION_DIR):
        os.makedirs(MIGRATION_DIR)
        console.print(f'[green]Initialized migrations in {MIGRATION_DIR}[/green]')
    else:
        console.print('[yellow]Migration directory already exists.[/yellow]')

@app.command(name='create')
def create_migration(name: str=typer.Argument(..., help='Migration Name')):
    if not os.path.exists(MIGRATION_DIR):
        init_migration()
    ts = int(time.time())
    filename = f'{ts}_{name}.json'
    path = os.path.join(MIGRATION_DIR, filename)
    template = {'name': name, 'timestamp': ts, 'up': [{'op': 'update', 'group': 'users', 'filter': {}, 'update': {'version': 2}}], 'down': []}
    with open(path, 'w') as f:
        json.dump(template, f, indent=2)
    console.print(f'[green]Created migration: {path}[/green]')

@app.command(name='up')
def apply_migrations(target: str=typer.Argument(..., help='Database Path')):
    if not os.path.exists(MIGRATION_DIR):
        console.print('[yellow]No migrations directory found.[/yellow]')
        return
    try:
        from hvpdb.utils import connect_db
        db = connect_db(target)
        migration_group = db.group('_migrations')
        applied = {doc['name'] for doc in migration_group.find()}
        files = sorted([f for f in os.listdir(MIGRATION_DIR) if f.endswith('.json')])
        count = 0
        for f in files:
            path = os.path.join(MIGRATION_DIR, f)
            with open(path, 'r') as json_file:
                data = json.load(json_file)
                name = data['name']
                if name in applied:
                    continue
                console.print(f'Applying {name}...')
                for op in data.get('up', []):
                    grp_name = op.get('group')
                    if not grp_name:
                        continue
                    grp = db.group(grp_name)
                    action = op.get('op')
                    if action == 'insert':
                        grp.insert(op['data'])
                    elif action == 'update':
                        grp.update(op.get('filter', {}), op['update'])
                    elif action == 'delete':
                        grp.delete(op.get('filter', {}))
                    elif action == 'create_index':
                        grp.create_index(op['field'], unique=op.get('unique', False))
                migration_group.insert({'name': name, 'filename': f, 'applied_at': time.time()})
                count += 1
        db.commit()
        if count > 0:
            console.print(f'[green]Successfully applied {count} migrations.[/green]')
        else:
            console.print('[green]Database is up to date.[/green]')
    except Exception as e:
        console.print(f'[red]Migration failed: {e}[/red]')

@app.command(name='status')
def migration_status(target: str=typer.Argument(..., help='Database Path')):
    try:
        from hvpdb.core import HVPDB
        password = os.environ.get('HVPDB_PASSWORD')
        if not target.startswith('hvp://') and (not target.endswith('.hvp')) and (not target.endswith('.hvdb')):
            target += '.hvp'
        db = HVPDB(target, password)
        migration_group = db.group('_migrations')
        applied = {doc['name'] for doc in migration_group.find()}
        if not os.path.exists(MIGRATION_DIR):
            console.print('[yellow]No migrations directory found.[/yellow]')
            return
        files = sorted([f for f in os.listdir(MIGRATION_DIR) if f.endswith('.json')])
        table = Table(title='Migration Status')
        table.add_column('Migration', style='cyan')
        table.add_column('Status', style='green')
        for f in files:
            with open(os.path.join(MIGRATION_DIR, f), 'r') as json_file:
                data = json.load(json_file)
                name = data['name']
                status = '[green]Applied[/green]' if name in applied else '[red]Pending[/red]'
                table.add_row(name, status)
        console.print(table)
    except Exception as e:
        console.print(f'[red]Error checking status: {e}[/red]')