import os
import pandas as pd
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# Load dataset
csv_path = "personas.csv"
df = pd.read_csv(csv_path, dtype=str)

@app.route('/', methods=['GET', 'POST'])
def index():
    fav_products = sorted(df['fav_product'].dropna().unique())
    fav_categories = sorted(df['fav_category'].dropna().unique())
    fav_discounts = sorted(df['fav_discount_bucket'].dropna().unique())
    fav_days = sorted(df['fav_day_time'].dropna().unique())
    fav_stores = sorted(df['fav_store'].dropna().unique())
    fav_channels = sorted(df['fav_channel'].dropna().unique())

    filtered_df = df.copy()

    # Handle multi-select filters
    fav_product = request.form.getlist('fav_product')
    fav_category = request.form.getlist('fav_category')
    fav_discount = request.form.getlist('fav_discount')
    fav_day = request.form.getlist('fav_day_time')
    fav_store = request.form.getlist('fav_store')
    fav_channel = request.form.getlist('fav_channel')
    phone_no = request.form.get('phone')

    # Apply filters
    if fav_product:
        filtered_df = filtered_df[filtered_df['fav_product'].isin(fav_product)]
    if fav_category:
        filtered_df = filtered_df[filtered_df['fav_category'].isin(fav_category)]
    if fav_discount:
        filtered_df = filtered_df[filtered_df['fav_discount_bucket'].isin(fav_discount)]
    if fav_day:
        filtered_df = filtered_df[filtered_df['fav_day_time'].isin(fav_day)]
    if fav_store:
        filtered_df = filtered_df[filtered_df['fav_store'].isin(fav_store)]
    if fav_channel:
        filtered_df = filtered_df[filtered_df['fav_channel'].isin(fav_channel)]
    if phone_no:
        filtered_df = filtered_df[filtered_df['phone_no'] == phone_no]

    # Handle CSV download request
    if 'download' in request.form:
        output_csv = "filtered_personas.csv"
        filtered_df.to_csv(output_csv, index=False)
        return send_file(output_csv, as_attachment=True)

    return render_template(
        'index.html',
        fav_products=fav_products, fav_categories=fav_categories,
        fav_discounts=fav_discounts, fav_days=fav_days,
        fav_stores=fav_stores, fav_channels=fav_channels,
        data=df
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    # return render_template(
    #     'index.html',
    #     data=df,  # Pass the dataframe
    #     fav_products=fav_products, fav_categories=fav_categories,
    #     fav_discounts=fav_discounts, fav_days=fav_days,
    #     fav_stores=fav_stores, fav_channels=fav_channels
    # )