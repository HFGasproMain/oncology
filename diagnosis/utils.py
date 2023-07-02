def calculate_accuracy(selected_symptoms, cancer_type):
    matched_symptoms = set(selected_symptoms)
    count = len(matched_symptoms)
    print(f'user symptoms => {matched_symptoms}, count({count})')
    total_symptoms = set(cancer_type.symptoms.all())
    count2 = len(total_symptoms)
    print(f'total symptoms for that cancer => {total_symptoms}, count2 ({count2})')
    accuracy = len(matched_symptoms) / len(total_symptoms) * 100
    return accuracy
