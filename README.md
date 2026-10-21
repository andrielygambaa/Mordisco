# 🍪 Mordisco — Estoque da Cantina

Sistema web para gerenciar o estoque da cantina de uma escola: você cadastra os
lanches, vê o que ainda tem na prateleira e acompanha o valor de tudo.

Feito em **HTML + CSS + JavaScript** no front-end e **Python + Flask + SQLite**
no back-end — a página conversa com a API usando `fetch()` (GET e POST).

---

## 🖼️ Como fica

> *(Dica: depois de rodar o sistema, tire um print da janela do navegador e
> cole a imagem aqui no README, entre estas linhas e o fim do bloco.)*

---

## 🚀 Como rodar (3 passos)

### 1º — Instale o Python (uma vez só)

Se você ainda não tem Python no computador:

1. Baixe em **https://www.python.org/downloads/**
2. Ao instalar, **marque a caixinha "Add Python to PATH"** (é importantinho!)
3. Pronto.

### 2º — Instale as dependências (uma vez só)

Abra a pasta do projeto e **dê dois cliques em `instalar.bat`**.

Esse arquivo cria o *ambiente virtual* (a pasta `.venv`) e baixa o Flask e o
Flask-Cors. Só precisa de internet nessa etapa. Quando aparecer
**"Pronto! Agora é só dar dois cliques no iniciar.bat"**, pode fechar a janela.

### 3º — Use o sistema

Dê dois cliques em **`iniciar.bat`**.

Ele sobe o servidor e **abre o navegador sozinho** em
`http://localhost:5000`. Para encerrar, feche a janela preta do servidor ou
aperte `CTRL + C` dentro dela.

> Não precisa digitar comando nenhum no dia a dia — o `iniciar.bat` faz tudo.

---

## ✅ Como testar

1. Abra o sistema pelo `iniciar.bat`.
2. No quadro **"Cadastrar produto"**, preencha:
   - **Nome do produto** — ex.: `Pão de queijo`
   - **Quantidade** — ex.: `24`
   - **Preço unitário (R$)** — ex.: `4.50`
3. Clique em **Salvar no estoque**.
4. Pronto! O produto aparece na lista **sem a página recarregar**, uma
   plaquinha verde confirma o sucesso e os valores do resumo se atualizam.
5. Para tirar um produto do estoque, clique no botão da lixeira ao lado dele.

Os dados ficam salvos no arquivo `estoque.db` (SQLite), na mesma pasta do
projeto — se você fechar e abrir o sistema de novo, tudo continua lá.

---

## 📁 Estrutura do projeto

```
mordisco/
├── app.py              # aplicação Flask e as rotas da API
├── produto.py          # classe Produto (um lanche: nome, quantidade, preço)
├── estoque.py          # classe Estoque (lista, cadastro e totais)
├── templates/
│   └── index.html      # a página do sistema
├── static/
│   ├── style.css       # o design (creme + laranja)
│   ├── script.js       # a ligação com a API (fetch GET e POST)
│   └── favicon.svg     # o ícone do site
├── requirements.txt    # dependências (Flask e Flask-Cors)
├── instalar.bat        # instala as dependências (uma vez só)
├── iniciar.bat         # abre o sistema (use este no dia a dia)
├── .gitignore
└── README.md
```

---

## 🧠 Como o sistema funciona

### As duas classes (programação orientada a objetos)

**`Produto`** (`produto.py`) representa um lanche:

```python
class Produto:
    def __init__(self, nome, quantidade, preco_unitario, id=None):
        ...

    def valor_total(self):
        return self.quantidade * self.preco_unitario   # quantidade x preço
```

**`Estoque`** (`estoque.py`) cuida do conjunto de produtos e do banco:

```python
estoque = Estoque()              # cria a tabela e carrega o que já tem salvo
produto = estoque.cadastrar("Pão de queijo", 24, 4.50)   # salva no SQLite
estoque.listar()                 # devolve a lista de objetos Produto
estoque.quantidade_total()       # soma das unidades
estoque.valor_total()            # soma do valor de todos os produtos
```

O `app.py` usa essas classes para montar as rotas da API.

### As rotas da API

| Método   | Endereço             | O que faz                                  |
| -------- | -------------------- | ------------------------------------------ |
| `GET`    | `/`                  | abre a página do sistema                   |
| `GET`    | `/produtos`          | lista todos os produtos do banco           |
| `POST`   | `/produtos`          | cadastra um produto novo                   |
| `DELETE` | `/produtos/<id>`     | exclui um produto                          |
| `GET`    | `/resumo`            | totais do estoque (calculados no servidor) |

O **CORS** está ativado no `app.py` com `CORS(app)`, para a página poder
buscar os dados na API sem problema.

### O lado do JavaScript (`static/script.js`)

```javascript
// GET: busca os produtos do banco e desenha na tela
async function listarProdutos() {
  const resposta = await fetch("http://localhost:5000/produtos");
  return await resposta.json();
}

// POST: cadastra um produto novo
async function cadastrarProduto(dados) {
  const resposta = await fetch("http://localhost:5000/produtos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
  return await resposta.json();
}
```

Depois do cadastro dar certo, o formulário é limpo, aparece a mensagem de
sucesso e a lista é atualizada com `await carregarEstoque()` — **sem recarregar
a página**. Todos os `fetch` estão dentro de `try/catch`, então se o servidor
estiver fora do ar a pessoa vê uma mensagem em vez de a tela quebrar.

> 💡 Se você mudar a porta do servidor, lembre de trocar a URL no começo do
> `script.js` (`const API = "http://localhost:5000";`).

---

## 🚀 Publicando no GitHub

O projeto já vem com o `.gitignore` pronto (ele não sobe o `.venv` nem o banco
de dados). No terminal, dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "Mordisco: sistema de estoque da cantina (Atividade 3)"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/mordisco.git
git push -u origin main
```

Depois é só abrir o link do repositório e conferir que está tudo lá.

---

## 🩺 Problemas comuns

| Situação | O que fazer |
| --- | --- |
| "Python não foi encontrado" | Instale o Python marcando **"Add Python to PATH"** e reinicie o computador. |
| "Porta 5000 já está em uso" | Feche a outra janela do servidor (ou rode `iniciar.bat` de novo depois de fechá-la). |
| A página abriu mas a lista está vazia | Normal: ainda não existe produto cadastrado. Cadastre o primeiro pelo formulário. |
| Quero recomeçar do zero | Apague o arquivo `estoque.db` e abra o sistema de novo — ele cria um novo. |
| Erro ao instalar as dependências | Precisa de internet na primeira instalação. Confira a conexão e rode o `instalar.bat` de novo. |

---

## ✏️ Créditos

Projeto da **Atividade 3 — DWS (Desenvolvimento de Websites)**, 4º bimestre.
Tecnologias: HTML, CSS, JavaScript puro, Python, Flask, Flask-Cors e SQLite.
