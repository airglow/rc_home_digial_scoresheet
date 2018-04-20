#!/usr/bin/python2.7
import sys
import os

def print_normal(s, bold=False):
    if not bold:
        print text_normal + s
    else:
        print text_bold + s + text_normal
    return s


def print_red(s):
    print text_red + s + text_normal
    return s


def print_green(s):
    print text_green + s + text_normal
    return s


def format_text(text, points=None):
    text_f = '{:100s} Points {:7.2f}'.format(text, points)
    return text_f


###############################################################################
print "Usage like ./digital_score_sheet.py <ScoreSheetTexFile> <TeamName>"

if len(sys.argv) != 3:
    quit()


filename = sys.argv[1]
score_sheet_tex_file = open(filename, "r")
lines = score_sheet_tex_file.readlines()

team_name = sys.argv[2]
test_name = os.path.basename(filename)[:os.path.basename(filename).find(".")]

text_green = "\033[1;32;40m"
text_normal = "\033[0;37;40m"
text_red = "\033[1;31;40m"
text_bold = "\033[1;37;40m"


headline = "Scoring "+test_name+ " for Team " + team_name
report = []
report.append(headline)
print_normal(headline, bold=True)

sum_points = 0.0
for l in lines:
    l = l.strip()
    if l[:14] == "\scoreheading{":
        print ""
        print ""
        print_normal(l[14:-1], bold=True)
        print ""

    if l[:10] == "\scoreitem":
        points = int(l[l.find("{")+1:l.find("}")])

        # find number of repetitions (in square brackets)
        repetitions = 1
        if l.find("[") != -1:
            try:
                repetitions = int(l[l.find("[")+1:l.find("]")])
            except Exception, e:
                print "argument not a number therefore no repetition interpreted"
        for i in range(repetitions):
            text = "* " + l[l.find("}{")+2:-1]
            print_normal(format_text(text, points), True)

            choice = str(raw_input('Input (yY for granting nN for not grating hH for half):'))

            granted_points = 0.0
            if choice == "y" or choice == "Y":
                print_green(format_text("Points granted",  points))
                granted_points = points
            elif choice == "h" or choice == "H":
                print_red(format_text("Half Points granted", points / 2.0))
                granted_points = points / 2.0
            else:
                print_red(format_text("No Points granted", 0.0))
            print ""

            sum_points += granted_points

            report.append(format_text(text, granted_points))

summary = format_text("Sum Points", sum_points)
print_normal(summary)
report.append(summary)

report_file = open("scores_"+team_name+"_"+test_name+".txt", "w")

for item in report:
    report_file.write("%s\n" % item)

print "\n\n######## REPORT"
for r in report:
    print r
