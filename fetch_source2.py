import urllib.request
import csv
import json
import datetime
import re

gids = {
    "Arrays & Strings": "924069017",
    "Linked Lists": "143193743",
    "Trees & Graphs": "276965359",
    "Dynamic Programming": "367757536",
    "Stack, Queue & Heap": "2038490881",
    "Binary Search & Backtracking": "737371575",
    "Advanced & Interview Level": "389530201"
}

url_template = "https://docs.google.com/spreadsheets/d/1ajo4qnnt1tf1QXGtSZQzCowJtSS59Lz_/export?format=csv&gid={}"

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
        
        header_idx = -1
        for i, row in enumerate(rows):
            if len(row) > 4 and row[0] == "#" and row[1] == "Problem Name":
                header_idx = i
                break
        
        if header_idx == -1:
            print(f"Header not found for {phase}")
            continue
            
        for row in rows[header_idx + 1:]:
            if len(row) < 5 or not row[0].strip().isdigit():
                continue
                
            problem_name = row[1].strip()
            topic = row[2].strip()
            difficulty = row[3].strip()
            lc_num = row[4].strip()
            
            status_raw = row[5].strip().lower() if len(row) > 5 else ""
            status = "done" if status_raw in ["yes", "done", "true", "1", "y", "☑"] else "pending"
            
            notes = row[6].strip() if len(row) > 6 else ""
            
            slug = re.sub(r'[^a-zA-Z0-9\s-]', '', problem_name).strip().replace(' ', '-').lower()
            link = f"https://leetcode.com/problems/{slug}/"
            
            title = f"[{phase}] #{lc_num} - {problem_name} ({difficulty})"
            
            all_questions.append({
                "id": q_id,
                "title": title,
                "link": link,
                "status": status,
                "notes": notes,
                "createdAt": datetime.datetime.now().isoformat()
            })
            q_id += 1

print(f"Total source 2 questions fetched: {len(all_questions)}")

html_file = "/Users/ritesh/taks/my_tracker.html"
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

source2_json = json.dumps(all_questions, indent=12)

# Now we need to replace appData.source2: []
# The regex looks for `source2:\s*\[.*?\]`
pattern = re.compile(r'(source2:\s*)\[.*?\]', re.DOTALL)
if pattern.search(html_content):
    new_html = pattern.sub(lambda m: m.group(1) + source2_json, html_content)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully updated my_tracker.html with source2 data")
else:
    print("Failed to find source2 pattern")
