import streamlit as st
st.set_page_config(layout="wide", page_title="My Streamlit App", page_icon="🌟")
# Basic HTML and Javascript example
html_code = """
<head>
  <meta charset="utf-8" />
  <style>
    /* This CSS will position the chat component in the bottom-right corner */
    #chat-container {
      position: sticky;
      bottom: 20px;
      right: 20px;
      max-height: 300px; /* Adjust as needed */
      max-width: 200px; /* Adjust as needed */
      overflow: hidden;
    }
  </style>
</head>
<body>
  <!-- Chat component container -->
  <style>
  /* This CSS will position the chat component in the bottom-right corner */
  #chat-container {
    position: -webkit-sticky; /* For Safari */
    position: sticky;
    bottom: 20px;
    right: 20px;
    max-height: 300px; /* Adjust as needed */
    max-width: 200px; /* Adjust as needed */
    overflow: hidden;
    margin-left: auto; /* Positions to the right in a flex container */
  }
  
  .parent-container {
    height: 1000px; /* Adjust according to the parent container */
    overflow-y: auto;
  }
</style>

<div class="parent-container">
  <!-- Chat component container -->
  <div id="chat-container">
    <script src="http://localhost:8000/copilot/index.js"></script>
    <script>
      window.addEventListener("chainlit-call-fn", (e) => {
          const { name, args, callback } = e.detail;
          callback("You sent: " + args.msg);
      });

      window.mountChainlitWidget({
        chainlitServer: "http://localhost:8000",
      });

      window.addEventListener("chainlit-call-fn", (e) => {
          const { name, args, callback } = e.detail;
          if (name === "test") {
              console.log(name, args);
              callback("You sent: " + args.msg);
          }
      });

      window.sendChainlitMessage({
        type: "system_message",
        output: "Hello World!",
      });
    </script>
  </div>
</div>

</body>
"""

# Embed the HTML and Javascript in the Streamlit app
st.components.v1.html(html_code, height=600)
