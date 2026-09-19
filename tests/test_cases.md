# Test Cases — Cybersecurity Asset Inventory System

These are manual test cases to run against `src/asset_inventory.py`.
For each one, take a screenshot of the terminal output and save it in
`screenshots/` with the matching filename.

## TC-01 — Add Asset (`01-add-asset.png`)
**Steps:**
1. Run the program.
2. Choose option `1` (Add Asset) and enter the sample data from the
   assignment. Repeat three times for A101, A102, and A103.

**Expected result:** Each asset is confirmed with "Asset '<ID>' added
successfully." and saved to `data/assets.json`.

---

## TC-02 — Display All Assets (`02-display-assets.png`)
**Steps:**
1. Choose option `5` (Display All Assets).

**Expected result:** All assets print in the formatted layout, followed by
the summary block:
```
Total Assets : 3
Critical Assets : 1
High Risk Assets : 1
Medium Risk Assets : 1
Vulnerable Assets : 1
```

---

## TC-03 — Search Asset (`03-search-asset.png`)
**Steps:**
1. Choose option `2` (Search Asset).
2. Search for `A102` and separately for `Web-Server`.

**Expected result:** The matching asset (Web-Server, Critical, Vulnerable)
is displayed. Searching for a non-existent ID (e.g. `A999`) returns "No
matching asset found."

---

## TC-04 — Update Asset (`04-update-asset.png`)
**Steps:**
1. Choose option `3` (Update Asset).
2. Enter `A103` and change Security Status from `Warning` to `Secure`.

**Expected result:** "Asset 'A103' updated successfully." and the change is
reflected in a subsequent Display All Assets call.

---

## TC-05 — Delete Asset (`05-delete-asset.png`)
**Steps:**
1. Choose option `4` (Delete Asset).
2. Enter `A101` and confirm with `y`.

**Expected result:** "Asset 'A101' deleted successfully." and Total Assets
drops to 2 in the next display/summary.

---

## TC-06 — Security Summary (`06-security-summary.png`)
**Steps:**
1. Choose option `6` (Security Summary).

**Expected result:** Correct counts for Total, Critical, High, Medium, and
Vulnerable assets based on current inventory state.

---

## TC-07 — Input Validation (`07-input-validation.png`)
**Steps:**
1. Choose option `7` (Input Validation) from the main menu.
2. Check Asset ID `A102` (already exists) and then `A104` (available).
3. Check Asset Type `Laptop` (invalid) and then `Workstation` (valid).
4. Check Risk Level `Extreme` (invalid) and then `Low` (valid).
5. Check Security Status `Unknown` (invalid) and then `Secure` (valid).
6. Choose `5` to return to the main menu.

**Expected result:** Each check reports `VALID` or `INVALID` against the
allowed values, without adding, changing, or deleting anything in the
inventory — this menu is a read-only sandbox for testing values.
