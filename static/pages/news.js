let btn = document.getElementById('btn');
let box = document.querySelector('.box');



btn.addEventListener('click', () =>{
        box.classList.add("block")
})

box.addEventListener('click', () =>{
    box.classList.remove("block")
})
