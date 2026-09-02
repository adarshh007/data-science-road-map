"""
Database seeding script for DS Journey
Populates the database with the 150-day Data Science syllabus
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Module, Day, Topic
from app.core.config import settings
from datetime import datetime

# Syllabus data - 11 Modules, 150 Days, 75 Topics
SYLLABUS_DATA = [
    # Module 1: Foundations for Data Science (Days 1-22)
    {
        "module": {"number": 1, "title": "M1: Foundations for Data Science", "description": "Basic concepts and foundations", "order": 1},
        "topics": [
            {"day_start": 1, "day_end": 2, "title": "Data acquisition, cleaning, and aggregation"},
            {"day_start": 3, "day_end": 4, "title": "Exploratory data analysis and visualization"},
            {"day_start": 5, "day_end": 6, "title": "Basic statistical and mathematical foundations for data science"},
            {"day_start": 7, "day_end": 8, "title": "Core Statistics Concepts & Measures of Central Tendency"},
            {"day_start": 9, "day_end": 10, "title": "Dispersion, partial ordering of dispersion & Simple Correlation"},
            {"day_start": 11, "day_end": 12, "title": "Descriptive statistics, distributions, hypothesis testing, and regression (overview)"},
            {"day_start": 13, "day_end": 14, "title": "Classification, Tabulation, Presentation of Data & types of frequency distribution tables"},
            {"day_start": 15, "day_end": 16, "title": "Introduction to probability & Conditional Probability in data science"},
            {"day_start": 17, "day_end": 18, "title": "Random Variables & Probability Distributions"},
            {"day_start": 19, "day_end": 20, "title": "File handling (reading/writing files, CSVs) & NumPy for numerical computing"},
            {"day_start": 21, "day_end": 22, "title": "Chi-Square Test, F-Distribution and Analysis of Variance (ANOVA)"},
        ]
    },
    # Module 2: Python Programming (Days 23-42)
    {
        "module": {"number": 2, "title": "M2: Python Programming", "description": "Python fundamentals and libraries", "order": 2},
        "topics": [
            {"day_start": 23, "day_end": 24, "title": "Bayesian Thinking: priors, posteriors, and maximum likelihood"},
            {"day_start": 25, "day_end": 26, "title": "Introduction to Python: installation, IDEs, Jupyter Notebook"},
            {"day_start": 27, "day_end": 28, "title": "Variables, data types, operators & strings/string methods"},
            {"day_start": 29, "day_end": 30, "title": "Conditional statements: if, elif, else"},
            {"day_start": 31, "day_end": 32, "title": "Loops: for, while, break, continue"},
            {"day_start": 33, "day_end": 34, "title": "Data structures: Lists, Tuples, Dictionaries and Sets"},
            {"day_start": 35, "day_end": 36, "title": "Functions: definition, arguments, return values, scope"},
            {"day_start": 37, "day_end": 38, "title": "Advanced functions: *args, **kwargs, lambda, recursion"},
            {"day_start": 39, "day_end": 40, "title": "Exception handling: try, except, else, finally, custom exceptions"},
            {"day_start": 41, "day_end": 42, "title": "Pandas (Series, DataFrames, querying, cleaning) & visualization with Matplotlib/Seaborn"},
        ]
    },
    # Module 3: Data Preparation & Statistical Testing (Days 43-60)
    {
        "module": {"number": 3, "title": "M3: Data Preparation & Statistical Testing", "description": "Advanced data preparation and testing", "order": 3},
        "topics": [
            {"day_start": 43, "day_end": 44, "title": "Introduction to Data Preparation & Data Preprocessing"},
            {"day_start": 45, "day_end": 46, "title": "Clustering: introduction, types & Classification vs Clustering"},
            {"day_start": 47, "day_end": 48, "title": "Text Mining & Analysis"},
            {"day_start": 49, "day_end": 50, "title": "The five fundamental steps involved in text mining"},
            {"day_start": 51, "day_end": 52, "title": "Distributions, sampling, and t-tests"},
            {"day_start": 53, "day_end": 54, "title": "Regression: why we use it, types of regression & selecting the right model"},
            {"day_start": 55, "day_end": 56, "title": "Testing of Hypothesis in case of Large Samples"},
            {"day_start": 57, "day_end": 58, "title": "Testing of Hypothesis in case of Small Samples"},
        ]
    },
    # Module 4: Machine Learning (Days 59-78)
    {
        "module": {"number": 4, "title": "M4: Machine Learning", "description": "Core machine learning algorithms and techniques", "order": 4},
        "topics": [
            {"day_start": 59, "day_end": 60, "title": "Introduction to ML using Data Analytics; relation to statistics and data analysis"},
            {"day_start": 61, "day_end": 62, "title": "Topic modeling: uncovering hidden themes in large document collections"},
            {"day_start": 63, "day_end": 64, "title": "How ML algorithms find patterns in data and are used to make decisions & predictions"},
            {"day_start": 65, "day_end": 66, "title": "Data preparation, handling missing data & custom solutions for different industries"},
            {"day_start": 67, "day_end": 68, "title": "Basic algorithmic techniques: sorting, searching, greedy algorithms, dynamic programming"},
            {"day_start": 69, "day_end": 70, "title": "Classification: foundations for ML, ML techniques overview & validation techniques"},
            {"day_start": 71, "day_end": 72, "title": "Clustering: distance measures, K-Medoids, K-Mode and density-based clustering"},
            {"day_start": 73, "day_end": 74, "title": "Classification algorithms: Naive Bayes, K-Nearest Neighbors & Support Vector Machines"},
            {"day_start": 75, "day_end": 76, "title": "Decision Trees (ID3, C4.5, CART) & Ensemble methods (Bagging & Boosting)"},
            {"day_start": 77, "day_end": 78, "title": "Association Rule Mining: Market Basket, Recommendation Engines, Apriori algorithm & FP-Trees"},
        ]
    },
    # Module 5: R Programming (Days 79-94)
    {
        "module": {"number": 5, "title": "M5: R Programming", "description": "R language and statistical computing", "order": 5},
        "topics": [
            {"day_start": 79, "day_end": 80, "title": "Introduction to R & RStudio, installing packages"},
            {"day_start": 81, "day_end": 82, "title": "R basics: variables, data types, vectors, operators"},
            {"day_start": 83, "day_end": 84, "title": "Data structures in R: matrices, lists, data frames"},
            {"day_start": 85, "day_end": 86, "title": "Control structures & functions in R"},
            {"day_start": 87, "day_end": 88, "title": "Data manipulation (dplyr, tidyr) & visualization (ggplot2)"},
            {"day_start": 89, "day_end": 90, "title": "Statistical analysis in R: descriptive stats, hypothesis testing"},
            {"day_start": 91, "day_end": 92, "title": "Machine Learning in R: regression, classification, clustering & decision trees"},
            {"day_start": 93, "day_end": 94, "title": "Advanced R: functional programming, packages, and optimization"},
        ]
    },
    # Module 6: AI & Deep Learning (Days 95-108)
    {
        "module": {"number": 6, "title": "M6: AI & Deep Learning", "description": "Neural networks and deep learning fundamentals", "order": 6},
        "topics": [
            {"day_start": 95, "day_end": 96, "title": "Foundations for AI, application areas & AI basics (Divide & Conquer, Greedy, Branch & Bound, Gradient Descent)"},
            {"day_start": 97, "day_end": 98, "title": "Neural network basics: Perceptron and MLP, FFN, Backpropagation"},
            {"day_start": 99, "day_end": 100, "title": "Recurrent Neural Networks & building recurrent NNs"},
            {"day_start": 101, "day_end": 102, "title": "Convolutional Neural Networks, image & text classification, hyper-parameter tuning"},
            {"day_start": 103, "day_end": 104, "title": "Long Short-Term Memory (LSTM) & Time Series Forecasting"},
            {"day_start": 105, "day_end": 106, "title": "Deep Learning: Auto-encoders, unsupervised and semi-supervised learning"},
            {"day_start": 107, "day_end": 108, "title": "Regularization: Dropout and Batch Normalization"},
        ]
    },
    # Module 7: Generative AI (Days 109-116)
    {
        "module": {"number": 7, "title": "M7: Generative AI", "description": "Large language models and generative AI", "order": 7},
        "topics": [
            {"day_start": 109, "day_end": 110, "title": "Introduction to Generative AI: concepts, applications & GenAI vs traditional ML"},
            {"day_start": 111, "day_end": 112, "title": "Foundations of Large Language Models & Transformer architecture (attention, tokens, embeddings)"},
            {"day_start": 113, "day_end": 114, "title": "Prompt Engineering: techniques, few-shot prompting, structuring prompts for tasks"},
            {"day_start": 115, "day_end": 116, "title": "Practical GenAI: using AI assistants for coding/analysis, intro to RAG & fine-tuning, responsible AI use"},
        ]
    },
    # Module 8: Tableau (Days 117-124)
    {
        "module": {"number": 8, "title": "M8: Tableau", "description": "Data visualization with Tableau", "order": 8},
        "topics": [
            {"day_start": 117, "day_end": 118, "title": "Tableau overview: interface, connecting to data sources"},
            {"day_start": 119, "day_end": 120, "title": "Building basic visualizations: bar, line, pie charts, maps"},
            {"day_start": 121, "day_end": 122, "title": "Calculated fields, filters, parameters & interactive dashboards"},
            {"day_start": 123, "day_end": 124, "title": "Stories, publishing and sharing Tableau workbooks"},
        ]
    },
    # Module 9: SQL & Databases (Days 125-134)
    {
        "module": {"number": 9, "title": "M9: SQL & Databases", "description": "Database design and SQL querying", "order": 9},
        "topics": [
            {"day_start": 125, "day_end": 126, "title": "Introduction to databases, RDBMS concepts, installing MySQL/SQL Server"},
            {"day_start": 127, "day_end": 128, "title": "DDL & DML: CREATE, INSERT, UPDATE, DELETE, constraints"},
            {"day_start": 129, "day_end": 130, "title": "SELECT queries (WHERE, ORDER BY, DISTINCT, LIMIT), aggregate functions, GROUP BY/HAVING"},
            {"day_start": 131, "day_end": 132, "title": "Joins: INNER, LEFT, RIGHT, FULL, SELF joins"},
            {"day_start": 133, "day_end": 134, "title": "Subqueries, Common Table Expressions (CTEs) & Window functions (RANK, ROW_NUMBER, LAG/LEAD)"},
        ]
    },
    # Module 10: Excel (Days 135-146)
    {
        "module": {"number": 10, "title": "M10: Excel", "description": "Excel for data analysis and visualization", "order": 10},
        "topics": [
            {"day_start": 135, "day_end": 136, "title": "Excel basics: interface, data entry, formatting, cell referencing"},
            {"day_start": 137, "day_end": 138, "title": "Formulas & functions: logical, lookup (VLOOKUP/INDEX-MATCH), text, date functions"},
            {"day_start": 139, "day_end": 140, "title": "Data cleaning in Excel: sorting, filtering, conditional formatting, data validation"},
            {"day_start": 141, "day_end": 142, "title": "PivotTables, PivotCharts & Power Query (import/transform data)"},
            {"day_start": 143, "day_end": 144, "title": "Power Pivot & data modeling; What-if analysis (Goal Seek, Data Tables, Scenario Manager)"},
            {"day_start": 145, "day_end": 146, "title": "Interactive dashboards: slicers, timelines, KPI cards, design principles & mini-project"},
        ]
    },
    # Module 11: Capstone Project (Days 147-150)
    {
        "module": {"number": 11, "title": "M11: Capstone Project", "description": "Final capstone project", "order": 11},
        "topics": [
            {"day_start": 147, "day_end": 148, "title": "Project orientation, problem statement, dataset selection, data cleaning & EDA"},
            {"day_start": 149, "day_end": 150, "title": "Model building, validation, dashboard/report creation & final presentation"},
        ]
    },
]

def seed_database():
    """Seed the database with syllabus data"""
    
    # Create engine and tables
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_modules = db.query(Module).count()
        if existing_modules > 0:
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database with syllabus data...")
        
        topic_count = 0
        
        for module_data in SYLLABUS_DATA:
            # Create module
            module = Module(
                number=module_data["module"]["number"],
                title=module_data["module"]["title"],
                description=module_data["module"].get("description"),
                total_days=2,  # Each topic spans 2 days
                order=module_data["module"]["order"]
            )
            db.add(module)
            db.flush()  # Flush to get module.id
            
            print(f"Created {module.title}")
            
            # Create days and topics
            for topic_data in module_data["topics"]:
                # Create or get days
                day_start_num = topic_data["day_start"]
                day_end_num = topic_data["day_end"]
                
                # Create topics
                topic = Topic(
                    module_id=module.id,
                    day_start=day_start_num,
                    day_end=day_end_num,
                    title=topic_data["title"],
                    description="",
                    status="NOT_STARTED",
                    progress=0.0,
                    confidence=0,
                    importance=3,
                    estimated_hours=2.0,
                    actual_hours=0.0
                )
                db.add(topic)
                topic_count += 1
        
        # Commit all changes
        db.commit()
        
        print(f"✅ Database seeded successfully!")
        print(f"   Modules: {len(SYLLABUS_DATA)}")
        print(f"   Topics: {topic_count}")
        print(f"   Total days: 150")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
