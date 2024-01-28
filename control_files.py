import pickle

class DataHandler:
    def __init__(self):
        pass

    @staticmethod
    def read_time():
        with open('data\\time.pkl', 'rb') as file:
            data = pickle.load(file)
            return data

    @staticmethod
    def save_time(time_to_save):
        with open('data\\time.pkl', 'wb') as file:
            pickle.dump(time_to_save, file)

    @staticmethod
    def read_status():
        with open('data\\status.pkl.pkl', 'rb') as file:
            data = pickle.load(file)
            return data

    @staticmethod
    def write_status(status_to_save):
        with open('data\\status.pkl', 'wb') as file:
            pickle.dump(status_to_save, file)

    @staticmethod
    def read_uses():
        with open('data\\uses.pkl', 'rb') as file:
            data = pickle.load(file)
            return data

    @staticmethod
    def write_uses(uses_to_save):
        with open('data\\uses.pkl', 'wb') as file:
            pickle.dump(uses_to_save, file)

    @staticmethod
    def read_localization():
        with open('data\\current_localization.pkl', 'rb') as file:
            data = pickle.load(file)
            return data

    @staticmethod
    def write_localization(latitude: float, longitude: float):
        with open('data\\current_localization.pkl', 'wb') as file:
            pickle.dump([latitude, longitude], file)