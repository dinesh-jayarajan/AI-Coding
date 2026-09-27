from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')


# Get the absolute path to the CSV file

# CSV_FILE = os.path.join(os.path.dirname(__file__), 'data', 'Tracker Canada -2025.csv')
# SEARCH_FIELDS = ['Job Title', 'Name', 'Mobile', 'email', 'Location', 'Visa Type ', 'Candidate rate', 'Submitted Rate']

# def read_csv():
#     """Read the master.csv file and return list of dictionaries"""
#     data = []
#     try:
#         with open(CSV_FILE, 'r', encoding='utf-8') as file:
#             csv_reader = csv.DictReader(file)
#             for row in csv_reader:
#                 data.append(row)
#     except FileNotFoundError:
#         print(f"Error: {CSV_FILE} not found")
#     return data

import openpyxl
from openpyxl import load_workbook

EXCEL_FILE = '/Users/dineshjayarajan/Desktop/Dinesh Jayarajan/Dinesh Jayarajan/Learning/front-end-app/data/Tracker Canada-2026.xlsx'
SHEET_NAMES = ['Capgemini', 'Tech M', 'TCS','Persistent']
SEARCH_FIELDS = ['Job Title', 'Name', 'Mobile', 'email', 'Location', 'Visa Type ', 'Candidate rate', 'Submitted Rate']



def read_excel():
    """Read specific sheets from Excel file and return combined list of dictionaries"""
    data = []
    try:
        workbook = load_workbook(EXCEL_FILE)
        
        for sheet_name in SHEET_NAMES:
            if sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                headers = []
                
                # Get headers from first row and handle None values
                for cell in sheet[1]:
                    headers.append(cell.value if cell.value is not None else '')
                
                # Read data rows
                for row in sheet.iter_rows(min_row=2, values_only=False):
                    record = {}
                    for i, cell in enumerate(row):
                        if i < len(headers):
                            # Convert cell value to string, handle None
                            cell_value = cell.value
                            if cell_value is None:
                                record[headers[i]] = ''
                            else:
                                record[headers[i]] = str(cell_value).strip()
                    
                    # Only add non-empty records
                    if any(record.values()):
                        data.append(record)
                        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()
    
    return data

def search_by_criteria(search_term):
    """Search for records matching any of the SEARCH_FIELDS"""
    data = read_excel()
    search_lower = search_term.lower()
    results = []
    seen = set()  # Track duplicates
    
    for record in data:
        for field in SEARCH_FIELDS:
            value = record.get(field, '')
            if value and isinstance(value, str) and search_lower in value.lower():
                # Create a unique key from record (using Name + Email to identify duplicates)
                record_key = (record.get('Name', ''), record.get('email', ''))
                
                if record_key not in seen:
                    results.append(record)
                    seen.add(record_key)
                break
    
    return results

def search_by_job_description(job_description):
    """Search for records matching the job description"""
    data = read_csv()
    job_desc_lower = job_description.lower()
    results = []
    
    for record in data:
        if job_desc_lower in record['job_description'].lower():
            results.append(record)
    
    return results

# import requests
# from io import BytesIO
# from openpyxl import load_workbook

# # SharePoint file URL (get from SharePoint - right-click file > Copy link)
# SHAREPOINT_URL = 'https://yourcompany.sharepoint.com/sites/YourSite/Shared%20Documents/Tracker%20Canada%20-2025.xlsx'

# def read_excel():
#     """Read Excel file directly from SharePoint"""
#     data = []
#     try:
#         # Download file from SharePoint
#         response = requests.get(SHAREPOINT_URL)
#         response.raise_for_status()
        
#         # Load workbook from bytes
#         workbook = load_workbook(BytesIO(response.content))
        
#         for sheet_name in SHEET_NAMES:
#             if sheet_name in workbook.sheetnames:
#                 sheet = workbook[sheet_name]
#                 headers = []
                
#                 for cell in sheet[1]:
#                     headers.append(cell.value if cell.value is not None else '')
                
#                 for row in sheet.iter_rows(min_row=2, values_only=False):
#                     record = {}
#                     for i, cell in enumerate(row):
#                         if i < len(headers):
#                             cell_value = cell.value
#                             if cell_value is None:
#                                 record[headers[i]] = ''
#                             else:
#                                 record[headers[i]] = str(cell_value).strip()
                    
#                     if any(record.values()):
#                         data.append(record)
                        
#     except Exception as e:
#         print(f"Error reading SharePoint file: {e}")
#         import traceback
#         traceback.print_exc()
    
#     return data

# def search_by_criteria(search_term):
#     """Search for records matching any of the SEARCH_FIELDS"""
#     data = read_csv()
#     search_lower = search_term.lower()
#     results = []
    
#     for record in data:
#         for field in SEARCH_FIELDS:
#             value = record.get(field, '')
#             if value and search_lower in value.lower():
#                 results.append(record)
#                 break
    
#     return results

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index1.html')

@app.route('/api/search', methods=['POST'])
def search():
    """Handle search"""
    try:
        data = request.get_json()
        search_term = data.get('search_term', '').strip()
        
        if not search_term:
            return jsonify({'success': False, 'message': 'Please enter a search term'}), 400
        
        results = search_by_criteria(search_term)
        
        if not results:
            return jsonify({'success': False, 'message': 'No matching records found'}), 404
        
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    

@app.route('/api/send-email', methods=['POST'])
def send_email():
    """Handle sending email to candidate"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({'success': False, 'message': 'Email address is required'}), 400
        
        return jsonify({'success': True, 'message': f'Email would be sent to {email}'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
