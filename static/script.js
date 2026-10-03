const canvas = document.querySelector("#drawingCanvas") // paper    
const ctx = canvas.getContext("2d") // ctx → pen/brush
const clearBtn = document.querySelector("#but1");
const predictBtn = document.querySelector("#but2");

let isDrawing = false;
let lastX;
let lastY;


ctx.strokeStyle = "white";
ctx.lineWidth = 18;
ctx.lineCap = "round";
ctx.lineJoin = "round";

//mousedown stores the starting point.

canvas.addEventListener("mousedown" , function(event){
    isDrawing = true;
    lastX = event.offsetX;
    lastY = event.offsetY;

});

canvas.addEventListener("mouseup", function(event){
    isDrawing = false;
});

//mousemove gets the new point.

canvas.addEventListener("mousemove", function(event){
    if (isDrawing === false){
        return;
    }

    const X = event.offsetX; // hori pos of mouse
    const Y = event.offsetY; // ver pos of mouse
 
    ctx.beginPath(); // strat a new path
    ctx.moveTo(lastX, lastY);  // start the path from prev pos
    ctx.lineTo(X, Y); // to this point
    ctx.stroke(); // and display the line

    lastX = X; // update the current values
    lastY = Y;

});

clearBtn.addEventListener('click', function(event){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    isDrawing = false;
})

predictBtn.addEventListener("click", async function () {

    const imageData = canvas.toDataURL();

    const response = await fetch("/predict", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            imageData: imageData
        })
    });

    const data = await response.json();

    document.querySelector("#prediction").textContent = data.Prediction;
    document.querySelector("#confidence").textContent = (data.Probability * 100).toFixed(2);

});











