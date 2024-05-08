from flask import Flask, render_template, request
from edgar import *  # Assuming you have the edgar library installed

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        cik = request.form["cik"]
        try:
            # Replace with your Edgar access information (if needed)
            set_identity("Rishabh Bhati rishabhbhati478@gmail.com")

            filings = get_filings()
            company = Company(cik)
            tenk = company.get_filings(form="10-K").latest(1).obj()
            financials = tenk.financials

            df = financials.income_statement.to_dataframe()
            df_transposed = df.transpose()
            print(df_transposed['EarningsPerShareBasic'])

            # Optional: Generate plot as base64 encoded image
            import matplotlib.pyplot as plt
            column_to_plot = 'EarningsPerShareBasic'

            plt.figure(figsize=(8, 5))  # Adjust figure size as needed
            plt.plot(df_transposed.index, df_transposed[column_to_plot])
            plt.xlabel('2023-09-30')  # Assuming latest filing date
            plt.ylabel(column_to_plot)
            plt.title(f"{column_to_plot} over Time")
            plt.grid(True)

            # Optional: Convert plot to base64 for embedding in HTML
            from io import BytesIO
            import base64

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            image_b64 = base64.b64encode(buffer.getvalue()).decode('ascii')

            return render_template("index.html", cik=cik, has_results=True, image_b64=image_b64)  # Pass cik, success flag, and image (optional)
        except Exception as e:
            return render_template("index.html", cik=cik, error=str(e))  # Pass error message
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
