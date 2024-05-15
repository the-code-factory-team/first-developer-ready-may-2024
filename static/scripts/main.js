//Слайдер
const slider = document.querySelector('.slider');
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
const slides = Array.from(slider.querySelectorAll('img'));
const slideCount = slides.length;
let slideIndex = 0;

prevButton.addEventListener('click', showPreviousSlide);
nextButton.addEventListener('click', showNextSlide);

function showPreviousSlide() {
  slideIndex = (slideIndex - 1 + slideCount) % slideCount;
  updateSlider();
}

setInterval(() => {
    showNextSlide()
}, 7000)

function showNextSlide() {
  slideIndex = (slideIndex + 1) % slideCount;
  updateSlider();
}

function updateSlider() {
  slides.forEach((slide, index) => {
    if (index === slideIndex) {    
      slide.style.display = 'block';
    } else {
      slide.style.display = 'none';
    }
  });
}

//Меню  
let menu = document.querySelector('.menu-content-block');
btnmenu.onclick = function() {
    if (menu.style.display === "block"){
        anime({
            targets: '.menu-content-block',
            translateX: [0, -500],
            duration: 1500
          });
        setTimeout(() => {
            menu.style.display = 'none'
        }, 500)}
    else {
        menu.style.display = 'block';
        anime({
            targets: '.menu-content-block',
            translateX: [-100, 0],
            duration: 1000
          });}
}

//Подсветка
document.addEventListener("DOMContentLoaded", function() {
window.addEventListener("scroll", function() {
    let blocks = [
        document.querySelector("#block1"),
        document.querySelector("#block2"),
        document.querySelector("#block3")];

    for (let block of blocks) {
        let blockPosition = block.getBoundingClientRect().top;
        if (Math.abs(blockPosition) < window.innerHeight / 2) {
            block.style.filter = 'none'
            if (block.id === 'block1' && flag !== block.id) {
                flag = block.id
                block1()
            } else if (block.id === 'block2' && flag !== block.id) {
                flag = block.id
                block2()
            } else if (block.id === 'block3' && flag !== block.id) {
                flag = block.id
                block3()
            }
        } else {
            block.style.filter = 'brightness(30%)'}}})});

// Анимации
anime({
    targets: ["#line", '#btnmenu'],
    translateY: [-200, 0],
    delay: 500,
    opacity: [{ 
        value: 0,
        duration: 500},{
        value: 1}],
    easing: 'easeInOutQuad',
    duration: 1000
  });

function block1() {
    update()
    anime({
        targets: "#title",
        opacity: [{ 
            value: 0,
            duration: 500},{
            value: 1}],
        easing: 'easeInOutQuad',
      });
      anime({
        targets: '#video',
        translateX: [500, 0],
        delay: 1500,
        opacity: [{ 
            value: 0,
            duration: 500},{
            value: 1}],
        easing: 'easeInOutQuad',
        duration: 1000
      });
  }

function block2() {
    update()
    anime({
        targets: '#global_title',
        translateY: [-400, 0],
        delay: 2500,
        opacity: [{ 
            value: 0,
            duration: 500},{
            value: 1}],
        easing: 'easeInOutQuad',
        duration: 1000
      });

    let lst_blocks = ['#txt1', '#txt2', '#txt3']
    for (let i = 1; i-1 < lst_blocks.length; i++) {
        setTimeout(() => {
            anime({
                targets: lst_blocks[i-1],
                translateY: [600, 0],
                opacity: [{ 
                    value: 0,
                    duration: 500},{
                    value: 1}],
                easing: 'easeInOutQuad',
                duration: 1000
            });
        }, 600*i)
    }
}

function block3() {
    update()
}

function AnimeonHover(element){
    anime({
        targets: element,
        translateY: -10,
        easing: 'easeInOutQuad',
        duration: 200
      });
}

function AnimeoffHover(element){
    anime({
        targets: element,
        translateY: 0,
        easing: 'easeInOutQuad',
        duration: 200
      });
}

function update() {
    let lst_els = [
    document.querySelector("#video"),
    document.querySelector("#title"),
    document.querySelector('#global_title'),
    document.querySelector('#txt1'),
    document.querySelector('#txt2'),
    document.querySelector('#txt3'),
    //document.querySelector('.slider-container')
    ]

    function zeroing(selectors) {
        for (let selector of selectors) {
            selector.style.opacity = '0'
        }
    }
    
    zeroing(lst_els)
}

//Инициализация при старте
block1()
updateSlider()
var flag = 'block1'