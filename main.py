import streamlit as st


# Function to parse the score input
def parse_score(assessment_score: str) -> object:
    """

    :param assessment_score:
    :return:
    """
    try:
        if assessment_score.lower() == "not yet done":
            return None
        else:
            x, y = map(int, assessment_score.split("/"))
            return x / y
    except:
        return None


# Function to calculate the final grade
def calculate_final_grade(grade_categories: dict) -> float:
    total_weight = 0
    weighted_sum = 0

    for category, data in grade_categories.items():
        total_category_score = 0
        num_scored_assessments = 0

        for score in data["scores"]:
            parsed_score = parse_score(score)
            if parsed_score is not None:
                total_category_score += parsed_score
                num_scored_assessments += 1

        if num_scored_assessments > 0:
            average_score = total_category_score / num_scored_assessments
            weighted_sum += average_score * data["weight"]
            total_weight += data["weight"]

    if total_weight == 0:
        return 0
    return (weighted_sum / total_weight) * 100


st.title("Student Grade Playground")

# Input for grade categories
st.header("Enter Grade Categories")
categories = {}
category_names = st.text_area("Enter category names, one per line").split("\n")

for category in category_names:
    if category.strip():
        st.subheader(category)
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input(
                f"Weight for {category}",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                key=f"weight_{category}",
            )
        with col2:
            num_assessments = st.number_input(
                f"Number of assessments for {category}",
                min_value=1,
                value=1,
                key=f"num_assessments_{category}",
            )
        categories[category] = {
            "weight": weight,
            "num_assessments": num_assessments,
            "scores": ["Not yet done"] * num_assessments,
        }

st.header("Enter Scores for Assessments")
try:
    tabs = st.tabs(list(categories.keys()))

    for tab, (category, data) in zip(tabs, categories.items()):
        with tab:
            st.subheader(f"Scores for {category}")
            for i in range(data["num_assessments"]):
                score = st.text_input(
                    f"Score for {category} Assessment {i+1} (format x/y)",
                    value="Not yet done",
                    key=f"score_{category}_{i}",
                )
                data["scores"][i] = score
except:
    pass

st.divider()

# Calculate and display the final grade
if st.button("Calculate Grade"):
    final_grade = calculate_final_grade(categories)
    st.success(f"Score: {final_grade:.2f}%")
