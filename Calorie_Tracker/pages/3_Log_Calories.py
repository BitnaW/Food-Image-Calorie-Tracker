import streamlit as st
from datetime import datetime
from backend import ImageProcessor
from database import get_database
from domain import CalorieEntry
from utils import SessionManager
from dotenv import load_dotenv

load_dotenv()

def main():
    SessionManager.require_authentication()(lambda: None)()
    
    st.title("Log Calories from Image")
    
    user = SessionManager.get_user()
    
    if user:
        st.write(f"Logged in as: **{user.username}**")
        
        st.divider()
        
        st.subheader("Upload Food Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image of food (JPG, PNG)",
            type=["jpg", "jpeg", "png"]
        )
        
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                st.write("### Processing Options")
                method = st.radio(
                    "Recognition method:",
                    ["Automatic", "Label Recognition", "Visual Estimation"]
                )
                
                if st.button("Process Image", key="process_btn"):
                    with st.spinner("Processing image..."):
                        
                        processor = ImageProcessor()
                        image_bytes = uploaded_file.read()
                        
                        if processor.validate_image(image_bytes):
                            if method == "Label Recognition":
                                result = processor.label_recognizer.recognize(image_bytes)
                            elif method == "Visual Estimation":
                                result = processor.visual_estimator.recognize(image_bytes)
                            else:
                                result = processor.process_image(image_bytes)
                            
                            if result.success:
                                #st.success("Image processed successfully!")
                                # st.json({
                                #     "method": result.method,
                                #     "info": result,
                                #     "confidence": result.confidence_score
                                # })

                                db = get_database()
                                for entry in result.convert_calorie_entires(user_id=user.id):
                                    db.execute("""INSERT INTO calories (user_id, calories, food_name, 
                                        food_type, quantity, unit, source, notes, logged_at)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                        tuple(entry.values()))
                                
                                st.success("Entry saved!")
                                db.connection.commit()
                            else:
                                st.warning(f"Processing not yet implemented: {result.error_message}")
                        else:
                            st.error("Invalid image file")
        
        st.divider()
        
        st.subheader("Or Log Calories Manually")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            food_name = st.text_input("Food Name")
        
        with col2:
            calories = st.number_input("Calories", min_value=0.0, step=0.1)
        
        with col3:
            food_type = st.selectbox(
                "Food Type",
                ["Vegetable", "Protein", "Grain", "Fruit", "Dairy", "Fat", "Other"]
            )
        
        quantity = st.number_input("Quantity", min_value=0.0, step=0.1)
        unit = st.selectbox("Unit", ["grams", "oz", "cups", "serving", "piece"])
        notes = st.text_area("Notes", height=80)
        
        if st.button("Save Entry", key="save_entry_btn"):
            if not food_name or calories == 0:
                st.error("Please enter food name and calories")
            else:
                entry = CalorieEntry(
                    user_id=user.id,
                    calories=calories,
                    food_name=food_name,
                    food_type=food_type.lower(),
                    quantity=quantity,
                    unit=unit,
                    source="estimate",
                    notes=notes
                )
        
                try:
                    db = get_database()
                    db.execute(
                        """
                        INSERT INTO calories
                        (user_id, calories, food_name, food_type,
                         quantity, unit, source, notes, logged_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            entry.user_id,
                            entry.calories,
                            entry.food_name,
                            entry.food_type,
                            entry.quantity,
                            entry.unit,
                            entry.source,
                            entry.notes,
                            entry.created_at
                        )
                    )
                    db.connection.commit()
                    st.success("Entry saved!")
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save entry: {e}")
        
        st.divider()
        
        st.subheader("Recent Entries")
        
        db = get_database()
        
        rows = db.fetch_all(
            """
            SELECT food_name, calories, quantity, unit, food_type,
                   source, notes, logged_at
            FROM calories
            WHERE user_id = ?
            ORDER BY logged_at DESC
            LIMIT 10
            """,
            (user.id,)
        )
        
        if rows:
            for row in rows:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**{row['food_name']}**")
                        st.write(
                            f"{row['quantity']} {row['unit']} • "
                            f"{row['food_type'].title()} • "
                            f"Source: {row['source']}"
                        )
                        if row["notes"]:
                            st.caption(row["notes"])
                    
                    with col2:
                        st.metric("Calories", f"{row['calories']:.0f}")
                    
                    #st.caption(f"Logged at: {row['logged_at']}")
                    st.divider()
        else:
            st.info("No entries yet.")
    
    else:
        st.warning("Please log in first")
        st.switch_page("pages/1_Login.py")


if __name__ == "__main__":
    main()