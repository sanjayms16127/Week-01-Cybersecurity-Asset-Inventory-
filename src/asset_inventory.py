"""
Cybersecurity Asset Inventory System
--------------------------------------
A command-line tool that lets a security administrator add, search,
update, delete, and display an organization's IT assets, classified
by asset type and security risk level.

Data is persisted to ../data/assets.json so the inventory survives
between runs.
"""

import json
import os
import sys

# ------------------------------------------------------------------
# Configuration / constants
# ------------------------------------------------------------------

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "assets.json")

ASSET_TYPES = ["Workstation", "Server", "Router", "Switch", "Application"]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
SECURITY_STATUSES = ["Secure", "Warning", "Vulnerable"]

LINE = "=" * 41
DIVIDER = "-" * 41


# ------------------------------------------------------------------
# Persistence helpers
# ------------------------------------------------------------------

def load_assets():
    """Load the asset list from the JSON data file, if it exists."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: could not read existing data file. Starting fresh.\n")
    return []


def save_assets(assets):
    """Write the asset list to the JSON data file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(assets, f, indent=2)


# ------------------------------------------------------------------
# Input validation helpers
# ------------------------------------------------------------------

def prompt_choice(label, options):
    """Prompt until the user enters one of the allowed options (case-insensitive)."""
    options_display = "/".join(options)
    while True:
        value = input(f"{label} ({options_display}): ").strip()
        for opt in options:
            if value.lower() == opt.lower():
                return opt
        print(f"  Invalid value. Please choose one of: {options_display}")


