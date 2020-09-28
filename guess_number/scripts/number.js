let rand_num = Math.floor(Math.random()*100) +1;
const guesses = document.querySelector('.guesses');
const lastresult = document.querySelector('.lastResult');
const lowOrHi = document.querySelector('.lowOrHi');
const guessSubmit = document.querySelector('.guessSubmit');
const guessField = document.querySelector('.guessField');

let guessCount =1;
let resetButton;

function checkGuess() {
    let userguess = Number(guessField.value);
    if(guessCount===1){
        guesses.textContent='Last number: ';
    }
    guesses.textContent += userguess + ' ';

    if(userguess === rand_num){
        lastresult.textContent ='Congrate!';
        lastresult.style.backgroundColor = 'green';
        lowOrHi.textContent = '';
        setGameOver();
    }else if(guessCount === 10){
        lastresult.textContent = 'Game Over!';
        lowOrHi.textContent = '';
        setGameOver();
    }else{
        lastresult.textContent = 'Wrong guess!';
        lastresult.style.backgroundColor = 'red';
        if(userguess<rand_num){
            lowOrHi.textContent = 'Too Low';
        }else if(userguess>rand_num){
            lowOrHi.textContent = 'Too High';
        }
    }

    guessCount++;
    guessField.value =''
    guessField.focus();
 }

guessSubmit.addEventListener('click', checkGuess);

function setGameOver(){
    guessField.disabled = true;
    guessSubmit.disabled = true;
    resetButton = document.createElement('button');
    resetButton.textContent = 'Start a new game!';
    document.body.appendChild(resetButton);
    resetButton.addEventListener('click', resetGame);
}

function resetGame(){
    guessSubmit =1;

    const resetParas = document.querySelectorAll('.resultParas p');
    for (let i =0; i<resetParas.length; i++){
        resetParas[i].textContent = '';
    }

    resetButton.parentNode.removeChild(resetButton);

    guessField.disabled =false;
    guessSubmit.disabled =false;
    guessField.value='';
    guessField.focus();

    lastresult.style.backgroundColor ='white';

    rand_num = Math.floor(Math.random() *100) +1;
}


