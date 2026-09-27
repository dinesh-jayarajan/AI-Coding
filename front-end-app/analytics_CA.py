import csv
import os
import pandas as pd
from datetime import datetime
from collections import defaultdict
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from io import BytesIO



## share point file url are not working, so I have downloaded the file and using it locally for now. I will fix the share point access issue later and update the code accordingly.

# sharepoint_url = "https://datapatternz.sharepoint.com/:x:/g/IQB_jBGn2IBrRYTVrWwdSrY0AXg9qMVdkkLZ8uqpdu0JAlU?e=3bg0lh"

# from office365.sharepoint.client_context import ClientContext
# from office365.runtime.auth.user_credential import UserCredential
# from io import BytesIO

# username = os.getenv("SHAREPOINT_USERNAME")
# account_secret = os.getenv("SHAREPOINT_SECRET")
# relative_url = "/sites/ProfileDB/Shared Documents/Tracker Canada-2026.xlsx"  # Adjust this path

# def get_excel_workbook():
#     try:
#         ctx = ClientContext(sharepoint_url).with_credentials(UserCredential(username, password))
#         file = ctx.web.get_file_by_server_relative_url(relative_url)
#         file_content = BytesIO()
#         file.download(file_content).execute_query()
#         file_content.seek(0)
#         return file_content
#     except Exception as e:
#         print(f"Error downloading Excel file from SharePoint: {e}")
#         return None


EXCEL_FILE = '/Users/dineshjayarajan/Desktop/Dinesh Jayarajan/Dinesh Jayarajan/Learning/front-end-app/data/Tracker Canada-2026.xlsx'
SHEET_NAMES = ['Capgemini', 'Tech M', 'TCS','Persistent']

# Email configuration for Outlook
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "deejay@datapattern.ai")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = 'ca-recruitment@datapattern.ai'  # Primary recipient email (can be the same as sender for BCC)
CC_EMAILS = 'deejay@datapattern.ai;dan@datapattern.ai;kathir@datapattern.ai;suryabharathi@datapattern.ai;ssmoses@datapattern.ai'  # CC recipients (semicolon separated)
BCC_EMAILS = 'ca-recruitment@datapattern.ai;ganesanv@datapattern.ai;gladson.moses@datapattern.ai'  # BCC recipients (semicolon separated)
#BCC_EMAILS=''

# def get_today_submissions():
#     results = defaultdict(lambda: defaultdict(lambda: {'New': 0, 'Profile DB': 0}))
#     today_date = datetime.now().strftime('%Y-%m-%d')
#     workbook_bytes = get_excel_workbook()
#     for sheet_name in SHEET_NAMES:
#         df = pd.read_excel(workbook_bytes, sheet_name=sheet_name)
#         df['Date of submission'] = pd.to_datetime(df['Date of submission'], errors='coerce').dt.strftime('%Y-%m-%d')
#         df_today = df[df['Date of submission'] == today_date]
#         print(f"Sheet: {sheet_name}, Looking for: {today_date}, Found: {len(df_today)} records")
#         for index, row in df_today.iterrows():
#             submitted_by = str(row['Recruiter Name']).strip() if pd.notna(row['Recruiter Name']) else 'Unknown'
#             source = str(row['Source']).strip() if pd.notna(row['Source']) else 'Unknown'
#             if source == 'New':
#                 results[submitted_by][sheet_name]['New'] += 1
#             elif source == 'Profile DB':
#                 results[submitted_by][sheet_name]['Profile DB'] += 1
#         workbook_bytes.seek(0)  # Reset pointer for next sheet
#     return results

