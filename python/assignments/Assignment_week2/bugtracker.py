class bugtracker:
    def __init__(self):
        self.bugs = {}
    def add_bug(self, bug_id, description, severity):
        self.bugs[bug_id] = {
            "description": description,
            "severity": severity,
            "status": "open"
        }
    def update_status(self, bug_id, new_status):
        self.bugs[bug_id]["status"] = new_status

    # def list_all_bugs(self):
    #     for bug_id in self.bugs.items():
    #         print(f"Bug ID: {bug_id}, Description: {bug_id['description']}, Severity: {bug_id['severity']}, Status: {bug_id['status']}")

if __name__ == "__main__":
    tracker = bugtracker()
    tracker.add_bug("0001", "Login button not working", "high")
    tracker.add_bug("0002", "Typo in homepage", "low")
    tracker.update_status("0001", "in progress")
    # tracker.list_all_bugs()