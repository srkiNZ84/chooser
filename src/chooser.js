function displayPosts(){
  console.log("Getting Posts from API");
  var request = new XMLHttpRequest();
  var getPostsURL = "https://us-central1-faas-helloworld.cloudfunctions.net/getposts";
  request.open('GET', getPostsURL, true);
  request.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
  request.onreadystatechange = function() {
    if(request.readyState == 4 && request.status == 200) {
      //document.getElementById("postsDisplay").innerHTML = request.responseText;
      var blogPosts = request.response;
      console.log("length of array is " + blogPosts.length);
      console.log("contents of response is " + blogPosts);
      for(var i = 0; i < blogPosts.length; i++){
        console.log("processing blog post " + i + " content is " + blogPosts[i].content);
        var listItem = document.createElement('li');
        listItem.textContent = blogPosts[i].content;
        document.getElementById("postsDisplay").appendChild(listItem);
      }
    }
  }
  request.responseType = 'json';
  request.send();
}

function addPost(){
  console.log("Adding new blog post");
  var userText = document.getElementById("myTextBox").value;
  var subjectText = document.getElementById("subjectTextBox").value;
  var myData = { "subject": subjectText, "document": userText };
  var request = new XMLHttpRequest();
  var postURL = "https://us-central1-faas-helloworld.cloudfunctions.net/addpost";
  request.open('POST', postURL, true);
  request.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
  request.onreadystatechange = function() {
    if(request.readyState == 4 && request.status == 200) {
      document.getElementById("myResultsBox").innerHTML = "Response was: " + request.responseText;
    }
  }
  request.send(JSON.stringify(myData));
}

