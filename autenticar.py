#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script auxiliar para autenticação com Google Sheets API
Este script facilita o processo de autenticação manual quando há problemas de SSL
"""

import os
import sys
import webbrowser

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Configurações
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CLIENT_SECRET_FILE = os.environ.get("GOOGLE_CLIENT_SECRET_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json"))
TOKEN_FILE = os.environ.get("GOOGLE_TOKEN_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json"))


def print_header(text):
    """Imprime um cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def verificar_credenciais():
    """Verifica se o arquivo credentials.json existe"""
    if not os.path.exists(CLIENT_SECRET_FILE):
        print("❌ Arquivo de credenciais não encontrado!")
        print(f"   Procurado em: {CLIENT_SECRET_FILE}")
        print("\n💡 SOLUÇÃO:")
        print("   1. Acesse: https://console.cloud.google.com/")
        print("   2. Crie um projeto (se não tiver)")
        print("   3. Ative a Google Sheets API")
        print("   4. Crie credenciais OAuth 2.0")
        print("   5. Baixe o arquivo JSON")
        print(f"   6. Salve como: {CLIENT_SECRET_FILE}")
        return False
    return True


def verificar_token_existente():
    """Verifica se já existe um token válido"""
    if os.path.exists(TOKEN_FILE):
        print(f"ℹ️  Token existente encontrado: {TOKEN_FILE}")
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            if creds and creds.valid:
                print("✅ Token válido! Você já está autenticado.")
                print("\n💡 Se quiser reautenticar, delete o arquivo token.json")
                return True
            elif creds and creds.expired:
                print("⚠️  Token expirado. Será necessário reautenticar.")
        except Exception as e:
            print(f"⚠️  Token corrompido: {e}")
    return False


def autenticar_manual():
    """Realiza autenticação manual via navegador"""
    print_header("AUTENTICAÇÃO MANUAL COM GOOGLE")

    print("\n📋 INSTRUÇÕES:")
    print("   1. Um navegador será aberto automaticamente")
    print("   2. Faça login com sua conta Google")
    print("   3. Autorize o aplicativo")
    print("   4. Você será redirecionado para uma página com ERRO")
    print("      (Isso é NORMAL e ESPERADO!)")
    print("   5. Copie a URL COMPLETA da barra de endereços")
    print("      (começa com 'http://localhost')")
    print("   6. Cole aqui quando solicitado")

    input("\n⏸️  Pressione ENTER quando estiver pronto...")

    try:
        # Criar flow
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

        # Gerar URL de autenticação
        auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

        print_header("PASSO 1: ABRIR NAVEGADOR")
        print(f"\n🌐 URL de autenticação:\n{auth_url}")
        print("\n🚀 Abrindo navegador...")

        webbrowser.open(auth_url)

        print_header("PASSO 2: AUTORIZAR APLICATIVO")
        print("\n✋ Aguarde a página carregar...")
        print("   → Faça login com sua conta Google")
        print("   → Clique em 'Permitir' ou 'Allow'")
        print("   → Aguarde o redirecionamento")

        print_header("PASSO 3: COPIAR URL")
        print("\n⚠️  IMPORTANTE:")
        print("   Após autorizar, você verá:")
        print("   'Não é possível acessar este site'")
        print("   'localhost recusou a conexão'")
        print("\n   ✅ ISSO É NORMAL! NÃO SE PREOCUPE!")
        print("\n   Copie a URL completa da barra de endereços.")
        print("   Exemplo:")
        print("   http://localhost:12345/?code=4/0AbC...&scope=https://...")

        # Solicitar URL de redirecionamento
        print("\n" + "-" * 70)
        redirect_response = input("📎 Cole a URL aqui e pressione ENTER:\n> ").strip()

        if not redirect_response:
            print("\n❌ URL não fornecida!")
            return False

        if not redirect_response.startswith("http://localhost"):
            print("\n❌ URL inválida! Deve começar com 'http://localhost'")
            print(f"   Você colou: {redirect_response[:50]}...")
            return False

        print("\n⏳ Processando código de autorização...")

        # Buscar token usando o código
        flow.fetch_token(authorization_response=redirect_response)
        creds = flow.credentials

        # Salvar credenciais
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

        print("\n✅ SUCESSO!")
        print(f"   Token salvo em: {TOKEN_FILE}")
        print("\n🎉 Autenticação concluída com sucesso!")
        print("   Você pode usar o programa normalmente agora.")

        return True

    except Exception as e:
        print(f"\n❌ Erro durante autenticação: {e}")
        print("\n🔧 POSSÍVEIS SOLUÇÕES:")
        print("   1. Verifique se copiou a URL completa")
        print("   2. Tente novamente e espere o redirecionamento completar")
        print("   3. Use dados móveis (hotspot) se estiver com problema de rede")
        print("   4. Desative temporariamente antivírus/firewall")
        return False


def deletar_token():
    """Deleta o token existente"""
    if os.path.exists(TOKEN_FILE):
        try:
            os.remove(TOKEN_FILE)
            print(f"✅ Token deletado: {TOKEN_FILE}")
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar token: {e}")
            return False
    else:
        print(f"ℹ️  Token não existe: {TOKEN_FILE}")
        return True


def menu():
    """Menu interativo"""
    print_header("🔐 AUTENTICAÇÃO GOOGLE SHEETS API")

    print("\n📂 Configuração:")
    print(f"   Credenciais: {CLIENT_SECRET_FILE}")
    print(f"   Token: {TOKEN_FILE}")

    print("\n⚙️  Opções:")
    print("   1. Autenticar (ou reautenticar)")
    print("   2. Verificar status da autenticação")
    print("   3. Deletar token e reautenticar")
    print("   4. Sair")

    escolha = input("\n🔢 Escolha uma opção (1-4): ").strip()
    return escolha


def main():
    """Função principal"""
    print("\n🚀 Script de Autenticação - Google Sheets API")
    print("   Desenvolvido para resolver problemas de SSL/TLS")

    # Verificar credenciais
    if not verificar_credenciais():
        return 1

    while True:
        escolha = menu()

        if escolha == "1":
            # Autenticar
            print_header("OPÇÃO 1: AUTENTICAR")
            if verificar_token_existente():
                resposta = input(
                    "\n❓ Já existe um token válido. Deseja reautenticar? (s/n): "
                ).lower()
                if resposta != "s":
                    print("   Operação cancelada.")
                    continue
                deletar_token()

            if autenticar_manual():
                print("\n✅ Você está pronto para usar o programa!")
                break
            else:
                print("\n❌ Autenticação falhou. Tente novamente.")
                continue

        elif escolha == "2":
            # Verificar status
            print_header("OPÇÃO 2: VERIFICAR STATUS")
            if verificar_token_existente():
                print("✅ Status: Autenticado")
            else:
                print("❌ Status: Não autenticado")
                print("💡 Execute a opção 1 para autenticar")

        elif escolha == "3":
            # Deletar e reautenticar
            print_header("OPÇÃO 3: DELETAR E REAUTENTICAR")
            if deletar_token():
                if autenticar_manual():
                    print("\n✅ Reautenticação concluída!")
                    break
                else:
                    print("\n❌ Reautenticação falhou.")
            else:
                print("\n❌ Não foi possível deletar o token.")

        elif escolha == "4":
            # Sair
            print("\n👋 Até logo!")
            return 0

        else:
            print("\n❌ Opção inválida! Escolha 1, 2, 3 ou 4.")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
