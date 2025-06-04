import os
from flask import Flask, render_template, request, redirect
from utils import read_file, write_file, append_file, load_placeholders, apply_placeholders

app = Flask(__name__)
GROUPS_DIR = "group_data"

# Ensure group_data folder exists
os.makedirs(GROUPS_DIR, exist_ok=True)

@app.route("/")
def index():
    groups = [g for g in os.listdir(GROUPS_DIR) if os.path.isdir(os.path.join(GROUPS_DIR, g))]
    return render_template("index.html", groups=groups)

@app.route("/create", methods=["POST"])
def create_group():
    group = request.form["group"]
    group_path = os.path.join(GROUPS_DIR, group)
    if not os.path.exists(group_path):
        os.makedirs(group_path)
        write_file(os.path.join(group_path, "messages.txt"), "")
        write_file(os.path.join(group_path, "tokens.txt"), "")
        write_file(os.path.join(group_path, "convo.txt"), "t_xxxxx")
        write_file(os.path.join(group_path, "delay.txt"), "5.0")
        write_file(os.path.join(group_path, "placeholders.txt"), "")
        write_file(os.path.join(group_path, "paused.txt"), "0")
    return redirect(f"/group/{group}")

@app.route("/group/<group>", methods=["GET", "POST"])
def group(group):
    group_path = os.path.join(GROUPS_DIR, group)
    if request.method == "POST":
        write_file(os.path.join(group_path, "messages.txt"), request.form["messages"])
        write_file(os.path.join(group_path, "tokens.txt"), request.form["tokens"])
        write_file(os.path.join(group_path, "delay.txt"), request.form["delay"])
        write_file(os.path.join(group_path, "convo.txt"), request.form["convo"])
        write_file(os.path.join(group_path, "placeholders.txt"), request.form["placeholders"])
        return redirect(f"/group/{group}")

    context = {
        "group": group,
        "messages": read_file(os.path.join(group_path, "messages.txt")),
        "tokens": read_file(os.path.join(group_path, "tokens.txt")),
        "delay": read_file(os.path.join(group_path, "delay.txt")),
        "convo": read_file(os.path.join(group_path, "convo.txt")),
        "placeholders": read_file(os.path.join(group_path, "placeholders.txt")),
        "paused": read_file(os.path.join(group_path, "paused.txt"))
    }
    return render_template("group.html", **context)

@app.route("/group/<group>/pause", methods=["POST"])
def pause_group(group):
    write_file(os.path.join(GROUPS_DIR, group, "paused.txt"), "1")
    return redirect(f"/group/{group}")

@app.route("/group/<group>/resume", methods=["POST"])
def resume_group(group):
    write_file(os.path.join(GROUPS_DIR, group, "paused.txt"), "0")
    return redirect(f"/group/{group}")

if __name__ == "__main__":
    os.makedirs(GROUPS_DIR, exist_ok=True)
    threading.Thread(target=start_all_groups, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
