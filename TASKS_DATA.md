# Data Analytic Engineer Test Scenarios
## Book Tracker App - 2-3 Hour Assessment

### 🎯 Overview
This document outlines focused test scenarios Data Analytic Engineer candidates. Designed to be completed in **2-3 hours** while demonstrating core skills from the job description.

---

## 📋 Single Test Scenario: Book Analytics Dashboard

### **Objective**: 
Create a data analytics solution for the Book Tracker App that demonstrates ETL, data modeling, and visualization skills.

---

## 🎯 Task Breakdown (2-3 hours)

### **Part 1: Data Preparation & ETL (45 minutes)**
**Goal**: Clean and prepare sample data for analysis

#### **Given Data**:
- Use the existing `books.json` from the backend
- Create additional sample data for user interactions and reading progress

#### **Requirements**:
1. **Data Cleaning** (Python/pandas):
   - Clean book metadata (handle missing values, standardize formats)
   - Create sample user interaction data (book views, searches, ratings)
   - Generate reading progress data (pages read, completion status)

2. **Data Transformation**:
   - Calculate derived metrics (completion rates, reading speed)
   - Create user segments based on reading behavior
   - Aggregate data for dashboard consumption

#### **Deliverable**:
- Clean CSV files ready for analysis
- Python script showing data cleaning process

---

### **Part 2: Data Modeling (30 minutes)**
**Goal**: Design a simple data model for analytics

#### **Requirements**:
1. **Create 3-4 tables**:
   - `books` (id, title, author, genre, pages, rating)
   - `user_interactions` (user_id, book_id, action, timestamp)
   - `reading_progress` (user_id, book_id, pages_read, completion_rate)
   - `user_segments` (user_id, segment, total_books_read)

2. **SQL Skills**:
   - Write 3-4 analytical queries
   - Use basic aggregations and joins
   - Create views for common metrics

#### **Sample Queries**:
```sql
-- Most popular genres
SELECT genre, COUNT(*) as book_count, AVG(rating) as avg_rating
FROM books 
GROUP BY genre 
ORDER BY book_count DESC;

-- User reading statistics
SELECT 
    user_id,
    COUNT(DISTINCT book_id) as books_read,
    AVG(completion_rate) as avg_completion
FROM reading_progress 
GROUP BY user_id;
```

#### **Deliverable**:
- SQL DDL scripts
- 3-4 analytical queries
- Brief explanation of data model

---

### **Part 3: Dashboard Creation (60 minutes)**
**Goal**: Build a simple dashboard with key insights

#### **Requirements**:
1. **Choose ONE tool**:
   - **Option A**: Python (matplotlib/plotly/seaborn) + Jupyter notebook
   - **Option B**: Google Looker Studio (free)
   - **Option C**: Power BI (if available)

2. **Create 4-5 visualizations**:
   - Book distribution by genre (bar chart)
   - Reading completion rates (histogram)
   - Top-rated books (table/list)
   - User activity over time (line chart)
   - Reading progress by user segment (pie chart)

3. **Business Insights**:
   - Identify top-performing genres
   - Highlight user engagement patterns
   - Suggest 2-3 actionable recommendations

#### **Deliverable**:
- Working dashboard (screenshot or live link)
- Brief explanation of insights
- 2-3 business recommendations

---

### **Part 4: Documentation (15 minutes)**
**Goal**: Document your work and findings

#### **Requirements**:
- README with setup instructions
- Brief explanation of methodology
- Key findings and recommendations
- Any assumptions or limitations

---

## 🛠️ Technical Requirements

### **Must Have**:
- **SQL**: Basic queries, joins, aggregations
- **Python**: pandas for data manipulation
- **Data Visualization**: Any tool of choice
- **Documentation**: Clear and concise

### **Nice to Have**:
- Data quality checks
- Error handling
- Code optimization
- Advanced visualizations

---

## 📊 Sample Data Structure

