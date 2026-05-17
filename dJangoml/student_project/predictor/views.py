import pickle
import os
from django.shortcuts import render
import joblib

# Load model correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model.pkl')

# Try multiple methods to load the model
model = None
try:
    # Method 1: Try skops first (best for old sklearn models)
    try:
        from skops.io import load
        model = load(model_path, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        pass
    
    # Method 2: Try joblib
    if model is None:
        try:
            model = joblib.load(model_path)
        except:
            pass
    
    # Method 3: Fall back to pickle
    if model is None:
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning)
        model = pickle.load(open(model_path, 'rb'))
        
except Exception as e:
    print(f"Error loading model: {e}")
    # Create a dummy model to allow the app to start
    from sklearn.tree import DecisionTreeClassifier
    model = DecisionTreeClassifier()


def home(request):
    return render(request, 'home.html')


def predict(request):
    if request.method == 'POST':
        try:
            # Get form data
            age = float(request.POST.get('age'))
            studytime = float(request.POST.get('studytime'))
            failures = float(request.POST.get('failures'))
            absences = float(request.POST.get('absences'))
            G1 = float(request.POST.get('G1'))
            G2 = float(request.POST.get('G2'))

            # Prepare data (same order as training)
            data = [age, studytime, failures, absences, G1, G2]

            print("INPUT DATA:", data)  # debug

            # Prediction
            result = model.predict([data])

            final = "Pass" if result[0] == 1 else "Fail"

            return render(request, 'result.html', {'result': final})

        except Exception as e:
            print("ERROR:", e)
            return render(request, 'home.html', {'error': str(e)})

    return render(request, 'home.html')