def prompt_nonempty(label):
    """Prompt until the user enters a non-empty value."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("  This field cannot be empty.")


def prompt_unique_id(assets, label="Asset ID"):
    """Prompt for an Asset ID that does not already exist in the inventory."""
    while True:
        asset_id = prompt_nonempty(label)
        if any(a["Asset ID"].lower() == asset_id.lower() for a in assets):
            print(f"  Asset ID '{asset_id}' already exists. Please enter a different ID.")
        else:
            return asset_id


# ------------------------------------------------------------------
# Core operations
# ------------------------------------------------------------------

def add_asset(assets):
    print("\n--- Add New Asset ---")
    asset = {
        "Asset ID": prompt_unique_id(assets),
        "Asset Name": prompt_nonempty("Asset Name"),
        "Asset Type": prompt_choice("Asset Type", ASSET_TYPES),
        "IP Address": prompt_nonempty("IP Address"),
        "Operating System": prompt_nonempty("Operating System"),
        "Department": prompt_nonempty("Owner/Department"),
        "Risk Level": prompt_choice("Risk Level", RISK_LEVELS),
        "Security Status": prompt_choice("Security Status", SECURITY_STATUSES),
    }
    assets.append(asset)
    save_assets(assets)
    print(f"\nAsset '{asset['Asset ID']}' added successfully.\n")


def find_asset_index(assets, asset_id):
    for i, a in enumerate(assets):
        if a["Asset ID"].lower() == asset_id.lower():
            return i
    return -1


def search_asset(assets):
    print("\n--- Search Asset ---")
    if not assets:
        print("No assets in inventory.\n")
        return
    term = input("Enter Asset ID or Asset Name to search: ").strip().lower()
    results = [
        a for a in assets
        if term in a["Asset ID"].lower() or term in a["Asset Name"].lower()
    ]
    if not results:
        print(f"No matching asset found for '{term}'.\n")
    else:
        print(f"\nFound {len(results)} matching asset(s):\n")
        display_assets(results, show_summary=False)


def update_asset(assets):
    print("\n--- Update Asset ---")
    if not assets:
        print("No assets in inventory.\n")
        return
    asset_id = input("Enter Asset ID to update: ").strip()
    idx = find_asset_index(assets, asset_id)
    if idx == -1:
        print(f"Asset ID '{asset_id}' not found.\n")
        return

    asset = assets[idx]
    print("Leave a field blank to keep its current value.\n")

    new_name = input(f"Asset Name [{asset['Asset Name']}]: ").strip()
    if new_name:
        asset["Asset Name"] = new_name

    new_type = input(f"Asset Type [{asset['Asset Type']}] ({'/'.join(ASSET_TYPES)}): ").strip()
    if new_type:
        match = next((t for t in ASSET_TYPES if t.lower() == new_type.lower()), None)
        if match:
            asset["Asset Type"] = match
        else:
            print("  Invalid Asset Type, keeping previous value.")

    new_ip = input(f"IP Address [{asset['IP Address']}]: ").strip()
    if new_ip:
        asset["IP Address"] = new_ip

    new_os = input(f"Operating System [{asset['Operating System']}]: ").strip()
    if new_os:
        asset["Operating System"] = new_os

    new_dept = input(f"Owner/Department [{asset['Department']}]: ").strip()
    if new_dept:
        asset["Department"] = new_dept

    new_risk = input(f"Risk Level [{asset['Risk Level']}] ({'/'.join(RISK_LEVELS)}): ").strip()
    if new_risk:
        match = next((r for r in RISK_LEVELS if r.lower() == new_risk.lower()), None)
        if match:
            asset["Risk Level"] = match
        else:
            print("  Invalid Risk Level, keeping previous value.")

    new_status = input(f"Security Status [{asset['Security Status']}] ({'/'.join(SECURITY_STATUSES)}): ").strip()
    if new_status:
        match = next((s for s in SECURITY_STATUSES if s.lower() == new_status.lower()), None)
        if match:
            asset["Security Status"] = match
        else:
            print("  Invalid Security Status, keeping previous value.")

    save_assets(assets)
    print(f"\nAsset '{asset['Asset ID']}' updated successfully.\n")


def delete_asset(assets):
    print("\n--- Delete Asset ---")
    if not assets:
        print("No assets in inventory.\n")
        return
    asset_id = input("Enter Asset ID to delete: ").strip()
    idx = find_asset_index(assets, asset_id)
    if idx == -1:
        print(f"Asset ID '{asset_id}' not found.\n")
        return
    confirm = input(f"Are you sure you want to delete '{asset_id}'? (y/n): ").strip().lower()
    if confirm == "y":
        removed = assets.pop(idx)
        save_assets(assets)
        print(f"Asset '{removed['Asset ID']}' deleted successfully.\n")
    else:
        print("Delete cancelled.\n")


def display_assets(assets, show_summary=True):
    print(LINE)
    print(" CYBERSECURITY ASSET INVENTORY")
    print(LINE)

    if not assets:
        print("No assets to display.")
        print(LINE)
        return

    for i, a in enumerate(assets):
        print(f"Asset ID        : {a['Asset ID']}")
        print(f"Asset Name      : {a['Asset Name']}")
        print(f"Asset Type      : {a['Asset Type']}")
        print(f"IP Address      : {a['IP Address']}")
        print(f"OS              : {a['Operating System']}")
        print(f"Department      : {a['Department']}")
        print(f"Risk Level      : {a['Risk Level']}")
        print(f"Status          : {a['Security Status']}")
        if i != len(assets) - 1:
            print(DIVIDER)

    if show_summary:
        print(LINE)
        print_summary(assets)
        print(LINE)
    else:
        print(LINE)


def print_summary(assets):
    total = len(assets)
    critical = sum(1 for a in assets if a["Risk Level"] == "Critical")
    high = sum(1 for a in assets if a["Risk Level"] == "High")
    medium = sum(1 for a in assets if a["Risk Level"] == "Medium")
    vulnerable = sum(1 for a in assets if a["Security Status"] == "Vulnerable")

    print(f"Total Assets : {total}")
    print(f"Critical Assets : {critical}")
    print(f"High Risk Assets : {high}")
    print(f"Medium Risk Assets : {medium}")
    print(f"Vulnerable Assets : {vulnerable}")


def security_summary(assets):
    print("\n--- Security Summary ---")
    if not assets:
        print("No assets in inventory.\n")
        return
    print_summary(assets)
    print()


def input_validation_tool(assets):
    """A standalone sandbox for checking whether a value would pass the
    system's validation rules, without adding or changing any asset."""
    print("\n--- Input Validation ---")
    print("Check whether a value would pass validation before you add or")
    print("update an asset. Nothing is saved or changed here.\n")
    print(f"Allowed Asset Types     : {', '.join(ASSET_TYPES)}")
    print(f"Allowed Risk Levels     : {', '.join(RISK_LEVELS)}")
    print(f"Allowed Security Status : {', '.join(SECURITY_STATUSES)}")

    while True:
        print("\nWhat would you like to validate?")
        print("  1. Asset ID (check for duplicates)")
        print("  2. Asset Type")
        print("  3. Risk Level")
        print("  4. Security Status")
        print("  5. Return to main menu")
        sub_choice = input("Enter choice (1-5): ").strip()

        if sub_choice == "1":
            asset_id = input("Enter Asset ID to check: ").strip()
            if not asset_id:
                print("  INVALID -> Asset ID cannot be empty.")
            elif any(a["Asset ID"].lower() == asset_id.lower() for a in assets):
                print(f"  INVALID -> '{asset_id}' already exists in the inventory.")
            else:
                print(f"  VALID -> '{asset_id}' is available to use.")
        elif sub_choice == "2":
            value = input("Enter Asset Type to check: ").strip()
            if any(value.lower() == t.lower() for t in ASSET_TYPES):
                print(f"  VALID -> '{value}' is an accepted Asset Type.")
            else:
                print(f"  INVALID -> '{value}' is not one of: {', '.join(ASSET_TYPES)}")
        elif sub_choice == "3":
            value = input("Enter Risk Level to check: ").strip()
            if any(value.lower() == r.lower() for r in RISK_LEVELS):
                print(f"  VALID -> '{value}' is an accepted Risk Level.")
            else:
                print(f"  INVALID -> '{value}' is not one of: {', '.join(RISK_LEVELS)}")
        elif sub_choice == "4":
            value = input("Enter Security Status to check: ").strip()
            if any(value.lower() == s.lower() for s in SECURITY_STATUSES):
                print(f"  VALID -> '{value}' is an accepted Security Status.")
            else:
                print(f"  INVALID -> '{value}' is not one of: {', '.join(SECURITY_STATUSES)}")
        elif sub_choice == "5":
            print()
            return
        else:
            print("  Invalid choice. Please enter a number between 1 and 5.")


# ------------------------------------------------------------------
# Menu / main loop
# ------------------------------------------------------------------

MENU = """
=========================================
 CYBERSECURITY ASSET INVENTORY SYSTEM
=========================================
1. Add Asset
2. Search Asset
3. Update Asset
4. Delete Asset
5. Display All Assets
6. Security Summary
7. Input Validation
8. Exit
=========================================
"""


def main():
    assets = load_assets()
    print("Cybersecurity Asset Inventory System")
    print(f"Loaded {len(assets)} existing asset(s) from data file.")

    while True:
        print(MENU)
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_asset(assets)
        elif choice == "2":
            search_asset(assets)
        elif choice == "3":
            update_asset(assets)
        elif choice == "4":
            delete_asset(assets)
        elif choice == "5":
            display_assets(assets)
        elif choice == "6":
            security_summary(assets)
        elif choice == "7":
            input_validation_tool(assets)
        elif choice == "8":
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 8.\n")


if __name__ == "__main__":
    main()
