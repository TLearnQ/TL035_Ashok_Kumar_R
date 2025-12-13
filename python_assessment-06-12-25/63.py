# QUESTION NO:63

data = [
    "Ashok,89,88,88",
    "vish,78,80,93",
    "mash,77,77,77",
]
# "name,mark1,mark2,attendance"
output = []

for data_link in data:
    parts = data_link.split(",")

    student = {
        "name":parts[0],
        "totalMarks":int(parts[1])+int(parts[2]),
        "attendance":float(parts[3])
    }

    if student["totalMarks"]>=180 and student["attendance"]>=80:
        student["grades"]="excellent"
    elif student["totalMarks"]>=150 and student["totalMarks"]<180 and student["attendance"]>=70:
        student["grades"]="on Track"
    elif student["totalMarks"]>=120 and student["totalMarks"]<150 and student["attendance"]>=60:
        student["grades"]="at Risk"
    else:
        student["grades"]="failing"

    output.append(student)

print(output)
