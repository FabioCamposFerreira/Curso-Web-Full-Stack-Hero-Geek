# Projeto Site de Noticias

## Objetivos

* Usar JSON como banco de dados
* Criar uma página com todas as notícias
* Criar uma página para cada notícia

## Teorial

### JSON (JavaScript Object Notation)

JSON é um formato leve para troca de dados. Ele é fácil de ler e escrever para humanos e fácil de interpretar e gerar para máquinas.

Exemplo de um objeto JSON simples:

```json
{
  "nome": "João",
  "idade": 30,
  "cidade": "São Paulo"
}
```

No contexto do projeto, usamos JSON para armazenar as notícias. Por exemplo, o arquivo `DataBase.json` contém um array de artigos:

```json
{
  "articles": [
    {
      "title": "Notícia 1",
      "author": "Autor 1",
      "url": "https://exemplo.com/noticia1"
    },
    {
      "title": "Notícia 2",
      "author": "Autor 2",
      "url": "https://exemplo.com/noticia2"
    }
  ]
}
```

Para acessar um artigo específico, usamos o método `find`:

```js
const artigo = data.articles.find((article) => article.url === noticiaUrl);
```
Explicação linha por linha:
- `const artigo = ...` cria uma variável chamada `artigo`.
- `data.articles` acessa o array de artigos dentro do objeto `data`.
- `.find((article) => ...)` procura o primeiro artigo que atende à condição.
- `article.url === noticiaUrl` compara a URL do artigo com o valor da variável `noticiaUrl`.

Código completo:

```js
const artigo = data.articles.find((article) => article.url === noticiaUrl);
```

### Fetch API

A Fetch API é usada para fazer requisições HTTP de forma assíncrona. No projeto, usamos para carregar o arquivo `DataBase.json`.

Exemplo básico de uso da Fetch API:

```js
fetch('url-do-arquivo.json')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erro:', error));
```
Explicação linha por linha:
- `fetch('url-do-arquivo.json')` faz uma requisição para buscar o arquivo JSON.
- `.then(response => response.json())` converte a resposta para um objeto JavaScript.
- `.then(data => console.log(data))` exibe os dados no console.
- `.catch(error => console.error('Erro:', error));` trata possíveis erros e exibe no console.

Código completo:

```js
fetch('url-do-arquivo.json')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erro:', error));
```

## Prática

### Passo 1: Index.html
* Criar o arquivo `index.html`

Explicação linha por linha:
```html
<!DOCTYPE html>
```
- Especifica o tipo de documento como HTML5.
```html
<html lang="pt">
```
- Abre a tag HTML e define o idioma como português.
```html
<head>
```
- Abre a tag `<head>`.
```html
    <meta charset="UTF-8">
```
- Define o conjunto de caracteres como UTF-8.
```html
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
```
- Garante que o site seja responsivo em dispositivos móveis.
```html
    <title>Notícias</title>
```
- Define o título da página.
```html
</head>
```
- Fecha a tag `<head>`.
```html
<body>
```
- Abre a tag `<body>`.
```html
    <div id="noticias">
    </div>
```
- Cria uma `<div>` com o id `noticias` para exibir as notícias.
```html
    <script src="./js/script.js"></script>
```
- Importa o arquivo JavaScript `script.js` para carregar as notícias na página.
```html
</body>
```
- Fecha a tag `<body>`.
```html
</html>
```
- Fecha a tag HTML.

Código completo:

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notícias</title>
</head>
<body>
    <div id="noticias">
    </div>
    <script src="./js/script.js"></script>
</body>
</html>
```

### Passo 2: script.js
* Criar o arquivo `script.js`

Explicação linha por linha:
```js
fetch('DataBase.json')
```
- Faz uma requisição para buscar o arquivo `DataBase.json`.
```js
  .then(response => response.json())
```
- Converte a resposta para um objeto JavaScript.
```js
  .then(data => {
```
- Inicia um bloco para manipular os dados recebidos.
```js
      const container = document.createElement('div');
```
- Cria um elemento `<div>` para ser o contêiner das notícias.
```js
      container.id = 'noticias-container';
```
- Define o id do contêiner como `noticias-container`.
```js
      data.articles.forEach(article => {
```
- Percorre cada artigo do array `articles`.
```js
          const noticia = document.createElement('div');
```
- Cria uma `<div>` para cada notícia.
```js
          noticia.className = 'noticia';
```
- Define a classe da `<div>` como `noticia`.
```js
          noticia.innerHTML = `
              <a href="./noticia.html?id=${article.url}" target="_blank">
                  <h2>${article.title}</h2>
                  <p><strong>Autor:</strong> ${article.author || 'Desconhecido'}</p>
                  <p>${article.description}</p>
                  <img src="${article.urlToImage}" alt="Imagem da notícia" style="max-width:300px;">
                  <hr>
              </a>
          `;
```
- Define o conteúdo HTML da notícia, incluindo link, título, autor, descrição e imagem.
```js
          container.appendChild(noticia);
```
- Adiciona a `<div>` da notícia ao contêiner.
```js
      });
```
- Fecha o loop de cada artigo.
```js
      const news = document.querySelector('#noticias');
```
- Seleciona o elemento com id `noticias` no HTML.
```js
      if (news) {
          news.appendChild(container);
      }
```
- Se o elemento existe, adiciona o contêiner de notícias nele.
```js
  })
```
- Fecha o bloco de manipulação dos dados.
```js
  .catch(error => console.error('Erro ao carregar as notícias:', error));
