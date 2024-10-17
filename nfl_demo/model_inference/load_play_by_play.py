from model_inference.organize_data import main_1
data = None

def load_model():
    global data
    data = main_1()

def get_data():
  if data is None:
      raise Exception("Expensive model not loaded")
  return data