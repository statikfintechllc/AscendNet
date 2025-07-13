# docs/build_dashboard_html.py

with open("dashboard_template.html", "r") as f:
    template = f.read()

with open("graph/traffic_totals.json", "r") as f:
    totals = f.read()

filled = template.replace("{{TRAFFIC_TOTALS}}", totals.strip())

with open("dashboard.html", "w") as f:
    f.write(filled)