def get_submissions(start_date, end_date):
    """Fetch submissions between start_date and end_date (inclusive), both as 'YYYY-MM-DD' strings."""
    results = defaultdict(lambda: defaultdict(lambda: {'New': 0, 'Profile DB': 0}))
    for sheet_name in SHEET_NAMES:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
        df['Date of submission'] = pd.to_datetime(df['Date of submission'], errors='coerce').dt.strftime('%Y-%m-%d')
        df_range = df[(df['Date of submission'] >= start_date) & (df['Date of submission'] <= end_date)]
        print(f"Sheet: {sheet_name}, Range: {start_date} to {end_date}, Found: {len(df_range)} records")
        for index, row in df_range.iterrows():
            submitted_by = str(row['Recruiter Name']).strip().lower() if pd.notna(row['Recruiter Name']) else 'unknown'
            source = str(row['Source']).strip() if pd.notna(row['Source']) else 'Unknown'
            if source == 'New':
                results[submitted_by][sheet_name]['New'] += 1
            elif source == 'Profile DB':
                results[submitted_by][sheet_name]['Profile DB'] += 1
    return results

def get_today_submissions():
    today_date = datetime.now().strftime('%Y-%m-%d')
    return get_submissions(today_date, today_date)

def get_weekly_submissions():
    """Returns submissions from last Friday to this Thursday (today-7 to today-1)."""
    from datetime import timedelta
    today = datetime.now()
    start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    return get_submissions(start_date, end_date)

