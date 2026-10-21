/* =========================================================
   Mordisco — script da página
   Conecta o front-end com a API Flask usando fetch (GET e POST).
   ========================================================= */

const API = "http://localhost:5000";
const ROTA_PRODUTOS = `${API}/produtos`;

/* ---------- elementos da página ---------- */
const formulario = document.getElementById("form-produto");
const campoNome = document.getElementById("nome");
const campoQuantidade = document.getElementById("quantidade");
const campoPreco = document.getElementById("preco");
const botaoSalvar = document.getElementById("botao-salvar");
const listaProdutos = document.getElementById("lista-produtos");
const totalProdutos = document.getElementById("total-produtos");
const totalUnidades = document.getElementById("total-unidades");
const valorTotal = document.getElementById("valor-total");
const caixaMensagem = document.getElementById("caixa-mensagem");

let timerMensagem = null;

/* ---------- funções utilitárias ---------- */
function formatarMoeda(valor) {
  return Number(valor || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

function formatarNumero(valor) {
  return Number(valor || 0).toLocaleString("pt-BR");
}

/* Evita que o texto do produto entre como código HTML na lista. */
function escaparTexto(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

function mostrarMensagem(texto, tipo = "sucesso") {
  caixaMensagem.textContent = texto;
  caixaMensagem.className = `toast visivel ${tipo}`;

  clearTimeout(timerMensagem);
  timerMensagem = setTimeout(() => {
    caixaMensagem.className = "toast";
  }, 4000);
}

/* =========================================================
   REQUISIÇÕES À API (fetch + async/await + try/catch)
   ========================================================= */

/* GET /produtos -> devolve a lista de produtos do banco */
async function listarProdutos() {
  const resposta = await fetch(ROTA_PRODUTOS);
  if (!resposta.ok) {
    throw new Error("Não consegui falar com o servidor. A API está rodando?");
  }
  return await resposta.json();
}

/* POST /produtos -> cadastra um produto novo no banco */
async function cadastrarProduto(dados) {
  const resposta = await fetch(ROTA_PRODUTOS, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });

  const resultado = await resposta.json();

  if (!resposta.ok) {
    throw new Error(resultado.erro || "Não foi possível cadastrar o produto.");
  }
  return resultado;
}

/* DELETE /produtos/<id> -> apaga um produto do banco */
async function excluirProduto(id) {
  const resposta = await fetch(`${ROTA_PRODUTOS}/${id}`, { method: "DELETE" });
  const resultado = await resposta.json();

  if (!resposta.ok) {
    throw new Error(resultado.erro || "Não foi possível excluir o produto.");
  }
  return resultado;
}

/* =========================================================
   DESENHAR A PÁGINA
   ========================================================= */

/* Lista de produtos */
function desenharProdutos(produtos) {
  listaProdutos.innerHTML = "";

  if (produtos.length === 0) {
    listaProdutos.innerHTML = `
      <div class="vazio">
        <svg viewBox="0 0 64 64" aria-hidden="true">
          <defs>
            <mask id="mascara-vazia">
              <rect width="64" height="64" fill="#fff"></rect>
              <circle cx="49" cy="15" r="12" fill="#000"></circle>
            </mask>
          </defs>
          <circle cx="32" cy="32" r="26" fill="#FFD8AE" mask="url(#mascara-vazia)"></circle>
          <circle cx="22" cy="24" r="3.4" fill="#FFF6E9"></circle>
          <circle cx="34" cy="18" r="2.6" fill="#FFF6E9"></circle>
          <circle cx="25" cy="42" r="3" fill="#FFF6E9"></circle>
        </svg>
        <strong>Nenhum lanche por aqui ainda</strong>
        Cadastre o primeiro produto no formulário ao lado para ele aparecer aqui.
      </div>`;
    return;
  }

  produtos.forEach((produto) => {
    const linha = document.createElement("div");
    linha.className = "item colunas c-linha";
    linha.innerHTML = `
      <div class="c-nome nome-produto">${escaparTexto(produto.nome)}</div>
      <div class="c-qtd"><span class="qtd">${formatarNumero(produto.quantidade)} un.</span></div>
      <div class="c-preco preco">${formatarMoeda(produto.preco_unitario)} / un.</div>
      <div class="c-total total">${formatarMoeda(produto.valor_total)}</div>
      <button class="c-acao remover" type="button" title="Excluir produto" aria-label="Excluir produto">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 7h16M9 7V5h6v2M6 7l1 13h10l1-13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
      </button>`;

    const botaoRemover = linha.querySelector(".remover");
    botaoRemover.addEventListener("click", () => removerProduto(produto));

    listaProdutos.appendChild(linha);
  });
}

/* Resumo do estoque (calculado com os dados reais vindos do banco) */
function desenharResumo(produtos) {
  const unidades = produtos.reduce((soma, p) => soma + Number(p.quantidade || 0), 0);
  const valor = produtos.reduce((soma, p) => soma + Number(p.valor_total || 0), 0);

  totalProdutos.textContent = formatarNumero(produtos.length);
  totalUnidades.textContent = formatarNumero(unidades);
  valorTotal.textContent = formatarMoeda(valor);
}

/* Carrega o estoque e desenha tudo na tela */
async function carregarEstoque() {
  try {
    const produtos = await listarProdutos();
    desenharProdutos(produtos);
    desenharResumo(produtos);
  } catch (erro) {
    mostrarMensagem(erro.message || "Erro ao carregar o estoque.", "erro");
  }
}

/* Exclui um produto (pede confirmação antes) */
async function removerProduto(produto) {
  const confirmar = window.confirm(`Excluir "${produto.nome}" do estoque?`);
  if (!confirmar) return;

  try {
    await excluirProduto(produto.id);
    mostrarMensagem(`"${produto.nome}" foi removido do estoque.`, "sucesso");
    await carregarEstoque();
  } catch (erro) {
    mostrarMensagem(erro.message || "Erro ao excluir o produto.", "erro");
  }
}

/* =========================================================
   FORMULÁRIO DE CADASTRO
   ========================================================= */
formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const dados = {
    nome: campoNome.value.trim(),
    quantidade: Number(campoQuantidade.value),
    preco_unitario: Number(campoPreco.value),
  };

  /* validação simples antes de chamar a API */
  if (!dados.nome) {
    mostrarMensagem("Escreva o nome do produto.", "erro");
    campoNome.focus();
    return;
  }
  if (campoQuantidade.value === "" || Number.isNaN(dados.quantidade) || dados.quantidade < 0) {
    mostrarMensagem("A quantidade precisa ser um número maior ou igual a zero.", "erro");
    campoQuantidade.focus();
    return;
  }
  if (campoPreco.value === "" || Number.isNaN(dados.preco_unitario) || dados.preco_unitario < 0) {
    mostrarMensagem("O preço unitário precisa ser um número maior ou igual a zero.", "erro");
    campoPreco.focus();
    return;
  }

  botaoSalvar.disabled = true;
  botaoSalvar.querySelector("span").textContent = "Salvando...";

  try {
    const produto = await cadastrarProduto(dados);

    formulario.reset();
    campoQuantidade.value = 1;
    campoNome.focus();

    mostrarMensagem(`"${produto.nome}" entrou no estoque!`, "sucesso");

    /* atualiza a lista e os valores sem recarregar a página */
    await carregarEstoque();
  } catch (erro) {
    mostrarMensagem(erro.message || "Erro ao cadastrar o produto.", "erro");
  } finally {
    botaoSalvar.disabled = false;
    botaoSalvar.querySelector("span").textContent = "Salvar no estoque";
  }
});

/* quando a página abre, já busca os produtos no banco */
carregarEstoque();
