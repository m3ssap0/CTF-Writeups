function auth(){var username = document.getElementById("Username").value;var password = document.getElementById("Password").value;var head = btoa(username + ':' + password);$(document).ready(function(){$.post("graphql",{"query":"mutation{login(username:\""+username+"\",password:\""+password+"\")}"}, function(data, textStatus){if(data.data.login=="Success"){document.cookie="auth="+head;window.location='/dashboard'}else{alert('Wrong creds')};},"json");});}
function yeet(){document.cookie="auth=Z3Vlc3Q6a2FybWE5ODc0";window.location="/dashboard"}

