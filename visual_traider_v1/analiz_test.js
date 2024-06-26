// const data = JSON.parse(test)
// console.log(data)

fetch("test.json")
  .then(response => response.json())
  .then(json => {
    data = json.map(el=>`
    <div>
    <p><b>${el.pos}</b> - ${el.name} : ${el.open} - ${el.close}</p>
    <img src="${el.open_image}">
    <img src="${el.close_img}">
    </div>
    `)
    document.getElementById('analiz').innerHTML = data
  });