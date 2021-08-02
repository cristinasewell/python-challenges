import os
import csv
from collections import Counter

poll_csv = os.path.join(".", "Resources", "election_data.csv")
total_votes = 0
candidates = None
total_candidates = []
winer = None

# have a dash line here because we're using it multiple times
dash_line = '------------------------------'

# have a total_results list of string that we can use for both
# printing on the terminal and writing on a file with
total_results = [
        'Election Results',
        dash_line,
        f'Total Votes: {total_votes}', 
        dash_line]

total_count = []

with open (poll_csv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ",")
    csv_header = next(csv_file)
    for row in csv_reader:
        total_votes +=1 
        total_candidates.append(row[2])
      
    candidates = Counter(total_candidates)

    # keep this to compare percentages and get the largets one
    max_percent = 0
    for name, votes in candidates.items():
        percent = (votes/total_votes)*100
        # check if current percentage is bigger than max_percentage
        # if so, replace the max_percentage with this one
        if percent >= max_percent:
            # replace the max_percent with percent 
            max_percent = percent
            # make the winner this one
            winner = name
        result = f"{name}: {percent:.3f}% (votes)"
        total_results.append(result)
        
winner_str = f'Winner: {winner}'
total_results.append(winner_str)
total_results.append(dash_line)

def print_on_terminal():
    for line in total_results:
        print(line)


def write_to_analysis():
    analysis_file = os.path.join(".", "analysis", "analysis.txt")
    with open (analysis_file, 'w') as text_file:
        for line in total_results:
            # write the elements in the list + a new line after each element
            text_file.write(line + '\n')
    
print_on_terminal()
write_to_analysis()
