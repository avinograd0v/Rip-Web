let [openButton] = document.getElementsByClassName("btn-show-more");
let [optionsContainer] = document.getElementsByClassName("main-ask-search");
let [input] = document.getElementsByClassName("input-lg");    
let [searchButton] = document.getElementsByClassName("btn-search");    
let askButton = searchButton.nextElementSibling;   
let [loginLink] = document.getElementsByClassName("login-link");
let [mainContainer] = document.getElementsByClassName("main-content-container");
let user_bar_link = document.getElementById("user-bar-link");

user_bar_link.onclick = function(){
	this.nextElementSibling.classList.toggle('visible');
};

openButton.onclick = function(){
	if(optionsContainer.classList.contains("options-opened")){
		input.focus();
	} else {
        optionsContainer.classList.add("options-opened");
	}
};

input.onkeydown = function(event){
	mainContainer.classList.remove('is-center');
    if (event.keyCode === 13){
    	optionsContainer.classList.add("options-opened");
    }
};

input.onfocus = function(){
    optionsContainer.classList.remove("options-opened");
};

input.onblur = function(){
	 askSearch.classList.remove("options-opened");
};

searchButton.onkeydown = function(event){
	if(event.keyCode === 37){
		input.focus();
	}
	else if(event.keyCode === 39){
		askButton.focus();
	}
	event.preventDefault();
};

askButton.onkeydown = function(event){
	if(event.keyCode === 37){
		searchButton.focus();
	}
};

