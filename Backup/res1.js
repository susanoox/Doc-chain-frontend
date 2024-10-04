let lastQuery = ""; // Variable to store the last query

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
  lastQuery = input; // Store the last query when a new query is sent
  var currentURL = window.location.href;
  console.log('currentURL', currentURL, !(currentURL.includes("preview") || currentURL.includes("ocr/") || currentURL.includes("summery/") || currentURL.includes("cabinets/")));
  let chatbotResUrl = "";
  if (!(currentURL.includes("preview") || currentURL.includes("ocr/") || currentURL.includes("summery/") || currentURL.includes("cabinets/"))) {
    chatbotResUrl = "chatbot_res";
  } else {
    var parts = currentURL.split('/');
    var docid = parts.filter(isPureNumber)[0];
    console.log("docid : ", docid, parts);
    chatbotResUrl = `chatbot_res_with_id/${docid}`;
  }
  console.log("docid : ", docid, parts, currentURL);

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
      let botHtml = `
        <p class="botText">
          <div class="bot-inner" style="color: white; padding: 10px; background: #04724D; width: 267px; margin-left: 10px; display: flex; border-radius: 4px; align-items: flex-start; justify-content: flex-start; text-align: justify; flex-direction: column; font-size: 12px; font-weight: 500;">
            ${data.response}
          </div>
          <div style="display: flex; flex-direction: row; align-content: center; align-items: center; justify-content: space-around; gap: 16%; margin-left: -12%;">
            <div>
              <button class="copy-button" style="margin-top: 5px;">
                <i style="font-size: 16px; padding: 5px;" class="material-icons">content_copy</i>
              </button>
              <button class="speak-button" style="margin-top: 5px;">
                <i style="font-size: 16px; padding: 5px;" class="material-icons">volume_up</i>
              </button>
            </div>
            <button class="regenerate-button" style="margin-top: 5px;">
              <i style="font-size: 16px; padding: 5px;" class="material-icons">autorenew</i>
            </button>
          </div>
        </p>`;
      lastBotText.removeAttr('style');
      lastBotText.html(botHtml);

      document.querySelector(".powered").scrollIntoView(true);

      // Add event listeners for the new buttons
      addButtonListeners();
      console.log(data.response, data);

      return data;
    },
    error: function (data) {
      console.log(data);
      return data;
    },
  });
}

// Function to add event listeners for the "Copy", "Speak Aloud", and "Regenerate" buttons
function addButtonListeners() {
  // Add copy-to-clipboard functionality
  document.querySelectorAll('.copy-button').forEach(function(button) {
    button.addEventListener('click', function() {
      // Use a variable to traverse up the DOM to find .bot-inner
      let botInner = null;
      let currentElement = this;
  
      // Traverse up the DOM tree to find the nearest .bot-inner
      while (currentElement && !botInner) {
        currentElement = currentElement.parentElement;
        if (currentElement) {
          botInner = currentElement.querySelector('.bot-inner');
        }
      }
  
      // Debugging logs
      console.log('Copy button clicked.');
      console.log('Closest bot-inner element:', botInner);
  
      if (botInner) {
        let text = botInner.textContent;
        navigator.clipboard.writeText(text)
          .then(function() {
            // Replace alert with Toastify notification
            Toastify({
              text: "Text Copied to clipboard",
              duration: 3000,
              close: true,
              gravity: "top", // 'top' or 'bottom'
              position: "right", // 'left', 'center', or 'right'
              backgroundColor: "#4CAF50", // Green color for success
            }).showToast();
          })
          .catch(function(error) {
            console.error('Failed to copy text: ', error);
          });
      } else {
        console.error("Error: .bot-inner not found.");
      }
    });
  });

  // Add speak-aloud functionality with toggle to stop/start speech
  document.querySelectorAll('.speak-button').forEach(function(button) {
    button.addEventListener('click', function() {
      let botInner = null;
      let currentElement = this;
  
      while (currentElement && !botInner) {
        currentElement = currentElement.parentElement;
        if (currentElement) {
          botInner = currentElement.querySelector('.bot-inner');
        }
      }
  
      console.log('Speak button clicked.');
      console.log('Closest bot-inner element:', botInner);
  
      if (botInner) {
        if (window.speechSynthesis.speaking) {
          window.speechSynthesis.cancel();
          this.querySelector('i').textContent = "volume_up";
        } else {
          let text = botInner.textContent;
          let utterance = new SpeechSynthesisUtterance(text);
          window.speechSynthesis.speak(utterance);
          this.querySelector('i').textContent = "volume_off"; 
        }
      } else {
        console.error("Error: .bot-inner not found.");
      }
    });
  });

  // Add functionality to regenerate the last query
  document.querySelectorAll('.regenerate-button').forEach(function(button) {
    button.addEventListener('click', function() {
      if (lastQuery) {
        getBotResponse(lastQuery); // Send the last query to the server again
        // Show Toastify notification
        Toastify({
          text: "Regenerating response...",
          duration: 3000,
          close: true,
          gravity: "top", // 'top' or 'bottom'
          position: "right", // 'left', 'center', or 'right'
          backgroundColor: "#2196F3", // Blue color for info
        }).showToast();
      } else {
        Toastify({
          text: "No previous query to regenerate.",
          duration: 3000,
          close: true,
          gravity: "top", // 'top' or 'bottom'
          position: "right", // 'left', 'center', or 'right'
          backgroundColor: "#FF5722", // Red color for error
        }).showToast();
      }
    });
  });
}

// Initially, bind listeners if any existing bot texts are present
addButtonListeners();
