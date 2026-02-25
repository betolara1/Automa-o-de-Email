import smtplib
from email.message import EmailMessage
import os

# Descomente as linhas abaixo se for usar python-dotenv para carregar o .env
# from dotenv import load_dotenv 
# load_dotenv()

def enviar_emails(lista_destinatarios, remetente, senha):
    # Corpo HTML predefinido
    corpo_email = """
    <p>Bom dia</p>
    <p>Venha aprender a mandar e-mail automatico</p>
    """
    
    # Gerenciar a conexão SMTP na estrutura "with" garante que seja fechada no final
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls() # Criptografia
            servidor.login(remetente, senha) # Login é feito UMA ÚNICA VEZ
            
            # Loop de envio reaproveitando o login
            for destinatario in lista_destinatarios:
                msg = EmailMessage()
                msg['Subject'] = 'ASSUNTO DA MENSAGEM'
                msg['From'] = remetente
                msg['To'] = destinatario
                
                # Define que o formato primário é HTML
                msg.set_content(corpo_email, subtype='html')
                
                try:
                    servidor.send_message(msg)
                    print(f'Email enviado com sucesso para: {destinatario}')
                except Exception as e:
                    print(f'Erro ao enviar para {destinatario}. Erro: {e}')
                    
    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação: Verifique seu e-mail e sua senha de aplicativo.")
    except Exception as erro_geral:
        print(f"Ocorreu um erro ao conectar: {erro_geral}")


if __name__ == "__main__":
    # 1. Obter credenciais de forma segura 
    # Idealmente, use variáveis de ambiente como: meu_email = os.getenv("EMAIL_REMETENTE")
    meu_email = "" # COLOQUE SEU E-MAIL AQUI
    minha_senha = ""  # COLOQUE SUA SENHA DE APLICATIVO AQUI
    
    # 2. Ler os e-mails corretamente
    try:
        with open("email.txt", "r") as arquivo:
            # Remove quebras de linha e espaços e filtra linhas em branco
            emails_para_enviar = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
            
        print(f"Foram encontrados {len(emails_para_enviar)} e-mails para envio.")
        
        # 3. Disparar a rotina
        if emails_para_enviar:
            enviar_emails(emails_para_enviar, meu_email, minha_senha)
        else:
            print("A lista de e-mails está vazia.")
            
    except FileNotFoundError:
        print("Erro: O arquivo 'email.txt' não foi encontrado na mesma pasta.")