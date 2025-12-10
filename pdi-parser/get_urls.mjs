// "https://www.gov.br/anp/pt-br/assuntos/exploracao-e-producao-de-oleo-e-gas/seguranca-operacional/publicidade-dos-programas-de-descomissionamento-de-instalacoes"
const links = document.querySelector("#parent-fieldname-text > table > tbody").children
const linksArr = Array.from(links)
const urls = []

linksArr.forEach(e => {
    const item = e.firstElementChild.firstElementChild
    const url = item.getAttribute("href")
    const title = item.innerText.replaceAll(";", ",")
    const name = url.split("/").reverse()[0].replace(".pdf", "")
    urls.push({ url, name, title })
})

const lines = []
lines.push("title;name;url")
urls.forEach(e =>
    lines.push(`${e.title};${e.name};${e.url}`)
)
const csv = lines.join("\n")