```
- Trata possíveis erros e exibe no console.

Código completo:

```js
fetch('DataBase.json')
  .then(response => response.json())
  .then(data => {
      const container = document.createElement('div');
      container.id = 'noticias-container';
      data.articles.forEach(article => {
          const noticia = document.createElement('div');
          noticia.className = 'noticia';
          noticia.innerHTML = `
              <a href="./noticia.html?id=${article.url}" target="_blank">
                  <h2>${article.title}</h2>
                  <p><strong>Autor:</strong> ${article.author || 'Desconhecido'}</p>
                  <p>${article.description}</p>
                  <img src="${article.urlToImage}" alt="Imagem da notícia" style="max-width:300px;">
                  <hr>
              </a>
          `;
          container.appendChild(noticia);
      });
      const news = document.querySelector('#noticias');
      if (news) {
          news.appendChild(container);
      }
  })
  .catch(error => console.error('Erro ao carregar as notícias:', error));
```

### Passo 3: noticia.html
* Criar o arquivo `noticia.html`

Explicação linha por linha:
```html
<!DOCTYPE html>
```
- Especifica o tipo de documento como HTML5.
```html
<html lang="pt">
```
- Abre a tag HTML e define o idioma como português.
```html
<head>
```
- Abre a tag `<head>`.
```html
    <meta charset="UTF-8">
```
- Define o conjunto de caracteres como UTF-8.
```html
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
```
- Garante que o site seja responsivo em dispositivos móveis.
```html
    <title>Notícia</title>
```
- Define o título da página.
```html
</head>
```
- Fecha a tag `<head>`.
```html
<body>
```
- Abre a tag `<body>`.
```html
    <h1 id="titulo"></h1>
```
- Cria um elemento `<h1>` para o título da notícia.
```html
    <h2 id="autor"></h2>
```
- Cria um elemento `<h2>` para o autor da notícia.
```html
    <img id="imagem" alt="">
```
- Cria um elemento `<img>` para a imagem da notícia.
```html
    <p id="conteudo"></p>
```
- Cria um elemento `<p>` para o conteúdo da notícia.
```html
    <script src="./js/noticia.js"></script>
```
- Importa o arquivo JavaScript `noticia.js` para carregar os dados da notícia.
```html
</body>
```
- Fecha a tag `<body>`.
```html
</html>
```
- Fecha a tag HTML.

Código completo:

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notícia</title>
</head>
<body>
    <h1 id="titulo"></h1>
    <h2 id="autor"></h2>
    <img id="imagem" alt="">
    <p id="conteudo"></p>
    <script src="./js/noticia.js"></script>
</body>
</html>
```

### Passo 4: noticia.js
* Criar o arquivo `noticia.js`

Explicação linha por linha:
```js
function getUrlParameter(name) {
```
- Declara uma função chamada `getUrlParameter` que recebe o nome do parâmetro.
```js
    const urlParams = new URLSearchParams(window.location.search);
```
- Cria um objeto para manipular os parâmetros da URL.
```js
    return urlParams.get(name);
```
- Retorna o valor do parâmetro solicitado.
```js
}
```
- Fecha a função.
```js
const noticiaUrl = getUrlParameter('id');
```
- Obtém o valor do parâmetro `id` da URL e armazena na variável `noticiaUrl`.
```js
fetch('DataBase.json')
```
- Faz uma requisição para buscar o arquivo `DataBase.json`.
```js
  .then(response => response.json())
```
- Converte a resposta para um objeto JavaScript.
```js
  .then(data => {
```
- Inicia um bloco para manipular os dados recebidos.
```js
      const noticia = data.articles.find(article => article.url === noticiaUrl);
```
- Procura a notícia que tem a URL igual ao valor do parâmetro `id`.
```js
      if (noticia) {
```
- Se a notícia foi encontrada, executa o bloco abaixo.
```js
          document.querySelector('title').innerText = noticia.title || 'Notícia';
```
- Atualiza o título da página com o título da notícia.
```js
          document.querySelector('#titulo').innerText = noticia.title || 'Título não disponível';
```
- Atualiza o elemento de título com o título da notícia.
```js
          document.querySelector('#autor').innerText = noticia.author || 'Autor desconhecido';
```
- Atualiza o elemento de autor com o autor da notícia.
```js
          document.querySelector('#imagem').src = noticia.urlToImage || '';
```
- Atualiza o elemento de imagem com a URL da imagem da notícia.
```js
          document.querySelector('#conteudo').innerText = noticia.content || 'Conteúdo não disponível';
```
- Atualiza o elemento de conteúdo com o texto da notícia.
```js
      } else {
```
- Se a notícia não foi encontrada, executa o bloco abaixo.
```js
          console.error('Notícia não encontrada.');
```
- Exibe uma mensagem de erro no console.
```js
      }
```
- Fecha o bloco condicional.
```js
  })
```
- Fecha o bloco de manipulação dos dados.
```js
  .catch(error => console.error('Erro ao carregar o arquivo DataBase.json:', error));
```
- Trata possíveis erros e exibe no console.

Código completo:

```js
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

const noticiaUrl = getUrlParameter('id');

fetch('DataBase.json')
  .then(response => response.json())
  .then(data => {
      const noticia = data.articles.find(article => article.url === noticiaUrl);
      if (noticia) {
          document.querySelector('title').innerText = noticia.title || 'Notícia';
          document.querySelector('#titulo').innerText = noticia.title || 'Título não disponível';
          document.querySelector('#autor').innerText = noticia.author || 'Autor desconhecido';
          document.querySelector('#imagem').src = noticia.urlToImage || '';
          document.querySelector('#conteudo').innerText = noticia.content || 'Conteúdo não disponível';
      } else {
          console.error('Notícia não encontrada.');
      }
  })
  .catch(error => console.error('Erro ao carregar o arquivo DataBase.json:', error));
```