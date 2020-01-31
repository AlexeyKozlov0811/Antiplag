
download.onclick = function(){
a = document.createElement("a")

const regex1 = /\+\s/g;
const regex2 = /\-\s/g;
const regex3 = /;/g;

console.log($(".selection_header").text().replace(regex3, '\n'))
console.log($(".selection_content").text().replace(regex1, '+\n').replace(regex2, '-\n'))

a.setAttribute("href", "data:text/plain," + $(".selection_header").text().replace(regex3, '\n') + '\n' + $(".selection_content").text().replace(regex1, '+\n').replace(regex2, '-\n'))
a.setAttribute("download", "Antiplag_selection_set.txt")


a.click()


}