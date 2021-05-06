
function getName(){
	login = document.getElementById("login").value;
	alert("Hi, " + login);
	return login;
}

function submitAnswers(answers){

	var total = answers.length;
	var score = 0;
	var choice = []
    
	for(var i = 1; i <= total; i++){
		
		choice[i] = document.forms["quizForm"]["q"+i].value;
	}
 

	for(i = 1; i <= total; i++){
		if(choice[i] == null || choice[i] == ''){
			alert('you missed question ' + i);
			return false;
		}
	}


	//set correct answer
	//var answers = ["b", "d", "a", "c", "c"];
	// new dynamic method 1 for checking answer
	for(i = 1; i <= total; i++){
		if(choice[i] == answers[i - 1]){
			score++;
		}
	}
	var URL="{% url 'scores' %}"
	var data = score;
	$.post(URL, data);
	
	//Display Result
	var results = document.getElementById('results');
	results.innerHTML = "<h3>You scored <span>" + score + "</span> out of <span>" + total + "</span></h3>"
	alert("You scored " + score + " out of " + total);

	return false;
}

