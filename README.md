# Automatic Ticket Triaging System
## Michele Morelli - 2019

A NLP-based system that automatically categorises and assigns technical support tickets in the context of an IT service provider.

The micro-service is based on Python 3.6 and Azure Functions, and it is potentially capable to operate with any ticketing system provided with a RESTful API (and, ideally, webhooks). The modules that compose the system are loosely coupled, so that the system can be extended easily. An example of implementation is provided for [Zammad](https://zammad.org/), the open-source ticketing system.

Provided with a dataset of existing tickets, it is possible to train the classifier (based on the Multinomial Naive-Bayes model) to predict metadata such as:
- problem type;
- which team the ticket should be assigned to; 
- which member(s) of the team are the most relevant for the specific ticket.

The system offers various possibilities for expansion (e.g adding the functions to determine the urgency of a ticket). 

