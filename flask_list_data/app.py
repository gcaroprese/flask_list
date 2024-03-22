from flask import Flask, render_template
import csv

app = Flask(__name__)

def get_data():
    records_per_year = {}
    shortest_names = {}
    longest_names = {}
    name_polindromes = {}
    names_used = {}

    with open("registered-names-1922-2015.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year = row['year']
            count_names = int(row['count'])
            checked_name = row.get('name').strip()
            checked_name_length = len(checked_name)

            # Records per year
            if year in records_per_year:
                records_per_year[year] += count_names
            else:
                records_per_year[year] = count_names

            # Shortest name
            if checked_name_length <= len(shortest_names):
                shortest_names = {checked_name_length: [checked_name]}
            elif checked_name_length == len(shortest_names):
                shortest_names[checked_name_length].append(checked_name)

            # Longest name
            if checked_name_length >= len(longest_names):
                longest_names = {checked_name_length: [checked_name]}
            elif checked_name_length == len(longest_names):
                longest_names[checked_name_length].append(checked_name)

            # Palindrome name
            if checked_name[::-1].lower() == checked_name.lower() and checked_name[:1].isalpha():
                name_polindromes[checked_name] = checked_name

            # Most used name
            name_count = int(row.get('count', 0))
            if name_count >= max(names_used.values()):
                if checked_name not in names_used:
                    names_used[checked_name] = name_count
                else:
                    names_used[checked_name] += name_count

    return records_per_year, shortest_names, longest_names, name_polindromes, names_used

@app.route('/')
def index():
    records_per_year, shortest_names, longest_names, name_polindromes, names_used = get_data()
    return render_template('index.html', records=records_per_year, shortest_names=shortest_names, longest_names=longest_names, name_polindromes=name_polindromes, most_used_name=max(names_used, key=lambda k: names_used[k]))

if __name__ == '__main__':
    app.run(debug=True)
