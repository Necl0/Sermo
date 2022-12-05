import typer
from rich import print
import json
import datetime
import webbrowser
import random
import string
import os
import csv

app = typer.Typer()
bm = typer.Typer()
app.add_typer(bm, name="bm")


@app.command()
def init():
    os.system("cls" if os.name == "nt" else "clear")

    print("\nWelcome to [bold blue]Bookmarkr[/bold blue], the CLI bookmark tool! Type 'exit' to quit.\n")


@app.command()
def exit():
    os.system("cls" if os.name == "nt" else "clear")

    print('\n[bold red]Exiting...[/bold red]')
    raise typer.Exit()


@bm.command()
def add(
        name: str = typer.Argument(..., help="Name of the bookmark"),
        url: str = typer.Argument(..., help="bookmark URL"),
        tag: str = typer.Argument(..., help="Tag for the bookmark")
        ):
    """Add a bookmark to the cli to be used later"""
    os.system("cls" if os.name == "nt" else "clear")

    if name == "":
        print("Invalid name. Please enter a name.")
        return

    with open("banned.txt", "r") as f:
        banned = f.read().splitlines()
        for word in banned:
            if word in name:
                print(f"\n[red]Error [/red]: name contains banned language. Please remove[red] {word}[/red] from the name.\n")
                return

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)

        if name in bms:
            print(f"\n[red] Error [/red]: bookmark {name} already exists. Please choose a different name.\n")
            return

        bms[name] = {
            "id": "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
            "name": name,
            "url": url,
            "tag": tag,
            "last modified": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        with open("bookmarks.json", "w") as f:
            json.dump(bms, f, indent=4)
            print(f"\nAdded bookmark[blue] {name} [/blue]to bookmarks.json\n")


@bm.command()
def list():

    # list all bookmarks in table view
    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:

        bms = json.load(f)
        print(f"\n[bold blue]Bookmarks[/bold blue] : {len(bms)}\n")
        print(f"{'ID':<20}{'Name':<20}{'URL':<40}{'Tag':<10}{'Last Modified':<20}")
        print("-" * 100)
        for bm in bms.values():
            print(f"{bm['id']:<20}{bm['name']:<20}{bm['url']:<40}{bm['tag']:<10}{bm['last modified']:<20}")

        print("\n")


@bm.command()
def delete(name: str = typer.Argument(..., help="Name of the bm to delete")):
    """Delete a bm from bookmarks.json"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            del bms[name]
            with open("bookmarks.json", "w") as f:
                json.dump(bms, f, indent=4)
                print(f"\nDeleted bookmark[blue] {name} [/blue]from bookmarks.json\n")
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command()
def view(name: str = typer.Argument(..., help="Name of the bm to open")):
    """Open a bookmark in the browser"""

    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            webbrowser.open(bms[name]["url"])
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command()
def search(query: str = typer.Argument(..., help="Query to search for")):
    """Search for a bookmark"""

    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        for bm in bms:
            if query in bm:
                print(f"\nFound bookmark [bold blue]{bm}[/bold blue]")
                for key, value in bms[bm].items():
                    print(f"{key}: {value}")

                print()
                return

    print(f"\n No bookmark found for query [bold blue]{query} [/bold blue]\n")


@bm.command()
def update(name: str = typer.Argument(..., help="Name of the bm to update")):
    """Update a bookmark"""

    os.system("cls" if os.name == "nt" else "clear")

    # update a bm
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            print(f"Updating bookmark [blue] {name} [/blue]")
            url = input("Enter new URL: ")
            tag = input("Enter new tag: ")
            bms[name]["url"] = url
            bms[name]["tag"] = tag
            with open("bookmarks.json", "w") as f:
                json.dump(bms, f, indent=4)
                print(f"\nUpdated bookmark [blue] {name} [/blue]to bookmarks.json\n")
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command()
def clear():
    """Clear all bookmarks"""

    os.system("cls" if os.name == "nt" else "clear")

    # check if you want to proceed
    print("""\nAre you sure you want to clear all bookmarks? [bold red]This cannot be undone.[/bold red]
    Type [bold blue]yes[/bold blue] to proceed or [bold blue]no[/bold blue] to cancel.\n""")


    if input(">>> ").lower().strip() == "yes":
        with open("bookmarks.json", "w") as f:
            json.dump({}, f, indent=4)
            print("Cleared bookmarks")


@bm.command()
def export_csv():
    """Export bookmarks to a CSV file"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        with open("bookmarks.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "URL", "Tag", "Last Modified"])
            for bm in bms.values():
                writer.writerow([bm["id"], bm["name"], bm["url"], bm["tag"], bm["last modified"]])

        print("\nExported bookmarks to bookmarks.csv\n")


@bm.command()
def import_csv():
    """Import bookmarks from bookmarks.csv file"""
    with open("bookmarks.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        bms = {}
        for row in reader:
            bms[row[1]] = {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "tag": row[3],
                "last modified": row[4]
            }

        with open("bookmarks.json", "w") as f:
            json.dump(bms, f, indent=4)
            print("\nImported bookmarks from [yellow]bookmarks.csv[/yellow]\n")


if __name__ == "__main__":
    app()
