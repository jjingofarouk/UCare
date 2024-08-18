import datetime
import sqlite3
import matplotlib.pyplot as plt

class CarbonFootprintTracker:
    def __init__(self):
        self.conn = sqlite3.connect('carbon_footprint.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY,
                date TEXT,
                category TEXT,
                amount REAL,
                unit TEXT,
                emissions REAL
            )
        ''')
        self.conn.commit()

    def add_activity(self, date, category, amount, unit):
        emissions = self.calculate_emissions(category, amount, unit)
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO activities (date, category, amount, unit, emissions)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, category, amount, unit, emissions))
        self.conn.commit()

    def calculate_emissions(self, category, amount, unit):
        # Emission factors (kg CO2e per unit)
        factors = {
            'electricity': 0.41,  # per kWh
            'natural_gas': 0.18,  # per kWh
            'car': 0.192,  # per km
            'bus': 0.103,  # per km
            'train': 0.041,  # per km
            'plane': 0.255,  # per km
            'meat': 6.61,  # per kg
            'dairy': 1.39,  # per kg
            'fruits_veggies': 0.37,  # per kg
            'grains': 0.81,  # per kg
        }
        return amount * factors.get(category, 0)

    def get_total_emissions(self, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT SUM(emissions) FROM activities
            WHERE date BETWEEN ? AND ?
        ''', (start_date, end_date))
        return cursor.fetchone()[0] or 0

    def get_emissions_by_category(self, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT category, SUM(emissions) FROM activities
            WHERE date BETWEEN ? AND ?
            GROUP BY category
        ''', (start_date, end_date))
        return dict(cursor.fetchall())

    def plot_emissions_by_category(self, start_date, end_date):
        emissions_by_category = self.get_emissions_by_category(start_date, end_date)
        categories = list(emissions_by_category.keys())
        emissions = list(emissions_by_category.values())

        plt.figure(figsize=(10, 6))
        plt.bar(categories, emissions)
        plt.title(f'Carbon Emissions by Category ({start_date} to {end_date})')
        plt.xlabel('Category')
        plt.ylabel('Emissions (kg CO2e)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def suggest_reductions(self, start_date, end_date):
        emissions_by_category = self.get_emissions_by_category(start_date, end_date)
        suggestions = []

        if emissions_by_category.get('car', 0) > 100:
            suggestions.append("Consider carpooling or using public transport to reduce car emissions.")
        if emissions_by_category.get('electricity', 0) > 200:
            suggestions.append("Try to reduce electricity usage or switch to renewable energy sources.")
        if emissions_by_category.get('meat', 0) > 50:
            suggestions.append("Consider reducing meat consumption or trying plant-based alternatives.")
        if emissions_by_category.get('plane', 0) > 500:
            suggestions.append("Look for alternatives to air travel when possible, such as train or videoconferencing.")

        return suggestions

def main():
    tracker = CarbonFootprintTracker()

    while True:
        print("\nCarbon Footprint Tracker")
        print("1. Add activity")
        print("2. View total emissions")
        print("3. View emissions by category")
        print("4. Get reduction suggestions")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            unit = input("Enter unit: ")
            tracker.add_activity(date, category, amount, unit)
            print("Activity added successfully!")

        elif choice == '2':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            total_emissions = tracker.get_total_emissions(start_date, end_date)
            print(f"Total emissions from {start_date} to {end_date}: {total_emissions:.2f} kg CO2e")

        elif choice == '3':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            tracker.plot_emissions_by_category(start_date, end_date)

        elif choice == '4':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            suggestions = tracker.suggest_reductions(start_date, end_date)
            print("Suggestions to reduce your carbon footprint:")
            for suggestion in suggestions:
                print(f"- {suggestion}")

        elif choice == '5':
            print("Thank you for using the Carbon Footprint Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
