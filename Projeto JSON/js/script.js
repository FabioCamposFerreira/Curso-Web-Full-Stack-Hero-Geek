// Função para gerar elementos HTML para cada notícia
fetch('DataBase.json')
	.then(response => response.json())
	.then(data => {
		const container = document.createElement('div');
		container.id = 'noticias-container';
		document.body.appendChild(container);
		data.articles.forEach(article => {
			const noticia = document.createElement('div');
			noticia.className = 'noticia';
			noticia.innerHTML = `
				<h2>${article.title}</h2>
				<p><strong>Autor:</strong> ${article.author || 'Desconhecido'}</p>
				<p>${article.description}</p>
				<img src="${article.urlToImage}" alt="Imagem da notícia" style="max-width:300px;">
				<p><a href="${article.url}" target="_blank">Leia mais</a></p>
				<hr>
			`;
			container.appendChild(noticia);
		});
			// Se quiser adicionar o container em um elemento específico, use:
			const news = document.querySelector('#noticias');
			if (news) {
				news.appendChild(container);
			}
		})
		.catch(error => {
			console.error('Erro ao carregar as notícias:', error);
		});

// https://newsapi.org/v2/everything?q=brasil&from=2025-09-06&sortBy=publishedAt&apiKey=366a4893cc3440b486f45b01e7fe90a5

