"""
Script auxiliar para diagnosticar e corrigir problemas de SSL com Google API
"""

import os
import sys
import certifi
import ssl


def verificar_certificados():
    """Verifica se os certificados SSL estão instalados corretamente"""
    print("=== DIAGNÓSTICO DE SSL ===\n")

    print(f"1. Caminho do certifi: {certifi.where()}")
    print(f"2. Arquivo existe: {os.path.exists(certifi.where())}")

    # Verificar versão do SSL
    print(f"3. Versão do OpenSSL: {ssl.OPENSSL_VERSION}")
    print(f"4. Versão do Python SSL: {ssl.PROTOCOL_TLS_CLIENT}")

    # Verificar se token.json existe
    token_path = "token.json"
    if os.path.exists(token_path):
        print(f"\n⚠️  ATENÇÃO: O arquivo '{token_path}' existe.")
        print("   Recomendação: Delete este arquivo para forçar nova autenticação.")
        print(f"   Execute: del {token_path}")
    else:
        print(
            f"\n✅ Arquivo '{token_path}' não encontrado (isso é bom para primeira autenticação)."
        )

    # Verificar credentials.json
    cred_path = "G:\\Meu Drive\\Workspace\\aleatorio\\principal-tarefas-aleatorias\\credentials.json"
    if os.path.exists(cred_path):
        print(f"✅ Arquivo 'credentials.json' encontrado.")
    else:
        print(f"❌ ERRO: Arquivo 'credentials.json' NÃO encontrado em: {cred_path}")

    print("\n=== SOLUÇÕES RECOMENDADAS ===\n")
    print("1. DELETE o arquivo token.json:")
    print("   del token.json")
    print("\n2. Atualize as bibliotecas:")
    print(
        "   pip install --upgrade certifi google-auth google-auth-oauthlib google-auth-httplib2"
    )
    print("\n3. Se o erro persistir, tente desativar temporariamente:")
    print("   - Antivírus")
    print("   - Firewall do Windows")
    print("   - VPN (se estiver usando)")
    print("\n4. Como último recurso, reinicie o computador")


def deletar_token():
    """Deleta o arquivo token.json se existir"""
    token_path = "token.json"
    if os.path.exists(token_path):
        try:
            os.remove(token_path)
            print(f"✅ Arquivo '{token_path}' deletado com sucesso!")
            print("Agora execute 'python main.py' novamente.")
        except Exception as e:
            print(f"❌ Erro ao deletar '{token_path}': {e}")
    else:
        print(f"ℹ️  Arquivo '{token_path}' não existe.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--delete-token":
        deletar_token()
    else:
        verificar_certificados()
        print("\n" + "=" * 50)
        print("Para deletar o token.json automaticamente, execute:")
        print("python fix_ssl.py --delete-token")
