// Função para obter o parâmetro 'id' da URL
function getUrlParameter(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

// Obter o parâmetro 'id' da URL
const noticiaUrl = getUrlParameter("id");

// Buscar o arquivo DataBase.json
fetch("DataBase.json")
  .then((response) => response.json())
  .then((data) => {
    // Encontrar a notícia correspondente ao parâmetro 'id'
    const noticia = data.articles.find((article) => article.url === noticiaUrl);

    if (noticia) {
      // Atualizar os elementos da página com os dados da notícia
      document.querySelector("title").innerText = noticia.title || "Notícia";
      document.querySelector("#titulo").innerText =
        noticia.title || "Título não disponível";
      document.querySelector("#autor").innerText =
        noticia.author || "Autor desconhecido";
      document.querySelector("#imagem").src = noticia.urlToImage || "";
      document.querySelector("#conteudo").innerText =
        noticia.content || "Conteúdo não disponível";
    }
  });

// https://newsapi.org/v2/everything?q=brasil&from=2025-09-06&sortBy=publishedAt&apiKey=366a4893cc3440b486f45b01e7fe90a5
