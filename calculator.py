class Calculator:

    @staticmethod
    def calculate_carbon_footprint(inputs):
        electricity = inputs['monthly_electricity_bill'] * 12 * 0.0005
        gas = inputs['monthly_natural_gas_bill'] * 12 * 0.0053
        fuel = inputs['monthly_fuel_bill'] * 12 * 2.32

        waste = inputs['waste_generated'] * 12 * (0.57 - inputs['recycled_or_composted_percentage'] / 100)

        travel = inputs['kilometers_traveled'] * (1 / inputs['fuel_efficiency']) * 2.31

        total = electricity + gas + fuel + waste + travel

        return {
            "electricity": electricity,
            "gas": gas,
            "fuel": fuel,
            "waste": waste,
            "travel": travel,
            "total": total
        }
