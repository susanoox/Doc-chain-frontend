let lastQuery = ""; // Variable to store the last query
let responsesMap = {}; // Dictionary to map unique IDs to responses

function cleanText(inputText) {
  let cleanText = inputText.replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').replace(/[\n\r]/g, '');
  return cleanText;
}

function isPureNumber(str) {
  return !isNaN(parseFloat(str)) && isFinite(str);
}

function getBotResponse(input) {
  lastQuery = input; // Store the last query when a new query is sent
  var currentURL = window.location.href;
  let chatbotResUrl = determineChatbotUrl(currentURL);
  let botHtml = '<p class="botText"><div class="bot-inner" style="color: white; padding: 10px; background: #04724D; width: 51px; margin-left: 10px; display: flex; border-radius: 4px; align-items: flex-start; justify-content: flex-start; text-align: justify; flex-direction: column; font-size: 12px; font-weight: 500;">' + '<div class="typing"> <div class="dot"></div> <div class="dot"></div> <div class="dot"></div> </div>'+ '</div></p>';
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
            <button class="copy-button" data-id="${messageId}">Copy</button>
            <button class="speak-button" data-id="${messageId}">Speak</button>
          </p>`;
}

function addButtonListeners() {
  $('.copy-button').on('click', function() {
    let messageId = $(this).data('id');
    let messageContent = responsesMap[messageId];

    // Create a temporary element to parse HTML and extract plain text
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = messageContent;
    let plainText = tempDiv.textContent || tempDiv.innerText || "";

    navigator.clipboard.writeText(plainText).then(() => {
      alert("Text Copied to clipboard");
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  });

  $('.speak-button').on('click', function() {
    let messageId = $(this).data('id');
    let messageContent = responsesMap[messageId];

    // Similarly, strip HTML tags for speaking
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = messageContent;
    let plainText = tempDiv.textContent || tempDiv.innerText || "";

    let utterance = new SpeechSynthesisUtterance(plainText);
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
    } else {
      window.speechSynthesis.speak(utterance);
    }
  });
}
