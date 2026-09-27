# Sample Company - Job Search Portal

A beautiful, modern web application for searching professionals by job description using Flask and HTML/CSS.

## 📋 Features

- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Quick Search**: Search by job title or keywords (e.g., "Python Developer", "Senior", "Full Stack")
- **Professional UI**: Modern gradient design with company branding
- **Real-time Results**: Displays matching records in a clean table format
- **Company Branding**: Sample company logo and #ExampleCompany hashtag integration

## 📁 Project Structure

```
FRONT-END-APP/
├── app.py                 # Flask application
├── master.csv            # Database with 10 professional records
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Front-end page with embedded CSS
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher installed
- pip (Python package manager)

### Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open your browser and navigate to: `http://localhost:5000`
   - The page will load with the sample company logo and search interface

## 💡 How to Use

1. **Enter Job Description**: Type a job description in the search box
   - Examples: "Python Developer", "Senior", "Full Stack", "Java", etc.

2. **Click Search**: Press the "Search" button or hit Enter key

3. **View Results**: Matching records are displayed in a professional table with:
   - Employee Name
   - Email ID
   - Job Description
   - Phone Number
   - Bill Rate ($)

## 📊 Database (master.csv)

The CSV file contains 10 sample records with the following fields:
- **name**: Employee name
- **emailid**: Corporate email address
- **job_description**: Job title/description
- **phone_number**: Contact phone number
- **bill_rate**: Hourly or daily billing rate

### Sample Records:
- John Smith - Python Developer - $85
- Sarah Johnson - Java Developer - $90
- Michael Brown - Full Stack Developer - $95
- Emily Davis - Senior Python Developer - $120
- David Wilson - Frontend Developer - $75
- Jessica Martinez - Data Analyst - $80
- Robert Taylor - DevOps Engineer - $110
- Lisa Anderson - Python Developer - $88
- James Thomas - Full Stack Developer - $92
- Jennifer White - Senior Java Developer - $125

## 🎨 Design Features

- **Gradient Background**: Purple gradient (667eea to 764ba2)
- **Smooth Animations**: Slide and fade-in effects
- **Interactive Elements**: Hover effects on buttons and table rows
- **Responsive Tables**: Auto-adjusts for smaller screens
- **Professional Typography**: Clean, modern font styling

## 🔧 Technical Stack

- **Backend**: Python with Flask framework
- **Frontend**: HTML5 with embedded CSS3
- **Data Format**: CSV (Comma-Separated Values)
- **API**: RESTful JSON API endpoint (`/api/search`)

## 📝 API Endpoint

### POST /api/search
**Request:**
```json
{
  "job_description": "Python Developer"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": [
    {
      "name": "John Smith",
      "emailid": "john.smith@example.com",
      "job_description": "Python Developer",
      "phone_number": "+1-555-0101",
      "bill_rate": "85"
    }
  ]
}
```

**Response (No matches):**
```json
{
  "success": false,
  "message": "No matching records found"
}
```

## 🔍 Search Algorithm

- **Case-Insensitive**: Searches are not case-sensitive
- **Partial Match**: Matches partial text in job descriptions
- **Examples**:
  - Search "Python" returns all Python-related positions
  - Search "Senior" returns all senior-level positions
  - Search "Developer" returns all developer positions

## 💻 Terminal Commands

### Start the Application
```bash
python app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🌐 Browser Compatibility

- Chrome (Latest)
- Firefox (Latest)
- Safari (Latest)
- Edge (Latest)

## 📱 Responsive Breakpoints

- Desktop: Full layout with all features
- Tablet: Adjusted padding and font sizes
- Mobile: Stacked layout, full-width search box

## 🎯 Features to Add (Future)

- User authentication
- Edit/Add/Delete functionality
- Export results to Excel/PDF
- Advanced filtering options
- Database integration (SQL)
- Dark mode toggle

## 📞 Support

For issues or suggestions, please check the Flask documentation at https://flask.palletsprojects.com/

---

**© 2029 Sample Company | #ExampleCompany**
