const customName = document.getElementById('customname');
const randomize = document.querySelector('.randomize');
const story = document.querySelector('.story');

function randomValueFromArray(array){
    const random = Math.floor(Math.random()*array.length);
    return array[random];
 }

let stroyText = '今天气温 34 摄氏度，:inserta:出去遛弯。当走到:insertb:门前时，突然就:insertc:。人们都惊呆了，李雷全程目睹但并没有慌，因为:inserta:是一个 130 公斤的胖子，天气又辣么热';
let insertX = ['怪兽威利','大老爹','圣诞老人'];
let insertY = ['肯德基','迪士尼','白宫'];
let insertZ = ['自燃了','化成了一滩泥','变成一条鼻涕虫爬走了'];


randomize.addEventListener('click', result);

function result() {

    let newStory = stroyText;

    let xItem = randomValueFromArray(insertX);
    let yItem = randomValueFromArray(insertY);
    let zItem = randomValueFromArray(insertZ);

    newStory = newStory.replace(/:inserta:/g, xItem);
    newStory = newStory.replace(':insertb:', yItem);
    newStory = newStory.replace(':insertc:', zItem);



    if(customName.value !== '') {
        let name = customName.value;
        newStory = newStory.replace('李雷', name);

    }

    if(document.getElementById("american").checked) {
        let weight = Math.round(34*9/5+32);
        let temperature = Math.round(130*2.204);

        newStory = newStory.replace('34 摄氏度', temperature+ ' 华氏度');
        newStory = newStory.replace('130 公斤', weight+" 磅");



    }

    story.textContent = newStory;
    story.style.visibility = 'visible';
}