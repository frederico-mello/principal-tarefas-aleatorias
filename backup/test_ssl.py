#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico de Conexão SSL/TLS para Google APIs
Este script testa a conectividade e identifica problemas comuns.
"""

import sys
import socket
import ssl
import certifi
import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Desabilitar warnings temporariamente
urllib3.disable_warnings(InsecureRequestWarning)


def print_header(title):
    """Imprime um cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_basic_internet():
    """Testa conectividade básica com a internet"""
    print_header("Teste 1: Conectividade Básica")

    try:
        response = requests.get("https://www.google.com", timeout=10)
        if response.status_code == 200:
            print("✅ Conexão com Google.com: OK")
            return True
        else:
            print(f"⚠️  Conexão com Google.com retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Falha ao conectar com Google.com: {e}")
        return False


def test_ssl_context():
    """Testa a criação de contexto SSL"""
    print_header("Teste 2: Contexto SSL")

    try:
        context = ssl.create_default_context(cafile=certifi.where())
        print(f"✅ Contexto SSL criado com sucesso")
        print(f"   Certificados em: {certifi.where()}")
        print(f"   Protocolo: {context.protocol}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar contexto SSL: {e}")
        return False


def test_google_oauth():
    """Testa conexão com servidores OAuth do Google"""
    print_header("Teste 3: Servidor OAuth do Google")

    urls = [
        "https://accounts.google.com",
        "https://oauth2.googleapis.com",
        "https://www.googleapis.com",
    ]

    all_ok = True
    for url in urls:
        try:
            response = requests.get(url, timeout=15, verify=certifi.where())
            print(f"✅ {url}: OK (status {response.status_code})")
        except requests.exceptions.SSLError as e:
            print(f"❌ {url}: ERRO SSL")
            print(f"   Detalhes: {str(e)[:100]}")
            all_ok = False
        except Exception as e:
            print(f"⚠️  {url}: Erro")
            print(f"   Detalhes: {str(e)[:100]}")
            all_ok = False

    return all_ok


def test_socket_connection():
    """Testa conexão direta via socket"""
    print_header("Teste 4: Conexão Socket TLS")

    hostname = "oauth2.googleapis.com"
    port = 443

    try:
        # Criar contexto SSL
        context = ssl.create_default_context(cafile=certifi.where())
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Forçar TLS 1.2 ou superior
        context.minimum_version = ssl.TLSVersion.TLSv1_2

        # Criar socket
        with socket.create_connection((hostname, port), timeout=15) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"✅ Conexão TLS estabelecida com {hostname}")
                print(f"   Versão TLS: {ssock.version()}")
                print(f"   Cipher: {ssock.cipher()[0]}")
                return True

    except ssl.SSLError as e:
        print(f"❌ Erro SSL ao conectar com {hostname}")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar com {hostname}")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {str(e)}")
        return False


def test_requests_with_session():
    """Testa requests com sessão customizada"""
    print_header("Teste 5: Sessão HTTP Customizada")

    try:
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        session = requests.Session()
        session.verify = certifi.where()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        response = session.get("https://oauth2.googleapis.com", timeout=15)
        print(f"✅ Sessão customizada funcionando (status {response.status_code})")
        return True

    except Exception as e:
        print(f"❌ Erro na sessão customizada: {e}")
        return False


def check_firewall_antivirus():
    """Verifica indicações de firewall/antivírus"""
    print_header("Teste 6: Verificação de Bloqueios")

    print("ℹ️  Verificando possíveis bloqueios...")

    # Tentar sem verificação SSL (não recomendado, apenas para teste)
    try:
        response = requests.get(
            "https://oauth2.googleapis.com", timeout=15, verify=False
        )
        print("⚠️  IMPORTANTE: Conexão funciona SEM verificação SSL")
        print("   Isso indica que pode haver:")
        print("   - Antivírus interceptando tráfego HTTPS")
        print("   - Firewall corporativo com inspeção SSL")
        print("   - Proxy transparente")
        print("   - Certificados SSL corporativos não confiáveis")
        return False
    except Exception as e:
        print("✅ Falha mesmo sem verificação SSL")
        print("   Isso indica problema de rede ou bloqueio total")
        return True


def print_system_info():
    """Imprime informações do sistema"""
    print_header("Informações do Sistema")

    import platform

    print(f"Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Certifi: {certifi.__version__}")
    print(f"Requests: {requests.__version__}")
    print(f"urllib3: {urllib3.__version__}")

    # Verificar variáveis de ambiente
    import os

    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY"]
    proxies_found = False

    for var in proxy_vars:
        if var in os.environ:
            print(f"⚠️  Variável de ambiente {var}: {os.environ[var]}")
            proxies_found = True

    if not proxies_found:
        print("✅ Nenhuma variável de proxy configurada")


def main():
    """Executa todos os testes"""
    print("\n" + "🔍 DIAGNÓSTICO DE CONEXÃO SSL/TLS" + "\n")
    print("Este script irá testar a conectividade com os servidores do Google")
    print("para identificar problemas de SSL/certificados/firewall.")

    print_system_info()

    results = []
    results.append(("Conectividade Básica", test_basic_internet()))
    results.append(("Contexto SSL", test_ssl_context()))
    results.append(("Servidores Google", test_google_oauth()))
    results.append(("Socket TLS", test_socket_connection()))
    results.append(("Sessão HTTP", test_requests_with_session()))
    results.append(("Bloqueios", check_firewall_antivirus()))

    # Resumo
    print_header("RESUMO DOS TESTES")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:.<40} {status}")

    print(f"\n📊 Resultado: {passed}/{total} testes passaram")

    # Recomendações
    print_header("RECOMENDAÇÕES")

    if passed == total:
        print("🎉 Todos os testes passaram!")
        print("   A conexão com Google APIs deve funcionar normalmente.")
    elif passed == 0:
        print("❌ Todos os testes falharam!")
        print("\n🔧 SOLUÇÕES:")
        print("   1. Verifique sua conexão com a internet")
        print("   2. Tente usar dados móveis (hotspot do celular)")
        print("   3. Desative temporariamente antivírus/firewall")
        print("   4. Se estiver em rede corporativa/escola, pode haver bloqueio")
        print("   5. Reinicie o roteador e o computador")
    else:
        print("⚠️  Alguns testes falharam")
        print("\n🔧 POSSÍVEIS CAUSAS:")

        if not results[2][1]:  # Teste de servidores Google falhou
            print("   • Servidores do Google podem estar bloqueados")
            print("     → Tente usar uma VPN ou dados móveis")

        if not results[3][1]:  # Teste de socket falhou
            print("   • Problema com certificados SSL")
            print("     → Execute: pip install --upgrade certifi")

        if not results[5][1]:  # Teste de bloqueios
            print("   • Firewall/Antivírus pode estar interceptando")
            print("     → Adicione exceção para Python e este programa")

    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Se os testes passaram, delete 'token.json' e tente novamente")
    print("   2. Se falharam, siga as recomendações acima")
    print("   3. Execute o programa principal: python main.py")
    print("\n")


if __name__ == "__main__":
    main()
