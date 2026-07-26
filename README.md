# 🪐 CurseMark - Advanced Web Fuzzer & Recon Tool

<p align="center">
  <img src="https://shields.io" alt="Python 3">
  <img src="https://shields.io" alt="License MIT">
  <img src="https://shields.io" alt="Stage Production">
</p>

O **CurseMark** é uma ferramenta leve e automatizada de fuzzer web desenvolvida em Python. Ela combina requisições HTTP furtivas com conexões diretas via Raw Sockets para mapear servidores, identificar tecnologias expostas (WAF, HSTS, CSP) e descobrir diretórios ocultos ou arquivos de ambiente sensíveis (`.env`).

---

## ⚡ Funcionalidades Integradas

* 🕵️ **User-Agent Spoofing:** Rotatividade automatizada de cabeçalhos legítimos.
* 🛡️ **IP Spoofing:** Injeção de falsos endereços via `X-Forwarded-For` e `X-Real-IP`.
* 📡 **Socket Banner Grabbing:** Conexão de baixo nível via sockets puros para capturar assinaturas reais do servidor.
* 🗂️ **Automated Root Scan:** Varredura automática prévia em busca de arquivos `.env` e variações na raiz do host.
* 🧬 **Extension Bruteforcing:** Aplicação dinâmica de múltiplas extensões (`.php`, `.html`, `.json`) para cada linha da sua wordlist.

---

## 🚀 Como Instalar e Executar

### 1. Clonar o Repositório
```bash
git clone https://github.com
cd CurseMark
```

### 2. Instalar as Dependências
O projeto utiliza bibliotecas nativas do Python, necessitando apenas do módulo `requests`:
```bash
pip install requests
```

### 3. Executar a Ferramenta
```bash
python canabyfuzz.py
```

---

## 🛠️ Interface de Configuração

Ao iniciar, o terminal exibirá a assinatura visual da ferramenta e solicitará os parâmetros de alvo:

```text
---> target url...: target.com
---> wordlist......: wordlists/common.txt
```

### Exemplo de Retorno do Mapeamento (Host Data):
```text
[>] data for host
 * status code: 200
 * size: 4122
 * server: nginx/1.18.0
 * powered by: not exposed
 * redirect to: nothing
 * cors origin: standard
 * waf indicator: unknown
 * get hsts: true
 * get csp: false
 * resolved ip: 93.184.216.34
 * target port: 80 (open)
 * socket banner: nginx/1.18.0
```

---

## 📁 Estrutura de Varredura Dinâmica
Durante o brute-force principal, o motor do **CurseMark** testa automaticamente cada termo combinado com os seguintes sufixos:
* `termo` (Diretório puro)
* `termo.php`
* `termo.html`
* `termo.txt`
* `termo.json`
* `termo/`
* `termo/.env` (E variações de backup local)

---

## ⚠️ Isenção de Responsabilidade (Disclaimer)

O uso do **CurseMark** para testar alvos sem autorização prévia é ilegal. O desenvolvedor não se responsabiliza pelo uso indevido ou danos causados por esta ferramenta. Utilize-a estritamente para fins educacionais, laboratórios de CTF ou auditorias de segurança autorizadas (Pentests).

---
<p align="center">
  Desenvolvido com 🎯 por <a href="https://github.com">cannabidi0lx</a>
</p>
