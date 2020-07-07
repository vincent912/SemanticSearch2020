# SemanticSearch2020

Implementation of a search tool that searhces based off of semantics insteaad of keywords.

Uses universal sentence encoder from:
https://tfhub.dev/google/universal-sentence-encoder/4
to encode queries and entries. For this project, entries are scraped from the Mist company's documentation websites.
https://www.mist.com/documentation

The results are loaded into an Elasticseach index, which which can be queired using a simple flask web app that acts like a testing harness/

The following schema is what the output should look like:

{
          "paragraph_number" : 2,
          "snippet" : "On the Client Events in the Insights page, you will see an AP Deauthentication being sent to the clients when the changes are made. You can refer the audit log for the same.",
          "subtitle" : null,
          "title" : "Why do clients disconnect when you add a new WLAN?",
          "image" : "Screen-Shot-2020-03-26-at-2.55.00-PM.png",
          "url" : "https://www.mist.com/documentation/why-do-clients-disconnect-when-you-add-a-new-wlan",
          "image_url" : "https://raw.githubusercontent.com/Abe13/Marvin_chatbot/master/images/Screen-Shot-2020-03-26-at-2.55.00-PM.png",
          "type" : "Wifi-FAQ",
          "creationDate" : 1589473908412,
          "snippet_vector" : [
	  ]
}
