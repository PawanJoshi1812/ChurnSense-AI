from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def get_preprocessor():

    scaler = StandardScaler()

    pipeline = Pipeline([
        ("scaler", scaler)
    ])

    return pipeline