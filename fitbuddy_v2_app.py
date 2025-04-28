# fitbuddy_v2.5_app.py

import streamlit as st
import datetime

# ----- Local Food Database -----
if "food_db" not in st.session_state:
    st.session_state.food_db = {
        "rajma chawal": {"calories": 350, "protein": 15},
        "apple": {"calories": 95, "protein": 0.5},
        "banana": {"calories": 105, "protein": 1.3},
        "paneer": {"calories": 265, "protein": 18},
        "egg": {"calories": 78, "protein": 6},
        "chicken breast": {"calories": 165, "protein": 31}
    }

# ----- Initialize session states -----
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "food_log" not in st.session_state:
    st.session_state.food_log = []

if "current_weight" not in st.session_state:
    st.session_state.current_weight = None

if "target_weight" not in st.session_state:
    st.session_state.target_weight = None

if "goal_days" not in st.session_state:
    st.session_state.goal_days = None

# ----- Title -----
st.title("🏋️ FitBuddy v2.5 - Smarter Fitness Assistant")

# ----- Tabs -----
tab1, tab2, tab3, tab4 = st.tabs(["📝 Time Table", "🍽️ Food Tracker", "⚖️ Weight Tracker", "🧠 Smart Advice"])

# ----- Tab 1: Time Table -----
with tab1:
    st.header("📅 Set Your Tasks")
    tasks_input = st.text_area("Enter tasks (separate by commas or new lines)")
    task_time = st.time_input("Set Time", value=datetime.time(9, 0))

    if st.button("Add Tasks"):
        tasks_list = [task.strip() for task in tasks_input.replace(',', '\n').split('\n') if task.strip()]
        for task in tasks_list:
            st.session_state.tasks.append((task, task_time))
        st.success(f"✅ {len(tasks_list)} Tasks Added Successfully!")

    st.subheader("Today's Tasks:")
    for idx, (t, t_time) in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4,1])
        with col1:
            st.write(f"🕘 {t_time.strftime('%I:%M %p')} - {t}")
        with col2:
            if st.button("❌", key=f"del_task_{idx}"):
                st.session_state.tasks.pop(idx)
                st.experimental_rerun()

# ----- Tab 2: Food Tracker -----
with tab2:
    st.header("🍛 Track Your Food")
    food_item = st.text_input("What did you eat?").lower().strip()
    
    if st.button("Add Food"):
        if food_item in st.session_state.food_db:
            st.session_state.food_log.append((food_item, st.session_state.food_db[food_item]))
            st.success(f"✅ {food_item.title()} added!")
        else:
            st.warning(f"⚠️ {food_item} not found! Please add manually.")
            calories = st.number_input("Enter calories for this food", min_value=0)
            protein = st.number_input("Enter protein content (grams)", min_value=0.0)
            if st.button("Save Food"):
                st.session_state.food_db[food_item] = {"calories": calories, "protein": protein}
                st.session_state.food_log.append((food_item, {"calories": calories, "protein": protein}))
                st.success(f"✅ {food_item.title()} added to database!")

    st.subheader("Today's Food Log:")
    total_calories = sum(item[1]["calories"] for item in st.session_state.food_log)
    total_protein = sum(item[1]["protein"] for item in st.session_state.food_log)

    for food, nutrition in st.session_state.food_log:
        st.write(f"🍴 {food.title()} - {nutrition['calories']} kcal, {nutrition['protein']}g protein")

    st.markdown(f"**🍽️ Total Calories:** {total_calories} kcal")
    st.markdown(f"**🍗 Total Protein:** {total_protein} g")

# ----- Tab 3: Weight Tracker -----
with tab3:
    st.header("⚖️ Weight Tracking")
    st.session_state.current_weight = st.number_input("Current Weight (kg)", min_value=1.0, value=st.session_state.current_weight or 60.0)
    st.session_state.target_weight = st.number_input("Target Weight (kg)", min_value=1.0, value=st.session_state.target_weight or 55.0)
    st.session_state.goal_days = st.number_input("Goal Duration (days)", min_value=1, value=st.session_state.goal_days or 60)
    
    st.write(f"🎯 You want to go from {st.session_state.current_weight}kg to {st.session_state.target_weight}kg in {st.session_state.goal_days} days.")

# ----- Tab 4: Smart Advice -----
with tab4:
    st.header("🧠 Smart Advice Based on Your Day")

    if total_calories < 1500:
        st.info("📢 You consumed fewer calories today. Consider eating a healthy snack like fruits or nuts.")
    elif total_calories > 2500:
        st.warning("⚠️ High calorie intake today! Tomorrow, try to eat lighter.")

    # Exercise Suggestion
    weight_diff = st.session_state.current_weight - st.session_state.target_weight
    total_calories_to_burn = weight_diff * 7700  # 1kg fat = 7700 calories
    daily_burn_needed = total_calories_to_burn / st.session_state.goal_days if st.session_state.goal_days else 0

    if weight_diff > 0:
        st.subheader("🏃 Exercise Plan")
        st.write(f"➡️ You should aim to burn approximately **{int(daily_burn_needed)} calories per day**.")
        st.write("- 🚶‍♂️ Brisk Walk: 1 hour (~300 calories)")
        st.write("- 🏃‍♂️ Jogging: 30 minutes (~300 calories)")
        st.write("- 🚴‍♂️ Cycling: 45 minutes (~400 calories)")
    else:
        st.success("🎉 You are already at or below your target weight! Keep maintaining it.")

# ----- Footer -----
st.markdown("---")
st.caption("Made with ❤️ by Prince's FitBuddy AI v2.5")

