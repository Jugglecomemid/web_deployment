
let myimage = document.querySelector('img');

myimage.onclick = function(){
    let mysrc = myimage.getAttribute('src');
    if(mysrc === 'images/web.jpg'){
        myimage.setAttribute('src', 'images/googleai.jpg');
    }else{
        myimage.setAttribute('src', 'images/web.jpg');
    }
}


let mybut = document.querySelector("button");
let myhead = document.querySelector('h1');

function setusername() {
    let myname = prompt("what's your name?");
    localStorage.setItem('name', myname);
    myhead.textContent = 'Weclome ' + myname;
}

if(!localStorage.getItem('name')){
    setusername();
}else{
    let storename = localStorage.getItem('name');
    myhead.textContent = 'Weclome '+ storename;
}

mybut.onclick = function() {
    setusername();
}

const para = document.querySelector('p');
para.addEventListener('click', updateName);

function updateName(){
    let name = prompt('Input a new name: ');
    para.textContent='changed: '+ name;
}



