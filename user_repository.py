import pickle


class UserRepository:
    def __init__(self, connection):
        self.connection = connection
        self.namespace = "users"

    def save(self, user):
        user_key = self.__key(user.username)
        user_bytes = pickle.dumps(user)
        self.connection.set(user_key, user_bytes)

    def get(self, username):
        user_key = self.__key(username)
        user_bytes = self.connection.get(user_key)
        if user_bytes:
            return pickle.loads(user_bytes)
        else:
            return None


    def __key(self, username):
        return self.namespace + ":" + username

    def check_credentials(self,username, password):
        user = self.get(username)
        if user and user.password == password:
            print("Credenciais válidas para o usuário:", username)
            return True
        elif not user:
            print("Nome de usuário ou senha inválidos.", username)
            return False
    
    def user_exists(self, username):
        user_key = self.__key(username)
        return self.connection.exists(user_key)