### **Books Table** (from existing books.json):
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "genre": "Classic",
  "pages": 180,
  "rating": 4.2
}
```

### **User Interactions** (create sample data):
```json
{
  "user_id": 1,
  "book_id": 1,
  "action": "view",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Reading Progress** (create sample data):
```json
{
  "user_id": 1,
  "book_id": 1,
  "pages_read": 120,
  "total_pages": 180,
  "completion_rate": 0.67
}
```

---

## 🎯 Evaluation Criteria

### **Technical Skills (50%)**:
- Data cleaning and preparation quality
- SQL query accuracy and efficiency
- Visualization clarity and relevance
- Code organization and documentation

### **Business Understanding (30%)**:
- Insight generation quality
- Business recommendation relevance
- Data interpretation accuracy
- Dashboard usability

### **Problem Solving (20%)**:
- Approach to data challenges
- Handling of edge cases
- Documentation clarity
- Time management

---

## 📝 Submission Requirements

1. **Code Repository**: 
   - Python scripts for data processing
   - SQL queries and data model
   - Jupyter notebook (if using Python)

2. **Dashboard**: 
   - Screenshots or live link
   - Brief explanation of insights

3. **Documentation**: 
   - README with setup instructions
   - Key findings and recommendations

---

## 🚀 How to Deliver Your Work

### **Option 1: Fork & Pull Request (Recommended)**
1. **Fork this repository** to your GitHub account
2. **Create a new branch** named `data-analytics-[your-name]`
   ```bash
   git checkout -b data-analytics-john-doe
   ```
3. **Work on your solution** in the new branch
4. **Commit your changes** with clear commit messages:
   ```bash
   git add .
   git commit -m "Add data preparation scripts and ETL pipeline"
   git commit -m "Create data model and SQL queries"
   git commit -m "Build dashboard with visualizations"
   git commit -m "Add documentation and README"
   ```
5. **Push your branch** to your fork:
   ```bash
   git push origin data-analytics-john-doe
   ```
6. **Create a Pull Request** to the main repository with:
   - Clear title: `Data Analytics Solution - [Your Name]`
   - Description of your approach and key findings
   - Link to dashboard (if hosted online)

### **Option 2: New Repository**
1. **Create a new repository** on GitHub
2. **Clone and set up** your repository:
   ```bash
   git clone https://github.com/yourusername/book-tracker-analytics.git
   cd book-tracker-analytics
   ```
3. **Copy the original books.json** from this repository
4. **Work on your solution** and commit regularly
5. **Share the repository link** with us

### **Option 3: Zip File (If Git is not available)**
1. **Download this repository** as ZIP
2. **Work on your solution** locally
3. **Create a new folder** with your name: `data-analytics-[your-name]`
4. **Include all deliverables** in the folder
5. **Zip the folder** and share via email

---

## 📁 Recommended Project Structure

```
data-analytics-[your-name]/
├── README.md                           # Setup instructions and findings
├── data/
│   ├── raw/
│   │   └── books.json                  # Original data
│   ├── processed/
│   │   ├── books_clean.csv
│   │   ├── user_interactions.csv
│   │   └── reading_progress.csv
│   └── sample_data_generator.py        # Script to create sample data
├── sql/
│   ├── data_model.sql                  # DDL scripts
│   └── analytical_queries.sql          # Your SQL queries
├── notebooks/
│   └── data_analysis.ipynb             # Jupyter notebook (if using Python)
├── dashboard/
│   ├── dashboard.html                  # Static dashboard
│   └── dashboard_screenshots/          # Screenshots if needed
└── scripts/
    ├── data_preparation.py             # ETL scripts
    └── requirements.txt                # Python dependencies
```

---

## ✅ Checklist Before Submission

- [ ] All code is properly commented and documented
- [ ] README includes setup instructions and key findings
- [ ] Data model is clearly explained
- [ ] Dashboard is functional with clear insights
- [ ] Business recommendations are provided
- [ ] Git commits have meaningful messages
- [ ] No sensitive data is included in the repository
- [ ] All deliverables are included and organized

---

## ⏱️ Time Allocation (2-3 hours)

- **Data Preparation & ETL**: 45 minutes
- **Data Modeling**: 30 minutes  
- **Dashboard Creation**: 60 minutes
- **Documentation**: 15 minutes
- **Buffer time**: 30 minutes

---

## 🚀 Bonus Points (Optional)

- Data quality validation
- Advanced SQL techniques (CTEs, window functions)
- Interactive dashboard features
- Automated data refresh
- Performance optimization

---

*This test is designed to assess core Data Analytic Engineer skills within a realistic timeframe while providing meaningful insights about the candidate's capabilities.*
