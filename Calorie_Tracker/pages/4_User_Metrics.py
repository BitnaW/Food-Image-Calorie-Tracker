"""Metrics page."""
import streamlit as st
from database import get_database, DatabaseSchema
from domain import User
from utils import SessionManager, PasswordManager, AuthValidator
import pandas as pd 
from datetime import datetime, timedelta

user = SessionManager.get_user()
db = get_database()
    
if user:
    st.subheader(f"Entries for User: {user.username}")
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
    
    weekly_total = db.fetch_one(
        """
        SELECT SUM(calories) as total_calories
        FROM calories
        WHERE user_id = ? AND logged_at >= ?
        """,
        (user.id, seven_days_ago)
    )
    
    daily_calories = db.fetch_all(
        """
        SELECT DATE(logged_at) as day, SUM(calories) as daily_total
        FROM calories
        WHERE user_id = ? AND logged_at >= ?
        GROUP BY DATE(logged_at)
        ORDER BY day ASC
        """,
        (user.id, seven_days_ago)
    )
    

    total_calories = weekly_total['total_calories'] if weekly_total and weekly_total['total_calories'] else 0
    

    chart_data = [row['daily_total'] for row in daily_calories] if daily_calories else []
    
    # delta calculation
    fourteen_days_ago = (datetime.now() - timedelta(days=14)).isoformat()
    previous_week_total = db.fetch_one(
        """
        SELECT SUM(calories) as total_calories
        FROM calories
        WHERE user_id = ? AND logged_at >= ? AND logged_at < ?
        """,
        (user.id, fourteen_days_ago, seven_days_ago)
    )
    
    previous_total = previous_week_total['total_calories'] if previous_week_total and previous_week_total['total_calories'] else 0
    delta = total_calories - previous_total

    row = st.container(horizontal=True)
    with row:
        st.metric(
            "Weekly Calories", 
            int(total_calories), 
            int(delta), 
            chart_data=chart_data, 
            chart_type="line", 
            border=True
        )
       
   
    # db query for total calories
    query = "SELECT * FROM calories WHERE user_id = ? ORDER BY logged_at DESC LIMIT 50"
    df = pd.read_sql_query(query, db.connection, params=(user.id,))
    
    if not df.empty:
        
        st.subheader("Log")

        rename_mapping = {
            'food_name': 'Food',
            'calories': 'Calories',
            'quantity': 'Qty',
            'unit': 'Unit',
            'food_type': 'Type',
            'source': 'Source',
            'notes': 'Notes',
            'logged_at': 'Logged'
        }
        
        desired_columns = ["Food", "Calories", "Qty", "Unit", "Type", "Source", "Logged"]
        
        df = df.rename(columns=rename_mapping)
        
        # dataframe formatting 
        df_display = df[desired_columns].copy()
        df_display['Calories'] = df_display['Calories'].apply(lambda x: f"{int(x)} cal" if pd.notna(x) else "-")
        df_display['Logged'] = pd.to_datetime(df_display['Logged']).dt.strftime('%b %d, %I:%M %p')
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Food": st.column_config.TextColumn(width="medium"),
                "Calories": st.column_config.TextColumn(width="small"),
                "Qty": st.column_config.TextColumn(width="small"),
                "Unit": st.column_config.TextColumn(width="small"),
                "Type": st.column_config.TextColumn(width="small"),
                "Source": st.column_config.TextColumn(width="small"),
                "Logged": st.column_config.TextColumn(width="medium"),
            }
        )
    else:
        st.info("No calorie entries yet.")
    
else:
    st.warning("Please log in first")
    st.switch_page("pages/1_Login.py")