import re
import os

html_file = "/Users/ritesh/taks/my_tracker.html"

with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

# Extract appData
app_data_match = re.search(r'(let appData = \{.*?\};)', content, re.DOTALL)
if not app_data_match:
    print("Could not find appData block!")
    exit(1)

app_data_str = app_data_match.group(1)

new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📋 Premium CP Tracker | Pro Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        :root {{
            --bg-base: #090e17;
            --bg-glass: rgba(15, 23, 42, 0.7);
            --border-glass: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --hover-bg: rgba(255, 255, 255, 0.05);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg-base);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.12), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.12), transparent 25%);
            background-attachment: fixed;
            min-height: 100vh;
            color: var(--text-main);
            padding: 2rem;
            line-height: 1.6;
        }}

        .container {{ max-width: 1400px; margin: 0 auto; }}

        .glass-panel {{
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            padding: 2rem;
        }}

        .header {{ text-align: center; margin-bottom: 2.5rem; animation: fadeInDown 0.8s ease-out; }}
        .header h1 {{
            font-size: 3rem; font-weight: 700;
            background: var(--accent-gradient);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem; letter-spacing: -1px;
        }}
        .header p {{ color: var(--text-muted); font-size: 1.1rem; font-weight: 300; }}

        .tabs {{
            display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem;
            border-bottom: 1px solid var(--border-glass); padding-bottom: 1.5rem;
        }}
        .tab-btn {{
            background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-glass);
            padding: 0.8rem 2rem; font-size: 1.1rem; font-weight: 500; cursor: pointer;
            color: var(--text-muted); border-radius: 12px; transition: all 0.3s ease; font-family: inherit;
        }}
        .tab-btn.active {{
            background: var(--accent-gradient); color: white; border-color: transparent;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transform: translateY(-2px);
        }}
        .tab-btn:hover:not(.active) {{ background: var(--hover-bg); color: var(--text-main); }}

        .add-form {{
            display: grid; grid-template-columns: 2fr 2fr 1fr 2fr auto; gap: 1rem;
            margin-bottom: 2rem; align-items: end;
        }}
        .form-group {{ display: flex; flex-direction: column; gap: 0.5rem; }}
        .form-group label {{ font-size: 0.85rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }}
        .form-group input, .form-group select {{
            padding: 0.8rem 1rem; border-radius: 12px; border: 1px solid var(--border-glass);
            background: rgba(0, 0, 0, 0.2); color: var(--text-main); font-family: inherit; font-size: 1rem; transition: all 0.3s ease;
        }}
        .form-group input:focus, .form-group select:focus {{ outline: none; border-color: var(--accent); background: rgba(0, 0, 0, 0.4); box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2); }}
        .add-btn {{
            background: var(--accent-gradient); border: none; padding: 0.8rem 1.5rem; border-radius: 12px;
            font-weight: 600; cursor: pointer; color: white; font-size: 1rem; font-family: inherit;
            height: 47px; transition: all 0.3s ease;
        }}
        .add-btn:hover {{ box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transform: translateY(-2px); }}

        .filters-stats-wrapper {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem; }}
        .filters {{ display: flex; gap: 0.5rem; align-items: center; }}
        .filter-btn {{
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-glass);
            padding: 0.5rem 1rem; border-radius: 20px; cursor: pointer; color: var(--text-muted);
            font-size: 0.9rem; font-family: inherit; transition: all 0.2s ease;
        }}
        .filter-btn.active-filter {{ background: rgba(59, 130, 246, 0.2); color: var(--accent); border-color: var(--accent); }}
        .filter-btn:hover:not(.active-filter) {{ background: rgba(255, 255, 255, 0.1); color: var(--text-main); }}
        .search-box {{
            padding: 0.6rem 1.2rem; border-radius: 20px; border: 1px solid var(--border-glass);
            background: rgba(0, 0, 0, 0.2); color: white; font-family: inherit; min-width: 250px; transition: all 0.3s ease;
        }}
        .search-box:focus {{ outline: none; border-color: var(--accent); width: 300px; }}

        .stats {{ display: flex; gap: 1rem; }}
        .stat-card {{ background: rgba(0, 0, 0, 0.2); padding: 0.5rem 1rem; border-radius: 12px; font-size: 0.9rem; font-weight: 500; border: 1px solid var(--border-glass); display: flex; align-items: center; gap: 0.5rem; }}
        .stat-card span {{ font-weight: 700; font-size: 1rem; }}
        .stat-card.total span {{ color: var(--accent); }}
        .stat-card.done span {{ color: var(--success); }}
        .stat-card.progress span {{ color: var(--warning); }}
        .stat-card.pending span {{ color: var(--text-muted); }}

        .table-wrapper {{ background: rgba(0, 0, 0, 0.2); border-radius: 16px; border: 1px solid var(--border-glass); overflow: hidden; margin-bottom: 2rem; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th, td {{ padding: 1.2rem 1rem; border-bottom: 1px solid var(--border-glass); }}
        th {{ background: rgba(255, 255, 255, 0.02); color: var(--text-muted); font-weight: 500; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        tbody tr {{ transition: background-color 0.2s ease, transform 0.2s ease; }}
        tbody tr:hover {{ background: rgba(255, 255, 255, 0.03); transform: translateX(4px); }}
        tbody tr:last-child td {{ border-bottom: none; }}

        .status-select {{
            background: rgba(0, 0, 0, 0.3); border: 1px solid var(--border-glass); border-radius: 20px;
            padding: 0.4rem 0.8rem; font-family: inherit; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.2s ease;
        }}
        .status-select:focus {{ outline: none; border-color: var(--accent); }}
        .status-select.done {{ border-color: var(--success); color: var(--success); background: rgba(16, 185, 129, 0.1); }}
        .status-select.progress {{ border-color: var(--warning); color: var(--warning); background: rgba(245, 158, 11, 0.1); }}
        .status-select.pending {{ border-color: var(--border-glass); color: var(--text-muted); background: rgba(255, 255, 255, 0.05); }}

        .notes-cell {{ max-width: 300px; color: var(--text-muted); font-size: 0.9rem; line-height: 1.4; }}
        .note-preview {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; }}
        td a {{ color: var(--accent); text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 0.25rem; transition: color 0.2s ease; }}
        td a:hover {{ color: #60a5fa; text-decoration: underline; }}

        .action-buttons {{ display: flex; gap: 0.5rem; }}
        .action-buttons button {{ background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-glass); width: 32px; height: 32px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }}
        .action-buttons button:hover {{ background: rgba(255, 255, 255, 0.15); transform: scale(1.1); }}

        /* Modal */
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); justify-content: center; align-items: center; z-index: 1000; opacity: 0; animation: fadeIn 0.3s forwards; }}
        .modal-content {{ background: var(--bg-base); border-radius: 24px; padding: 2.5rem; width: 90%; max-width: 650px; border: 1px solid var(--border-glass); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5); transform: translateY(20px); animation: slideUp 0.3s forwards; }}
        .modal-content h3 {{ margin-bottom: 0.5rem; font-size: 1.5rem; font-weight: 600; }}
        .modal-content textarea {{ width: 100%; min-height: 250px; background: rgba(0, 0, 0, 0.2); border: 1px solid var(--border-glass); color: var(--text-main); padding: 1.5rem; border-radius: 16px; font-family: inherit; font-size: 1rem; line-height: 1.6; margin: 1.5rem 0; resize: vertical; transition: all 0.3s ease; }}
        .modal-content textarea:focus {{ outline: none; border-color: var(--accent); background: rgba(0, 0, 0, 0.4); }}
        .modal-buttons {{ display: flex; gap: 1rem; justify-content: flex-end; }}
        
        .btn-secondary {{ background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-glass); padding: 0.8rem 1.5rem; border-radius: 12px; cursor: pointer; color: var(--text-main); font-family: inherit; font-weight: 500; transition: all 0.2s ease; }}
        .btn-secondary:hover {{ background: rgba(255, 255, 255, 0.1); }}
        .btn-primary {{ background: var(--accent-gradient); border: none; padding: 0.8rem 1.5rem; border-radius: 12px; cursor: pointer; color: white; font-family: inherit; font-weight: 500; transition: all 0.2s ease; }}
        .btn-primary:hover {{ box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transform: translateY(-2px); }}

        .export-import {{ display: flex; gap: 1rem; justify-content: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-glass); }}
        .small-btn {{ background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-glass); padding: 0.6rem 1.2rem; border-radius: 20px; font-size: 0.85rem; font-family: inherit; cursor: pointer; color: var(--text-muted); transition: all 0.2s ease; }}
        .small-btn:hover {{ background: rgba(255, 255, 255, 0.1); color: var(--text-main); }}
        .small-btn.danger:hover {{ background: rgba(239, 68, 68, 0.1); border-color: var(--danger); color: var(--danger); }}

        @keyframes fadeIn {{ to {{ opacity: 1; }} }}
        @keyframes slideUp {{ to {{ transform: translateY(0); }} }}
        @keyframes fadeInDown {{ from {{ opacity: 0; transform: translateY(-20px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        @media (max-width: 1024px) {{ .add-form {{ grid-template-columns: 1fr 1fr; }} .add-btn {{ grid-column: 1 / -1; }} }}
        @media (max-width: 768px) {{ .filters-stats-wrapper {{ flex-direction: column; align-items: flex-start; }} .stats {{ flex-wrap: wrap; }} .tabs {{ flex-direction: column; }} .search-box, .search-box:focus {{ width: 100%; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="glass-panel">
            <div class="header">
                <h1>Premium CP Tracker</h1>
                <p>Master your coding journey with real-time tracking, beautiful UI, and auto-saves</p>
            </div>

            <!-- Tabs for Two Sources -->
            <div class="tabs">
                <button class="tab-btn active" data-source="source1">Roadmap (Phase 1-8)</button>
                <button class="tab-btn" data-source="source2">LeetCode Top 500</button>
            </div>

            <!-- Add Question Form -->
            <div class="add-form">
                <div class="form-group">
                    <label>📌 Question Title</label>
                    <input type="text" id="questionTitle" placeholder="e.g., Two Sum, DFS..." autocomplete="off">
                </div>
                <div class="form-group">
                    <label>🔗 Link (optional)</label>
                    <input type="text" id="questionLink" placeholder="https://...">
                </div>
                <div class="form-group">
                    <label>📊 Status</label>
                    <select id="questionStatus">
                        <option value="pending">⏳ Pending</option>
                        <option value="progress">🔄 In Progress</option>
                        <option value="done">✅ Done</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>📝 Quick Note</label>
                    <input type="text" id="quickNote" placeholder="BFS, prefix sum...">
                </div>
                <button class="add-btn" id="addQuestionBtn">+ Add</button>
            </div>

            <!-- Filters & Stats -->
            <div class="filters-stats-wrapper">
                <div class="filters">
                    <button class="filter-btn active-filter" data-filter="all">All</button>
                    <button class="filter-btn" data-filter="pending">Pending</button>
                    <button class="filter-btn" data-filter="progress">In Progress</button>
                    <button class="filter-btn" data-filter="done">Done</button>
                    <input type="text" class="search-box" id="searchInput" placeholder="🔍 Search questions...">
                </div>
                <div class="stats" id="statsArea">
                    <!-- dynamic stats -->
                </div>
            </div>

            <!-- Questions Table -->
            <div class="table-wrapper">
                <table id="questionsTable">
                    <thead>
                        <tr>
                            <th style="width: 5%">#</th>
                            <th style="width: 30%">Question</th>
                            <th style="width: 10%">Link</th>
                            <th style="width: 15%">Status</th>
                            <th style="width: 30%">Notes</th>
                            <th style="width: 10%">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        <tr>
                            <td colspan="6" style="text-align:center">Loading questions...</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="export-import">
                <button class="small-btn" id="exportDataBtn">💾 Export Backup</button>
                <input type="file" id="importFileInput" accept=".json" style="display:none">
                <button class="small-btn" id="importDataBtn">📂 Import Backup</button>
                <button class="small-btn danger" id="resetDataBtn">⚠️ Reset All Data</button>
            </div>
        </div>
    </div>

    <!-- Modal for editing long notes -->
    <div id="notesModal" class="modal">
        <div class="modal-content">
            <h3>✏️ Edit Detailed Notes</h3>
            <p style="font-size:0.9rem; color:var(--text-muted)">Add your approach, complexities, or alternative solutions.</p>
            <textarea id="modalNotesInput" placeholder="Write your detailed notes here..."></textarea>
            <div class="modal-buttons">
                <button class="btn-secondary" id="closeModalBtn">Cancel</button>
                <button class="btn-primary" id="saveModalBtn">Save Notes</button>
            </div>
        </div>
    </div>

    <script>
        {app_data_str}
        
        let currentSource = "source1";
        let currentFilter = "all";
        let currentSearch = "";
        let editQuestionId = null;

        function loadData() {{
            const saved = localStorage.getItem("CP_Question_Tracker_Pro");
            if (saved) {{
                try {{
                    const parsed = JSON.parse(saved);
                    // Merging logic so new fetched questions aren't wiped out by old local storage, 
                    // unless the local storage has actual modifications.
                    // For simplicity, we just trust local storage if it has both arrays.
                    if (parsed.source1 && parsed.source2) appData = parsed;
                }} catch (e) {{ console.log("parse error"); }}
            }}
            renderCurrentView();
        }}

        function saveToLocal() {{
            localStorage.setItem("CP_Question_Tracker_Pro", JSON.stringify(appData));
        }}

        function getCurrentQuestions() {{ return appData[currentSource]; }}

        function setCurrentQuestions(newArr) {{
            appData[currentSource] = newArr;
            saveToLocal();
            renderCurrentView();
        }}

        function addQuestion(title, link, status, quickNote) {{
            if (!title.trim()) return false;
            const questions = getCurrentQuestions();
            questions.push({{
                id: Date.now(),
                title: title.trim(),
                link: link.trim(),
                status: status,
                notes: quickNote || "",
                createdAt: new Date().toISOString()
            }});
            setCurrentQuestions(questions);
            return true;
        }}

        function deleteQuestionById(id) {{
            let questions = getCurrentQuestions();
            questions = questions.filter(q => q.id !== id);
            setCurrentQuestions(questions);
        }}

        function updateQuestionNotes(id, newNotes) {{
            let questions = getCurrentQuestions();
            const index = questions.findIndex(q => q.id === id);
            if (index !== -1) {{
                questions[index].notes = newNotes;
                setCurrentQuestions(questions);
            }}
        }}

        function updateQuestionStatus(id, newStatus) {{
            let questions = getCurrentQuestions();
            const index = questions.findIndex(q => q.id === id);
            if (index !== -1) {{
                questions[index].status = newStatus;
                setCurrentQuestions(questions);
            }}
        }}

        function getFilteredQuestions() {{
            let questions = getCurrentQuestions();
            if (currentFilter !== "all") {{
                questions = questions.filter(q => q.status === currentFilter);
            }}
            if (currentSearch.trim() !== "") {{
                const searchLower = currentSearch.toLowerCase();
                questions = questions.filter(q => q.title.toLowerCase().includes(searchLower));
            }}
            return questions; // Keeping original order instead of reverse for sequential roadmap feeling
        }}

        function renderStats(filteredQuestions) {{
            const all = getCurrentQuestions();
            const doneCount = all.filter(q => q.status === "done").length;
            const progressCount = all.filter(q => q.status === "progress").length;
            const pendingCount = all.filter(q => q.status === "pending").length;
            document.getElementById("statsArea").innerHTML = `
                <div class="stat-card total">Total <span>${{all.length}}</span></div>
                <div class="stat-card done">Done <span>${{doneCount}}</span></div>
                <div class="stat-card progress">In Progress <span>${{progressCount}}</span></div>
                <div class="stat-card pending">Pending <span>${{pendingCount}}</span></div>
            `;
        }}

        function renderCurrentView() {{
            const filtered = getFilteredQuestions();
            const tbody = document.getElementById("tableBody");
            if (filtered.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 3rem; color: var(--text-muted);">✨ No questions found.</td></tr>`;
                renderStats(filtered);
                return;
            }}
            
            let html = "";
            filtered.forEach((q, idx) => {{
                const linkDisplay = q.link ? `<a href="${{escapeHtml(q.link)}}" target="_blank">↗ Link</a>` : "—";
                const notePreview = q.notes ? `<div class="note-preview">${{escapeHtml(q.notes)}}</div>` : `<span style="opacity:0.5">No notes</span>`;
                html += `<tr>
                    <td>${{idx + 1}}</td>
                    <td><strong style="color:var(--text-main); font-weight:500;">${{escapeHtml(q.title)}}</strong></td>
                    <td>${{linkDisplay}}</td>
                    <td>
                        <select class="status-select ${{q.status}}" data-id="${{q.id}}">
                            <option value="pending" ${{q.status === "pending" ? "selected" : ""}}>⏳ Pending</option>
                            <option value="progress" ${{q.status === "progress" ? "selected" : ""}}>🔄 In Progress</option>
                            <option value="done" ${{q.status === "done" ? "selected" : ""}}>✅ Done</option>
                        </select>
                    </td>
                    <td class="notes-cell">${{notePreview}}</td>
                    <td>
                        <div class="action-buttons">
                            <button class="edit-note-btn" data-id="${{q.id}}" title="Edit notes">✏️</button>
                            <button class="delete-btn" data-id="${{q.id}}" title="Delete">🗑️</button>
                        </div>
                    </td>
                </tr>`;
            }});
            tbody.innerHTML = html;
            renderStats(filtered);

            document.querySelectorAll(".status-select").forEach(select => {{
                select.addEventListener("change", (e) => {{
                    const qid = parseInt(select.getAttribute("data-id"));
                    // Update class for immediate visual feedback
                    select.className = "status-select " + select.value;
                    updateQuestionStatus(qid, select.value);
                }});
            }});

            document.querySelectorAll(".edit-note-btn").forEach(btn => {{
                btn.addEventListener("click", () => openNotesModal(parseInt(btn.getAttribute("data-id"))));
            }});

            document.querySelectorAll(".delete-btn").forEach(btn => {{
                btn.addEventListener("click", () => {{
                    if (confirm("Delete this question?")) deleteQuestionById(parseInt(btn.getAttribute("data-id")));
                }});
            }});
        }}

        function openNotesModal(questionId) {{
            const q = getCurrentQuestions().find(q => q.id === questionId);
            if (!q) return;
            editQuestionId = questionId;
            const modal = document.getElementById("notesModal");
            document.getElementById("modalNotesInput").value = q.notes || "";
            modal.style.display = "flex";
        }}

        function escapeHtml(str) {{
            if (!str) return "";
            return str.replace(/[&<>]/g, m => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;" }}[m]));
        }}

        document.addEventListener("DOMContentLoaded", () => {{
            loadData();

            document.querySelectorAll(".tab-btn").forEach(btn => {{
                btn.addEventListener("click", () => {{
                    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
                    btn.classList.add("active");
                    currentSource = btn.getAttribute("data-source");
                    currentFilter = "all";
                    document.getElementById("searchInput").value = "";
                    currentSearch = "";
                    document.querySelectorAll(".filter-btn").forEach(fb => fb.classList.remove("active-filter"));
                    document.querySelector(".filter-btn[data-filter='all']").classList.add("active-filter");
                    renderCurrentView();
                }});
            }});

            document.querySelectorAll(".filter-btn").forEach(btn => {{
                btn.addEventListener("click", () => {{
                    document.querySelectorAll(".filter-btn").forEach(f => f.classList.remove("active-filter"));
                    btn.classList.add("active-filter");
                    currentFilter = btn.getAttribute("data-filter");
                    renderCurrentView();
                }});
            }});

            document.getElementById("searchInput").addEventListener("input", (e) => {{
                currentSearch = e.target.value;
                renderCurrentView();
            }});

            document.getElementById("addQuestionBtn").addEventListener("click", () => {{
                const title = document.getElementById("questionTitle");
                const link = document.getElementById("questionLink");
                const status = document.getElementById("questionStatus");
                const quickNote = document.getElementById("quickNote");
                if (addQuestion(title.value, link.value, status.value, quickNote.value)) {{
                    title.value = ""; link.value = ""; quickNote.value = ""; status.value = "pending";
                }} else {{
                    alert("Please enter a question title.");
                }}
            }});

            const modal = document.getElementById("notesModal");
            document.getElementById("closeModalBtn").addEventListener("click", () => {{ modal.style.display = "none"; editQuestionId = null; }});
            document.getElementById("saveModalBtn").addEventListener("click", () => {{
                if (editQuestionId !== null) {{
                    updateQuestionNotes(editQuestionId, document.getElementById("modalNotesInput").value);
                    modal.style.display = "none"; editQuestionId = null;
                }}
            }});
            window.addEventListener("click", (e) => {{ if (e.target === modal) modal.style.display = "none"; }});

            document.getElementById("exportDataBtn").addEventListener("click", () => {{
                const blob = new Blob([JSON.stringify(appData, null, 2)], {{ type: "application/json" }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url; a.download = `premium_tracker_backup_${{new Date().toISOString().slice(0, 19)}}.json`;
                a.click(); URL.revokeObjectURL(url);
            }});
            document.getElementById("importDataBtn").addEventListener("click", () => document.getElementById("importFileInput").click());
            document.getElementById("importFileInput").addEventListener("change", (e) => {{
                const file = e.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = (ev) => {{
                    try {{
                        const imported = JSON.parse(ev.target.result);
                        if (imported.source1 && imported.source2) {{
                            appData = imported; saveToLocal(); renderCurrentView(); alert("Import successful!");
                        }} else alert("Invalid backup file format.");
                    }} catch (err) {{ alert("Error parsing backup."); }}
                    e.target.value = "";
                }};
                reader.readAsText(file);
            }});
            document.getElementById("resetDataBtn").addEventListener("click", () => {{
                if (confirm("⚠️ Delete ALL questions and customizations permanently?")) {{
                    appData = {{ source1: [], source2: [] }}; saveToLocal(); renderCurrentView();
                }}
            }});
        }});
    </script>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Redesigned and applied new premium HTML/CSS successfully.")
