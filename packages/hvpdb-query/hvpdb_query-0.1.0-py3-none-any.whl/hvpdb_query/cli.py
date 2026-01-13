import typer
import os
from typing import Optional
from rich.console import Console
from rich.table import Table
from .parser import PolyglotParser
from .engine import QueryEngine
from hvpdb.utils import connect_db
app = typer.Typer(help='Polyglot Query Engine (SQL, Mongo, Redis)')
console = Console()

@app.command(name='run')
def run_query(query: str=typer.Argument(..., help='Query string (SQL, Mongo, Redis)'), target: str=typer.Argument(..., help='Database Path/URI'), password: Optional[str]=typer.Argument(None, help='Database Password')):
    try:
        db = connect_db(target, password)
    except Exception as e:
        console.print(f'[red]Connection Failed: {e}[/red]')
        raise typer.Exit(1)
    parser = PolyglotParser()
    engine = QueryEngine(db)
    try:
        plan = parser.parse(query)
        if not plan:
            console.print('[red]Invalid Query Syntax or Unsupported Language.[/red]')
            raise typer.Exit(1)
        results = engine.execute(plan)
        if isinstance(results, list):
            console.print(f'[green]Found {len(results)} results.[/green]')
            if results:
                cols = set()
                for r in results[:20]:
                    if isinstance(r, dict):
                        cols.update(r.keys())
                if cols:
                    cols = sorted(list(cols))
                    table = Table(show_header=True)
                    for c in cols:
                        table.add_column(c)
                    for r in results:
                        if isinstance(r, dict):
                            table.add_row(*[str(r.get(c, '')) for c in cols])
                        else:
                            pass
                    console.print(table)
                else:
                    console.print(results)
        else:
            console.print(f'[green]Result:[/green] {results}')
    except Exception as e:
        console.print(f'[red]Query Execution Error: {e}[/red]')
        raise typer.Exit(1)

@app.command(name='parse')
def parse_query(query: str=typer.Argument(..., help='Query string')):
    parser = PolyglotParser()
    try:
        plan = parser.parse(query)
        console.print(plan)
    except Exception as e:
        console.print(f'[red]Parse Error: {e}[/red]')

@app.command(name='explain')
def explain_query(query: str=typer.Argument(..., help='Query string')):
    parser = PolyglotParser()
    try:
        plan = parser.parse(query)
        console.print(Panel(str(plan), title='Execution Plan'))
        console.print('[dim]Note: Full cost estimation not implemented yet.[/dim]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@app.command(name='compat')
def show_compat():
    from rich.panel import Panel
    console.print(Panel('\n        [bold]SQL Subset:[/bold] SELECT * FROM table WHERE ...\n        [bold]MongoDB-style:[/bold] db.collection.find({...})\n        [bold]Redis-style:[/bold] GET key, SET key value\n        ', title='Compatibility Matrix'))

@app.command(name='repl')
def query_repl(target: str=typer.Argument(..., help='Database Path'), password: Optional[str]=typer.Argument(None, help='Password')):
    try:
        db = connect_db(target, password)
    except Exception as e:
        console.print(f'[red]Connection Failed: {e}[/red]')
        raise typer.Exit(1)
    parser = PolyglotParser()
    engine = QueryEngine(db)
    console.print(f'[bold cyan]HVPDB Query REPL ({target})[/bold cyan]')
    console.print("Type 'exit' to quit.")
    while True:
        try:
            q = console.input('[bold green]query > [/bold green]')
            if q.strip().lower() in ('exit', 'quit'):
                break
            if not q.strip():
                continue
            plan = parser.parse(q)
            if not plan:
                console.print('[red]Invalid Query[/red]')
                continue
            results = engine.execute(plan)
            console.print(results)
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f'[red]Error: {e}[/red]')

@app.command(name='test')
def test_queries(target: str=typer.Argument(..., help='Database Path'), password: Optional[str]=typer.Argument(None, help='Password')):
    try:
        db = connect_db(target, password)
    except Exception as e:
        console.print(f'[red]Connection Failed: {e}[/red]')
        raise typer.Exit(1)
    engine = QueryEngine(db)
    parser = PolyglotParser()
    tests = ['SELECT * FROM users', "db.users.find({'role': 'admin'})", 'GET config_key']
    for q in tests:
        console.print(f'[bold]Running:[/bold] {q}')
        try:
            plan = parser.parse(q)
            res = engine.execute(plan)
            console.print(f'[green]OK[/green] ({(len(res) if isinstance(res, list) else 1)} results)')
        except Exception as e:
            console.print(f'[red]Fail:[/red] {e}')