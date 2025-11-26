// "https://www.gov.br/anp/pt-br/assuntos/exploracao-e-producao-de-oleo-e-gas/seguranca-operacional/publicidade-dos-programas-de-descomissionamento-de-instalacoes"
const links = document.querySelector("#parent-fieldname-text > table > tbody").children
const linksArr = Array.from(links)
const urls = []
linksArr.forEach(e => {
    const url = e.firstElementChild.firstElementChild.getAttribute("href")
    urls.push(url)
})