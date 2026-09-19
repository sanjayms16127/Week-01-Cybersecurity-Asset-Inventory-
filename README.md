# Week 01 — Cybersecurity Asset Inventory System

A command-line Python application for managing an organization's IT asset
inventory, built for Weekly Mini Project 01.

## Problem Statement

An organization maintains several IT assets such as computers, servers,
routers, switches, and software applications. Managing these assets
manually makes it difficult to identify the assets, track their security
status, and determine which assets require immediate attention.

This system lets a security administrator **add, search, update, delete,
and display** information about the organization's IT assets, classified
by **asset type** and **security risk level**.

## Features

- Add a new asset
- Search assets by ID or name
- Update any field on an existing asset
- Delete an asset (with confirmation)
- Display all assets in the required formatted layout
- Security summary: total assets, Critical/High/Medium risk counts, and
  Vulnerable asset count
- **Input Validation** menu — a standalone sandbox where you can test
  whether an Asset ID, Asset Type, Risk Level, or Security Status would
  pass validation, without adding, changing, or deleting any asset
- Data persists between runs in `data/assets.json`

## Asset Fields

| Field | Description |
|---|---|
| Asset ID | Unique identifier |
| Asset Name | Descriptive name |
| Asset Type | Workstation / Server / Router / Switch / Application |
| IP Address | Network address |
| Operating System | OS running on the asset |
| Owner/Department | Owning department |
| Risk Level | Low / Medium / High / Critical |
| Security Status | Secure / Warning / Vulnerable |

## Repository Structure

```
Week-01-Cybersecurity-Asset-Inventory/
├── src/
│   └── asset_inventory.py
├── data/
│   └── assets.json
├── tests/
│   └── test_cases.md
├── screenshots/
│   ├── 01-add-asset.png
│   ├── 02-display-assets.png
│   ├── 03-search-asset.png
│   ├── 04-update-asset.png
│   ├── 05-delete-asset.png
│   ├── 06-security-summary.png
│   └── 07-input-validation.png
└── README.md
```

## How to Run

Requires Python 3.7+, no external dependencies.

```bash
cd src
python3 asset_inventory.py
```

You'll see a menu:

```
1. Add Asset
2. Search Asset
3. Update Asset
4. Delete Asset
5. Display All Assets
6. Security Summary
7. Input Validation
8. Exit
```

The repo ships with `data/assets.json` pre-populated with the sample data
from the assignment (A101, A102, A103), so you can run option `6`
immediately to see the expected output.

## Sample Output

```
=========================================
 CYBERSECURITY ASSET INVENTORY
=========================================
Asset ID        : A101
Asset Name      : HR-PC-01
Asset Type      : Workstation
IP Address      : 192.168.1.10
OS              : Windows 11
Department      : HR
Risk Level      : Medium
Status          : Secure
-----------------------------------------
Asset ID        : A102
Asset Name      : Web-Server
Asset Type      : Server
IP Address      : 192.168.1.20
OS              : Ubuntu
Department      : IT
Risk Level      : Critical
Status          : Vulnerable
-----------------------------------------
Asset ID        : A103
Asset Name      : Core-Router
Asset Type      : Router
IP Address      : 192.168.1.1
OS              : Cisco IOS
Department      : Network
Risk Level      : High
Status          : Warning
=========================================
Total Assets : 3
Critical Assets : 1
High Risk Assets : 1
Medium Risk Assets : 1
Vulnerable Assets : 1
=========================================
```

## Testing

See [`tests/test_cases.md`](tests/test_cases.md) for the manual test cases
used to produce the screenshots in `screenshots/`.

## Author

Weekly Mini Project — Cybersecurity Asset Inventory System
