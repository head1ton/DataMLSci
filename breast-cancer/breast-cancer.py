import streamlit as st
import pandas as pd
import shap
import base64
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import os

from sklearn.model_selection import train_test_split

base_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout='wide')

def set_background(image_file):
    """
    This function sets the background of a Streamlit app to an image specified by the given image file.

    Parameters:
        image_file (str): The path to the image file to be used as the background.

    Returns:
        None
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

back_path = os.path.join(base_dir, 'pexels-leeloothefirst-7805653.jpg')
set_background(back_path)

# st.title("Breast Cancer Prediction")

st.write("""
# Breast Cancer Prediction

This app predicts the **Breast Cancer**!
""")

st.write('---')

cancer = datasets.load_breast_cancer()
# print(cancer.feature_names)
feat_names = cancer.feature_names
X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
X_rename = X.rename(columns={
    "mean radius": "mean_radius",
    "mean texture": "mean_texture",
    "mean perimeter": "mean_perimeter",
    "mean area": "mean_area",
    "mean smoothness": "mean_smoothness",
    "mean compactness": "mean_compactness",
    "mean concavity": "mean_concavity",
    "mean concave points": "mean_concave_points",
    "mean symmetry": "mean_symmetry",
    "mean fractal dimension": "mean_fractal_dimension",
    "radius error": "radius_error",
    "texture error": "texture_error",
    "perimeter error": "perimeter_error",
    "area error": "area_error",
    "smoothness error": "smoothness_error",
    "compactness error": "compactness_error",
    "concavity error": "concavity_error",
    "concave points error": "concave_points_error",
    "symmetry error": "symmetry_error",
    "fractal dimension error": "fractal_dimension_error",
    "worst radius": "worst_radius",
    "worst texture": "worst_texture",
    "worst perimeter": "worst_perimeter",
    "worst area": "worst_area",
    "worst smoothness": "worst_smoothness",
    "worst compactness": "worst_compactness",
    "worst concavity": "worst_concavity",
    "worst concave points": "worst_concave_points",
    "worst symmetry": "worst_symmetry",
    "worst fractal dimension": "worst_fractal_dimension"
})
X = X_rename.copy()
# print(X)
y = pd.DataFrame(cancer.target, columns=["TARGET"])

x_train, x_test, y_train, y_test = train_test_split(cancer.data, cancer.target,
                                                    stratify=cancer.target, random_state=0)

st.sidebar.header("Specify Input Parameters")

def user_input_features():
    mean_radius = st.sidebar.slider('mean_radius', X.mean_radius.min(), X.mean_radius.max(), X.mean_radius.mean())
    mean_texture = st.sidebar.slider('mean_texture', X.mean_texture.min(), X.mean_texture.max(), X.mean_texture.mean())
    mean_perimeter = st.sidebar.slider('mean_perimeter', X.mean_perimeter.min(), X.mean_perimeter.max(), X.mean_perimeter.mean())
    mean_area = st.sidebar.slider('mean_area', X.mean_area.min(), X.mean_area.max(), X.mean_area.mean())
    mean_smoothness = st.sidebar.slider('mean_smoothness', X.mean_smoothness.min(), X.mean_smoothness.max(), X.mean_smoothness.mean())
    mean_compactness = st.sidebar.slider('mean_compactness', X.mean_compactness.min(), X.mean_compactness.max(), X.mean_compactness.mean())
    mean_concavity = st.sidebar.slider('mean_concavity', X.mean_concavity.min(), X.mean_concavity.max(), X.mean_concavity.mean())
    mean_concave_points = st.sidebar.slider('mean_concave_points', X.mean_concave_points.min(), X.mean_concave_points.max(), X.mean_concave_points.mean())
    mean_symmetry = st.sidebar.slider('mean_symmetry', X.mean_symmetry.min(), X.mean_symmetry.max(), X.mean_symmetry.mean())
    mean_fractal_dimension = st.sidebar.slider('mean_fractal_dimension', X.mean_fractal_dimension.min(), X.mean_fractal_dimension.max(), X.mean_fractal_dimension.mean())
    radius_error = st.sidebar.slider('radius_error', X.radius_error.min(), X.radius_error.max(), X.radius_error.mean())
    texture_error = st.sidebar.slider('texture_error', X.texture_error.min(), X.texture_error.max(), X.texture_error.mean())
    perimeter_error = st.sidebar.slider('perimeter_error', X.perimeter_error.min(), X.perimeter_error.max(), X.perimeter_error.mean())
    area_error = st.sidebar.slider('area_error', X.area_error.min(), X.area_error.max(), X.area_error.mean())
    smoothness_error = st.sidebar.slider('smoothness_error', X.smoothness_error.min(), X.smoothness_error.max(), X.smoothness_error.mean())
    compactness_error = st.sidebar.slider('compactness_error', X.compactness_error.min(), X.compactness_error.max(), X.compactness_error.mean())
    concavity_error = st.sidebar.slider('concavity_error', X.concavity_error.min(), X.concavity_error.max(), X.concavity_error.mean())
    concave_points_error = st.sidebar.slider('concave_points_error', X.concave_points_error.min(), X.concave_points_error.max(), X.concave_points_error.mean())
    symmetry_error = st.sidebar.slider('symmetry_error', X.symmetry_error.min(), X.symmetry_error.max(), X.symmetry_error.mean())
    fractal_dimension_error = st.sidebar.slider('fractal_dimension_error', X.fractal_dimension_error.min(), X.fractal_dimension_error.max(), X.fractal_dimension_error.mean())
    worst_radius = st.sidebar.slider('worst_radius', X.worst_radius.min(), X.worst_radius.max(), X.worst_radius.mean())
    worst_texture = st.sidebar.slider('worst_texture', X.worst_texture.min(), X.worst_texture.max(), X.worst_texture.mean())
    worst_perimeter = st.sidebar.slider('worst_perimeter', X.worst_perimeter.min(), X.worst_perimeter.max(), X.worst_perimeter.mean())
    worst_area = st.sidebar.slider('worst_area', X.worst_area.min(), X.worst_area.max(), X.worst_area.mean())
    worst_smoothness = st.sidebar.slider('worst_smoothness', X.worst_smoothness.min(), X.worst_smoothness.max(), X.worst_smoothness.mean())
    worst_compactness = st.sidebar.slider('worst_compactness', X.worst_compactness.min(), X.worst_compactness.max(), X.worst_compactness.mean())
    worst_concavity = st.sidebar.slider('worst_concavity', X.worst_concavity.min(), X.worst_concavity.max(), X.worst_concavity.mean())
    worst_concave_points = st.sidebar.slider('worst_concave_points', X.worst_concave_points.min(), X.worst_concave_points.max(), X.worst_concave_points.mean())
    worst_symmetry = st.sidebar.slider('worst_symmetry', X.worst_symmetry.min(), X.worst_symmetry.max(), X.worst_symmetry.mean())
    worst_fractal_dimension = st.sidebar.slider('worst_fractal_dimension', X.worst_fractal_dimension.min(), X.worst_fractal_dimension.max(), X.worst_fractal_dimension.mean())

    data = {'mean_radius': mean_radius,
            'mean_texture': mean_texture,
            'mean_perimeter': mean_perimeter,
            'mean_area': mean_area,
            'mean_smoothness': mean_smoothness,
            'mean_compactness': mean_compactness,
            'mean_concavity': mean_concavity,
            'mean_concave_points': mean_concave_points,
            'mean_symmetry': mean_symmetry,
            'mean_fractal_dimension': mean_fractal_dimension,
            'radius_error': radius_error,
            'texture_error': texture_error,
            'perimeter_error': perimeter_error,
            'area_error': area_error,
            'smoothness_error': smoothness_error,
            'compactness_error': compactness_error,
            'concavity_error': concavity_error,
            'concave_points_error': concave_points_error,
            'symmetry_error': symmetry_error,
            'fractal_dimension_error': fractal_dimension_error,
            'worst_radius': worst_radius,
            'worst_texture': worst_texture,
            'worst_perimeter': worst_perimeter,
            'worst_area': worst_area,
            'worst_smoothness': worst_smoothness,
            'worst_compactness': worst_compactness,
            'worst_concavity': worst_concavity,
            'worst_concave_points': worst_concave_points,
            'worst_symmetry': worst_symmetry,
            'worst_fractal_dimension': worst_fractal_dimension
    }
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

st.header('Specified Input parameters')
st.write(df)
st.write('---')

# 해당 로직은 그냥 기본만 돌려본 거뿐 정규화나 모델링은 다시 적용해야함.
model = RandomForestClassifier(n_estimators=100)
# model.fit(X, y)
model.fit(x_train, y_train)

prediction = model.predict(df)

st.header('Prediction of Target')
st.write(prediction)
# print(feat_names[prediction])
st.write('---')

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(x_train)
# print(shap_values)

st.header('Feature Importance')

# fig, axes = plt.subplots(nrows=2, ncols=1)

# plt.title('Feature importance based on SHAP values')
# axes[0] = shap.summary_plot(shap_values, X)
# # shap.plots.violin(shap_values, X, feat_names, plot_type='layered_violin')
# st.pyplot(plt)
# st.write('---')
#
# plt.title('Feature importance based on SHAP values (Bar)')
# axes[1] = shap.summary_plot(shap_values, X, plot_type="bar")
# # shap.summary_plot(shap_values, X, plot_type='layered_violin')
# # shap.plots.bar(shap_values)
# st.pyplot(plt)
# plt.show()

plt.title('Feature importance based on SHAP values')
# 첫 번째 SHAP Summary Plot
plt.figure()
shap.summary_plot(shap_values, feat_names, show=False)  # ax를 명시적으로 전달
st.pyplot(plt.gcf())  # 현재 figure를 Streamlit에 렌더링
plt.clf()  # 현재 figure를 초기화


## 이건 다시 고쳐야함
plt.title('Feature importance based on SHAP values (Bar)')
# 두 번째 SHAP Summary Plot (Bar)
plt.figure()
shap.summary_plot(shap_values, x_train, feat_names, plot_type="bar", show=False)
st.pyplot(plt.gcf())  # 현재 figure를 Streamlit에 렌더링
plt.clf()  # 현재 figure를 초기화