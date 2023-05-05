

let journal = document.getElementById('journal');
let article = document.getElementById('article');
let btn1 = document.getElementById('btn1');
let btn2 = document.getElementById('btn2');

btn1.addEventListener('click', () =>{
    article.classList.remove("block")
    journal.classList.toggle("block")
})

btn2.addEventListener('click', () =>{
    journal.classList.remove("block")
    article.classList.toggle("block")
})