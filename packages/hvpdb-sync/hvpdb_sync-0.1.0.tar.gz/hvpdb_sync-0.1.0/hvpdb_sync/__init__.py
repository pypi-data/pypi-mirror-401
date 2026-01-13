import typer
from rich.console import Console
import json
import csv
import sys
from typing import Optional
app = typer.Typer(help='Data Import/Export Connectors')
console = Console()

@app.command(name='import-csv')
def import_csv(target: str=typer.Argument(..., help='Database Path'), file: str=typer.Argument(..., help='CSV File'), group: str=typer.Argument(..., help='Target Group'), pk: str=typer.Option(None, help='Primary Key Column (used as _id)')):
    from hvpdb.utils import connect_db
    try:
        db = connect_db(target)
        count = 0
        with open(file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if pk and pk in row:
                    row['_id'] = row[pk]
                db.group(group).insert(row)
                count += 1
        db.commit()
        console.print(f'[green]Imported {count} rows from {file} into {group}[/green]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@app.command(name='export-csv')
def export_csv(target: str=typer.Argument(..., help='Database Path'), group: str=typer.Argument(..., help='Source Group'), file: str=typer.Argument(..., help='Output CSV File')):
    from hvpdb.utils import connect_db
    try:
        db = connect_db(target)
        docs = db.group(group).get_all()
        if not docs:
            console.print('[yellow]No documents found in group.[/yellow]')
            return
        keys = set()
        for d in docs:
            keys.update(d.keys())
        fieldnames = sorted(list(keys))
        with open(file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for d in docs:
                writer.writerow(d)
        console.print(f'[green]Exported {len(docs)} docs to {file}[/green]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@app.command(name='ndjson')
def import_ndjson(target: str=typer.Argument(..., help='Database Path'), file: str=typer.Argument(..., help='NDJSON File'), group: str=typer.Argument(..., help='Target Group')):
    from hvpdb.utils import connect_db
    try:
        db = connect_db(target)
        count = 0
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    doc = json.loads(line)
                    db.group(group).insert(doc)
                    count += 1
        db.commit()
        console.print(f'[green]Imported {count} docs from {file}[/green]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')