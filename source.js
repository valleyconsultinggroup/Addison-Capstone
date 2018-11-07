names = []
Array.from(document.getElementsByClassName("actor-name")).forEach(function(x){names.push(x.innerText)})
names.pop()
names.shift()
names.toString()
