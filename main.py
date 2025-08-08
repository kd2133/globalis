# Projektstruktur (kommentierte Architektur):



#Globalis/


#├── data/                

#├── data_input/                    
#│   ├── reddit_data.py
#│   └── news_data.py

#├── docs/

#├── fine_tune/

#├── models/                         
#│   ├── sentiment_analyzer.py      
#│   ├── opinion_analyzer.py         
#│   └── topic_analyzer.py                    

#├── models_calibration/ 

#├── templates/ 

#├── tests/ 

#├── utils/        
#│   ├── data_loader.py   
#│   ├── explain_results.py
#│   ├── globalis_pipeline.py
#│   └── helpers.py              

#├── venv/ 
#├── .env
#├── .gitignore  
#├── mvp.html 
#├── gsi_db_setup.py
#├── init_historical.py
#├── main.py
#├── README.md
#├── requirements.txt
#└── sentmock.py







# main.py: Main entry point for GSI calculation and demo run

import sys
from utils.globalis_pipeline import GlobalisPipeline
from utils.data_loader import load_data
from utils.explain_results import explain_topic_result, plot_topic_scores
from models.sentiment_analyzer import analyze_sentiment  # For compatibility check
from models.topic_analyzer import analyze_topic
from models.opinion_analyzer import analyze_opinion
from utils.helpers import load_historical_stats, save_historical_stats

def main():
    # 1. Choose data source (default: csv, override with arg)
    source = 'csv'
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ('db', 'json', 'csv'):
            source = arg
        else:
            print(f"⚠️ Invalid source '{arg}', using default 'csv'.")

    print(f"📂 Loading data from source: {source}")
    data = load_data(source=source)

    if not data:
        print("⚠️ No data loaded, exiting.")
        return

    # 2. Initialize Pipeline
    pipeline = GlobalisPipeline()
    df, gsi_weighted, total_analyzed_posts = pipeline.run(data)  # Assuming data is list of posts

    # 3. Calculate and save historical stats
    stats = load_historical_stats()
    save_historical_stats(stats)

    # 4. Output Results
    print("\n🌍 Global Sentiment Index (weighted):", gsi_weighted)
    print("===========================================")
    print(df)

    # 5. Explain and Plot (example for one topic result)
    if not df.empty:
        topic_result = df.iloc[0].to_dict()  # Take first row as example
        explain_topic_result(topic_result, gsi_weighted)
        plot_topic_scores([topic_result])  # Plot for visualization

if __name__ == "__main__":
    main()