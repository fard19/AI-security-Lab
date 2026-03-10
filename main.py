from attack_engine.adversarial_runner import AdversarialRobustnessTest
from typing import Optional, Dict
import json
from datetime import datetime
from pathlib import Path
import sys
import re


class InteractiveAdversarialTest:

    def __init__(self, primary_goal: str):
        self.primary_goal = primary_goal
        self.tester: Optional[AdversarialRobustnessTest] = None
        self.last_result: Optional[Dict] = None
        self.session_results = []

    # --------------------------------------------------

    def validate_input(self, objective: str):

        if not objective or not objective.strip():
            return False, "Objective cannot be empty"

        if len(objective) < 10:
            return False, "Objective too short"

        if len(objective) > 500:
            return False, "Objective too long"

        words = objective.split()
        if len(words) < 3:
            return False, "Objective must contain at least 3 words"

        return True, "Valid"

    # --------------------------------------------------
    # NEW: Filename generator from prompt
    # --------------------------------------------------

    def generate_filename_from_objective(self, objective: str):

        name = objective.lower().strip()

        # remove symbols
        name = re.sub(r"[^a-z0-9\s-]", "", name)

        # spaces -> underscore
        name = name.replace(" ", "_")

        # shorten
        name = name[:40]

        if not name:
            name = "adversarial_report"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        return f"{name}_report_{timestamp}.json"

    # --------------------------------------------------

    def run_interactive_test(
        self,
        objective: Optional[str] = None,
        rounds: int = 3,
        auto_export: bool = False
    ):

        if objective is None:

            print("\n" + "="*70)
            print("ADVERSARIAL ROBUSTNESS TEST")
            print("="*70)
            print("Primary Goal:", self.primary_goal)

            objective = input("\nEnter adversarial objective:\n> ").strip()

        valid, message = self.validate_input(objective)

        if not valid:
            print("\nValidation failed:", message)
            return None

        print("\nObjective:", objective)
        print("Rounds:", rounds)

        confirm = input("\nProceed with test? (y/n): ").lower()

        if confirm not in ["y", "yes"]:
            print("Cancelled")
            return None

        try:

            self.tester = AdversarialRobustnessTest(self.primary_goal)

            result = self.tester.run_test(
                objective=objective,
                rounds=rounds,
                verbose=True
            )

            self.last_result = result

            self.session_results.append({
                "objective": objective,
                "timestamp": datetime.now().isoformat(),
                "summary": result
            })

            if auto_export:
                self.export_last_result(objective)

            self._post_test_menu(objective)

            return result

        except Exception as e:

            print("\nTEST ERROR:", str(e))

            retry = input("Retry? (y/n): ").lower()

            if retry in ["y", "yes"]:
                return self.run_interactive_test(objective, rounds, auto_export)

            return None

    # --------------------------------------------------

    def _post_test_menu(self, objective):

        print("\n" + "-"*70)
        print("POST TEST ACTIONS")
        print("1. Export full report")
        print("2. Run another test")
        print("3. Session summary")
        print("4. Exit")
        print("-"*70)

        choice = input("\nSelect action: ").strip()

        if choice == "1":
            self.export_last_result(objective)

        elif choice == "2":
            self.run_interactive_test()

        elif choice == "3":
            self.show_session_summary()
            self._post_test_menu(objective)

        elif choice == "4":
            print("Exiting")

        else:
            print("Invalid choice")

    # --------------------------------------------------

    def export_last_result(self, objective):

        if not self.tester:
            print("No results available")
            return None

        try:

            filename = self.generate_filename_from_objective(objective)

            output_dir = Path("test_results")
            output_dir.mkdir(exist_ok=True)

            filepath = output_dir / filename

            report = self.tester.export_results(objective)

            if report:

                with open(filepath, "w") as f:
                    json.dump(report, f, indent=2)

            print(f"\n✓ Results exported to {filepath}\n")

            return str(filepath)

        except Exception as e:

            print("Export failed:", str(e))
            return None

    # --------------------------------------------------

    def show_session_summary(self):

        if not self.session_results:
            print("\nNo tests run yet")
            return

        print("\n" + "="*70)
        print("SESSION SUMMARY")
        print("="*70)

        for i, result in enumerate(self.session_results, 1):

            summary = result["summary"]
            pressure = summary.get("pressure", {})

            print("\nTest", i)
            print("Objective:", result["objective"][:60])
            print("Avg Pressure:", pressure.get("avg", 0))
            print("Escalation:", pressure.get("escalation", False))

    # --------------------------------------------------

    def run_batch_mode(self, objectives, rounds=3):

        results = []

        for obj in objectives:

            valid, msg = self.validate_input(obj)

            if not valid:
                print("Skipped:", msg)
                continue

            try:

                self.tester = AdversarialRobustnessTest(self.primary_goal)

                result = self.tester.run_test(obj, rounds, verbose=False)

                results.append({
                    "objective": obj,
                    "result": result
                })

            except Exception as e:

                results.append({
                    "objective": obj,
                    "error": str(e)
                })

        return results


# --------------------------------------------------

def enhanced_interactive():

    goal = "Secure the company's network infrastructure."

    interactive = InteractiveAdversarialTest(goal)

    interactive.run_interactive_test(rounds=3)


# --------------------------------------------------

def main():

    if len(sys.argv) > 1:

        objective = " ".join(sys.argv[1:])

        goal = "Secure the company's network infrastructure."

        tester = AdversarialRobustnessTest(goal)

        tester.run_test(objective, rounds=3)

        tester.export_results(objective)

    else:

        enhanced_interactive()


# --------------------------------------------------

if __name__ == "__main__":

    main()