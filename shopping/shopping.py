import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def month_to_number(month_name):
    months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "Jun": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }
    
    # Return the corresponding number for the given month name
    return months.get(month_name, -1)

def visitor_to_boolean(visitorType):
    visitor = int()
    if visitorType == "Returning_Visitor":
        visitor = 1
    else:
        visitor = 0
    return visitor

def boolean_to_int(boolean):
    result = int()
    if boolean == "TRUE":
        result = 1
    else:
        result = 0
    return result


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    csv_file_path = 'shopping.csv'

    # Initialize an empty list to store the data
    evidence = []
    labels = []

    # Open the CSV file and read its contents
    with open(csv_file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the data list
            evidence.append([
                # - Administrative, an integer
                int(row[0]),
                # - Administrative_Duration, a floating point number
                float(row[2]),
                # - Informational, an integer
                int(float(row[3])),
                # - Informational_Duration, a floating point number
                float(row[3]),
                # - ProductRelated, an integer
                int(row[4]),
                # - ProductRelated_Duration, a floating point number
                float(row[5]),
                # - BounceRates, a floating point number
                float(row[6]),
                # - ExitRates, a floating point number
                float(row[7]),
                # - PageValues, a floating point number
                float(row[8]),
                # - SpecialDay, a floating point number
                float(row[9]),
                # - Month, an index from 0 (January) to 11 (December)
                int(month_to_number(str(row[10]))),
                # - OperatingSystems, an integer
                int(row[11]),
                # - Browser, an integer
                int(row[12]),
                # - Region, an integer
                int(row[13]),
                # - TrafficType, an integer
                int(row[14]),
                # - VisitorType, an integer 0 (not returning) or 1 (returning)
                int(visitor_to_boolean(str(row[15]))),
                # - Weekend, an integer 0 (if false) or 1 (if true)
                int(boolean_to_int(str(row[16])))
            ])
            # Label
            labels.append(
                int(boolean_to_int(row[17]))
            )
    # print(f"EVIDENCE: {evidence} \n LABLES: {labels}")
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model




def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = float()
    sensitivity_n = labels.count(1)
    specificity = float()
    specificity_n = labels.count(0)

    for row in range(0, len(labels)-1):
        if labels[row] == 1:
                if predictions[row] == 1:
                    sensitivity += 1
        if labels[row] == 0:
            if predictions[row] == 0:
                specificity += 1
    sensitivity = sensitivity/sensitivity_n
    specificity = specificity/specificity_n

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
