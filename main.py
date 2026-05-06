from rich.console import Console
from datetime import datetime

try:
    from structures import MyHashTable, BSTree, BSTIterator
    console = Console()
    
    console.print("Modules imported successfully: ", style="green")
except ImportError as e:
    print(f"Import error {e}")
    exit()


def main():


    console.print("Start testing MyHashTable", style="yellow")

    try:
        table = MyHashTable(capacity=7)
        console.print("An instance of the MyHashTable class has been successfully created ", style="green")
    except Exception as e:
        console.print(f" Failed to create object: {e}", style="red")

    table["apple"] = 10
    table["banana"] = 20
    console.print("Data has been added to the hash table ", style="green")

    console.print("Start recording audit results to the log.txt file")

    try:
        with open("log.txt", "w", encoding="utf-8") as f:

            f.write(f"Report for {datetime.now()}\n")

            f.write(f"Hash table: number of elements: {len(table)}\n")
        
        console.print("Data successfully written to log.txt file ", style="green" )
    except Exception as e:
        console.print(f"File writing error: {e}", style="red")

    console.print("Checking for missing key search", style="yellow")

    try:
        value = table["pear"]
    except KeyError as e:
        console.print(f"Error: Key 'pear' not found: {e}", style="red")


    console.print("Download JSON ", style="yellow")

    tree = BSTree()
    file_name = "tree.json"

    try:
        tree.load_from_json(file_name)
        console.print("Data loaded from {file_name}", style="green")
    except FileNotFoundError:
        console.print("No previous entries found.", style="red")


    console.print("Adding new transactions", style="yellow")
    dt = datetime(2026, 11, 11, 14, 20)
    dt1 = datetime(2026, 12, 12, 20, 14)

    tree.insert(dt.timestamp(), {"amount": 400, "desc": "TV"})
    tree.insert(dt1.timestamp(), {"amount": 500, "desc": "Cafe"})

    try:
        tree.save_to_json(file_name)
        console.print(f"Current state saved in {file_name}", style="green")
    except Exception as e:
        console.print("Saving error: {e}", style="red")











    

if __name__ == "__main__":
    main()