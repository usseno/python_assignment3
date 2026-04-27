import os
import csv
import json


# ---------- FileManager ----------
class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print("File found:", self.filename)
            return True
        else:
            print("File not found")
            return False

    def create_output_folder(self):
        if not os.path.exists("output"):
            os.makedirs("output")
            print("Output folder created")
        else:
            print("Output folder already exists")


# ---------- DataLoader ----------
class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("\nLoading data...")
        try:
            with open(self.filename) as file:
                reader = csv.DictReader(file)
                self.students = list(reader)

            print("Loaded:", len(self.students), "students")
        except:
            print("Error loading file")

        return self.students

    def preview(self):
        print("\nFirst 5 rows:")
        for i in range(5):
            s = self.students[i]
            print(s["student_id"], s["country"], s["GPA"])


# ---------- DataAnalyser (VARIANT B) ----------
class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        country_counts = {}

        for s in self.students:
            country = s["country"]

            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1

        # sort with lambda
        sorted_countries = sorted(
            country_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # lambda + filter
        high_gpa = list(filter(lambda s: float(s["GPA"]) > 3.5, self.students))

        self.result = {
            "total_countries": len(country_counts),
            "top_3": sorted_countries[:3],
            "high_gpa_count": len(high_gpa)
        }

        return self.result

    def print_results(self):
        print("\nCountry Analysis")
        print("Total countries:", self.result["total_countries"])

        print("Top 3:")
        for i, (c, n) in enumerate(self.result["top_3"]):
            print(i+1, c, n)

        print("Students with GPA > 3.5:", self.result["high_gpa_count"])


# ---------- ResultSaver ----------
class ResultSaver:
    def __init__(self, result):
        self.result = result

    def save(self):
        try:
            with open("output/result.json", "w") as f:
                json.dump(self.result, f, indent=4)

            print("\nSaved to output/result.json")
        except:
            print("Error saving")


# ---------- MAIN ----------
fm = FileManager("students.csv")

if not fm.check_file():
    exit()

fm.create_output_folder()

dl = DataLoader("students.csv")
dl.load()
dl.preview()

analyser = DataAnalyser(dl.students)
analyser.analyse()
analyser.print_results()

saver = ResultSaver(analyser.result)
saver.save()