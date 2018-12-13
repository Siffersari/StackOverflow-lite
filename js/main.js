function deleter(){
    var purges = confirm('This change is irreversible. Do you want to proceed ?');
    
    if (purges) {
        alert('This question has been deleted.');
        window.location.replace("post.html");
    }
}
function home(){
    return window.location.replace("index.html");
}

function myFunction(x){
    x.classList.toggle(newFunction());

    function newFunction() {
        return "fa-thumbs-up";
    }
}
  