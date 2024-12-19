from calculator import Calculator
from company import Company
from question_list import questions_list


def get_user_inputs():
    print("\nWelcome to the Carbon Footprint Monitoring Tool")
    company_name = input("Enter your company name: ")

    inputs = {}
    for category, fields in questions_list.items():
        print(f"\n{category}")
        for field, details in fields.items():
            question = details['question']
            while True:
                try:
                    value = float(input(question + " "))
                    inputs[field] = value
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")

    return Company(company_name, **inputs)


if __name__ == '__main__':
    all_companies = []

    while True:
        company = get_user_inputs()
        all_companies.append(company)

        results = Calculator.calculate_carbon_footprint(company.data)
        print(f"Carbon footprint: {results}")

        choice = input("\nDo you want to (1) Stop or (2) Add another company? Enter 1 or 2: ")
        if choice == "1":
            break
