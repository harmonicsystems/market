#!/usr/bin/env python3
"""Generate the Kinderhook Farmers' Market content management spreadsheet."""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from datetime import date, timedelta

wb = openpyxl.Workbook()

# Shared styles
header_font = Font(name="Arial", bold=True, size=11, color="FFFFFF")
header_fill = PatternFill(start_color="1A1A1A", end_color="1A1A1A", fill_type="solid")
orange_fill = PatternFill(start_color="F26A2A", end_color="F26A2A", fill_type="solid")
teal_fill = PatternFill(start_color="2AAFCE", end_color="2AAFCE", fill_type="solid")
cream_fill = PatternFill(start_color="FFF9F0", end_color="FFF9F0", fill_type="solid")
green_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
yellow_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
thin_border = Border(
    left=Side(style="thin", color="DDDDDD"),
    right=Side(style="thin", color="DDDDDD"),
    top=Side(style="thin", color="DDDDDD"),
    bottom=Side(style="thin", color="DDDDDD"),
)
wrap_alignment = Alignment(wrap_text=True, vertical="top")
center_alignment = Alignment(horizontal="center", vertical="center")


def style_headers(ws, num_cols):
    for col in range(1, num_cols + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def style_data_rows(ws, num_cols):
    for row in ws.iter_rows(min_row=2, max_col=num_cols):
        for cell in row:
            cell.border = thin_border
            cell.alignment = wrap_alignment
            # Alternate row shading
            if cell.row % 2 == 0:
                cell.fill = cream_fill


# ─── Tab 1: Weekly Schedule ───

ws1 = wb.active
ws1.title = "Weekly Schedule"
ws1.sheet_properties.tabColor = "F26A2A"

headers_1 = [
    "Date",
    "Display Date",
    "Theme",
    "Note",
    "Music Act",
    "Music Time",
    "Special Event Name",
    "Special Event Time",
    "Special Event Description",
    "Guest Vendors",
    "Community Partners",
    "Regular Vendors",
    "Status",
]
ws1.append(headers_1)

# Column widths
widths_1 = [14, 28, 20, 18, 20, 20, 24, 16, 34, 34, 30, 34, 12]
for i, w in enumerate(widths_1, 1):
    ws1.column_dimensions[get_column_letter(i)].width = w

# 2026 season music lineup (10am–12pm each Saturday).
music_lineup = {
    "2026-05-02": "Alley Cats",
    "2026-05-09": "Scott Stockman",
    "2026-05-16": "Mike Pagnani",
    "2026-05-23": "Alejandra Maciel & Friend",
    "2026-05-30": "Jasperoo",
    "2026-06-06": "The Sound of Somewhere",
    "2026-06-13": "Scott Stockman",
    "2026-06-20": "Alejandra Maciel & Friend",
    "2026-06-27": "Jasperoo",
    "2026-07-04": "Brad & Friends (official title to come)",
    "2026-07-11": "Scott Stockman",
    "2026-07-18": "The Last Pangeans",
    "2026-07-25": "Jasperoo",
    "2026-08-01": "Alley Cats",
    "2026-08-08": "Scott Stockman",
    "2026-08-15": "Too Lazy Boys",
    "2026-08-22": "Jasperoo",
    "2026-08-29": "The Sound of Somewhere",
    "2026-09-05": "Mike Pagnani",
    "2026-09-12": "Scott Stockman",
    "2026-09-19": "Jasperoo",
    "2026-09-26": "Alley Cats",
    "2026-10-03": "Mike Pagnani",
    "2026-10-10": "Scott Stockman & Friends",
    "2026-10-17": "Monty Bopp",
    "2026-10-24": "Alejandra Maciel & Friend",
    "2026-10-31": "TC",
}

# Pre-fill Saturdays for 2026 season (May 2 - Oct 31)
season_start = date(2026, 5, 2)
season_end = date(2026, 10, 31)
current = season_start
row_num = 2
while current <= season_end:
    iso = current.strftime("%Y-%m-%d")
    ws1.cell(row=row_num, column=1, value=iso)
    # Display date
    ws1.cell(
        row=row_num,
        column=2,
        value=current.strftime("%A, %B %-d, %Y"),
    )
    # Default note
    ws1.cell(row=row_num, column=4, value="Rain or Shine")
    # Pre-fill music from 2026 lineup
    if iso in music_lineup:
        ws1.cell(row=row_num, column=5, value=music_lineup[iso])
        ws1.cell(row=row_num, column=6, value="10:00am - 12:00pm")
    # Default status
    ws1.cell(row=row_num, column=13, value="Draft")
    current += timedelta(weeks=1)
    row_num += 1

# 2026 weekly vendors (present every Saturday).
weekly_vendors_list = (
    "Albany Distilling, Cedar Ridge Farm Ghent, Damsel Garden, "
    "Glencadia Greenhouses, Hamrah's Lebanese Foods & Takeaway, "
    "Heritage Hill Pork (Formerly Lovers Leap Farm), Hickory Creek Farms, "
    "Kipling & Raven Dog Treats, Mort's Maple, O'Boys Soaps, "
    "Our Old House Bakery, River House Market, Valatie Food Pantry, "
    "Worldling's Pleasure"
)
for row in range(2, row_num):
    ws1.cell(row=row, column=12, value=weekly_vendors_list)

# Pre-fill per-date themes, guest vendors, special events, and extended hours.
# (Any remaining blanks are for the coordinator to fill in week by week.)
weekly_overrides = {
    "2026-05-02": {
        "theme": "Opening Day — Early Spring Market",
        "guest_vendors": "Columbia Friends of the Electric Trail, Wild Lavender Crafts",
        "special_name": "Season Opening Celebration",
        "special_time": "8:30am",
        "special_desc": "Welcome back the market for the 2026 season!",
        "status": "Ready",
    },
    "2026-05-09": {
        "special_name": "Super Stories Open Maker Hours — Mother's Day Card Making",
        "special_time": "10:00am - 12:00pm",
        "special_desc": "Drop in to Super Stories and make a card for Mother's Day.",
    },
    "2026-05-30": {
        "theme": "Kinderhook Makers Market — Extended Market Day",
        "note": "Extended hours: 8:30am - 2:00pm. Rain or Shine",
        "special_name": "Kinderhook Makers Market / Fyfe & Drumms Muster & Parade / Modus Operandi Opening",
        "special_time": "8:30am - 2:00pm (market); Parade noon; Gallery 2pm",
        "special_desc": "Extended market day. Fyfe & Drumms Muster & Parade on Broad Street at noon. Modus Operandi opens at The School (Jack Shainman) at 2pm.",
    },
    "2026-06-20": {
        "special_name": "Rising Star Dance Academy Performance",
        "special_time": "11:00am",
        "special_desc": "Live performance at the market.",
    },
    "2026-07-04": {
        "theme": "July 4th — Extended Market Day",
        "note": "Extended hours: 8:30am - 1:30pm. Rain or Shine",
        "special_name": "KBPA People's Parade",
        "special_time": "11:30am",
        "special_desc": "Parade kicks off from Rothermel Park. Market runs extended hours to 1:30pm.",
    },
    "2026-10-10": {
        "theme": "Fall Festival — Extended Market Day",
        "note": "Extended hours: 8:30am - 2:00pm. Rain or Shine",
        "special_name": "Fall Festival & Kinderhook Makers Market",
        "special_time": "8:30am - 2:00pm",
        "special_desc": "Extended market day with the Kinderhook Makers Market.",
    },
    "2026-10-31": {
        "theme": "Final Market Day of 2026 Season",
    },
}

# Apply overrides.
for row in range(2, row_num):
    iso = ws1.cell(row=row, column=1).value
    override = weekly_overrides.get(iso)
    if not override:
        continue
    if "theme" in override:
        ws1.cell(row=row, column=3, value=override["theme"])
    if "note" in override:
        ws1.cell(row=row, column=4, value=override["note"])
    if "special_name" in override:
        ws1.cell(row=row, column=7, value=override["special_name"])
    if "special_time" in override:
        ws1.cell(row=row, column=8, value=override["special_time"])
    if "special_desc" in override:
        ws1.cell(row=row, column=9, value=override["special_desc"])
    if "guest_vendors" in override:
        ws1.cell(row=row, column=10, value=override["guest_vendors"])
    if "status" in override:
        ws1.cell(row=row, column=13, value=override["status"])

# Status dropdown validation
status_val = DataValidation(type="list", formula1='"Draft,Ready,Published"', allow_blank=True)
status_val.error = "Please select Draft, Ready, or Published"
status_val.errorTitle = "Invalid Status"
ws1.add_data_validation(status_val)
for row in range(2, row_num):
    status_val.add(ws1.cell(row=row, column=13))

style_headers(ws1, len(headers_1))
style_data_rows(ws1, len(headers_1))

# Conditional color for status column
for row in range(2, row_num):
    cell = ws1.cell(row=row, column=13)
    cell.alignment = center_alignment
    val = cell.value
    if val == "Ready":
        cell.fill = yellow_fill
    elif val == "Published":
        cell.fill = green_fill


# ─── Tab 2: Vendors ───

ws2 = wb.create_sheet("Vendors")
ws2.sheet_properties.tabColor = "B8BF3D"

headers_2 = [
    "Name",
    "Type",
    "Tagline",
    "Categories",
    "Description",
    "Website",
    "Instagram",
    "Facebook",
    "Featured",
    "Active",
]
ws2.append(headers_2)

widths_2 = [24, 14, 28, 24, 40, 30, 20, 30, 12, 10]
for i, w in enumerate(widths_2, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

# Example vendors
vendors = [
    ["Samascott Orchards", "Weekly", "Family-owned since 1821", "produce, fruit, cider",
     "Six generations of family farming in the Hudson Valley", "https://samascottorchards.com",
     "@samascottorchards", "", "Yes", "Yes"],
    ["River House Market", "Weekly", "Farm-fresh local goods", "produce, prepared foods",
     "Local market featuring Hudson Valley produce", "",
     "", "", "Yes", "Yes"],
    ["Grandaddy Weaves Honey", "Weekly", "Pure local honey", "honey, preserves",
     "Raw honey and beeswax products from local hives", "",
     "", "", "No", "Yes"],
    ["Crème de la Crème Bakery", "Rotating", "Artisan baked goods", "baked goods",
     "Fresh-baked breads, pastries, and seasonal treats", "",
     "", "", "No", "Yes"],
    ["Peta's Pocket Caribbean BBQ", "Rotating", "Island flavors, local ingredients", "prepared foods",
     "Caribbean-inspired dishes made with market-fresh produce", "",
     "", "", "No", "Yes"],
]
for v in vendors:
    ws2.append(v)

# Type dropdown
type_val = DataValidation(type="list", formula1='"Weekly,Rotating"', allow_blank=True)
ws2.add_data_validation(type_val)
for row in range(2, 2 + len(vendors) + 20):  # extra rows for future entries
    type_val.add(ws2.cell(row=row, column=2))

# Featured/Active dropdowns
yn_val = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
ws2.add_data_validation(yn_val)
for row in range(2, 2 + len(vendors) + 20):
    yn_val.add(ws2.cell(row=row, column=9))
    yn_val.add(ws2.cell(row=row, column=10))

style_headers(ws2, len(headers_2))
style_data_rows(ws2, len(headers_2))


# ─── Tab 3: Recipes ───

ws3 = wb.create_sheet("Recipes")
ws3.sheet_properties.tabColor = "2AAFCE"

headers_3 = [
    "Title",
    "Contributor",
    "Contributor Link",
    "Prep Time",
    "Cook Time",
    "Servings",
    "Difficulty",
    "Season",
    "Produce Used",
    "Tags",
    "Ingredients",
    "Instructions",
    "Status",
]
ws3.append(headers_3)

widths_3 = [28, 20, 26, 14, 14, 10, 12, 12, 24, 24, 40, 50, 12]
for i, w in enumerate(widths_3, 1):
    ws3.column_dimensions[get_column_letter(i)].width = w

# Example recipes
recipes = [
    ["Spring Asparagus Salad", "Community Recipe", "", "15 minutes", "5 minutes", 4,
     "easy", "spring", "asparagus, radishes, spring greens",
     "vegetarian, quick, spring",
     "1 bunch asparagus\n4 radishes, sliced\n2 cups spring greens\nLemon vinaigrette",
     "1. Blanch asparagus 2 min\n2. Toss with greens and radishes\n3. Dress with vinaigrette",
     "Published"],
    ["Samascott Orchard Apple Crisp", "Samascott Orchards", "https://samascottorchards.com",
     "20 minutes", "45 minutes", 6, "easy", "fall", "apples",
     "dessert, fall, family-friendly",
     "6 Samascott apples, sliced\n1 cup oats\n1/2 cup brown sugar\n1/4 cup butter\nCinnamon",
     "1. Slice apples into baking dish\n2. Mix topping ingredients\n3. Spread over apples\n4. Bake 375°F for 45 min",
     "Published"],
    ["Peta's Market Day Jerk Chicken Bowl", "Peta's Pocket Caribbean BBQ", "",
     "30 minutes", "25 minutes", 4, "medium", "summer", "peppers, tomatoes, corn",
     "caribbean, bowls, summer",
     "4 chicken thighs\nJerk seasoning\nRice\nGrilled corn\nPeppers\nMango salsa",
     "1. Marinate chicken in jerk seasoning\n2. Grill chicken 25 min\n3. Prepare rice and toppings\n4. Assemble bowls",
     "Published"],
    ["Kinderhook Dutch Baby Pancake", "Community Recipe", "",
     "10 minutes", "20 minutes", 4, "easy", "all", "",
     "breakfast, dutch heritage, family-friendly",
     "3 eggs\n1/2 cup flour\n1/2 cup milk\n2 tbsp butter\nPowdered sugar\nLemon",
     "1. Preheat oven to 425°F\n2. Melt butter in cast iron\n3. Whisk eggs, flour, milk\n4. Pour in pan, bake 20 min\n5. Top with sugar and lemon",
     "Published"],
    ["Grandaddy's Honey Glazed Carrots", "Grandaddy Weaves Honey", "",
     "10 minutes", "20 minutes", 4, "easy", "fall", "carrots",
     "side dish, honey, fall",
     "1 lb carrots\n3 tbsp Grandaddy's honey\n2 tbsp butter\nSalt, thyme",
     "1. Peel and slice carrots\n2. Simmer in butter and honey\n3. Cook until glazed, 20 min\n4. Season with salt and thyme",
     "Published"],
]
for r in recipes:
    ws3.append(r)

# Difficulty dropdown
diff_val = DataValidation(type="list", formula1='"easy,medium,hard"', allow_blank=True)
ws3.add_data_validation(diff_val)
for row in range(2, 50):
    diff_val.add(ws3.cell(row=row, column=7))

# Season dropdown
season_val = DataValidation(type="list", formula1='"spring,summer,fall,all"', allow_blank=True)
ws3.add_data_validation(season_val)
for row in range(2, 50):
    season_val.add(ws3.cell(row=row, column=8))

# Recipe status dropdown
recipe_status_val = DataValidation(type="list", formula1='"Draft,Ready,Published"', allow_blank=True)
ws3.add_data_validation(recipe_status_val)
for row in range(2, 50):
    recipe_status_val.add(ws3.cell(row=row, column=13))

style_headers(ws3, len(headers_3))
style_data_rows(ws3, len(headers_3))


# ─── Tab 4: Music Schedule ───

ws_music = wb.create_sheet("Music Schedule")
ws_music.sheet_properties.tabColor = "5D3C54"

headers_music = ["Date", "Day", "Performer", "Time", "Notes"]
ws_music.append(headers_music)
for i, w in enumerate([14, 20, 32, 22, 30], 1):
    ws_music.column_dimensions[get_column_letter(i)].width = w

for iso, act in music_lineup.items():
    d = date.fromisoformat(iso)
    note = "Official title to come" if "(official title" in act else ""
    act_clean = act.replace(" (official title to come)", "")
    ws_music.append([iso, d.strftime("%A, %B %-d"), act_clean, "10:00am - 12:00pm", note])

style_headers(ws_music, len(headers_music))
style_data_rows(ws_music, len(headers_music))


# ─── Tab 5: Village Events ───

ws_events = wb.create_sheet("Village Events")
ws_events.sheet_properties.tabColor = "B8860B"

headers_events = ["Date", "Event", "Host / Location", "Time", "Category", "Notes"]
ws_events.append(headers_events)
for i, w in enumerate([14, 40, 30, 22, 14, 40], 1):
    ws_events.column_dimensions[get_column_letter(i)].width = w

village_events = [
    ["2026-05-09", "Open Maker Hours — Mother's Day Card Making", "Super Stories", "10:00am - 12:00pm", "community", ""],
    ["2026-05-30", "Kinderhook Makers Market (Extended Market Day)", "Kinderhook Farmers Market & Makers Market / Village Green", "8:30am - 2:00pm", "community", "Extended market hours"],
    ["2026-05-30", "Fyfe & Drumms Muster & Parade", "Broad Street", "Noon", "community", ""],
    ["2026-05-30", "Modus Operandi — Exhibition Opening", "The School / Jack Shainman Gallery", "2:00pm", "art", ""],
    ["2026-06-05", "Seen Scenes — Exhibition Opens (runs through June 28)", "Kinderhook Knitting Mill / Create Council on the Arts", "", "art", ""],
    ["2026-06-06", "Seen Scenes — Opening Reception", "Kinderhook Knitting Mill", "3:00pm - 5:00pm", "art", ""],
    ["2026-06-06", "OK 5K", "Kinderhook", "TBD", "community", ""],
    ["2026-06-06", "Persons of Color Cemetery Tour", "The Cultural Landscape Foundation", "TBD", "community", ""],
    ["2026-06-20", "Rising Star Dance Academy Performance", "Village Green / Market", "11:00am", "community", "At the market"],
    ["2026-06-27", "Kinderhook Pride Parade", "Hudson Street to Village Square", "2:00pm", "community", ""],
    ["2026-07-04", "People's Parade", "KBPA / Rothermel Park", "11:30am", "community", "Market extended to 1:30pm"],
    ["2026-10-10", "Fall Festival & Kinderhook Makers Market", "Kinderhook Farmers Market & Makers Market / Village Green", "8:30am - 2:00pm", "community", "Extended market hours"],
    ["2026-10-31", "Final Market Day of 2026 Season", "Kinderhook Farmers Market / Village Green", "8:30am - 12:30pm", "food", ""],
]
for e in village_events:
    ws_events.append(e)

style_headers(ws_events, len(headers_events))
style_data_rows(ws_events, len(headers_events))


# ─── Tab 6: Sponsors ───

ws_sponsors = wb.create_sheet("Sponsors")
ws_sponsors.sheet_properties.tabColor = "F26A2A"

headers_sponsors = ["Sponsor", "Website", "Logo Status", "Notes"]
ws_sponsors.append(headers_sponsors)
for i, w in enumerate([40, 40, 16, 40], 1):
    ws_sponsors.column_dimensions[get_column_letter(i)].width = w

sponsors_list = [
    ["Berkshire Hathaway Home Services Blake Realty", "", "To come", ""],
    ["Columbia County Tourism", "", "To come", ""],
    ["Herringtons", "", "To come", ""],
    ["Julia Jayne Pilates", "", "To come", ""],
    ["Todd Farrell's Car Care Center", "", "To come", ""],
    ["Valkin Properties", "", "To come", ""],
]
for s in sponsors_list:
    ws_sponsors.append(s)

style_headers(ws_sponsors, len(headers_sponsors))
style_data_rows(ws_sponsors, len(headers_sponsors))


# ─── Tab 7: Site Config ───

ws4 = wb.create_sheet("Site Config")
ws4.sheet_properties.tabColor = "1A1A1A"

ws4.column_dimensions["A"].width = 22
ws4.column_dimensions["B"].width = 50
ws4.column_dimensions["C"].width = 40

# Header
ws4.append(["Setting", "Value", "Notes"])
style_headers(ws4, 3)

config_rows = [
    ["Season Start", "2026-05-02", "First market Saturday"],
    ["Season End", "2026-10-31", "Last market Saturday"],
    ["Market Day", "Saturday", ""],
    ["Start Time", "8:30 AM", ""],
    ["End Time", "12:30 PM", ""],
    ["Location Name", "Village Green", ""],
    ["Address", "Broad Street, Kinderhook, NY 12106", ""],
    ["Email", "info@kinderhookfarmersmarket.com", ""],
    ["Facebook", "https://www.facebook.com/KinderhookFarmersMarket", ""],
    ["Instagram", "https://www.instagram.com/kinderhookfarmersmarket", ""],
    ["Sponsor", "Kinderhook Business and Professional Association", ""],
    ["Tagline", "It's OK!", "Martin Van Buren / Old Kinderhook reference"],
]
for r in config_rows:
    ws4.append(r)

style_data_rows(ws4, 3)

# Bold the setting names
for row in range(2, 2 + len(config_rows)):
    ws4.cell(row=row, column=1).font = Font(name="Arial", bold=True, size=11)
    ws4.cell(row=row, column=3).font = Font(name="Arial", italic=True, size=10, color="888888")


# ─── Tab 5: Instructions ───

ws5 = wb.create_sheet("How to Use")
ws5.sheet_properties.tabColor = "2AAFCE"
ws5.column_dimensions["A"].width = 80

instructions = [
    "KINDERHOOK FARMERS' MARKET - CONTENT MANAGEMENT SHEET",
    "",
    "HOW TO USE THIS SPREADSHEET",
    "=" * 50,
    "",
    "WEEKLY SCHEDULE TAB:",
    "  - Each row is one Saturday market day (pre-filled for the full season)",
    "  - Fill in the Theme, Music, Events, and Vendors for each week",
    "  - Set Status to 'Ready' when the week's info is complete",
    "  - After the website is updated, status changes to 'Published'",
    "  - Guest Vendors, Community Partners, and Regular Vendors are comma-separated lists",
    "  - Leave fields blank if not applicable (e.g., no music that week)",
    "",
    "VENDORS TAB:",
    "  - One row per vendor (both weekly regulars and rotating guests)",
    "  - Categories are comma-separated (e.g., 'produce, fruit, cider')",
    "  - Set Active to 'No' if a vendor is taking a break",
    "  - Set Featured to 'Yes' for vendors to highlight on the homepage",
    "",
    "RECIPES TAB:",
    "  - One row per recipe",
    "  - Ingredients and Instructions can have line breaks (Alt+Enter in Google Sheets)",
    "  - Produce Used links recipes to the seasonal guide",
    "  - Set Status to 'Ready' when a recipe is reviewed and good to publish",
    "",
    "SITE CONFIG TAB:",
    "  - Rarely needs updating - only for season dates, hours, or contact changes",
    "",
    "WORKFLOW:",
    "  1. Fill in the upcoming week's row on the Weekly Schedule tab",
    "  2. Set the Status to 'Ready'",
    "  3. Share with David or notify the web team",
    "  4. Website gets updated and status changes to 'Published'",
]

for i, line in enumerate(instructions, 1):
    cell = ws5.cell(row=i, column=1, value=line)
    if i == 1:
        cell.font = Font(name="Arial", bold=True, size=14, color="F26A2A")
    elif line.startswith("="):
        cell.font = Font(name="Arial", size=10, color="DDDDDD")
    elif line.endswith(":") and line == line.upper():
        cell.font = Font(name="Arial", bold=True, size=12, color="1A1A1A")
    elif line.startswith("  -"):
        cell.font = Font(name="Arial", size=10)
    else:
        cell.font = Font(name="Arial", size=11)


# Save
output_path = "/Users/davidnyman/Code/market/kinderhook-market-content.xlsx"
wb.save(output_path)
print(f"Spreadsheet saved to: {output_path}")
