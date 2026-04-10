# 🔒 SOLUÇÃO PARA PROBLEMAS DE SSL/TLS

## 📋 Diagnóstico Realizado

O diagnóstico identificou que o problema está relacionado a:
- **Antivírus interceptando tráfego HTTPS**
- **Firewall com inspeção SSL**
- **Proxy transparente**
- **Certificados SSL corporativos**

## ✅ SOLUÇÃO IMPLEMENTADA

O código foi atualizado para usar **autenticação manual**, que é mais robusta e contorna problemas de SSL.

## 🚀 COMO USAR AGORA

### Passo 1: Deletar token antigo (se existir)
```cmd
del token.json
```

### Passo 2: Executar o programa
```cmd
python main.py
```

### Passo 3: Seguir as instruções de autenticação

Quando solicitado, você verá algo assim:

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

============================================================

📋 Aguardando autorização...
Cole aqui a URL completa que apareceu no navegador:
> _
```

### Passo 4: Copiar a URL de redirecionamento

1. O navegador abrirá automaticamente
2. Faça login com sua conta Google
3. Autorize o aplicativo
4. **IMPORTANTE**: Após autorizar, você verá uma página com erro:
   ```
   Não é possível acessar este site
   localhost recusou a conexão
   ```
5. **NÃO SE PREOCUPE!** Este erro é esperado.
6. Na barra de endereços do navegador, você verá uma URL como:
   ```
   http://localhost:12345/?code=4/0ABCD...&scope=https://...
   ```
7. **COPIE TODA ESSA URL** (Ctrl+C)
8. **COLE** no terminal onde o programa está pedindo

### Passo 5: Aguardar confirmação

Se tudo der certo, você verá:
```
✅ Autenticação manual realizada com sucesso!
✅ Credenciais salvas com sucesso!
```

## 🔍 SE AINDA ASSIM DER ERRO

### Opção 1: Usar dados móveis
Se você tem um smartphone, tente:
1. Criar um hotspot WiFi no celular
2. Conectar o computador ao hotspot
3. Executar o programa novamente

Isso geralmente resolve porque evita o firewall/antivírus da rede local.

### Opção 2: Desativar antivírus temporariamente
**CUIDADO**: Faça isso apenas se confiar no código.
1. Desative o antivírus por alguns minutos
2. Execute o programa
3. Reative o antivírus

### Opção 3: Adicionar exceção no firewall/antivírus
1. Abra as configurações do seu antivírus/firewall
2. Adicione exceção para:
   - `python.exe`
   - `pythonw.exe`
   - A pasta do projeto: `G:\Meu Drive\Workspace\aleatorio\principal-tarefas-aleatorias`

### Opção 4: Executar diagnóstico
Execute o script de diagnóstico para mais detalhes:
```cmd
python test_ssl.py
```

## ⚙️ COMANDOS ÚTEIS

### Ver se token existe
```cmd
dir token.json
```

### Deletar token
```cmd
del token.json
```

### Atualizar bibliotecas
```cmd
pip install --upgrade certifi google-auth google-auth-oauthlib google-auth-httplib2
```

### Ver versões instaladas
```cmd
pip list | findstr google
```

## 📝 NOTAS IMPORTANTES

1. **O erro "localhost recusou conexão" é NORMAL** durante a autenticação manual
2. Você só precisa fazer a autenticação **uma vez**
3. Após autenticar, o `token.json` será salvo e reutilizado
4. Se mudar as permissões (SCOPES), delete o `token.json` e autentique novamente

## 🆘 AINDA PRECISA DE AJUDA?

Se nenhuma das soluções funcionou, o problema pode ser:
- Rede corporativa/escola com bloqueio severo
- Necessidade de VPN
- Problema com a conta Google (verificação em 2 etapas, etc)

Tente:
1. Usar outro computador
2. Usar outra rede (casa de amigo, biblioteca, etc)
3. Verificar se a conta Google tem 2FA ativado corretamente