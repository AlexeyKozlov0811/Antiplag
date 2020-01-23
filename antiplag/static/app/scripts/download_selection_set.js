a = document.createElement("a")

const regex1 = /\+\s/g;
const regex2 = /\-\s/g;

console.log($(".content").text().replace(regex1, '+\n').replace(regex2, '-\n'))

a.setAttribute("href", "data:text/plain," + $(".content").text().replace(regex1, '+\n').replace(regex2, '-\n'))
a.setAttribute("download", "filename.txt")
b.onclick = function(){ a.click() }