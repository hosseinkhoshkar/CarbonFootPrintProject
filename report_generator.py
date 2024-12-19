import matplotlib.pyplot as plt
from fpdf import FPDF
from calculator import Calculator
import os


class ReportGenerator:

    @staticmethod
    def generate_pdf_report(company, results, all_companies):
        if not os.path.exists("report"):
            os.mkdir("report")

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt=f"Carbon Footprint Report: {company.name}", ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, txt="Category-wise Breakdown (in tons of CO2)", ln=True)
        for category, value in results.items():
            if category != "total":
                pdf.cell(200, 10, txt=f"{category.capitalize()}: {value:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total: {results['total']:.2f}", ln=True)

        pdf.ln(10)
        labels = [k.capitalize() for k in results.keys() if k != "total"]
        sizes = [v for k, v in results.items() if k != "total"]
        explode = [0.1 if i == max(sizes) else 0 for i in sizes]
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explode, shadow=True, startangle=140,
                colors=plt.cm.Paired.colors, textprops={'fontsize': 10, 'weight': 'bold'})
        plt.title("Company Carbon Footprint Breakdown", fontsize=14)
        plt.tight_layout()
        pie_chart_path = "report/temp_pie_chart.png"
        plt.savefig(pie_chart_path, dpi=300)
        plt.close()
        pdf.image(pie_chart_path, x=30, y=150, w=100)
        os.remove(pie_chart_path)

        pdf.add_page()
        companies = [comp.name for comp in all_companies]
        totals = [Calculator.calculate_carbon_footprint(comp.data)['total'] for comp in all_companies]
        plt.figure(figsize=(10, 6))
        plt.bar(companies, totals, color=plt.cm.Paired.colors)
        plt.title("Total Carbon Footprint Comparison", fontsize=14)
        plt.xlabel("Companies", fontsize=12)
        plt.ylabel("Total CO2 (tons)", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()
        bar_chart_path = "report/temp_bar_chart.png"
        plt.savefig(bar_chart_path, dpi=300)
        plt.close()
        pdf.image(bar_chart_path, x=30, y=50, w=150)
        os.remove(bar_chart_path)

        # Summary Table
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Summary Table", ln=True)

        pdf.set_font("Arial", size=10)
        pdf.cell(40, 10, "Company Name", 1)
        pdf.cell(40, 10, "Electricity", 1)
        pdf.cell(40, 10, "Gas", 1)
        pdf.cell(40, 10, "Fuel", 1)
        pdf.cell(40, 10, "Total", 1, ln=True)

        for comp in all_companies:
            comp_results = Calculator.calculate_carbon_footprint(comp.data)
            pdf.cell(40, 10, comp.name, 1)
            pdf.cell(40, 10, f"{comp_results['electricity']:.2f}", 1)
            pdf.cell(40, 10, f"{comp_results['gas']:.2f}", 1)
            pdf.cell(40, 10, f"{comp_results['fuel']:.2f}", 1)
            pdf.cell(40, 10, f"{comp_results['total']:.2f}", 1, ln=True)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Recommendations", ln=True)
        recommendations = "1. Optimize energy usage by adopting renewable energy sources.\n" \
                          "2. Encourage recycling and reduce waste.\n" \
                          "3. Promote carpooling or use of fuel-efficient vehicles."
        pdf.multi_cell(200, 10, txt=recommendations)

        filename = f"report/{company.name}_report.pdf"
        pdf.output(filename)
        print(f"\nReport generated: {filename}")
