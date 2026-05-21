import urllib.request
import csv
import json
import datetime
import re
import os

gids = {
    "Phase1": "2014700145",
    "Phase2": "1670697114",
    "Phase3": "1045099150",
    "Phase4": "2018069044",
    "Phase5": "1418252590",
    "Phase6": "1277148414",
    "Phase7": "831648111",
    "Phase8": "705719937"
}

url_template = "https://docs.google.com/spreadsheets/d/1k306th8rcidGtP4LMc1zgOppRe5aKuTw/export?format=csv&gid={}"

all_questions = []
q_id = int(datetime.datetime.now().timestamp() * 1000)

for phase, gid in gids.items():
    print(f"Fetching {phase}...")
    url = url_template.format(gid)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        reader = csv.reader(content.splitlines())
        rows = list(reader)
        
        # Find header row
        header_idx = -1
        for i, row in enumerate(rows):
            if len(row) > 6 and row[0] == "#" and row[1] == "Problem ID":
                header_idx = i
                break
        
        if header_idx == -1:
            print(f"Header not found for {phase}")
            continue
            
        for row in rows[header_idx + 1:]:
            if len(row) < 7 or not row[0].strip().isdigit():
                continue # Skip empty or invalid rows
                
            problem_id = row[1].strip()
            problem_name = row[2].strip()
            link = row[6].strip()
            
            solved_raw = row[7].strip().lower() if len(row) > 7 else ""
            status = "done" if solved_raw in ["yes", "done", "true", "1", "y"] else "pending"
            
            notes = row[8].strip() if len(row) > 8 else ""
            
            title = f"[{phase}] {problem_id} - {problem_name}"
            
            all_questions.append({
                "id": q_id,
                "title": title,
                "link": link,
                "status": status,
                "notes": notes,
                "createdAt": datetime.datetime.now().isoformat()
            })
            q_id += 1

print(f"Total questions fetched: {len(all_questions)}")

html_file = "/Users/ritesh/taks/my_tracker.html"
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace source1 array
source1_json = json.dumps(all_questions, indent=12)
pattern = re.compile(r'(appData\s*=\s*{\s*source1:\s*)\[.*?\](,\s*source2:)', re.DOTALL)

if pattern.search(html_content):
    new_html = pattern.sub(lambda m: m.group(1) + source1_json + m.group(2), html_content)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully updated my_tracker.html")
else:
    print("Failed to find appData.source1 pattern in html file")
