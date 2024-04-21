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
  console.log('currentURL', currentURL, !( currentURL.includes("preview") || currentURL.includes("ocr/") || currentURL.includes("summery/") || currentURL.includes("cabinets/") ), currentURL.includes("preview") , currentURL.includes("ocr/") , currentURL.includes("summery/") , currentURL.includes("cabinets/"))
  let chatbotResUrl = "";
  if (!( currentURL.includes("preview") || currentURL.includes("ocr/") || currentURL.includes("summery/") || currentURL.includes("cabinets/") ) ) {
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
    $.ajax({
      type: "GET",
      url: chatbotResUrl,
      data: {
        message: input,
      },
      success: function (data) {
        let botHtml = '<p class="botText"><div style="padding: 10px; background: #ecf0f1; width: 290px; margin-left: 10px; display: flex; border-radius: 0px 20px 20px 12px; align-items: flex-start; justify-content: flex-start; text-align: justify;">' + data.response + '</div></p>';
        $("#chatbox").append(botHtml);
        console.log(data.response, data)
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
        .then(function() {
          // Alert the user that the text has been copied
          alert("Copied to clipboard: " + text);
        })
        .catch(function(error) {
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