# 🔐 Guia de Autenticação - Google Sheets API

## 🎯 Problema Identificado

Você está enfrentando um erro de SSL ao tentar autenticar com o Google:
```
SSLEOFError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol
```

**Causa**: Antivírus, Firewall ou Proxy interceptando o tráfego HTTPS.

## ✅ Solução Implementada

O código foi modificado para usar **autenticação manual**, que é mais robusta e contorna problemas de SSL.

---

## 🚀 COMO USAR

### Opção 1: Script de Autenticação Dedicado (RECOMENDADO)

Execute o script auxiliar que facilita todo o processo:

```cmd
python autenticar.py
```

Siga as instruções na tela. O script irá:
- ✅ Verificar suas credenciais
- ✅ Abrir o navegador automaticamente
- ✅ Guiar você passo a passo
- ✅ Salvar o token para uso futuro

---

### Opção 2: Usar o Programa Principal Diretamente

1. **Deletar token antigo** (se existir):
   ```cmd
   del token.json
   ```

2. **Executar o programa**:
   ```cmd
   python main.py
   ```

3. **Seguir as instruções** quando a autenticação for solicitada.

---

## 📋 PASSO A PASSO DA AUTENTICAÇÃO MANUAL

Quando você executar o programa, verá algo assim:

```
🔐 Iniciando processo de autenticação...
⚠️  Detectado problema de SSL - usando método alternativo

============================================================
🌐 AUTENTICAÇÃO MANUAL
============================================================

1. Abra este link no seu navegador:

https://accounts.google.com/o/oauth2/auth?...

2. Faça login com sua conta Google
3. Autorize o aplicativo
4. Você será redirecionado para uma página
   (pode mostrar erro 'Não foi possível acessar o site')
5. COPIE A URL COMPLETA da barra de endereços
   (deve começar com 'http://localhost')
```

### O que fazer:

1. **O navegador abrirá automaticamente** - Se não abrir, copie e cole o link manualmente

2. **Faça login** com sua conta Google

3. **Autorize o aplicativo** clicando em "Permitir" ou "Allow"

4. **⚠️ IMPORTANTE**: Você verá uma página de ERRO:
   ```
   Não é possível acessar este site
   localhost recusou a conexão
   ERR_CONNECTION_REFUSED
   ```
   
   **✅ ISSO É NORMAL! NÃO FECHE O NAVEGADOR!**

5. **Copie a URL completa** da barra de endereços do navegador:
   ```
   http://localhost:55555/?code=4/0AbCdEf...&scope=https://...
   ```
   - Clique na barra de endereços
   - Selecione tudo (Ctrl+A)
   - Copie (Ctrl+C)

6. **Cole no terminal** onde o programa está aguardando:
   ```
   📋 Aguardando autorização...
   Cole aqui a URL completa que apareceu no navegador:
   > [COLE AQUI E PRESSIONE ENTER]
   ```

7. **Aguarde a confirmação**:
   ```
   ✅ Autenticação manual realizada com sucesso!
   ✅ Credenciais salvas com sucesso!
   ```

---

## 🔍 DIAGNÓSTICO

Para identificar problemas de conectividade:

```cmd
python test_ssl.py
```

Este script testa:
- ✅ Conectividade básica com a internet
- ✅ Contexto SSL/TLS
- ✅ Conexão com servidores do Google
- ✅ Possíveis bloqueios de firewall/antivírus

---

## 🛠️ SOLUÇÕES SE AINDA DER ERRO

### 1. Usar Dados Móveis (MAIS EFETIVO)

Se você tem um smartphone:
1. Ative o **Hotspot WiFi** no celular
2. Conecte o computador ao hotspot
3. Execute o programa novamente

Isso geralmente resolve porque evita o firewall/antivírus da rede local.

### 2. Desativar Antivírus Temporariamente

⚠️ **CUIDADO**: Faça isso apenas se confiar no código.

1. Desative o antivírus por 5 minutos
2. Execute o programa e faça a autenticação
3. Reative o antivírus imediatamente

### 3. Adicionar Exceção no Antivírus/Firewall

Configure seu antivírus para permitir:
- `python.exe`
- `pythonw.exe`
- Esta pasta: `G:\Meu Drive\Workspace\aleatorio\principal-tarefas-aleatorias`

### 4. Tentar em Outra Rede

- Casa de um amigo
- Biblioteca pública
- Coworking
- Cafeteria com WiFi

### 5. Atualizar Bibliotecas

```cmd
pip install --upgrade certifi google-auth google-auth-oauthlib google-auth-httplib2
```

### 6. Reiniciar o Computador

Às vezes resolve problemas de SSL no Windows.

---

## 📝 NOTAS IMPORTANTES

1. ✅ O erro **"localhost recusou a conexão"** é **NORMAL** durante a autenticação manual
2. ✅ Você só precisa autenticar **UMA VEZ**
3. ✅ Após autenticar, o arquivo `token.json` será criado e reutilizado
4. ✅ O token é válido por um bom tempo (semanas/meses)
5. ⚠️ Se mudar as permissões, delete o `token.json` e autentique novamente

---

## 🆘 AINDA NÃO FUNCIONOU?

Se nenhuma das soluções acima funcionou, o problema pode ser:

- **Rede corporativa/escola** com bloqueio severo
- **Necessidade de VPN** para acessar serviços do Google
- **Problema com a conta Google** (verificação em 2 etapas mal configurada)
- **Região geográfica** com restrições

### Últimas tentativas:

1. Usar **outro computador** (de um amigo, familiar)
2. Usar **outra rede** completamente diferente
3. Verificar se a conta Google está funcionando normalmente
4. Tentar em **outro sistema operacional** (Linux via Live USB)

---

## 📚 Arquivos Importantes

- `credentials.json` - Credenciais do projeto Google Cloud (NÃO compartilhe!)
- `token.json` - Token de acesso gerado após autenticação (NÃO compartilhe!)
- `autenticar.py` - Script auxiliar para facilitar autenticação
- `test_ssl.py` - Script de diagnóstico de problemas de SSL
- `SOLUCAO_SSL.md` - Documentação detalhada sobre o problema

---

## ✨ Resumo Rápido

```cmd
# 1. Se for a primeira vez ou deu erro:
del token.json

# 2. Opção A - Script dedicado (recomendado):
python autenticar.py

# 2. Opção B - Programa principal:
python main.py

# 3. Se precisar diagnosticar:
python test_ssl.py
```

**Boa sorte! 🍀**