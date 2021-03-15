const $cupcakeList = $('#cupcake-list');
const $cupcakeForm = $('#cupcake-form');

let cupcakes = [];

async function start() {
  cupcakes = await Cupcake.fetchAllCupcakes();
  getCupcakeList(cupcakes)
}

function getCupcakeList(cupcakes) {
  for (let cupcake of cupcakes) {
    appendCupcakeToList(cupcake);
  }
}

function appendCupcakeToList(cupcake) {
  let $cupcake = $(`<li>${cupcake.flavor}</li>`)
  $cupcakeList.append($cupcake)
}

async function makeNewCupcake(evt) {
  evt.preventDefault();
  let flavor = $('#flavor').val();
  let rating = $('#rating').val();
  let size = $('#size').val();
  let image = $('#image').val();
  let cupcakeInfo = {flavor, rating, size, image}
  let cupcake = await Cupcake.createCupcake(cupcakeInfo)
  cupcakes.push(cupcake);
  appendCupcakeToList(cupcake);
  $("#cupcake-form").trigger("reset");
}
$cupcakeForm.on("submit", makeNewCupcake);


class Cupcake{

  constructor({id, flavor, rating, size, image}) {
    this.id = id;
    this.flavor = flavor;
    this.rating = rating;
    this.size = size;
    this.image = image;
    //this.ingredients = ingredients [Ingredient1, Ingredient2]
  }

  static async fetchAllCupcakes() {
    let cupcakes = [];
    let response = await axios.get("/api/cupcakes");
    let cupcakeData = response.data.cupcakes;
    for (let cupcake of cupcakeData) {
      let newCupcake = new Cupcake(cupcake);
      cupcakes.push(newCupcake);
    }
    return cupcakes;
  }

  static async createCupcake(cupcakeInfo) {
    let response = await axios.post("/api/cupcakes",
    cupcakeInfo);
    let newCupcake = response.data.cupcake;
    let newCupcakeObj = new Cupcake(newCupcake);
    return newCupcakeObj;
  }
}


start();
