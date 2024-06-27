import redis
import datetime

from model.user import User
from model.message import Message
from model.timeline import TimelineType

from repository.user_repository import UserRepository
from repository.message_repository import MessageRepository
from repository.timeline_repository import TimelineRepository


conn = redis.Redis(host="127.0.0.1", port=6379)   #Troque o valor de host para o endereço de loopback local
#Caso seja necessário o host utilizado no trabalho avise


user_repository = UserRepository(connection=conn)
message_repository = MessageRepository(connection=conn)
timeline_repository = TimelineRepository(connection=conn)


def login(username, password):

    user_repository = UserRepository(conn)

    if user_repository.check_credentials(username, password):
        return True
    else:
        return None
    
def register_user():
    username=str(input("Digite seu nome de usuário: "))
    
    user = User(
        username = username,
        fullname = str(input("Digite seu nome completo: ")),
        email= str(input("Digite seu email: ")),
        password = str(input("Digite sua senha: "))
    )
    if user_repository.check_credentials(user.username,user.password):
        print(":p  ;) Você ja possui cadastro no StonedChat :)  :D")
    elif user_repository.check_credentials(user.username,user.password) == False:
        user_repository.save(user)
        print(":p  ;) Cadastro concluido com sucesso :)  :D !!!")
    return True



while True:
    print("StonedChat\n(1) para login\n(2) para se cadastrar\n(0) sair da aplicação")
    option = input("Digite uma das opções acima: ")
    
    if option == "1":
        username = input("Digite seu nome de usuário: ")
        password = input("Digite sua senha: ")
        logged_in_user = login(username, password)
        if logged_in_user:
            print("Bem-vindo!\n")
            while True:
                print("\n->StonedChat\n(1) para ler caixa de entrada\n(2) para ler caixa de saída\n(3) para enviar uma nova mensagem\n(0) para deslogar")
                second_step = input("Digite uma das opções acima: ")
                if second_step == '1':
                    userInboxToday = timeline_repository.get(
                        owner=username,
                        type=TimelineType.INBOX,
                        date=datetime.datetime.now(),
                    )
                    if not userInboxToday.messages:
                        print(" :[ Caixa de entrada vazia. =(")
                    else:
                        print(f"\n{username}'s INBOX:")
                        for message_key in userInboxToday.messages:
                            m = message_repository.get(message_key)
                            print(
                                "From: " + m.sender,
                                "Message: " + m.text,
                                "At: " + str(m.created_at),
                                sep="\n",
                                end="\n\n",
                            )
                elif second_step == '2':
                    userSentToday = timeline_repository.get(
                        owner=username,
                        type=TimelineType.SENT,
                        date=datetime.datetime.now(),
                    )
                    print(f"{username} SENT:")
                    if not userSentToday.messages:
                        print("Você não possui mensagens enviadas.")
                    else:
                        for message_key in userSentToday.messages:
                            m = message_repository.get(message_key)
                            print(
                                "To: " + m.recipient,
                                "Message: " + m.text,
                                "At: " + str(m.created_at),
                                sep="\n",
                                end="\n\n",
                            )
                elif second_step == '3':
                    #enviar mensagem
                    friend=str(input('Digite o username do destinatário: '))
                    if user_repository.user_exists(friend):
                        txt=str(input("Digite uma mensagem: "))
                        message = Message(
                            sender=username,
                            recipient=friend,
                            text=txt,
                        )
                        #salvar mensagem enviada
                        timeline_repository.post_message(message)
                    elif user_repository.user_exists(friend) == False:
                        print("Usuário não encontrado.")
                elif second_step == '0':
                    print("Você foi desconectado do StonedChat")
                    break
                else:
                    print("Opção inválida")
                    break

    elif option == "2":
        register_user()
    
    elif option == "0":
        break
 