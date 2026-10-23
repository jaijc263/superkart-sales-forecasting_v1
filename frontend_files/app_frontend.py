import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title='SuperKart Sales Forecaster', layout='wide')
st.title('SuperKart Sales Revenue Forecasting System')

# Define the Backend URL pointing to the Flask API inside the Docker network
BACKEND_URL = 'http://backend-api:7860'

tab1, tab2 = st.tabs(['Online Single Prediction', 'Batch CSV Prediction'])

with tab1:
    st.header('Single Product Sales Prediction')
    st.write('Enter details of a specific product and store location below:')
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_weight = st.number_input('Product Weight (kg)', min_value=1.0, max_value=50.0, value=12.5, step=0.1)
        product_sugar = st.selectbox('Product Sugar Content', ['Low Sugar', 'Regular', 'No Sugar'])
        allocated_area = st.slider('Product Allocated Area Ratio', min_value=0.0, max_value=1.0, value=0.05, step=0.01)
        product_mrp = st.number_input('Product Maximum Retail Price (MRP)', min_value=1.0, max_value=500.0, value=150.0, step=0.5)
        product_id_char = st.selectbox('Product ID Category (First 2 chars)', ['FD', 'DR', 'NC'])
        
    with col2:
        store_size = st.selectbox('Store Size', ['Small', 'Medium', 'High'])
        store_location = st.selectbox('Store Location City Type', ['Tier 1', 'Tier 2', 'Tier 3'])
        store_type = st.selectbox('Store Type', ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Food Mart'])
        store_age = st.number_input('Store Age (Years)', min_value=0, max_value=100, value=15, step=1)
        product_category = st.selectbox('Product Category Group', ['Perishables', 'Non Perishables'])
        
    if st.button('Predict Sales'):
        # Prepare the single inference payload
        payload = {
            'Product_Weight': float(product_weight),
            'Product_Sugar_Content': product_sugar,
            'Product_Allocated_Area': float(allocated_area),
            'Product_MRP': float(product_mrp),
            'Store_Size': store_size,
            'Store_Location_City_Type': store_location,
            'Store_Type': store_type,
            'Product_Id_char': product_id_char,
            'Store_Age_Years': int(store_age),
            'Product_Type_Category': product_category
        }
        
        try:
            response = requests.post(f'{BACKEND_URL}/v1/predict', json=payload)
            if response.status_code == 200:
                prediction = response.json().get('prediction', 0.0)
                st.success(f'### Predicted Total Store Sales: ${prediction:,.2f}')
            else:
                st.error(f'Error from API: {response.json().get("error", "Unknown error")}')
        except Exception as e:
            st.error(f'Connection failed to backend API server: {e}')

with tab2:
    st.header('Batch Sales Prediction via CSV Upload')
    st.write('Upload a CSV file containing batch details of products/stores. Required columns are specified in the guidebook.')
    
    uploaded_file = st.file_uploader('Choose a CSV file...', type='csv')
    
    if uploaded_file is not None:
        # Read and display input CSV preview
        input_df = pd.read_csv(uploaded_file)
        st.write('### Input Data Preview', input_df.head())
        
        if st.button('Run Batch Inference'):
            # Reset file pointer and prepare payload
            uploaded_file.seek(0)
            files = {'file': uploaded_file.getvalue()}
            
            try:
                response = requests.post(f'{BACKEND_URL}/v1/predictbatch', files={'file': ('batch.csv', uploaded_file.getvalue(), 'text/csv')})
                if response.status_code == 200:
                    predictions_dict = response.json()
                    
                    # Map predictions back onto the input dataframe
                    pred_list = [predictions_dict[str(i)] for i in range(len(predictions_dict))]
                    input_df['Predicted_Sales_Total'] = pred_list
                    
                    st.success('Batch predictions processed successfully!')
                    st.write('### Predicted Output Results', input_df)
                    
                    # Option to download predictions CSV
                    csv_output = input_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label='Download Prediction Results as CSV',
                        data=csv_output,
                        file_name='superkart_batch_predictions.csv',
                        mime='text/csv'
                    )
                else:
                    st.error(f'Error from API: {response.json().get("error", "Unknown error")}')
            except Exception as e:
                st.error(f'Connection failed to backend API server: {e}')