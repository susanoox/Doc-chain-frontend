let lastQuery = ""; // Variable to store the last query
let responsesMap = {}; // Dictionary to map unique IDs to responses

function cleanText(inputText) {
  let cleanText = inputText.replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').replace(/[\n\r]/g, '');
  return cleanText;
}

function isPureNumber(str) {
  return !isNaN(parseFloat(str)) && isFinite(str);
}

function determineChatbotUrl(currentURL) {
  if (currentURL.includes("preview") || currentURL.includes("ocr/") || currentURL.includes("summery/") || currentURL.includes("cabinets/")) {
    let parts = currentURL.split('/');
    let docid = parts.filter(isPureNumber)[0];
    return `chatbot_res_with_id/${docid}`;
  }
  return "chatbot_res";
}

function createBotHtml(responseContent, messageId) {
  return `<p class="botText">
    <div class="bot-inner" id="${messageId}" style="color: white; padding: 10px; background: #04724D; width: 267px; margin-left: 10px; display: flex; border-radius: 4px; align-items: flex-start; justify-content: flex-start; text-align: justify; flex-direction: column; font-size: 12px; font-weight: 500;">
      ${responseContent}
    </div>
    <div style="display: flex; flex-direction: row; align-content: center; align-items: center; justify-content: space-around; gap: 16%; margin-left: -12%;">
      <div>
        <button class="copy-button" style="margin-top: 5px;" data-id="${messageId}">
          <i style="font-size: 16px; padding: 5px;" class="material-icons">content_copy</i>
        </button>
        <button class="speak-button" style="margin-top: 5px;" data-id="${messageId}">
          <i style="font-size: 16px; padding: 5px;" class="material-icons">volume_up</i>
        </button>
      </div>
      <button class="regenerate-button" style="margin-top: 5px;" data-id="${messageId}">
        <i style="font-size: 16px; padding: 5px;" class="material-icons">autorenew</i>
      </button>
    </div>
  </p>`;
}

function addButtonListeners() {
  $('.copy-button').on('click', function() {
    let messageId = $(this).data('id');
    let messageContent = responsesMap[messageId];
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = messageContent;
    let plainText = tempDiv.textContent || tempDiv.innerText || "";
    navigator.clipboard.writeText(plainText).then(() => {
      Toastify({
        text: "Text Copied to clipboard",
        duration: 3000,
        gravity: "top",
        position: "right",
        close: true,
        backgroundColor: "#4CAF50",
      }).showToast();
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  });

  $('.speak-button').on('click', function() {
    let messageId = $(this).data('id');
    let messageContent = responsesMap[messageId];
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = messageContent;
    let plainText = tempDiv.textContent || tempDiv.innerText || "";
    let utterance = new SpeechSynthesisUtterance(plainText);
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      this.querySelector('i').textContent = "volume_up"; 
    } else {
      window.speechSynthesis.speak(utterance);
      this.querySelector('i').textContent = "volume_off";
    }
  });

  $('.regenerate-button').on('click', function() {
    if (lastQuery) {
      getBotResponse(lastQuery);
      Toastify({
        text: "Regenerating response...",
        duration: 3000,
        gravity: "top",
        position: "right",
        close: true,
        backgroundColor: "#2196F3",
      }).showToast();
    } else {
      Toastify({
        text: "No query to regenerate.",
        duration: 3000,
        gravity: "top",
        position: "right",
        close: true,
        backgroundColor: "#FF5722",
      }).showToast();
    }
  });
}

function getBotResponse(input) {
  lastQuery = input; // Store the last query when a new query is sent
  var currentURL = window.location.href;
  let chatbotResUrl = determineChatbotUrl(currentURL);
  let botHtml = '<p class="botText"><div class="bot-inner" style="color: white; padding: 10px; background: #04724D; width: 51px; margin-left: 10px; display: flex; border-radius: 4px; align-items: flex-start; justify-content: flex-start; text-align: justify; flex-direction: column; font-size: 12px; font-weight: 500;">' + '<div class="typing"> <div class="dot"></div> <div class="dot"></div> <div the="dot"></div> </div>'+ '</div></p>';
  $("#chatbox").append(botHtml);

  $.ajax({
    type: "GET",
    url: chatbotResUrl,
    data: { message: input },
    success: function (data) {
      let lastBotText = $("#chatbox").find(".bot-inner").last();
      let messageId = Date.now().toString(); // Generate a unique ID
      responsesMap[messageId] = data.response; // Store response in the dictionary

      let botHtml = createBotHtml(data.response, messageId);
      lastBotText.removeAttr('style');
      lastBotText.html(botHtml);

      document.querySelector(".powered").scrollIntoView(true);
      addButtonListeners();
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
}

$(document).ready(function() {
  addButtonListeners();
});
