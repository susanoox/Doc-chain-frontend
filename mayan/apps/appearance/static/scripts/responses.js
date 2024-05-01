function cleanText(inputText) {
  // Remove special characters using a regular expression
  let cleanText = inputText.replace(/[^\w\s]/g, '');

  // Remove extra spaces by replacing multiple spaces with a single space
  cleanText = cleanText.replace(/\s+/g, ' ');

  // Remove newline characters (line breaks) and carriage returns
  cleanText = cleanText.replace(/[\n\r]/g, '');

  return cleanText;
}

function isPureNumber(str) {
  return !isNaN(parseFloat(str)) && isFinite(str);
}

function getBotResponse(input) {
  var currentURL = window.location.href;
  console.log('currentURL', currentURL, !(currentURL.includes("preview") || currentURL.includes("ocr/") || currentURL.includes("summery/") || currentURL.includes("cabinets/")))
  let chatbotResUrl = "";
  if (!(currentURL.includes("preview") || currentURL.includes("ocr/") || currentURL.includes("summery/") || currentURL.includes("cabinets/"))) {
    chatbotResUrl = "chatbot_res";
  } else {
    var parts = currentURL.split('/');
    // Filter the array to get only the purely numeric elements
    var docid = parts.filter(isPureNumber)[0];
    // var docid = parts[parts.length - 2];
    console.log("docid : ", docid, parts)
    chatbotResUrl = `chatbot_res_with_id/${docid}`;
  }
  console.log("docid : ", docid, parts, currentURL)

  let botHtml = '<p class="botText"><div class="bot-inner" style="color: white; padding: 10px; background: #04724D; width: 51px; margin-left: 10px; display: flex; border-radius: 4px; align-items: flex-start; justify-content: flex-start; text-align: justify; flex-direction: column; font-size: 12px; font-weight: 500;">' + '<div class="typing"> <div class="dot"></div> <div class="dot"></div> <div class="dot"></div> </div>'+ '</div></p>';
  $("#chatbox").append(botHtml);

  
  $.ajax({
    type: "GET",
    url: chatbotResUrl,
    data: {
      message: input,
    },
    success: function (data) {
      let lastBotText = $("#chatbox").find(".bot-inner").last();
      let botHtml = '<p class="botText"><div class="bot-inner" style="color: white; padding: 10px; background: #04724D; width: 267px; margin-left: 10px; display: flex; border-radius: 4px; align-items: flex-start; justify-content: flex-start; text-align: justify; flex-direction: column; font-size: 12px; font-weight: 500;">' + data.response +'</div></p>';
      lastBotText.removeAttr('style');

      lastBotText.html(botHtml)
      document.querySelector(".powered").scrollIntoView(true);

      // $("#chatbox").append(botHtml);
      console.log(data.response, data)
      document.querySelector(".powered").scrollIntoView(true);

      return data
    },
    error: function (data) {
      console.log(data)
      return data
    },
  });
}



let botTextElements = document.querySelectorAll('.botText');

// Loop through each element and attach a click event listener
botTextElements.forEach(function (element) {
  element.addEventListener('click', function () {
    // Get the text content of the clicked p tag
    let text = this.querySelector('span').textContent;
    // Copy the text to clipboard
    navigator.clipboard.writeText(text)
      .then(function () {
        // Alert the user that the text has been copied
        alert("Copied to clipboard: " + text);
      })
      .catch(function (error) {
        console.error('Failed to copy text: ', error);
      });
  });
});






// function getBotResponse(input) {
//     //rock paper scissors
//     if (input == "rock") {
//         return "paper";
//     } else if (input == "paper") {
//         return "scissors";
//     } else if (input == "scissors") {
//         return "rock";
//     }

//     // Simple responses
//     if (input == "hello") {
//         return "Hello there!";
//     } else if (input == "goodbye") {
//         return "Talk to you later!";
//     } else {
//         return "Try asking something else!";
//     }
// }