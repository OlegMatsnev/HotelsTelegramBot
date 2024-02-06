
const rangeInput = document.querySelectorAll(".range-input input"), // (0) - querySelector
priceInput = document.querySelectorAll(".price-input input"),
range = document.querySelector(".slider .progress");
let priceGap = 100; // (1) - let

const stars = document.querySelectorAll("button");
const radioButtons = document.querySelectorAll('input[name="guestRating"]');

let chosenStar = 2;
let chosenRating = "any";
let finishButton = document.querySelector("#ready");


priceInput.forEach(input =>{ // (2) - forEach
    input.addEventListener("input", e =>{ // (3) - addEventListener
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);
        console.log(finishButton);
        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max && minPrice >= rangeInput[0].min){
            if(e.target.className === "input-min"){
                rangeInput[0].value = minPrice;
                range.style.left = ((minPrice / rangeInput[0].max) * 100) + "%";
            }else{
                rangeInput[1].value = maxPrice;
                range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
            }
        }
    });
});



rangeInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-min"){
                rangeInput[0].value = maxVal - priceGap
            }else{
                rangeInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
    });
});

stars.forEach((star, star_i) => {
  star.addEventListener("click", () =>  {
    stars.forEach((changeStar, i) => {
      // console.log("press" + star_i);
      // console.log(i);
      // if (star_i >= i) {
      //   changeStar.style.backgroundColor = "yellow";
      // } else {
      //   changeStar.style.backgroundColor = "#fff";
      // }
      star_i <= i ? changeStar.classList.add('active') : changeStar.classList.remove('active');
    });
    // console.log(star_i); --> получение индекса выбранной звезды (2 звезды - 0i)
    chosenStar = star_i + 2;
  });
});

// Добавляем обработчик события change к каждой радиокнопке
radioButtons.forEach(radioButton => {
  radioButton.addEventListener('change', function() {
    // Проверяем, какая радиокнопка была выбрана
    if (this.checked) {
      // console.log('Выбрана радиокнопка с значением:', this.value);
      chosenRating = this.value;
      // Здесь можно выполнить дополнительные действия в зависимости от выбора пользователя
    }
  });
});

finishButton.addEventListener("click", () => {
//  console.log("min price: " + priceInput[0].value);
//  console.log("max price: " + priceInput[1].value);
//  console.log("stars count: " + chosenStar);
//  console.log("guest rating: " + chosenRating);
    let tg = window.Telegram.WebApp;
    tg.expand();

    let data = {
        price: {
            max: parseInt(priceInput[1].value),
            min: parseInt(priceInput[0].value)
        },
        star: chosenStar,
        guestRating: chosenRating
    }
    tg.sendData(JSON.stringify(data))
    tg.close();
})

// (0): querySelector: Document метод querySelector() возвращает первый элемент (Element) документа,
//      который соответствует указанному селектору или группе селекторов. Если совпадений не найдено, возвращает значение null.
// (1): let: declare variable can be changed
//      var differs from let by scope - let is local
// (2):
///  const array1 = ['a', 'b', 'c'];
//   array1.forEach((element) => console.log(element));
//   Expected output: "a"
//   Expected output: "b"
//   Expected output: "c"
// (3): addEventListener(type, listener, options)
//      addEventListener(type, listener, useCapture)
