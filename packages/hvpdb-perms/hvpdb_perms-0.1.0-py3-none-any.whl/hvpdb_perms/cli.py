import typer
from rich.console import Console
from typing import Optional
from hvpdb.utils import connect_db
from .manager import PermissionManager
app = typer.Typer(help='Permission Management Plugin')
console = Console()

@app.command()
def create_user(username: str=typer.Argument(..., help='Username'), password: str=typer.Argument(..., help='Password'), role: str=typer.Argument('user', help='Role (user/admin)'), target: str=typer.Argument(..., help='Database Path'), db_password: Optional[str]=typer.Argument(None, help='DB Password')):
    try:
        db = connect_db(target, db_password)
        pm = PermissionManager(db)
        pm.create_user(username, password, role)
        db.commit()
        console.print(f'[green]User {username} created.[/green]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@app.command()
def grant(username: str=typer.Argument(..., help='Username'), group: str=typer.Argument(..., help='Group Name'), target: str=typer.Argument(..., help='Database Path'), db_password: Optional[str]=typer.Argument(None, help='DB Password')):
    try:
        db = connect_db(target, db_password)
        pm = PermissionManager(db)
        pm.grant(username, group)
        db.commit()
        console.print(f'[green]Granted {group} to {username}.[/green]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@app.command()
def revoke(username: str=typer.Argument(..., help='Username'), group: str=typer.Argument(..., help='Group Name'), target: str=typer.Argument(..., help='Database Path'), db_password: Optional[str]=typer.Argument(None, help='DB Password')):
    try:
        db = connect_db(target, db_password)
        pm = PermissionManager(db)
        pm.revoke(username, group)
        db.commit()
        console.print(f'[green]Revoked {group} from {username}.[/green]')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@app.command('list')
def list_users(target: str=typer.Argument(..., help='Database Path'), db_password: Optional[str]=typer.Argument(None, help='DB Password')):
    try:
        db = connect_db(target, db_password)
        pm = PermissionManager(db)
        users = pm.list_users()
        from rich.table import Table
        table = Table(title='Users')
        table.add_column('Username')
        table.add_column('Role')
        table.add_column('Groups')
        for u, data in users.items():
            table.add_row(u, data.get('role', 'user'), str(data.get('groups', [])))
        console.print(table)
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')