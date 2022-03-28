# [Fortune Br] - Bom Application

Generate bill of materials of an article for calculating the cost and displays the report. Detailed report can be exported in a styled Excel format (bulk exporting is supported as well). Also, bulk cost report in CSV file format is exportable for analysing purpose. 

The latest bom heirarchy and items data from SAP is used to update the application database. Other tables can also be updated within the application like OsCharges, Price Structure.

## Look into Code
- Python 3.10 - Base language
- PyQt6 - For GUI
- SQL Alchemy - Database management
- pyodbc - For MSSQL database connection
- pandas - A lot of complex works just got simplified
- xlsxwriter - For styled excel report

<br/>

## Prerequisite and Setup
1. Download and install [ODBC Driver 17 for SQL Server](https://go.microsoft.com/fwlink/?linkid=2187214)
2. Open and install the application: `Bom-[version]-win64.msi`
4. Goto the installed directory and update `config.ini` file if the server credentials are different (Database name must be set to "harpy_eagle" in the sql server)

<br/>
<br/>

Design and developed by kalaLokia  (#just me, that's why it is so messy)