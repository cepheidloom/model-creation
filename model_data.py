import os
os.add_dll_directory(r"C:/Users/Manish-Pratap.Singh/Tools/Graphviz-14.1.2-win64/bin")
os.environ["PATH"] += os.pathsep + r"C:/Users/Manish-Pratap.Singh/Tools/Graphviz-14.1.2-win64/bin"

from eralchemy2 import render_er

schema_markdown = """
[Dim_Client]
*ClientID
Lol
ClientName

[Fact_Orders]
*OrderID
Lol
ClientID

TotalAmount

Fact_Orders *--1 Dim_Client
"""

try:
    render_er(schema_markdown.split('\n'), '_DATA_AND_OUTPUTS/client_er_diapgram.png')
    print("Success! ER diagram generate.")
except Exception as e:
    print(f"An error occured: {e}")