def create_email_body(results, date_label=None):
    """Create HTML email body with a single combined table"""
    if date_label is None:
        date_label = datetime.now().strftime('%Y-%m-%d')
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <p>Hi Recruitment Team,</p>
        <p>Please find below the resourcing update for <strong>{date_label}</strong>:</p>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #ffb347; color: white;">
                    <th style="padding: 12px; text-align: left;">Recruiter</th>
                    {''.join([f'<th colspan="3" style="padding: 12px; text-align: center;">{vendor}</th>' for vendor in SHEET_NAMES])}
                    <th colspan="3" style="padding: 12px; text-align: center;">DAILY TOTAL</th>
                </tr>
                <tr style="background-color: #ffe4b2; color: #333;">
                    <th></th>
                    {''.join(['<th style="padding: 8px; text-align: center;">New</th><th style="padding: 8px; text-align: center;">Profile DB</th><th style="padding: 8px; text-align: center;">Total</th>' for _ in SHEET_NAMES])}
                    <th style="padding: 8px; text-align: center;">New</th><th style="padding: 8px; text-align: center;">Profile DB</th><th style="padding: 8px; text-align: center;">Total</th>
                </tr>
            </thead>
            <tbody>
    """
    # Collect all recruiters
    recruiters = sorted(results.keys())
    # Precompute daily totals
    daily_new = 0
    daily_db = 0
    daily_total = 0
    for recruiter in recruiters:
        row_html = f'<tr><td style="padding: 12px;">{recruiter}</td>'
        recruiter_new = 0
        recruiter_db = 0
        recruiter_total = 0
        for vendor in SHEET_NAMES:
            new_count = results[recruiter][vendor]['New'] if vendor in results[recruiter] else 0
            db_count = results[recruiter][vendor]['Profile DB'] if vendor in results[recruiter] else 0
            total = new_count + db_count
            recruiter_new += new_count
            recruiter_db += db_count
            recruiter_total += total
            row_html += f'<td style="padding: 8px; text-align: center;">{new_count}</td><td style="padding: 8px; text-align: center;">{db_count}</td><td style="padding: 8px; text-align: center;">{total}</td>'
        row_html += f'<td style="padding: 8px; text-align: center; font-weight: bold;">{recruiter_new}</td><td style="padding: 8px; text-align: center; font-weight: bold;">{recruiter_db}</td><td style="padding: 8px; text-align: center; font-weight: bold;">{recruiter_total}</td></tr>'
        html_body += row_html
        daily_new += recruiter_new
        daily_db += recruiter_db
        daily_total += recruiter_total
    # Add daily total row
    html_body += f'<tr style="background-color: #f0f0f0; font-weight: bold;"><td style="padding: 12px;">DAILY TOTAL</td>'
    for vendor in SHEET_NAMES:
        v_new = sum(results[recruiter][vendor]['New'] if vendor in results[recruiter] else 0 for recruiter in recruiters)
        v_db = sum(results[recruiter][vendor]['Profile DB'] if vendor in results[recruiter] else 0 for recruiter in recruiters)
        v_total = v_new + v_db
        html_body += f'<td style="padding: 8px; text-align: center;">{v_new}</td><td style="padding: 8px; text-align: center;">{v_db}</td><td style="padding: 8px; text-align: center;">{v_total}</td>'
    html_body += f'<td style="padding: 8px; text-align: center; font-weight: bold;">{daily_new}</td><td style="padding: 8px; text-align: center; font-weight: bold;">{daily_db}</td><td style="padding: 8px; text-align: center; font-weight: bold;">{daily_total}</td></tr>'
    html_body += """
                </tbody>
            </table>
            <p style="margin-top: 30px;">Best regards,<br>Data Pattern Analytics</p>
        </body>
    </html>
    """
    return html_body

def send_email_report(results, report_type='Daily', date_label=None):
    """Send email with the report using Outlook"""
    if not results:
        print("❌ No data to send")
        return
    
    try:
        current_date = datetime.now().strftime('%Y-%m-%d')
        subject = f"Recruitment Team {report_type} Update - {current_date}"
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = RECIPIENT_EMAIL
        msg['Cc'] = CC_EMAILS
        msg['Bcc'] = BCC_EMAILS
        
        # Email body
        html_body = create_email_body(results, date_label=date_label)
        msg.attach(MIMEText(html_body, 'html'))
        
        # Convert email strings to lists for sendmail
        to_list = [RECIPIENT_EMAIL]
        cc_list = [email.strip() for email in CC_EMAILS.split(';')]
        bcc_list = [email.strip() for email in BCC_EMAILS.split(';')]
        
        # Combine all recipients for sendmail
        all_recipients = to_list + cc_list + bcc_list
        
        # Send email via Outlook SMTP
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, all_recipients, msg.as_string())
        
        print(f"✅ Email sent successfully")
        print(f"   TO: {RECIPIENT_EMAIL}")
        print(f"   CC: {CC_EMAILS}")
        print(f"   BCC: {BCC_EMAILS}")
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def daily_report_at_7pm():
    """Function to run at 7:00 PM daily"""
    print(f"\n🔔 DAILY REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    today_date = datetime.now().strftime('%Y-%m-%d')
    results = get_today_submissions()
    if results:
        send_email_report(results, report_type='Daily', date_label=today_date)
    else:
        print("❌ No submissions found for today")

def weekly_report_on_friday():
    """Function to run every Friday — covers last Friday to this Thursday (today-6 to today-0)"""
    from datetime import timedelta
    print(f"\n🔔 WEEKLY REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    today = datetime.now()
    start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
    end_date = (today - timedelta(days=0)).strftime('%Y-%m-%d')
    date_label = f"{start_date} to {end_date}"
    results = get_weekly_submissions()
    if results:
        send_email_report(results, report_type='Weekly', date_label=date_label)
    else:
        print("❌ No submissions found for this week")

def schedule_daily_report():
    """Schedule the report to run daily at 8:00 PM"""
    schedule.every().day.at("20:13").do(daily_report_at_7pm)
    print("✅ Daily report scheduled for 8:00 PM every day")
    print("Press Ctrl+C to stop the scheduler\n")
    while True:
        schedule.run_pending()
        time.sleep(60)

def schedule_weekly_report():
    """Schedule the report to run every Thursday at 8:02 PM"""
    schedule.every().thursday.at("20:02").do(weekly_report_on_friday)
    print("✅ Weekly report scheduled for every Thursday at 8:02 PM")
    print("Press Ctrl+C to stop the scheduler\n")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'daily':
            schedule_daily_report()
        elif mode == 'weekly':
            schedule_weekly_report()
        else:
            print(f"❌ Unknown argument '{sys.argv[1]}'. Use 'daily' or 'weekly'.")
            sys.exit(1)
    else:
        # Run daily report once immediately (default)
        today_date = datetime.now().strftime('%Y-%m-%d')
        results = get_today_submissions()
        if results:
            send_email_report(results, report_type='Daily', date_label=today_date)
        else:
            print("❌ No submissions found for today")