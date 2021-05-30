const SERVER_URL = "http://raspberrypi.local:8000";
const WEBSOCKET_URL = "ws://raspberrypi.local:8000/websocket/";

async function ledOn(n) {
  const url = `${SERVER_URL}/state/${n}/on/`;
  const response = await fetch(url, {
    method: "POST",
    //headers: { "Content-Type": "application/x-json" },
    //body: JSON.stringify({
    //route: randomRoute(8),
    //}),
  });
  if (!response.ok) {
    alert("Error while switching on led");
  }
}

async function ledOff(n) {
  const url = `${SERVER_URL}/state/${n}/off/`;
  const response = await fetch(url, {
    method: "POST",
  });
  if (!response.ok) {
    alert("Error while switching off led");
  }
}

function isOn(element) {
  return !(element.style.backgroundColor === "rgb(0, 0, 0)");
}

async function handleElementClick(e) {
  if (isOn(e.target)) {
    await ledOff(e.target.dataset.ledIndex);
  } else {
    await ledOn(e.target.dataset.ledIndex);
  }
}

function initialize() {
  document
    .querySelectorAll(".matrix-element")
    .forEach((elem) => elem.addEventListener("click", handleElementClick));

  var ws = new WebSocket(WEBSOCKET_URL);
  ws.onopen = () => {
    ws.send("client ready");
  };

  ws.onmessage = function (e) {
    const [ledNo, r, g, b] = e.data.replaceAll(" ", "").split(",");
    console.log(ledNo, r, g, b)
    document.getElementById(
      `element${ledNo}`
    ).style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
  };
}

document.addEventListener("DOMContentLoaded", function () {
  initialize();
});
